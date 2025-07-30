from dataclasses import dataclass

from jsons import Optional


@dataclass
class VRPLocation:
    id: str
    latitude: float
    longitude: float
    address: str


@dataclass
class VRPOrder:
    id: str
    pickup_location: VRPLocation
    delivery_location: VRPLocation
    pickup_time_window: tuple[
        int, int
    ]  # (start_time, end_time) in minutes from start of day
    delivery_time_window: tuple[int, int]
    demand: int  # weight or volume
    priority: int = 1  # higher number = higher priority


@dataclass
class VRPVehicle:
    id: str
    capacity: int
    start_location: VRPLocation
    # If None, same as start_location
    end_location: Optional[VRPLocation] = None


@dataclass
class VRPSolution:
    routes: list[list[int]]
    total_distance: float
    total_time: int
    vehicle_assignments: dict[int, str]  # vehicle_index -> vehicle_id
