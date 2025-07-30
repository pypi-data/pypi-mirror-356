from colav_proto.generated.python.colav.automaton.automaton_mission_output_pb2 import AutomatonOutput
from typing import List
from colav_proto.types import (
    Waypoint,
    Stamp,
    Dynamics
)
from colav_proto.constants import AutomatonControlModeEnum, AutomatonStatusEnum



def gen_automaton_mission_output_msg(
    automaton_mode: AutomatonControlModeEnum,
    automaton_status: AutomatonStatusEnum,
    num_planned_goal_waypoints: int,
    planned_goal_waypoints: List[Waypoint],
    current_goal_waypoint_index: int,
    current_virtual_waypoints: List[Waypoint],
    dynamics: Dynamics,
    stamp: Stamp,
    error: bool,
    message: str
) -> AutomatonOutput:
    """
    Generate an AutomatonOutput message for mission status reporting.

    This function constructs and returns an AutomatonOutput protobuf message
    containing the current automaton control mode, status, planned and virtual waypoints,
    dynamics, timestamp, error flag, and a status message.

    Args:
        automaton_mode (AutomatonControlModeEnum): The current control mode of the automaton.
        automaton_status (AutomatonStatusEnum): The current status of the automaton.
        num_planned_goal_waypoints (int): Number of planned goal waypoints.
        planned_goal_waypoints (List[Waypoint]): List of planned goal waypoints.
        current_goal_waypoint_index (int): Index of the current goal waypoint.
        current_virtual_waypoints (List[Waypoint]): List of current virtual waypoints.
        dynamics (Dynamics): Current dynamics information.
        stamp (Stamp): Timestamp of the message.
        error (bool): Indicates if an error has occurred.
        message (str): Additional status or error message.

    Returns:
        AutomatonOutput: The constructed AutomatonOutput protobuf message.
    """
    automaton_output = AutomatonOutput()
    automaton_output.control_mode = automaton_mode.value
    automaton_output.status = automaton_status.value
    automaton_output.num_planned_goal_waypoints = num_planned_goal_waypoints
    for waypoint in planned_goal_waypoints:
        automaton_output.planned_goal_waypoints.add()
        automaton_output.planned_goal_waypoints[-1].position.x = waypoint.position[0]
        automaton_output.planned_goal_waypoints[-1].position.y = waypoint.position[1]
        automaton_output.planned_goal_waypoints[-1].position.z = waypoint.position[2]
        automaton_output.planned_goal_waypoints[-1].acceptance_radius = waypoint.acceptance_radius

    automaton_output.current_goal_waypoint_index =  current_goal_waypoint_index

    for virtual_waypoint in current_virtual_waypoints:
        automaton_output.current_virtual_waypoints.add()
        automaton_output.current_virtual_waypoints[-1].position.x = virtual_waypoint.position[0]
        automaton_output.current_virtual_waypoints[-1].position.y = virtual_waypoint.position[1]
        automaton_output.current_virtual_waypoints[-1].position.z = virtual_waypoint.position[2]
        automaton_output.current_virtual_waypoints[-1].acceptance_radius = virtual_waypoint.acceptance_radius
    
    automaton_output.dynamics.controller_name = dynamics.controller_name
    automaton_output.dynamics.cmd.velocity = dynamics.cmd.velocity
    automaton_output.dynamics.cmd.yaw_rate = dynamics.cmd.yaw_rate

    automaton_output.stamp.sec = stamp.sec
    automaton_output.stamp.nanosec = stamp.nanosec

    automaton_output.error = error
    automaton_output.message = message

    return automaton_output


# def main():
#     # Example usage
#     automaton_uuid = "12345"
#     automaton_mode = "CRUISE"
#     automaton_status = "ACTIVE"
#     controller_name = "Controller1"
#     velocity = 1.0
#     yaw_rate = 0.5
#     waypoints = [Waypoint((1.0, 2.0, 3.0), 0.5)]
#     stamp = Stamp(123456789, 987654321)
#     elapsed_time = Stamp(123456789, 987654321)
#     error = False
#     error_message = ""

#     automaton_output = gen_automaton_output(
#         automaton_uuid,
#         automaton_mode,
#         automaton_status,
#         controller_name,
#         velocity,
#         yaw_rate,
#         waypoints,
#         stamp,
#         elapsed_time,
#         error,
#         error_message,
#     )

#     print(automaton_output)


# if __name__ == "__main__":
#     main()
