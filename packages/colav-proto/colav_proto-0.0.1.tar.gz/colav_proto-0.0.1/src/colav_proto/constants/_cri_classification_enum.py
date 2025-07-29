from enum import Enum

class CRIClassificationEnum(Enum):
    CRI_UNDEFINED = 0

    CRI_NO_RISK = 1
    CRI_LOW_RISK = 2
    CRI_MEDIUM_RISK = 3
    CRI_HIGH_RISK = 4
    CRI_CRITICAL_RISK = 5