from colav_proto.generated.python.colav.automaton.states.dynamic_obstacle_state_pb2 import DynamicObstacleState
from colav_proto.types import Position, Orientation 
import logging


logger = logging.getLogger(__name__)

def gen_dynamic_obstacle_state_msg(
    tag: str,
    type: str, 
    position: Position,
    orientation: Orientation,
    velocity: float,
    yaw_rate: float,
    loa: float,
    beam: float,
    safety_radius: float
):
    """
    Generate a DynamicObstacleState protobuf message for a detected dynamic obstacle.

    Constructs and returns a DynamicObstacleState message containing the obstacle's tag, type, pose (position and orientation),
    velocity, yaw rate, and physical dimensions. Raises an exception if message construction fails.

    Args:
        tag (str): Unique identifier for the obstacle.
        type (str): Type or classification of the obstacle.
        position (Position): Obstacle's position in 3D space.
        orientation (Orientation): Obstacle's orientation as a quaternion.
        velocity (float): Obstacle's linear velocity.
        yaw_rate (float): Obstacle's yaw rate (angular velocity around the z-axis).
        loa (float): Length overall of the obstacle.
        beam (float): Width (beam) of the obstacle.
        safety_radius (float): Safety radius around the obstacle.

    Raises:
        Exception: If message construction fails.

    Returns:
        DynamicObstacleState: The constructed DynamicObstacleState protobuf message.
    """
    try:
        msg = DynamicObstacleState()
        
        msg.tag = tag
        msg.type = type

        msg.state.pose.position.x = position.x
        msg.state.pose.position.y = position.y
        msg.state.pose.position.z = position.z
        msg.state.pose.orientation.x = orientation.x
        msg.state.pose.orientation.y = orientation.y
        msg.state.pose.orientation.z = orientation.z
        msg.state.pose.orientation.w = orientation.w
        msg.state.velocity = velocity
        msg.state.yaw_rate = yaw_rate
        msg.loa = loa
        msg.beam = beam
        msg.safety_radius = safety_radius

        return msg
    except Exception as e:
        raise Exception(e)