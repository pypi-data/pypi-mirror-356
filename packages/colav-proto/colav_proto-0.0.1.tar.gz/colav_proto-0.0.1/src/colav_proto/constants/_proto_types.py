from enum import Enum

class StateProtoTypeEnum(Enum):
    AGENT_STATE = 0
    OBSTACLES_STATE = 1 
    OBSTACLES_RISK_STATE = 2   
    UNSAFE_SET_STATE = 3
    
class SystemProtoTypeEnum(Enum):
    MISSION_REQUEST = 0
    MISSION_RESPONSE = 1
    AUTOMATON_OUTPUT = 2
    MAP_METADATA = 3