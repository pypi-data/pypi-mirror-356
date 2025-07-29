"""IPMI client implementation."""
from typing import Dict, Any, Optional, List, Union

from greenfish.core.ipmi.protocols.ipmi import IPMIProtocol
from greenfish.core.ipmi.operations.power import PowerOperations
from greenfish.core.ipmi.operations.sensor import SensorOperations
from greenfish.core.ipmi.operations.sel import SELOperations
from greenfish.core.ipmi.operations.fru import FRUOperations
from greenfish.core.ipmi.operations.sol import SOLOperations
from greenfish.core.ipmi.operations.users import UserOperations
from greenfish.core.ipmi.config.bmc_config import BMCConfig
from greenfish.utils.logger import Logger

class IPMIClient:
    """IPMI client for interacting with BMCs."""

    def __init__(self):
        """Initialize IPMI client."""
        self.protocol = None
        self.connected = False
        self.host = None
        self.username = None
        self.password = None

        # Operations
        self.power = None
        self.sensor = None
        self.sel = None
        self.fru = None
        self.sol = None
        self.users = None
        self.bmc_config = None

    def connect(self, host: str, username: str, password: str, port: int = 623,
                interface: str = 'lanplus', timeout: int = 5,
                kg_key: str = None, privilege_level: str = 'ADMINISTRATOR') -> bool:
        """Connect to a BMC via IPMI.

        Args:
            host: BMC hostname or IP address
            username: BMC username
            password: BMC password
            port: IPMI port (default: 623)
            interface: IPMI interface (default: lanplus)
            timeout: Connection timeout in seconds (default: 5)
            kg_key: K_g key for authentication (default: None)
            privilege_level: IPMI privilege level (default: ADMINISTRATOR)

        Returns:
            bool: True if connection successful
        """
        try:
            # Initialize protocol
            self.protocol = IPMIProtocol()

            # Connect to BMC
            result = self.protocol.connect(
                host=host,
                username=username,
                password=password,
                port=port,
                interface=interface,
                timeout=timeout,
                kg_key=kg_key,
                privilege_level=privilege_level
            )

            if not result:
                Logger.error(f"Failed to connect to BMC at {host}")
                return False

            # Store connection info
            self.connected = True
            self.host = host
            self.username = username
            self.password = password

            # Initialize operations
            self.power = PowerOperations(self.protocol)
            self.sensor = SensorOperations(self.protocol)
            self.sel = SELOperations(self.protocol)
            self.fru = FRUOperations(self.protocol)
            self.sol = SOLOperations(self.protocol)
            self.users = UserOperations(self.protocol)
            self.bmc_config = BMCConfig(self.protocol)

            Logger.info(f"Connected to BMC at {host} via IPMI")
            return True

        except Exception as e:
            Logger.error(f"Error connecting to BMC: {str(e)}")
            self.connected = False
            return False

    def disconnect(self) -> bool:
        """Disconnect from the BMC.

        Returns:
            bool: True if disconnection successful
        """
        if not self.connected:
            return True

        try:
            # Close any active SOL session
            if self.sol and hasattr(self.sol, 'stop_sol_session'):
                self.sol.stop_sol_session()

            # Disconnect protocol
            if self.protocol:
                self.protocol.disconnect()

            self.connected = False
            self.protocol = None
            self.power = None
            self.sensor = None
            self.sel = None
            self.fru = None
            self.sol = None
            self.users = None
            self.bmc_config = None

            Logger.info(f"Disconnected from BMC at {self.host}")
            return True

        except Exception as e:
            Logger.error(f"Error disconnecting from BMC: {str(e)}")
            return False

    def is_connected(self) -> bool:
        """Check if connected to BMC.

        Returns:
            bool: True if connected
        """
        return self.connected

    def get_connection_info(self) -> Dict[str, Any]:
        """Get current connection information.

        Returns:
            Dict: Connection information
        """
        if not self.connected:
            return {
                'connected': False
            }

        return {
            'connected': True,
            'host': self.host,
            'username': self.username,
            'interface': self.protocol.interface if self.protocol else None
        }

    def get_bmc_info(self) -> Dict[str, Any]:
        """Get BMC information.

        Returns:
            Dict: BMC information
        """
        if not self.connected:
            Logger.error("Not connected to BMC")
            return {}

        try:
            # Get device ID
            response = self.protocol.send_command(0x06, 0x01)  # NetFn App, Cmd Get Device ID

            if response['completion_code'] != 0:
                Logger.error(f"Failed to get BMC info: {response['completion_code']:#x}")
                return {}

            data = response['data']
            if len(data) < 12:
                Logger.error("Invalid BMC info response")
                return {}

            # Parse device ID response
            device_id = data[0]
            device_revision = data[1] & 0x0F
            firmware_major = data[2] & 0x7F
            firmware_minor = data[3]
            ipmi_version = data[4]
            manufacturer_id = (data[7] << 16) | (data[6] << 8) | data[5]
            product_id = (data[9] << 8) | data[8]

            return {
                'device_id': device_id,
                'device_revision': device_revision,
                'firmware_version': f"{firmware_major}.{firmware_minor:02x}",
                'ipmi_version': f"{ipmi_version >> 4}.{ipmi_version & 0x0F}",
                'manufacturer_id': manufacturer_id,
                'product_id': product_id
            }

        except Exception as e:
            Logger.error(f"Error getting BMC info: {str(e)}")
            return {}

    def get_chassis_status(self) -> Dict[str, Any]:
        """Get chassis status.

        Returns:
            Dict: Chassis status information
        """
        if not self.connected:
            Logger.error("Not connected to BMC")
            return {}

        try:
            # Get chassis status
            response = self.protocol.send_command(0x00, 0x01)  # NetFn Chassis, Cmd Get Chassis Status

            if response['completion_code'] != 0:
                Logger.error(f"Failed to get chassis status: {response['completion_code']:#x}")
                return {}

            data = response['data']
            if len(data) < 3:
                Logger.error("Invalid chassis status response")
                return {}

            # Parse chassis status response
            current_power_state = data[0] & 0x01
            last_power_event = data[0] >> 4
            misc_chassis_state = data[1]
            front_panel_button_state = data[2]

            power_states = {
                0: "off",
                1: "on"
            }

            power_events = {
                0: "none",
                1: "ac_failed",
                2: "overload",
                3: "interlock",
                4: "fault",
                5: "command"
            }

            return {
                'power_state': power_states.get(current_power_state, "unknown"),
                'last_power_event': power_events.get(last_power_event, "unknown"),
                'power_control_fault': bool(misc_chassis_state & 0x01),
                'power_restore_policy': (misc_chassis_state >> 5) & 0x03,
                'power_button_disabled': bool(front_panel_button_state & 0x01),
                'reset_button_disabled': bool(front_panel_button_state & 0x02),
                'diagnostic_interrupt_disabled': bool(front_panel_button_state & 0x04),
                'standby_button_disabled': bool(front_panel_button_state & 0x08)
            }

        except Exception as e:
            Logger.error(f"Error getting chassis status: {str(e)}")
            return {}

    def get_system_info(self) -> Dict[str, Any]:
        """Get comprehensive system information.

        Returns:
            Dict: System information
        """
        if not self.connected:
            Logger.error("Not connected to BMC")
            return {}

        info = {}

        # Get BMC info
        bmc_info = self.get_bmc_info()
        if bmc_info:
            info['bmc'] = bmc_info

        # Get chassis status
        chassis_status = self.get_chassis_status()
        if chassis_status:
            info['chassis'] = chassis_status

        # Get FRU information
        if self.fru:
            try:
                fru_info = self.fru.get_fru_inventory()
                if fru_info:
                    info['fru'] = fru_info
            except Exception as e:
                Logger.error(f"Error getting FRU info: {str(e)}")

        # Get sensor readings
        if self.sensor:
            try:
                sensors = self.sensor.get_sensor_readings()
                if sensors:
                    info['sensors'] = sensors
            except Exception as e:
                Logger.error(f"Error getting sensor readings: {str(e)}")

        # Get SEL info
        if self.sel:
            try:
                sel_info = self.sel.get_sel_info()
                if sel_info:
                    info['sel'] = sel_info
            except Exception as e:
                Logger.error(f"Error getting SEL info: {str(e)}")

        # Get network configuration
        if self.bmc_config:
            try:
                network_config = self.bmc_config.get_network_config()
                if network_config:
                    info['network'] = network_config
            except Exception as e:
                Logger.error(f"Error getting network config: {str(e)}")

        return info
