"""IPMI power operations module."""
from typing import Dict, Any, Optional

from greenfish.utils.logger import Logger

# IPMI constants
IPMI_NETFN_CHASSIS = 0x00
IPMI_CMD_GET_CHASSIS_STATUS = 0x01
IPMI_CMD_CHASSIS_CONTROL = 0x02
IPMI_CMD_CHASSIS_RESET = 0x03
IPMI_CMD_CHASSIS_IDENTIFY = 0x04
IPMI_CMD_SET_CHASSIS_CAPABILITIES = 0x05
IPMI_CMD_SET_POWER_RESTORE_POLICY = 0x06
IPMI_CMD_GET_SYSTEM_RESTART_CAUSE = 0x07
IPMI_CMD_SET_SYSTEM_BOOT_OPTIONS = 0x08
IPMI_CMD_GET_SYSTEM_BOOT_OPTIONS = 0x09

# Chassis control commands
CHASSIS_CONTROL_POWER_DOWN = 0x00
CHASSIS_CONTROL_POWER_UP = 0x01
CHASSIS_CONTROL_POWER_CYCLE = 0x02
CHASSIS_CONTROL_HARD_RESET = 0x03
CHASSIS_CONTROL_DIAGNOSTIC_INTERRUPT = 0x04
CHASSIS_CONTROL_SOFT_SHUTDOWN = 0x05

# Power restore policy
POWER_RESTORE_POLICY_ALWAYS_OFF = 0x00
POWER_RESTORE_POLICY_PREVIOUS = 0x01
POWER_RESTORE_POLICY_ALWAYS_ON = 0x02

