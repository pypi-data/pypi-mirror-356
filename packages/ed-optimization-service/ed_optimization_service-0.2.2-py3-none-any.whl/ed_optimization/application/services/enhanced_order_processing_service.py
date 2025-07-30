from datetime import UTC, datetime, timedelta
from typing import Optional
from uuid import UUID

import numpy as np
from ed_domain.core.aggregate_roots.delivery_job import DeliveryJobStatus
from ed_domain.core.aggregate_roots.order import Order, OrderStatus
from ed_domain.core.entities.waypoint import WaypointStatus, WaypointType
from ed_domain.persistence.async_repositories import ABCAsyncUnitOfWork

from ed_optimization.application.contracts.infrastructure.api.abc_api import \
    ABCApi
from ed_optimization.application.contracts.infrastructure.google.abc_google_maps_route_api import \
    ABCGoogleMapsRoutesAPI
from ed_optimization.application.services.business_service import \
    BusinessService
from ed_optimization.application.services.consumer_service import \
    ConsumerService
from ed_optimization.application.services.delivery_job_service import \
    DeliveryJobService
from ed_optimization.application.services.location_service import \
    LocationService
from ed_optimization.application.services.vrp_solver_service import (
    ORToolsVRPSolver, VRPLocation, VRPOrder, VRPSolution, VRPVehicle)
from ed_optimization.application.services.waypoint_service import (
    CreateWaypointModel, WaypointService)
from ed_optimization.common.logging_helpers import get_logger

LOG = get_logger()

# Configuration constants
MAX_BATCH_SIZE = 2  # Increased from 2 to allow for better optimization
# Increased to allow more orders to accumulate
MAX_WAIT_TIME = timedelta(minutes=10)
MAX_OPTIMIZATION_TIME_SECONDS = 30
REOPTIMIZATION_INTERVAL = timedelta(minutes=5)


