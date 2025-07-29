from .proto_type_enums import ProtoTypeEnum
from colav_proto.generated.python.colav import WrapperMessage
import time
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def unwrap_proto(payload:bytes):
    """ deserialize wrappermessage, extract the type of prototype then deserialize the payload based on that."""
    pass
    # try:
    #     wrapper_proto = WrapperMessage()
    #     wrapper_proto.type = type
    #     wrapper_proto.payload = payload
    #     wrapper_proto.payload_size = 1024
    #     wrapper_proto.sequence_number = 1
    #     wrapper_proto.timestamp_ns = time.time_ns()

    #     return wrapper_proto 
    # except Exception as e:
    #     logger.error("Exception occurred in some_function: %s", e, exc_info=True)
    #     raise