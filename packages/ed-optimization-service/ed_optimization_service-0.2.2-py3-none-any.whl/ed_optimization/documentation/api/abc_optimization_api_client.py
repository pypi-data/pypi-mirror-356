from abc import ABCMeta, abstractmethod

from ed_domain.documentation.api.definitions import ApiResponse

from ed_optimization.application.features.order.dtos import (
    CalculateOrderDetailsDto, RouteInformationDto)


class ABCOptimizationApiClient(metaclass=ABCMeta):
    @abstractmethod
    async def create_order(self) -> ApiResponse[None]: ...

    @abstractmethod
    async def calcualte_order_details(
        self, calculate_order_details_dto: CalculateOrderDetailsDto
    ) -> ApiResponse[RouteInformationDto]: ...
