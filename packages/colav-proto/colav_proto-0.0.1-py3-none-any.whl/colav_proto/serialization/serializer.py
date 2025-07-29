from colav_proto.generated.python.colav.system import (
    MapMetaData,
    MissionRequest,
    MissionResponse
)
from colav_proto.generated.python.colav.automaton.dynamics import (
    Dynamics
)
from colav_proto.generated.python.colav.automaton.states import (
    AgentState,
    DynamicObstacleRiskState,
    DynamicObstacleState,
    StaticObstacleRiskState,
    StaticObstacleState,
    ObstaclesState,
    ObstaclesRiskState,
    UnsafeSetState
)
from colav_proto.generated.python.colav.automaton import (
    AutomatonOutput
)
from colav_proto._internal import wrap_proto
from typing import Union
from colav_proto._internal import ProtoTypeEnum


PROTO_TYPE_MAP = {
    MissionRequest: ProtoTypeEnum.MISSION_REQUEST,
    MissionResponse: ProtoTypeEnum.MISSION_RESPONSE,
    MapMetaData: ProtoTypeEnum.MAP_MISSION_METADATA,
    Dynamics: ProtoTypeEnum.DYNAMICS,
    AgentState: ProtoTypeEnum.AGENT_STATE,
    DynamicObstacleState: ProtoTypeEnum.DYNAMIC_OBSTACLE_STATE,
    DynamicObstacleRiskState: ProtoTypeEnum.DYNAMIC_OBSTACLE_RISK_STATE,
    StaticObstacleState: ProtoTypeEnum.STATIC_OBSTACLE_STATE,
    StaticObstacleRiskState: ProtoTypeEnum.STATIC_OBSTACLE_RISK_STATE,
    ObstaclesState: ProtoTypeEnum.OBSTACLES_STATE,
    ObstaclesRiskState: ProtoTypeEnum.OBSTACLES_RISK_STATE,
    UnsafeSetState: ProtoTypeEnum.UNSAFE_SET_STATE,
    AutomatonOutput: ProtoTypeEnum.AUTOMATON_OUTPUT,
}

def serialize_protobuf(
    protobuf: Union[
        MapMetaData,
        MissionRequest,
        MissionResponse,
        Dynamics,
        AgentState,
        DynamicObstacleRiskState,
        DynamicObstacleState,
        StaticObstacleRiskState,
        StaticObstacleState,
        ObstaclesState,
        ObstaclesRiskState,
        UnsafeSetState,
        AutomatonOutput
    ]
) -> bytes:
    proto_type = PROTO_TYPE_MAP.get(type(protobuf))
    
    if proto_type is None:
        raise TypeError(f"protobuf type {type(protobuf)} is not supported")

    try:
        return wrap_proto(payload=protobuf.SerializeToString(), type=proto_type)
    except Exception as e:
        raise Exception(f"Error serializing protobuf: {e}")