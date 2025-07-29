from dataclasses import dataclass
from uuid import UUID

from ed_domain.core.aggregate_roots import Location
from ed_domain.core.aggregate_roots.order import OrderStatus
from ed_domain.persistence.async_repositories import ABCAsyncUnitOfWork

from ed_optimization.application.contracts.infrastructure.google.abc_google_maps_route_api import \
    ABCGoogleMapsRoutesAPI
from ed_optimization.application.services.optimization.vrp.capacitated import \
    CVRPSolver
from ed_optimization.application.services.optimization.vrp.simple import \
    SimpleVRPSolver


@dataclass
class SimpleLocation:
    lat: float
    lng: float


class OrderProcessingService:
    def __init__(
        self, uow: ABCAsyncUnitOfWork, google_maps_routes: ABCGoogleMapsRoutesAPI
    ) -> None:
        self._uow = uow
        self._google_maps_routes = google_maps_routes

    async def optimize(self):
        drivers = await self._uow.driver_repository.get_all(available=False)
        x_car_locations = list(
            map(
                self.to_simple_location,
                [await self.get_location(driver.location_id) for driver in drivers],
            )
        )
        x_car_capacities = [4 * driver.car.seats for driver in drivers]

        orders = await self._uow.order_repository.get_all(
            order_status=OrderStatus.PENDING
        )
        x_pick_up_locations = list(
            map(
                self.to_simple_location,
                [
                    await self.get_business_location(order.business_id)
                    for order in orders
                ],
            )
        )
        x_drop_off_locations = list(
            map(
                self.to_simple_location,
                [
                    await self.get_consumer_location(order.consumer_id)
                    for order in orders
                ],
            )
        )

        x_all_locations = x_car_locations + x_pick_up_locations + x_drop_off_locations
        distance_matrix: list[list[int]] = [
            [0 for _ in range(len(x_all_locations))]
            for _ in range(len(x_all_locations))
        ]

        for i in range(len(distance_matrix)):
            for j in range(len(distance_matrix)):
                if i == j:
                    continue

                origin, destination = x_all_locations[i], x_all_locations[j]
                distance = await self._google_maps_routes.get_simple_route(
                    origin.lat, origin.lng, destination.lat, destination.lng
                )

                if "distance_meters" not in distance:
                    continue

                distance_matrix[i][j] = distance["distance_meters"]

        x_demands = (
            [0 for _ in range(len(x_car_locations))]
            + [1 for _ in range(len(x_pick_up_locations))]
            + [1 for _ in range(len(x_drop_off_locations))]
        )

        __import__("pprint").pprint(distance_matrix)
        __import__("pprint").pprint(len(drivers))
        __import__("pprint").pprint(x_car_capacities)
        __import__("pprint").pprint(x_demands)
        solver = SimpleVRPSolver(
            distance_matrix, len(drivers)  # , x_car_capacities, x_demands
        )
        solution = solver.solve()

        print(solution)

    async def get_consumer_location(self, consumer_id: UUID) -> Location:
        consumer = await self._uow.consumer_repository.get(id=consumer_id)
        assert consumer is not None

        location = await self._uow.location_repository.get(id=consumer.location_id)
        assert location is not None

        return location

    async def get_business_location(self, business_id: UUID) -> Location:
        business = await self._uow.business_repository.get(id=business_id)
        assert business is not None

        location = await self._uow.location_repository.get(id=business.location_id)
        assert location is not None

        return location

    async def get_location(self, location_id: UUID) -> Location:
        location = await self._uow.location_repository.get(id=location_id)
        assert location is not None

        return location

    def to_simple_location(self, location: Location) -> SimpleLocation:
        return SimpleLocation(lat=location.latitude, lng=location.longitude)