class PowerOperations:
    """IPMI power operations handler."""

    def __init__(self, protocol):
        """Initialize power operations handler.

        Args:
            protocol: IPMI protocol handler
        """
        self.protocol = protocol

    def get_chassis_status(self) -> Dict[str, Any]:
        """Get chassis status.

        Returns:
            Dict containing chassis status information
        """
        response = self.protocol.send_command(IPMI_NETFN_CHASSIS, IPMI_CMD_GET_CHASSIS_STATUS)
        if response['completion_code'] != 0:
            Logger.error(f"Failed to get chassis status: {response['completion_code']:#x}")
            return {}

        data = response['data']
        if len(data) < 3:
            Logger.error("Invalid chassis status response")
            return {}

        current_power_state = data[0] & 0x01
        last_power_event = data[0] >> 4
        misc_chassis_state = data[1]
        front_panel_button_capabilities = data[2]

        return {
            'power_state': 'on' if current_power_state else 'off',
            'power_overload': bool(data[0] & 0x02),
            'interlock_active': bool(data[0] & 0x04),
            'power_fault': bool(data[0] & 0x08),
            'power_control_fault': bool(data[0] & 0x10),
            'power_restore_policy': (data[0] >> 5) & 0x03,
            'last_power_event': {
                'ac_failed': bool(last_power_event & 0x01),
                'power_down_due_to_power_overload': bool(last_power_event & 0x02),
                'power_down_due_to_power_interlock': bool(last_power_event & 0x04),
                'power_down_due_to_power_fault': bool(last_power_event & 0x08),
                'power_on_via_ipmi': bool(last_power_event & 0x10)
            },
            'chassis_intrusion_active': bool(misc_chassis_state & 0x01),
            'front_panel_lockout_active': bool(misc_chassis_state & 0x02),
            'drive_fault': bool(misc_chassis_state & 0x04),
            'cooling_fault': bool(misc_chassis_state & 0x08),
            'button_capabilities': {
                'power_off_disabled': bool(front_panel_button_capabilities & 0x01),
                'reset_disabled': bool(front_panel_button_capabilities & 0x02),
                'diagnostic_interrupt_disabled': bool(front_panel_button_capabilities & 0x04),
                'standby_disabled': bool(front_panel_button_capabilities & 0x08),
                'power_off_disabled_allowed': bool(front_panel_button_capabilities & 0x10),
                'reset_disabled_allowed': bool(front_panel_button_capabilities & 0x20),
                'diagnostic_interrupt_disabled_allowed': bool(front_panel_button_capabilities & 0x40),
                'standby_disabled_allowed': bool(front_panel_button_capabilities & 0x80)
            }
        }

    def power_on(self) -> bool:
        """Power on the system.

        Returns:
            bool: True if command was successful
        """
        return self._chassis_control(CHASSIS_CONTROL_POWER_UP)

    def power_off(self) -> bool:
        """Power off the system.

        Returns:
            bool: True if command was successful
        """
        return self._chassis_control(CHASSIS_CONTROL_POWER_DOWN)

    def power_cycle(self) -> bool:
        """Power cycle the system.

        Returns:
            bool: True if command was successful
        """
        return self._chassis_control(CHASSIS_CONTROL_POWER_CYCLE)

    def reset(self) -> bool:
        """Hard reset the system.

        Returns:
            bool: True if command was successful
        """
        return self._chassis_control(CHASSIS_CONTROL_HARD_RESET)

    def diagnostic_interrupt(self) -> bool:
        """Issue diagnostic interrupt.

        Returns:
            bool: True if command was successful
        """
        return self._chassis_control(CHASSIS_CONTROL_DIAGNOSTIC_INTERRUPT)

    def soft_shutdown(self) -> bool:
        """Initiate soft shutdown.

        Returns:
            bool: True if command was successful
        """
        return self._chassis_control(CHASSIS_CONTROL_SOFT_SHUTDOWN)

    def _chassis_control(self, command: int) -> bool:
        """Send chassis control command.

        Args:
            command: Chassis control command

        Returns:
            bool: True if command was successful
        """
        data = bytes([command])
        response = self.protocol.send_command(IPMI_NETFN_CHASSIS, IPMI_CMD_CHASSIS_CONTROL, data)

        success = response['completion_code'] == 0
        if not success:
            Logger.error(f"Chassis control command {command} failed: {response['completion_code']:#x}")

        return success

    def set_power_restore_policy(self, policy: int) -> bool:
        """Set power restore policy.

        Args:
            policy: Power restore policy
                0 = always off
                1 = previous state
                2 = always on

        Returns:
            bool: True if command was successful
        """
        if policy not in [POWER_RESTORE_POLICY_ALWAYS_OFF,
                         POWER_RESTORE_POLICY_PREVIOUS,
                         POWER_RESTORE_POLICY_ALWAYS_ON]:
            Logger.error(f"Invalid power restore policy: {policy}")
            return False

        data = bytes([policy])
        response = self.protocol.send_command(IPMI_NETFN_CHASSIS, IPMI_CMD_SET_POWER_RESTORE_POLICY, data)

        success = response['completion_code'] == 0
        if not success:
            Logger.error(f"Set power restore policy failed: {response['completion_code']:#x}")

        return success

    def get_system_restart_cause(self) -> Dict[str, Any]:
        """Get system restart cause.

        Returns:
            Dict containing restart cause information
        """
        response = self.protocol.send_command(IPMI_NETFN_CHASSIS, IPMI_CMD_GET_SYSTEM_RESTART_CAUSE)
        if response['completion_code'] != 0:
            Logger.error(f"Failed to get system restart cause: {response['completion_code']:#x}")
            return {}

        data = response['data']
        if len(data) < 2:
            Logger.error("Invalid system restart cause response")
            return {}

        restart_cause = data[0] & 0x0F

        # Map restart cause to string
        cause_map = {
            0x00: "unknown",
            0x01: "chassis_control_command",
            0x02: "reset_button",
            0x03: "power_button",
            0x04: "watchdog",
            0x05: "oem",
            0x06: "automatic_power_up",
            0x07: "remote_reset",
            0x08: "power_up_due_to_power_restore_policy",
            0x09: "hypervisor_reset",
            0x0A: "automatic_boot_on_error"
        }

        cause_str = cause_map.get(restart_cause, "unknown")

        return {
            'restart_cause': restart_cause,
            'restart_cause_description': cause_str,
            'channel_number': data[1] & 0x0F
        }

    def set_system_boot_options(self, parameter: int, data: bytes) -> bool:
        """Set system boot options.

        Args:
            parameter: Boot option parameter selector
            data: Parameter data

        Returns:
            bool: True if command was successful
        """
        request_data = bytes([
            0x00,  # Parameter validity
            parameter,  # Parameter selector
        ]) + data

        response = self.protocol.send_command(IPMI_NETFN_CHASSIS, IPMI_CMD_SET_SYSTEM_BOOT_OPTIONS, request_data)

        success = response['completion_code'] == 0
        if not success:
            Logger.error(f"Set system boot options failed: {response['completion_code']:#x}")

        return success

    def get_system_boot_options(self, parameter: int) -> Dict[str, Any]:
        """Get system boot options.

        Args:
            parameter: Boot option parameter selector

        Returns:
            Dict containing boot option information
        """
        request_data = bytes([
            0x00,  # Parameter validity
            parameter,  # Parameter selector
            0x00   # Set selector
        ])

        response = self.protocol.send_command(IPMI_NETFN_CHASSIS, IPMI_CMD_GET_SYSTEM_BOOT_OPTIONS, request_data)
        if response['completion_code'] != 0:
            Logger.error(f"Failed to get system boot options: {response['completion_code']:#x}")
            return {}

        data = response['data']
        if len(data) < 2:
            Logger.error("Invalid system boot options response")
            return {}

        return {
            'parameter_version': data[0] >> 4,
            'parameter_valid': bool(data[0] & 0x80),
            'parameter': data[1] & 0x7F,
            'data': data[2:]
        }
