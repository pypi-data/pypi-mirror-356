from ortools.constraint_solver import pywrapcp, routing_enums_pb2


class CVRPSolver:
    def __init__(
        self,
        distance_matrix: list[list[int]],
        len_vehicles: int,
        vehicle_capacities: list[int],
        demands: list[int],
    ) -> None:
        self._distance_matrix = distance_matrix
        self._num_vehicles = len_vehicles
        self._vehicle_capacities = vehicle_capacities
        self._demands = demands

        assert len(self._vehicle_capacities) == self._num_vehicles
        assert len(self._distance_matrix) == len(self._demands)

    def solve(self):
        manager = pywrapcp.RoutingIndexManager(
            len(self._distance_matrix),
            self._num_vehicles,
            list(range(self._num_vehicles)),
            list(range(self._num_vehicles)),
        )

        routing = pywrapcp.RoutingModel(manager)

        # for event_node in range(1, len(data["time_windows"])):
        #     event_index = manager.NodeToIndex(event_node)
        #     routing.AddDisjunction([event_index], 1000000000)

        def distance_callback(from_index: int, to_index: int) -> float:
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return self._distance_matrix[from_node][to_node]

        transit_callback_index = routing.RegisterTransitCallback(
            distance_callback)
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        def demand_callback(from_index):
            from_node = manager.IndexToNode(from_index)
            return self._demands[from_node]

        demand_callback_index = routing.RegisterUnaryTransitCallback(
            demand_callback)
        routing.AddDimensionWithVehicleCapacity(
            demand_callback_index,
            0,
            self._vehicle_capacities,
            True,
            "Capacity",
        )

        dimension_name = "Distance"
        routing.AddDimension(
            transit_callback_index,
            0,
            3000,
            True,
            dimension_name,
        )
        distance_dimension = routing.GetDimensionOrDie(dimension_name)
        distance_dimension.SetGlobalSpanCostCoefficient(100)

        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
        )

        solution = routing.SolveWithParameters(search_parameters)
        return solution
