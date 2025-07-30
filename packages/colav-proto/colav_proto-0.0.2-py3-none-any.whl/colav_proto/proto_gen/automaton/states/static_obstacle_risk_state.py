from colav_proto.generated.python.colav.automaton.states.static_obstacle_risk_state_pb2 import StaticObstacleRiskState
from colav_proto.constants import CRIClassificationEnum
from colav_proto.types import Vector3
import logging

logger = logging.getLogger(__name__)

def gen_static_obstacle_risk_state_msg(
        obstacle_tag: str,
        relative_position: Vector3,
        raw_clearance: float,
        buffered_clearance: float,
        proximity_risk: float,
        dsf_risk: float,
        cri: float,
        dsf: float,
        is_collision: bool,
        ttc: float,
        cri_classification: CRIClassificationEnum
):
    """
    Generate a StaticObstacleRiskState protobuf message for a detected static obstacle.

    Constructs and returns a StaticObstacleRiskState message containing the obstacle's tag, relative position,
    clearance values, risk metrics, collision status, time to collision, and CRI classification. Raises an exception
    if message construction fails.

    Args:
        obstacle_tag (str): Unique identifier for the static obstacle.
        relative_position (Vector3): Relative position vector between agent and obstacle.
        raw_clearance (float): Raw clearance distance to the obstacle.
        buffered_clearance (float): Buffered clearance distance to the obstacle.
        proximity_risk (float): Proximity risk metric.
        dsf_risk (float): Distance safety factor risk metric.
        cri (float): Collision risk index.
        dsf (float): Distance safety factor.
        is_collision (bool): Collision flag.
        ttc (float): Time to collision.
        cri_classification (CRIClassificationEnum): CRI classification enum.

    Raises:
        Exception: If message construction fails.

    Returns:
        StaticObstacleRiskState: The constructed StaticObstacleRiskState protobuf message.
    """
    try:
        msg = StaticObstacleRiskState()
        msg.obstacle_tag = obstacle_tag
        msg.relative_position.x = relative_position.x
        msg.relative_position.y = relative_position.y
        msg.relative_position.z = relative_position.z

        msg.raw_clearance = raw_clearance
        msg.buffered_clearance = buffered_clearance
        msg.proximity_risk = proximity_risk
        msg.dsf_risk = dsf_risk
        msg.cri = cri
        msg.dsf = dsf
        msg.is_collision = is_collision
        msg.ttc = ttc
        msg.cri_classification = cri_classification.value

        return msg
    except Exception as e: 
        raise e