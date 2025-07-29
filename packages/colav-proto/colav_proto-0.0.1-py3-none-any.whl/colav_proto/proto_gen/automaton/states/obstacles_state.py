from colav_proto.generated.python.colav.automaton.states.dynamic_obstacle_state_pb2 import DynamicObstacleState
from colav_proto.generated.python.colav.automaton.states.static_obstacle_state_pb2 import StaticObstacleState
from colav_proto.generated.python.colav.automaton.states.obstacles_state_pb2 import ObstaclesState
from colav_proto.types import Stamp
from typing import List

def gen_obstacles_state_msg(
    dynamic_obstacles_state: List[DynamicObstacleState],
    static_obstacles_state: List[StaticObstacleState],
    stamp: Stamp,
):
    """
    Generate an ObstaclesState protobuf message containing all detected obstacles.

    Constructs and returns an ObstaclesState message with lists of dynamic and static obstacle states,
    along with a timestamp. Raises an exception if message construction fails.

    Args:
        dynamic_obstacles_state (List[DynamicObstacleState]): List of dynamic obstacle state messages.
        static_obstacles_state (List[StaticObstacleState]): List of static obstacle state messages.
        stamp (Stamp): Timestamp for the obstacles state message.

    Raises:
        Exception: If message construction fails.

    Returns:
        ObstaclesState: The constructed ObstaclesState protobuf message.
    """
    try:
        # need to validate the lists
        msg = ObstaclesState()
        for obstacle in dynamic_obstacles_state:
            msg.dynamic_obstacles_state.add().CopyFrom(obstacle)
        for obstacle in static_obstacles_state:
            msg.static_obstacles_state.add().CopyFrom(obstacle)
        msg.stamp.sec = stamp.sec
        msg.stamp.nanosec = stamp.nanosec

        return msg
    except Exception as e:
        raise Exception(e)