from typing import NamedTuple

class Stamp(NamedTuple):
    sec: int
    nanosec: int

class Position(NamedTuple):
    x: float
    y: float
    z: float

class Waypoint(NamedTuple):
    position: Position
    acceptance_radius: float

class Command(NamedTuple):
    velocity: float
    yaw_rate: float

class Orientation(NamedTuple):
    x: float
    y: float
    z: float
    w: float

class Dynamics(NamedTuple):
    controller_name: str
    cmd: Command

class Vector3(NamedTuple):
    x: float
    y: float
    z: float

class Pose(NamedTuple):
    position: Position
    orientation: Orientation