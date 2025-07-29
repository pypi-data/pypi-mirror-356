from colav_proto.generated.python.colav.automaton.states.unsafe_set_state_pb2 import UnsafeSetState  # Assuming Vertex is the correct message type
from colav_proto.types import Stamp, Position
from typing import List, Tuple
import logging

logger = logging.getLogger(__name__)


def gen_unsafe_set_state_msg(
        stamp: Stamp,
        dsf: float,
        i1: List[str],
        i2: List[str],
        i3: List[str],
        uioi: List[str],
        convex_hull_vertices: List[Position]
) -> UnsafeSetState:
    """
    Generate an UnsafeSetState protobuf message representing the current unsafe set state.

    Constructs and returns an UnsafeSetState message containing timestamp, distance safety factor (dsf),
    several string identifier lists (i1, i2, i3, uioi), and the convex hull vertices of the unsafe set.

    Args:
        stamp (Stamp): Timestamp for the unsafe set state message.
        dsf (float): Distance safety factor value.
        i1 (List[str]): List of identifiers for the first unsafe set group.
        i2 (List[str]): List of identifiers for the second unsafe set group.
        i3 (List[str]): List of identifiers for the third unsafe set group.
        uioi (List[str]): List of identifiers for the union of interest.
        convex_hull_vertices (List[Position]): List of Position objects representing the convex hull vertices.

    Raises:
        Exception: If message construction fails.

    Returns:
        UnsafeSetState: The constructed UnsafeSetState protobuf message.
    """
    try:
        msg = UnsafeSetState()
        msg.stamp.sec = stamp.sec
        msg.stamp.nanosec = stamp.nanosec
        
        for item in i1: 
            msg.i1.append(item)
        for item in i2: 
            msg.i2.append(item)
        for item in i3: 
            msg.i3.append(item)
        for item in uioi: 
            msg.uioi.append(item)

        msg.dsf = dsf
        
        for coordinate in convex_hull_vertices:
            vertex = msg.convex_hull_vertices.add() 
            vertex.x = coordinate[0]
            vertex.y = coordinate[1]
            vertex.z = coordinate[2]  

        return msg  
    except Exception as e: 
        logger.error(str(e))
        raise e