class EnhancedOrderProcessingService:
    """Enhanced Order Processing Service with Dynamic VRP capabilities."""

    def __init__(
        self,
        uow: ABCAsyncUnitOfWork,
        api: ABCApi,
        google_maps_api: ABCGoogleMapsRoutesAPI,
    ):
        self._uow = uow
        self._api = api
        self._google_maps_api = google_maps_api

        # Service dependencies
        self._business_service = BusinessService(uow)
        self._consumer_service = ConsumerService(uow)
        self._location_service = LocationService(uow)
        self._delivery_job_service = DeliveryJobService(uow)
        self._waypoint_service = WaypointService(uow)

        # VRP solver
        self._vrp_solver = ORToolsVRPSolver()

        # Last optimization timestamp
        self._last_optimization = datetime.now(UTC)

    async def process_incoming_order(self, order: Order) -> None:
        """Process a new incoming order with dynamic VRP optimization."""
        LOG.info(f"Enhanced service received order ID: {order.id}")

        # Get current state
        pending_orders = await self._get_pending_orders()
        active_routes = await self._get_active_routes()

        # Determine if we need immediate optimization or can wait
        should_optimize = await self._should_trigger_optimization(
            pending_orders, active_routes
        )

        if should_optimize:
            LOG.info(
                f"Triggering VRP optimization for {len(pending_orders)} pending orders"
            )
            await self._optimize_and_dispatch(pending_orders, active_routes)
        else:
            LOG.info(
                f"Queuing order {order.id}, waiting for more orders or time trigger"
            )
            await self._save_pending_orders(pending_orders)

    async def _should_trigger_optimization(
        self, pending_orders: list[Order], active_routes: dict
    ) -> bool:
        """Determine if VRP optimization should be triggered."""

        if len(pending_orders) >= MAX_BATCH_SIZE:
            LOG.info(f"Batch size threshold ({MAX_BATCH_SIZE}) reached")
            return True

        if pending_orders:
            oldest_order = min(pending_orders, key=lambda o: o.create_datetime)
            if datetime.now(UTC) - oldest_order.create_datetime > MAX_WAIT_TIME:
                LOG.info("Oldest order too old, forcing optimization")
                return True

        if datetime.now(UTC) - self._last_optimization > REOPTIMIZATION_INTERVAL:
            LOG.info("Reoptimization interval reached")
            return True

        return False

    async def _optimize_and_dispatch(
        self, pending_orders: list[Order], active_routes: dict
    ) -> None:
        """Perform VRP optimization and dispatch the results."""
        try:
            vrp_orders = await self._convert_orders_to_vrp_format(pending_orders)
            vrp_vehicles = await self._get_available_vehicles()
            distance_matrix = await self._build_distance_matrix(
                vrp_orders, vrp_vehicles
            )

            solution = self._vrp_solver.solve(
                vrp_orders, vrp_vehicles, distance_matrix)

            if solution:
                LOG.info(
                    f"VRP solution found: {len(solution.routes)} routes, "
                    f"total distance: {solution.total_distance}, total time: {solution.total_time}"
                )

                await self._create_delivery_jobs_from_solution(
                    solution, vrp_orders, vrp_vehicles
                )

                await self._save_pending_orders([])

                self._last_optimization = datetime.now(UTC)
            else:
                LOG.error(
                    "No VRP solution found, falling back to simple batching")
                await self._fallback_to_simple_batching(pending_orders)

        except Exception as e:
            LOG.error(f"Error during VRP optimization: {e}", exc_info=True)
            await self._fallback_to_simple_batching(pending_orders)

    async def _convert_orders_to_vrp_format(
        self, orders: list[Order]
    ) -> list[VRPOrder]:
        """Convert domain orders to VRP format."""
        vrp_orders = []

        for order in orders:
            # Get business and consumer information
            business = await self._business_service.get(order.business_id)
            consumer = await self._consumer_service.get(order.consumer_id)

            if not business or not consumer:
                LOG.warning(
                    f"Missing business or consumer for order {order.id}")
                continue

            # Get locations
            business_location = await self._location_service.get(business.location_id)
            consumer_location = await self._location_service.get(consumer.location_id)

            if not business_location or not consumer_location:
                LOG.warning(f"Missing locations for order {order.id}")
                continue

            # Convert to VRP locations
            pickup_location = VRPLocation(
                id=f"pickup_{order.id}",
                latitude=business_location.latitude,
                longitude=business_location.longitude,
                address=business_location.address,
            )

            delivery_location = VRPLocation(
                id=f"delivery_{order.id}",
                latitude=consumer_location.latitude,
                longitude=consumer_location.longitude,
                address=consumer_location.address,
            )

            # Calculate time windows (convert to minutes from start of day)
            pickup_time_window = self._calculate_time_window(
                order.create_datetime, order.latest_time_of_delivery
            )
            delivery_time_window = self._calculate_time_window(
                order.create_datetime, order.latest_time_of_delivery, is_delivery=True
            )

            vrp_order = VRPOrder(
                id=str(order.id),
                pickup_location=pickup_location,
                delivery_location=delivery_location,
                pickup_time_window=pickup_time_window,
                delivery_time_window=delivery_time_window,
                # Default weight if not specified
                demand=getattr(order, "weight", 1),
                priority=getattr(order, "priority", 1),
            )

            vrp_orders.append(vrp_order)

        return vrp_orders

    def _calculate_time_window(
        self,
        create_time: datetime,
        latest_delivery: datetime,
        is_delivery: bool = False,
    ) -> tuple[int, int]:
        """Calculate time window in minutes from start of day."""
        # For simplicity, use a 2-hour window starting from order creation
        start_of_day = create_time.replace(
            hour=0, minute=0, second=0, microsecond=0)

        if is_delivery:
            # Delivery window: from 1 hour after creation to latest delivery time
            start_minutes = int(
                (create_time - start_of_day).total_seconds() / 60) + 60
            end_minutes = int(
                (latest_delivery - start_of_day).total_seconds() / 60)
        else:
            start_minutes = int(
                (create_time - start_of_day).total_seconds() / 60)
            end_minutes = start_minutes + 120  # 2 hours

        return (max(0, start_minutes), min(1440, end_minutes))

    async def _get_available_vehicles(self) -> list[VRPVehicle]:
        drivers = await self._uow.driver_repository.get_all(available=True)

        vehicles: list[VRPVehicle] = []
        for driver in drivers:
            car = driver.car
            location = await self._location_service.get(driver.location_id)
            assert location is not None

            vehicles.append(
                VRPVehicle(
                    id=str(car.id),
                    capacity=car.seats,
                    start_location=VRPLocation(
                        id=str(location.id),
                        latitude=location.latitude,
                        longitude=location.longitude,
                        address=location.address,
                    ),
                    end_location=None,
                )
            )

        return vehicles

    async def _build_distance_matrix(
        self, orders: list[VRPOrder], vehicles: list[VRPVehicle]
    ) -> np.ndarray:
        """Build distance matrix for all locations."""
        locations = []

        depot_locations = set()
        for vehicle in vehicles:
            depot_key = (
                vehicle.start_location.latitude,
                vehicle.start_location.longitude,
            )
            if depot_key not in depot_locations:
                locations.append(vehicle.start_location)
                depot_locations.add(depot_key)

        for order in orders:
            locations.append(order.pickup_location)
            locations.append(order.delivery_location)

        n_locations = len(locations)
        distance_matrix = np.zeros((n_locations, n_locations))

        for i in range(n_locations):
            for j in range(n_locations):
                if i == j:
                    distance_matrix[i][j] = 0
                else:
                    try:
                        route_info = await self._google_maps_api.get_route(
                            locations[i], locations[j]
                        )
                        distance_matrix[i][j] = route_info.get(
                            "distance_meters", 0)
                    except Exception as e:
                        LOG.warning(
                            f"Failed to get distance between {i} and {j}: {e}")
                        distance_matrix[i][j] = self._calculate_euclidean_distance(
                            locations[i], locations[j]
                        )

        return distance_matrix

    async def _create_delivery_jobs_from_solution(
        self, solution: VRPSolution, orders: list[VRPOrder], vehicles: list[VRPVehicle]
    ) -> None:
        """Create DeliveryJob objects from VRP solution."""
        for vehicle_idx, route in enumerate(solution.routes):
            if len(route) <= 2:  # Only depot start and end
                continue

            vehicle_id = solution.vehicle_assignments[vehicle_idx]

            # Create delivery job
            delivery_job = await self._delivery_job_service.create_default()
            delivery_job.estimated_distance_in_kms = (
                solution.total_distance / 1000
            )  # Convert to km
            delivery_job.estimated_time_in_minutes = solution.total_time

            # Create waypoints from route
            waypoints = []
            sequence = 0

            for location_idx in route[1:-1]:  # Skip depot start and end
                # Determine if this is a pickup or delivery location
                order_idx, is_pickup = self._get_order_info_for_location_index(
                    location_idx, len(orders)
                )

                if order_idx is not None and order_idx < len(orders):
                    order = orders[order_idx]

                    # Find the corresponding domain order
                    domain_order_id = UUID(order.id)

                    waypoint = await self._waypoint_service.create_waypoint(
                        CreateWaypointModel(
                            delivery_job_id=delivery_job.id,
                            order_id=domain_order_id,
                            sequence=sequence,
                            expected_arrival_time=datetime.now(UTC)
                            # Rough estimate
                            + timedelta(minutes=sequence * 15),
                            waypoint_type=(
                                WaypointType.PICK_UP
                                if is_pickup
                                else WaypointType.DROP_OFF
                            ),
                            waypoint_status=WaypointStatus.PENDING,
                        )
                    )
                    waypoints.append(waypoint)
                    sequence += 1

            delivery_job.waypoints = waypoints
            await self._delivery_job_service.save(delivery_job)

            LOG.info(
                f"Created delivery job {delivery_job.id} for vehicle {vehicle_id} with {len(waypoints)} waypoints"
            )

    def _get_order_info_for_location_index(
        self, location_idx: int, num_orders: int
    ) -> tuple[Optional[int], bool]:
        """Get order index and pickup/delivery flag for a location index."""
        if location_idx == 0:  # Depot
            return None, False

        adjusted_idx = location_idx - 1  # Subtract 1 for depot
        if adjusted_idx < num_orders:  # Pickup location
            return adjusted_idx, True
        else:  # Delivery location
            return adjusted_idx - num_orders, False

    async def _fallback_to_simple_batching(self, orders: list[Order]) -> None:
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
        # optimized_waypoints, estimated_distance_km, estimated_time_minutes = (
        #     await self._optimize_waypoints_with_Maps(
        #         raw_waypoints_data, delivery_job.id
        #     )
        # )
        #
        # delivery_job.waypoints = optimized_waypoints
        # delivery_job.estimated_time_in_minutes = estimated_time_minutes
        # delivery_job.estimated_distance_in_kms = estimated_distance_km

        await self._delivery_job_service.save(delivery_job)

    async def _get_pending_orders(self) -> list[Order]:
        """Get pending orders from cache."""
        orders = await self._uow.order_repository.get_all(
            order_status=OrderStatus.PENDING
        )
        return orders

    async def _save_pending_orders(self, orders: list[Order]) -> None:
        """Save pending orders to cache."""
        LOG.info(f"Saved {len(orders)} orders to pending cache")
        ...

    async def _get_active_routes(self) -> dict:
        """Get active routes from cache."""
        delivery_jobs = await self._uow.delivery_job_repository.get_all(
            status=DeliveryJobStatus.IN_PROGRESS
        )
        return {delivery_job.id: delivery_job for delivery_job in delivery_jobs}

    async def _save_active_routes(self, routes: dict) -> None:
        """Save active routes to cache."""
        ...

    def _calculate_euclidean_distance(
        self, loc1: VRPLocation, loc2: VRPLocation
    ) -> float:
        """Calculate Euclidean distance between two locations (in meters, approximately)."""
        lat_diff = (loc1.latitude - loc2.latitude) * 111000
        lon_diff = (
            (loc1.longitude - loc2.longitude)
            * 111000
            * np.cos(np.radians(loc1.latitude))
        )
        return np.sqrt(lat_diff**2 + lon_diff**2)
