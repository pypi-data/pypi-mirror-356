from enum import Enum

class AutomatonStatusEnum(Enum):
    INITIALIZING = 0
    ACTIVE_MODE = 1
    TRANSITIONING = 2
    COMPLETED = 3
    DEACTIVATING = 4
    ERROR = 5