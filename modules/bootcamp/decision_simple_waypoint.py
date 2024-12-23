"""
BOOTCAMPERS TO COMPLETE.

Travel to designated waypoint.
"""

from .. import commands
from .. import drone_report

# Disable for bootcamp use
# pylint: disable-next=unused-import
from .. import drone_status
from .. import location
from ..private.decision import base_decision


# Disable for bootcamp use
# No enable
# pylint: disable=duplicate-code,unused-argument


class DecisionSimpleWaypoint(base_decision.BaseDecision):
    """
    Travel to the designed waypoint.
    """

    def __init__(self, waypoint: location.Location, acceptance_radius: float) -> None:
        """
        Initialize all persistent variables here with self.
        """
        self.waypoint = waypoint
        print(f"Waypoint: {waypoint}")

        self.acceptance_radius = acceptance_radius

        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============
        # print(self.acceptance_radius)
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def _squared_distance_between_locations(
        self, l1: location.Location, l2: location.Location
    ) -> float:
        """
        Returns the squared distance between two locations,
        used to reduce computational overhead for calculating relative distance parity
        """
        x1 = l1.location_x
        x2 = l2.location_x
        y1 = l1.location_y
        y2 = l2.location_y
        distance = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance

    def _within_radius(self, current_location: location.Location) -> bool:
        """
        Returns whether the drone is within the waypoint
        """
        distance = self._squared_distance_between_locations(current_location, self.waypoint)
        if distance < self.acceptance_radius**2:
            return True
        return False

    def run(
        self, report: drone_report.DroneReport, landing_pad_locations: "list[location.Location]"
    ) -> commands.Command:
        """
        Make the drone fly to the waypoint.

        You are allowed to create as many helper methods as you want,
        as long as you do not change the __init__() and run() signatures.

        This method will be called in an infinite loop, something like this:

        ```py
        while True:
            report, landing_pad_locations = get_input()
            command = Decision.run(report, landing_pad_locations)
            put_output(command)
        ```
        """
        # Default command
        command = commands.Command.create_null_command()

        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============

        # Do something based on the report and the state of this class...
        current_position = report.position
        current_status = report.status
        current_destination = report.destination
        if current_status == drone_status.DroneStatus.HALTED and self._within_radius(
            current_position
        ):  # the drone is at the waypoint and stopped
            command = commands.Command.create_land_command()

        elif current_status.value == drone_status.DroneStatus.MOVING and self._within_radius(
            current_position
        ):  # necessary? Halt when reach the waypoint
            command = commands.Command.create_halt_command()

        elif current_destination != self.waypoint or (
            current_status.value == drone_status.DroneStatus.HALTED
            and not self._within_radius(current_position)
        ):  # incorrect final destination or halt location
            command = commands.Command.create_set_relative_destination_command(
                self.waypoint.location_x - current_position.location_x,
                self.waypoint.location_y - current_position.location_y,
            )

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
