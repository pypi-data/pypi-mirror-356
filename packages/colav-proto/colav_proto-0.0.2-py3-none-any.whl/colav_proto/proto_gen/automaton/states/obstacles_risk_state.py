from colav_proto.generated.python.colav.automaton.states.obstacles_risk_state_pb2 import ObstaclesRiskState
from typing import List
from colav_proto.generated.python.colav.automaton.states.dynamic_obstacle_risk_state_pb2 import DynamicObstacleRiskState
from colav_proto.generated.python.colav.automaton.states.static_obstacle_risk_state_pb2 import StaticObstacleRiskState
from colav_proto.types import Stamp

def gen_obstacles_risk_state_msg(
    dynamic_obstacles_risk_state: List[DynamicObstacleRiskState],
    static_obstacles_risk_state: List[StaticObstacleRiskState],
    stamp: Stamp
):
    """
    Generate an ObstaclesRiskState protobuf message summarizing risk for all detected obstacles.

    Constructs and returns an ObstaclesRiskState message containing lists of dynamic and static obstacle risk states,
    along with a timestamp.

    Args:
        dynamic_obstacles_risk_state (List[DynamicObstacleRiskState]): List of risk states for dynamic obstacles.
        static_obstacles_risk_state (List[StaticObstacleRiskState]): List of risk states for static obstacles.
        stamp (Stamp): Timestamp for the risk state message.

    Returns:
        ObstaclesRiskState: The constructed ObstaclesRiskState protobuf message.
    """
    msg = ObstaclesRiskState()

    for obstacle_state in dynamic_obstacles_risk_state:
        msg.dynamic_obstacles_risk_state.append(obstacle_state)

    for obstacle_state in static_obstacles_risk_state:
        msg.static_obstacles_risk_state.append(obstacle_state)

    msg.stamp.sec = stamp.sec
    msg.stamp.nanosec = stamp.nanosec

    return msg