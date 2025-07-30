from enum import Enum

class AutomatonControlModeEnum(Enum):
    CRUISE = 0
    T2LOS = 1
    FALLBACK = 2
    WAYPOINT_REACHED = 3
