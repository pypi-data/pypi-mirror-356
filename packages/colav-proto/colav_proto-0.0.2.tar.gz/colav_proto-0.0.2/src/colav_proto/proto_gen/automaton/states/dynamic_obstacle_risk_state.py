from colav_proto.generated.python.colav.automaton.states.dynamic_obstacle_risk_state_pb2 import DynamicObstacleRiskState
from colav_proto.constants import CRIClassificationEnum, COLREGClassificationEnum
from colav_proto.types import Vector3, Position, Orientation, Pose
import logging

logger = logging.getLogger(__name__)

def gen_dynamic_obstacle_risk_state(
    obstacle_tag: str,
    relative_velocity: Vector3,
    relative_position: Vector3,
    raw_clearance: float,
    buffered_clearance: float,
    tsf: float,
    dsf: float,
    tcpa: float,
    dcpa: float,
    dtcpa: float,
    is_collision: float,
    ttc: float,
    cpa_pose_agent: Pose,
    cpa_pose_obstacle: Pose,
    proximity_risk: float,
    dcpa_risk: float,
    tcpa_risk: float,
    cri: float,
    cri_classification: CRIClassificationEnum,
    colreg_classification: COLREGClassificationEnum
):
    """
    Generate a DynamicObstacleRiskState protobuf message for a detected dynamic obstacle.

    Constructs and returns a DynamicObstacleRiskState message containing information about a dynamic obstacle,
    including relative kinematics, risk metrics, closest point of approach (CPA) poses, and classification results.

    Args:
        obstacle_tag (str): Unique identifier for the obstacle.
        relative_velocity (Vector3): Relative velocity vector between agent and obstacle.
        relative_position (Vector3): Relative position vector between agent and obstacle.
        raw_clearance (float): Raw clearance distance to the obstacle.
        buffered_clearance (float): Buffered clearance distance to the obstacle.
        tsf (float): Time safety factor.
        dsf (float): Distance safety factor.
        tcpa (float): Time to closest point of approach.
        dcpa (float): Distance at closest point of approach.
        dtcpa (float): Delta time to closest point of approach.
        is_collision (float): Collision flag or probability.
        ttc (float): Time to collision.
        cpa_pose_agent (Pose): Agent's pose at CPA.
        cpa_pose_obstacle (Pose): Obstacle's pose at CPA.
        proximity_risk (float): Proximity risk metric.
        dcpa_risk (float): DCPA risk metric.
        tcpa_risk (float): TCPA risk metric.
        cri (float): Collision risk index.
        cri_classification (CRIClassificationEnum): CRI classification enum.
        colreg_classification (COLREGClassificationEnum): COLREG classification enum.

    Raises:
        Exception: If message construction fails.

    Returns:
        DynamicObstacleRiskState: The constructed DynamicObstacleRiskState protobuf message.
    """
    try:
        msg = DynamicObstacleRiskState()
        msg.obstacle_tag = obstacle_tag
        msg.relative_velocity.x = relative_velocity.x
        msg.relative_velocity.y = relative_velocity.y
        msg.relative_velocity.z = relative_velocity.z
        msg.relative_position.x = relative_position.x
        msg.relative_position.y = relative_position.y
        msg.relative_position.z = relative_position.z
        msg.raw_clearance = raw_clearance
        msg.buffered_clearance = buffered_clearance
        msg.tsf = tsf
        msg.dsf = dsf
        msg.tcpa = tcpa
        msg.dcpa = dcpa
        msg.dtcpa = dtcpa
        msg.is_collision = is_collision
        msg.dcpa = dcpa
        msg.tcpa = tcpa
        msg.is_collision = is_collision
        msg.ttc = ttc

        msg.cpa_pose_agent.position.x = cpa_pose_agent.position.x
        msg.cpa_pose_agent.position.y = cpa_pose_agent.position.y
        msg.cpa_pose_agent.position.z = cpa_pose_agent.position.z

        msg.cpa_pose_agent.orientation.x = cpa_pose_agent.orientation.x
        msg.cpa_pose_agent.orientation.y = cpa_pose_agent.orientation.y
        msg.cpa_pose_agent.orientation.z = cpa_pose_agent.orientation.z
        msg.cpa_pose_agent.orientation.w = cpa_pose_agent.orientation.w

        msg.cpa_pose_obstacle.position.x = cpa_pose_obstacle.position.x
        msg.cpa_pose_obstacle.position.y = cpa_pose_obstacle.position.y
        msg.cpa_pose_obstacle.position.z = cpa_pose_obstacle.position.z

        msg.cpa_pose_obstacle.orientation.x = cpa_pose_obstacle.orientation.x
        msg.cpa_pose_obstacle.orientation.y = cpa_pose_obstacle.orientation.y
        msg.cpa_pose_obstacle.orientation.z = cpa_pose_obstacle.orientation.z
        msg.cpa_pose_obstacle.orientation.w = cpa_pose_obstacle.orientation.w

        msg.proximity_risk = proximity_risk
        msg.dcpa_risk = dcpa_risk
        msg.tcpa_risk = tcpa_risk
        msg.cri = cri
        msg.cri_classification = cri_classification
        msg.colreg_classification = colreg_classification

        return msg
    except Exception as e: 
        raise e
    