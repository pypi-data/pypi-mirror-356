from .proto_type_enums import ProtoTypeEnum

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

PROTO_CLASS_MAP = {
    ProtoTypeEnum.MISSION_REQUEST: MissionRequest,
    ProtoTypeEnum.MISSION_RESPONSE: MissionResponse,
    ProtoTypeEnum.MAP_MISSION_METADATA: MapMetaData,
    ProtoTypeEnum.DYNAMICS: Dynamics,
    ProtoTypeEnum.AGENT_STATE: AgentState,
    ProtoTypeEnum.DYNAMIC_OBSTACLE_STATE: DynamicObstacleState,
    ProtoTypeEnum.DYNAMIC_OBSTACLE_RISK_STATE: DynamicObstacleRiskState,
    ProtoTypeEnum.STATIC_OBSTACLE_STATE: StaticObstacleState,
    ProtoTypeEnum.STATIC_OBSTACLE_RISK_STATE: StaticObstacleRiskState,
    ProtoTypeEnum.OBSTACLES_STATE: ObstaclesState,
    ProtoTypeEnum.OBSTACLES_RISK_STATE: ObstaclesRiskState,
    ProtoTypeEnum.UNSAFE_SET_STATE: UnsafeSetState,
    ProtoTypeEnum.AUTOMATON_OUTPUT: AutomatonOutput,
}