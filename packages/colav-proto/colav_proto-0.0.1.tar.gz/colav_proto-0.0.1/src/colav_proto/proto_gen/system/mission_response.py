from colav_proto.generated.python.colav.system.mission_response_pb2 import MissionResponse
from colav_proto.types import Stamp

def gen_mission_response_msg(
    mission_tag: str,
    stamp: Stamp,
    mission_accepted: bool,
    error: bool,
    message: str
):
    """
    Generate a MissionResponse protobuf message for a mission response.

    Constructs and returns a MissionResponse message containing the mission tag, timestamp, acceptance status,
    error flag, and an optional message. Raises an exception if message construction fails.

    Args:
        mission_tag (str): Unique identifier for the mission.
        stamp (Stamp): Timestamp for the mission response.
        mission_accepted (bool): Indicates if the mission was accepted.
        error (bool): Indicates if there was an error processing the mission.
        message (str): Additional information or error message.

    Raises:
        Exception: If message construction fails.

    Returns:
        MissionResponse: The constructed MissionResponse protobuf message.
    """
    try:
        msg = MissionResponse()
        msg.mission_tag = mission_tag
        msg.stamp.sec = stamp.sec
        msg.stamp.nanosec = stamp.nanosec
        msg.mission_accepted = mission_accepted
        msg.error = error
        msg.message = message

        return msg 
    except Exception as e:
        raise e

