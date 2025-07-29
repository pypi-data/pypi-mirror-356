from colav_proto.generated.python.colav.system.map_metadata_pb2 import MapMetaData
from colav_proto.types import Stamp, Pose

def gen_map_metadata_msg(
    map_load_time: Stamp,
    resolution: float,
    width: float,
    height: float,
    origin: Pose
) -> MapMetaData:
    """
    Generate a MapMetaData protobuf message containing map metadata information.

    Constructs and returns a MapMetaData message with the map load time, resolution, dimensions, and origin pose.
    Raises an exception if message construction fails.

    Args:
        map_load_time (Stamp): Timestamp indicating when the map was loaded.
        resolution (float): Map resolution in meters per pixel.
        width (float): Width of the map in pixels.
        height (float): Height of the map in pixels.
        origin (Pose): Pose representing the origin of the map.

    Raises:
        Exception: If message construction fails.

    Returns:
        MapMetaData: The constructed MapMetaData protobuf message.
    """
    try:
        msg = MapMetaData()
        
        msg.map_load_time.sec = map_load_time.sec
        msg.map_load_time.nanosec = map_load_time.nanosec
        
        msg.resolution = resolution
        msg.width = width
        msg.height = height

        msg.origin.position.x = origin.position.x
        msg.origin.position.y = origin.position.y
        msg.origin.position.z = origin.position.z

        msg.origin.orientation.x = origin.orientation.x
        msg.origin.orientation.y = origin.orientation.y
        msg.origin.orientation.z = origin.orientation.z
        msg.origin.orientation.z = origin.orientation.z

        return msg
    except Exception as e: 
        raise e