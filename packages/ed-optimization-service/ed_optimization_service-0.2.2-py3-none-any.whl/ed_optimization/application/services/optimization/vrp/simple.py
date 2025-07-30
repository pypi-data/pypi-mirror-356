from ortools.constraint_solver import pywrapcp, routing_enums_pb2


class SimpleVRPSolver:
    def __init__(
        self,
        distance_matrix: list[list[int]],
        num_vehicles: int,
    ) -> None:
        self._distance_matrix = distance_matrix
        self._num_vehicles = num_vehicles

    def solve(self):
        manager = pywrapcp.RoutingIndexManager(
            len(self._distance_matrix),
            self._num_vehicles,
            list(range(self._num_vehicles)),
            list(range(self._num_vehicles)),
        )

        routing = pywrapcp.RoutingModel(manager)

        def distance_callback(from_index: int, to_index: int) -> float:
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return self._distance_matrix[from_node][to_node]

        transit_callback_index = routing.RegisterTransitCallback(
            distance_callback)
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        dimension_name = "Distance"
        routing.AddDimension(
            transit_callback_index,
            0,  # no slack
            3000,  # vehicle maximum travel distance
            True,  # start cumul to zero
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
