from colav_proto.generated.python.colav.system.mission_request_pb2 import MissionRequest
from colav_proto.types import Stamp, Waypoint
from typing import List

def gen_mission_request_msg(
    mission_tag: str,
    stamp: Stamp,
    goal_waypoints: List[Waypoint]
):
    """
    Generate a MissionRequest protobuf message for a mission request.

    Constructs and returns a MissionRequest message containing the mission tag, timestamp, and a list of goal waypoints,
    each with position and orientation information. Raises an exception if message construction fails.

    Args:
        mission_tag (str): Unique identifier for the mission.
        stamp (Stamp): Timestamp for the mission request.
        goal_waypoints (List[Waypoint]): List of goal waypoints, each with position and orientation.

    Returns:
        MissionRequest: The constructed MissionRequest protobuf message.

    Raises:
        Exception: If message construction fails.
    """
    try: 
        msg = MissionRequest()
        msg.mission_tag = mission_tag
        msg.stamp.sec = stamp.sec
        msg.stamp.nanosec = stamp.nanosec

        for waypoint in goal_waypoints:
            wp = msg.goal_waypoints.add()
            wp.position.x = waypoint.position.x
            wp.position.y = waypoint.position.y
            wp.position.z = waypoint.position.z

            wp.acceptance_radius = waypoint.acceptance_radius

        return msg
    except Exception as e:
        raise