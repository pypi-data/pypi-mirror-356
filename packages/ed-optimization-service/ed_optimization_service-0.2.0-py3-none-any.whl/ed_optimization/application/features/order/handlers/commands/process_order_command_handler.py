from datetime import UTC

from ed_core.application.services.business_service import (BusinessService,
                                                           LocationService)
from ed_core.application.services.consumer_service import ConsumerService
from ed_domain.core.aggregate_roots import DeliveryJob, Order
from ed_domain.core.aggregate_roots.order import OrderStatus
from ed_domain.core.entities.waypoint import WaypointStatus, WaypointType
from ed_domain.persistence.async_repositories import ABCAsyncUnitOfWork
from jsons import datetime
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_optimization.application.common.responses.base_response import \
    BaseResponse
from ed_optimization.application.contracts.infrastructure.api.abc_api import \
    ABCApi
from ed_optimization.application.contracts.infrastructure.google.abc_google_maps_route_api import \
    ABCGoogleMapsRoutesAPI
from ed_optimization.application.features.order.requests.commands import \
    ProcessOrderCommand
from ed_optimization.application.services.delivery_job_service import \
    DeliveryJobService
from ed_optimization.application.services.optimization.order_processing_service import \
    OrderProcessingService
from ed_optimization.application.services.waypoint_service import (
    CreateWaypointModel, WaypointService)
from ed_optimization.common.logging_helpers import get_logger

LOG = get_logger()

MAX_BATCH_SIZE = 2


@request_handler(ProcessOrderCommand, BaseResponse[None])
class ProcessOrderCommandHandler(RequestHandler):
    def __init__(
        self,
        uow: ABCAsyncUnitOfWork,
        google_maps_api: ABCGoogleMapsRoutesAPI,
    ):
        self._uow = uow
        self._order_processing_service = OrderProcessingService(
            uow, google_maps_api)

        self._business_service = BusinessService(uow)
        self._consumer_service = ConsumerService(uow)
        self._location_service = LocationService(uow)
        self._delivery_job_service = DeliveryJobService(uow)
        self._waypoint_service = WaypointService(uow)

        self._google_maps_api = google_maps_api

    async def handle(self, request: ProcessOrderCommand) -> BaseResponse[None]:
        LOG.info(
            f"Handler received command for order ID: {request.model['id']}")
        async with self._uow.transaction():
            orders = await self._uow.order_repository.get_all(
                order_status=OrderStatus.PENDING
            )

            if len(orders) >= MAX_BATCH_SIZE:
                delivery_job = await self._flush_pending_orders(orders)

                LOG.info(delivery_job)

            return BaseResponse[None].success(
                message="Order processing request received successfully",
                data=None,
            )

    async def _flush_pending_orders(self, orders: list[Order]) -> DeliveryJob:
        LOG.info(f"Flushing {len(orders)} orders into a DeliveryJob.")

        raw_waypoints_data = []
        for order in orders:
            business = await self._business_service.get(order.business_id)
            assert business is not None

            consumer = await self._consumer_service.get(order.consumer_id)
            assert consumer is not None

            business_loc = await self._location_service.get(business.location_id)
            customer_loc = await self._location_service.get(consumer.location_id)

            raw_waypoints_data.append(
                {
                    "order_id": order.id,
                    "type": WaypointType.PICK_UP,
                    "eta": order.latest_time_of_delivery,
                    "location": business_loc,
                }
            )
            raw_waypoints_data.append(
                {
                    "order_id": order.id,
                    "type": WaypointType.DROP_OFF,
                    "eta": order.latest_time_of_delivery,
                    "location": customer_loc,
                }
            )

        delivery_job = await self._delivery_job_service.create_default()
        route_information = await self._google_maps_api.optimize_routes(
            raw_waypoints_data
        )
        assert route_information is not None

        print("ROUTE INFORMATION", route_information)

        waypoints = route_information["waypoints"]
        for idx, waypoint in enumerate(waypoints):
            created_waypoint = await self._waypoint_service.create_waypoint(
                CreateWaypointModel(
                    delivery_job_id=delivery_job.id,
                    order_id=waypoint["order_id"],
                    expected_arrival_time=datetime.now(UTC),
                    sequence=idx,
                    waypoint_type=waypoint["type"],
                    waypoint_status=WaypointStatus.PENDING,
                )
            )

            order = await self._uow.order_repository.get(id=waypoint["order_id"])
            assert order is not None

            order.update_status(OrderStatus.IN_PROGRESS)
            await self._uow.order_repository.save(order)

            delivery_job.add_waypoint(created_waypoint)

        delivery_job.estimated_time_in_minutes = route_information["duration_seconds"]
        delivery_job.estimated_distance_in_kms = (
            route_information["distance_meters"] / 1000
            if "distance_meters" in route_information
            else 0
        )

        await self._delivery_job_service.save(delivery_job)

        return delivery_job
