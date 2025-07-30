from colav_proto.generated.python.colav.automaton.states.static_obstacle_state_pb2 import StaticObstacleState
from colav_proto.types import Position, Orientation
import logging

logger = logging.getLogger(__name__)

def gen_static_obstacle_state_msg(
    tag: str,
    type: str,
    position: Position,
    orientation: Orientation,
    loa: float,
    beam: float,
    safety_radius: float
):
    """
    Generate a StaticObstacleState protobuf message for a detected static obstacle.

    Constructs and returns a StaticObstacleState message containing the obstacle's tag, type, pose (position and orientation),
    and physical dimensions. Raises an exception if message construction fails.

    Args:
        tag (str): Unique identifier for the static obstacle.
        type (str): Type or classification of the static obstacle.
        position (Position): Obstacle's position in 3D space.
        orientation (Orientation): Obstacle's orientation as a quaternion.
        loa (float): Length overall of the obstacle.
        beam (float): Width (beam) of the obstacle.
        safety_radius (float): Safety radius around the obstacle.

    Raises:
        Exception: If message construction fails.

    Returns:
        StaticObstacleState: The constructed StaticObstacleState protobuf message.
    """
    try:
        msg = StaticObstacleState()
        
        msg.tag = tag
        msg.type = type

        msg.pose.position.x = position.x
        msg.pose.position.y = position.y
        msg.pose.position.z = position.z
        msg.pose.orientation.x = orientation.x
        msg.pose.orientation.y = orientation.y
        msg.pose.orientation.z = orientation.z
        msg.pose.orientation.w = orientation.w
        
        msg.loa = loa
        msg.beam = beam
        msg.safety_radius = safety_radius

        return msg
    except Exception as e: 
        logger.error(f"Error generating static obstacle state message: {e}")
        raise Exception(e)