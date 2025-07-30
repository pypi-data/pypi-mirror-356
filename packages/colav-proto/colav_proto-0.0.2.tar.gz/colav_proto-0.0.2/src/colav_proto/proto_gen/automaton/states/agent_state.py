from colav_proto.generated.python.colav.automaton.states.agent_state_pb2 import AgentState
from colav_proto.types import Stamp, Position, Orientation 
import logging


logger = logging.getLogger(__name__)

def gen_agent_state_msg(
    agent_tag: str,
    position: Position,
    orientation: Orientation,
    velocity: float,
    yaw_rate: float,
    loa: float,
    beam: float,
    safety_radius: float,
    stamp: Stamp,
) -> AgentState:
    """
    Generate an AgentState protobuf message for a single agent.

    Constructs and returns an AgentState message containing the agent's tag, pose (position and orientation),
    velocity, yaw rate, physical dimensions, safety radius, and timestamp. Validates all input parameters
    and raises exceptions for invalid data or message construction errors.

    Args:
        agent_tag (str): Unique identifier for the agent.
        position (Position): Agent's position in 3D space.
        orientation (Orientation): Agent's orientation as a quaternion.
        velocity (float): Agent's linear velocity.
        yaw_rate (float): Agent's yaw rate (angular velocity around the z-axis).
        loa (float): Length overall of the agent.
        beam (float): Width (beam) of the agent.
        safety_radius (float): Safety radius around the agent.
        stamp (Stamp): Timestamp for the state message.

    Raises:
        TypeError: If input types or protobuf structure are invalid.
        RuntimeError: If message construction fails for other reasons.

    Returns:
        AgentState: The constructed AgentState protobuf message.
    """
    # Input validation
    _validate_inputs(agent_tag, position, orientation, velocity, yaw_rate, 
                    loa, beam, safety_radius, stamp)
    
    try:
        msg = AgentState()
        
        # Set agent identifier
        msg.agent_tag = agent_tag
        
        # Set position
        msg.state.pose.position.x = position.x
        msg.state.pose.position.y = position.y
        msg.state.pose.position.z = position.z
        
        # Set orientation (quaternion)
        msg.state.pose.orientation.x = orientation.x
        msg.state.pose.orientation.y = orientation.y
        msg.state.pose.orientation.z = orientation.z
        msg.state.pose.orientation.w = orientation.w
        
        # Set motion parameters
        msg.state.velocity = velocity
        msg.state.yaw_rate = yaw_rate
        
        # Set physical dimensions
        msg.loa = loa
        msg.beam = beam
        msg.safety_radius = safety_radius
        
        # Set timestamp
        msg.stamp.sec = stamp.sec
        msg.stamp.nanosec = stamp.nanosec
        
        logger.debug(f"Generated AgentState message for agent: {agent_tag}")
        return msg
        
    except AttributeError as e:
        raise TypeError(f"Invalid protobuf message structure: {e}")
    except Exception as e:
        logger.error(f"Failed to generate AgentState message for {agent_tag}: {e}")
        raise RuntimeError(f"Failed to generate AgentState message: {e}")
    
def _validate_inputs(
    agent_tag: str,
    position: Position,
    orientation: Orientation,
    velocity: float,
    yaw_rate: float,
    loa: float,
    beam: float,
    safety_radius: float,
    stamp: Stamp,
) -> None:
    """
    Validate input parameters for agent state message generation.

    Checks the types, value ranges, and required attributes of all parameters used to generate an AgentState message.
    Raises exceptions if any parameter is invalid.

    Args:
        agent_tag (str): Unique identifier for the agent.
        position (Position): Agent's position in 3D space.
        orientation (Orientation): Agent's orientation as a quaternion.
        velocity (float): Agent's linear velocity.
        yaw_rate (float): Agent's yaw rate (angular velocity around the z-axis).
        loa (float): Length overall of the agent.
        beam (float): Width (beam) of the agent.
        safety_radius (float): Safety radius around the agent.
        stamp (Stamp): Timestamp for the state message.

    Raises:
        ValueError: If a parameter value is out of range or missing.
        TypeError: If a parameter type or attribute is incorrect.
    """
    
    # Validate agent_tag
    if not isinstance(agent_tag, str) or not agent_tag.strip():
        raise ValueError("agent_tag must be a non-empty string")
    
    # Validate position
    if not hasattr(position, 'x') or not hasattr(position, 'y') or not hasattr(position, 'z'):
        raise TypeError("position must have x, y, z attributes")
    
    # Validate orientation (quaternion)
    required_orient_attrs = ['x', 'y', 'z', 'w']
    if not all(hasattr(orientation, attr) for attr in required_orient_attrs):
        raise TypeError("orientation must have x, y, z, w attributes")
    
    # Validate quaternion normalization (optional but recommended)
    quat_norm = (orientation.x**2 + orientation.y**2 + 
                 orientation.z**2 + orientation.w**2)**0.5
    if abs(quat_norm - 1.0) > 1e-6:
        logger.warning(f"Quaternion not normalized (norm={quat_norm:.6f})")
    
    # Validate numeric parameters
    numeric_params = {
        'velocity': velocity,
        'yaw_rate': yaw_rate,
        'loa': loa,
        'beam': beam,
        'safety_radius': safety_radius
    }
    
    for param_name, param_value in numeric_params.items():
        if not isinstance(param_value, (int, float)):
            raise TypeError(f"{param_name} must be a number")
        if not (-1e6 < param_value < 1e6):  # Reasonable bounds check
            raise ValueError(f"{param_name} value {param_value} is out of reasonable range")
    
    # Validate positive-only parameters
    positive_params = ['loa', 'beam', 'safety_radius']
    for param_name in positive_params:
        if numeric_params[param_name] <= 0:
            raise ValueError(f"{param_name} must be positive, got {numeric_params[param_name]}")
    
    # Validate timestamp
    if not hasattr(stamp, 'sec') or not hasattr(stamp, 'nanosec'):
        raise TypeError("stamp must have sec and nanosec attributes")
    
    if not isinstance(stamp.sec, int) or not isinstance(stamp.nanosec, int):
        raise TypeError("stamp.sec and stamp.nanosec must be integers")
    
    if stamp.sec < 0 or stamp.nanosec < 0 or stamp.nanosec >= 1_000_000_000:
        raise ValueError("Invalid timestamp values")