from .proto_type_enums import ProtoTypeEnum
from colav_proto.generated.python.colav.colav_wrapper_message_pb2 import ProtoType
from colav_proto._internal.proto_type_enums import ProtoTypeEnum
from colav_proto.generated.python.colav import WrapperMessage
import time
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def wrap_proto(payload:bytes, type: ProtoTypeEnum, payload_size: int = 1024, sequence_number = 0):
    try:
        wrapper_proto = WrapperMessage()
        wrapper_proto.type = type.value
        wrapper_proto.payload = payload
        wrapper_proto.payload_size = 1024
        wrapper_proto.sequence_number = 1
        wrapper_proto.timestamp_ns = time.time_ns()

        return wrapper_proto.SerializeToString() 
    except Exception as e:
        logger.error("Exception occurred in some_function: %s", e, exc_info=True)
        raise