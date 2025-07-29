"""IPMI BMC configuration module."""
from typing import Dict, Any, List, Optional
import ipaddress

from greenfish.utils.logger import Logger

# IPMI constants
IPMI_NETFN_APP = 0x06
IPMI_NETFN_TRANSPORT = 0x0C

# LAN configuration commands
IPMI_CMD_GET_LAN_CONFIG = 0x02
IPMI_CMD_SET_LAN_CONFIG = 0x01

# LAN configuration parameters
LAN_PARAM_SET_IN_PROGRESS = 0x00
LAN_PARAM_AUTH_TYPE = 0x01
LAN_PARAM_AUTH_TYPE_ENABLE = 0x02
LAN_PARAM_IP_ADDRESS = 0x03
LAN_PARAM_IP_SOURCE = 0x04
LAN_PARAM_MAC_ADDRESS = 0x05
LAN_PARAM_SUBNET_MASK = 0x06
LAN_PARAM_IPV4_HEADER_PARAMS = 0x07
LAN_PARAM_PRIMARY_RMCP_PORT = 0x08
LAN_PARAM_SECONDARY_RMCP_PORT = 0x09
LAN_PARAM_BMC_GENERATED_ARP = 0x0A
LAN_PARAM_GRATUITOUS_ARP = 0x0B
LAN_PARAM_DEFAULT_GATEWAY_IP = 0x0C
LAN_PARAM_DEFAULT_GATEWAY_MAC = 0x0D
LAN_PARAM_BACKUP_GATEWAY_IP = 0x0E
LAN_PARAM_BACKUP_GATEWAY_MAC = 0x0F
LAN_PARAM_COMMUNITY_STRING = 0x10
LAN_PARAM_ALERT_DESTINATION = 0x11
LAN_PARAM_ALERT_ACK_TIMEOUT = 0x12
LAN_PARAM_RETRY_COUNT = 0x13
LAN_PARAM_ALERT_DESTINATION_TYPE = 0x14
LAN_PARAM_ALERT_DESTINATION_ADDR = 0x15
LAN_PARAM_VLAN_ID = 0x16
LAN_PARAM_VLAN_PRIORITY = 0x17
LAN_PARAM_RMCP_CIPHER_SUPPORT = 0x18
LAN_PARAM_RMCP_CIPHERS = 0x19
LAN_PARAM_RMCP_PRIV_LEVELS = 0x1A
LAN_PARAM_DEST_ADDR_VLAN_TAG = 0x1B
LAN_PARAM_DEST_ADDR_VLAN_PRIORITY = 0x1C
LAN_PARAM_CHANNEL_ACCESS_MODE = 0x1D
LAN_PARAM_CHANNEL_PRIVILEGE_LIMIT = 0x1E
LAN_PARAM_CHANNEL_PRIVILEGE_AUTH = 0x1F

# NTP configuration commands
IPMI_CMD_GET_NTP_CONFIG = 0x30  # OEM command
IPMI_CMD_SET_NTP_CONFIG = 0x31  # OEM command

# SNMP configuration commands
IPMI_CMD_GET_SNMP_CONFIG = 0x32  # OEM command
IPMI_CMD_SET_SNMP_CONFIG = 0x33  # OEM command

# Syslog configuration commands
IPMI_CMD_GET_SYSLOG_CONFIG = 0x34  # OEM command
IPMI_CMD_SET_SYSLOG_CONFIG = 0x35  # OEM command

class BMCConfig:
    """IPMI BMC configuration handler."""

    def __init__(self, protocol):
        """Initialize BMC configuration handler.

        Args:
            protocol: IPMI protocol handler
        """
        self.protocol = protocol

    def get_lan_config(self, channel: int = 1, parameter: int = LAN_PARAM_IP_ADDRESS) -> Dict[str, Any]:
        """Get LAN configuration parameter.

        Args:
            channel: Channel number
            parameter: LAN parameter

        Returns:
            Dict containing LAN configuration
        """
        request_data = bytes([
            channel,
            parameter,
            0x00,  # Set selector
            0x00   # Block selector
        ])

        response = self.protocol.send_command(IPMI_NETFN_TRANSPORT, IPMI_CMD_GET_LAN_CONFIG, request_data)

        if response['completion_code'] != 0:
            Logger.error(f"Failed to get LAN configuration: {response['completion_code']:#x}")
            return {}

        data = response['data']
        if len(data) < 2:
            Logger.error("Invalid LAN configuration response")
            return {}

        result = {
            'parameter_revision': data[0],
            'parameter': parameter,
            'data': data[1:]
        }

        # Parse specific parameters
        if parameter == LAN_PARAM_SET_IN_PROGRESS:
            result['set_in_progress'] = data[1] & 0x03
        elif parameter == LAN_PARAM_IP_ADDRESS:
            result['ip_address'] = f"{data[1]}.{data[2]}.{data[3]}.{data[4]}"
        elif parameter == LAN_PARAM_IP_SOURCE:
            sources = {
                0x00: "unspecified",
                0x01: "static",
                0x02: "dhcp",
                0x03: "bios",
                0x04: "other"
            }
            result['ip_source'] = sources.get(data[1] & 0x0F, "unknown")
        elif parameter == LAN_PARAM_MAC_ADDRESS:
            result['mac_address'] = ":".join([f"{b:02x}" for b in data[1:7]])
        elif parameter == LAN_PARAM_SUBNET_MASK:
            result['subnet_mask'] = f"{data[1]}.{data[2]}.{data[3]}.{data[4]}"
        elif parameter == LAN_PARAM_DEFAULT_GATEWAY_IP:
            result['default_gateway_ip'] = f"{data[1]}.{data[2]}.{data[3]}.{data[4]}"
        elif parameter == LAN_PARAM_DEFAULT_GATEWAY_MAC:
            result['default_gateway_mac'] = ":".join([f"{b:02x}" for b in data[1:7]])
        elif parameter == LAN_PARAM_COMMUNITY_STRING:
            try:
                result['community_string'] = data[1:].decode('ascii').rstrip('\x00')
            except UnicodeDecodeError:
                result['community_string'] = data[1:].hex()
        elif parameter == LAN_PARAM_VLAN_ID:
            result['vlan_id'] = ((data[1] & 0x0F) << 8) | data[2]
            result['vlan_enabled'] = bool(data[1] & 0x80)

        return result

    def set_lan_config(self, channel: int = 1, parameter: int = LAN_PARAM_IP_ADDRESS, data: bytes = b'\x00\x00\x00\x00') -> bool:
        """Set LAN configuration parameter.

        Args:
            channel: Channel number
            parameter: LAN parameter
            data: Parameter data

        Returns:
            bool: True if successful
        """
        request_data = bytes([
            channel,
            parameter,
            0x00,  # Set selector
            0x00   # Block selector
        ]) + data

        response = self.protocol.send_command(IPMI_NETFN_TRANSPORT, IPMI_CMD_SET_LAN_CONFIG, request_data)

        if response['completion_code'] != 0:
            Logger.error(f"Failed to set LAN configuration: {response['completion_code']:#x}")
            return False

        return True

    def get_network_config(self, channel: int = 1) -> Dict[str, Any]:
        """Get network configuration.

        Args:
            channel: Channel number

        Returns:
            Dict containing network configuration
        """
        result = {}

        # Get IP address
        ip_config = self.get_lan_config(channel, LAN_PARAM_IP_ADDRESS)
        if ip_config:
            result['ip_address'] = ip_config.get('ip_address')

        # Get IP source
        source_config = self.get_lan_config(channel, LAN_PARAM_IP_SOURCE)
        if source_config:
            result['ip_source'] = source_config.get('ip_source')

        # Get MAC address
        mac_config = self.get_lan_config(channel, LAN_PARAM_MAC_ADDRESS)
        if mac_config:
            result['mac_address'] = mac_config.get('mac_address')

        # Get subnet mask
        subnet_config = self.get_lan_config(channel, LAN_PARAM_SUBNET_MASK)
        if subnet_config:
            result['subnet_mask'] = subnet_config.get('subnet_mask')

        # Get default gateway
        gateway_config = self.get_lan_config(channel, LAN_PARAM_DEFAULT_GATEWAY_IP)
        if gateway_config:
            result['default_gateway'] = gateway_config.get('default_gateway_ip')

        # Get VLAN settings
        vlan_config = self.get_lan_config(channel, LAN_PARAM_VLAN_ID)
        if vlan_config:
            result['vlan_id'] = vlan_config.get('vlan_id')
            result['vlan_enabled'] = vlan_config.get('vlan_enabled')

        return result

    def set_static_ip_config(self, channel: int = 1, ip_address: str = None, subnet_mask: str = None,
                           gateway: str = None, vlan_id: int = None, vlan_enabled: bool = None) -> bool:
        """Set static IP configuration.

        Args:
            channel: Channel number
            ip_address: IP address
            subnet_mask: Subnet mask
            gateway: Default gateway
            vlan_id: VLAN ID
            vlan_enabled: Enable VLAN

        Returns:
            bool: True if successful
        """
        success = True

        # Set IP source to static
        if not self.set_lan_config(channel, LAN_PARAM_IP_SOURCE, bytes([0x01])):
            success = False

        # Set IP address
        if ip_address:
            try:
                ip = ipaddress.IPv4Address(ip_address)
                ip_bytes = bytes(ip.packed)
                if not self.set_lan_config(channel, LAN_PARAM_IP_ADDRESS, ip_bytes):
                    success = False
            except ValueError:
                Logger.error(f"Invalid IP address: {ip_address}")
                success = False

        # Set subnet mask
        if subnet_mask:
            try:
                mask = ipaddress.IPv4Address(subnet_mask)
                mask_bytes = bytes(mask.packed)
                if not self.set_lan_config(channel, LAN_PARAM_SUBNET_MASK, mask_bytes):
                    success = False
            except ValueError:
                Logger.error(f"Invalid subnet mask: {subnet_mask}")
                success = False

        # Set default gateway
        if gateway:
            try:
                gw = ipaddress.IPv4Address(gateway)
                gw_bytes = bytes(gw.packed)
                if not self.set_lan_config(channel, LAN_PARAM_DEFAULT_GATEWAY_IP, gw_bytes):
                    success = False
            except ValueError:
                Logger.error(f"Invalid gateway: {gateway}")
                success = False

        # Set VLAN settings
        if vlan_id is not None or vlan_enabled is not None:
            # Get current VLAN settings
            vlan_config = self.get_lan_config(channel, LAN_PARAM_VLAN_ID)
            current_vlan_id = vlan_config.get('vlan_id', 0)
            current_vlan_enabled = vlan_config.get('vlan_enabled', False)

            # Update with new values if provided
            if vlan_id is not None:
                current_vlan_id = vlan_id

            if vlan_enabled is not None:
                current_vlan_enabled = vlan_enabled

            # Construct VLAN data
            vlan_data = bytes([
                (0x80 if current_vlan_enabled else 0x00) | ((current_vlan_id >> 8) & 0x0F),
                current_vlan_id & 0xFF
            ])

            if not self.set_lan_config(channel, LAN_PARAM_VLAN_ID, vlan_data):
                success = False

        return success

    def set_dhcp_config(self, channel: int = 1) -> bool:
        """Set DHCP configuration.

        Args:
            channel: Channel number

        Returns:
            bool: True if successful
        """
        # Set IP source to DHCP
        return self.set_lan_config(channel, LAN_PARAM_IP_SOURCE, bytes([0x02]))

    def get_snmp_config(self) -> Dict[str, Any]:
        """Get SNMP configuration.

        Args:
            None

        Returns:
            Dict containing SNMP configuration
        """
        # Get community string
        community_config = self.get_lan_config(1, LAN_PARAM_COMMUNITY_STRING)

        return {
            'community_string': community_config.get('community_string', "")
        }

    def set_snmp_config(self, community_string: str = None) -> bool:
        """Set SNMP configuration.

        Args:
            community_string: SNMP community string

        Returns:
            bool: True if successful
        """
        if community_string is not None:
            # Encode and pad community string
            community_bytes = community_string.encode('ascii')[:18].ljust(18, b'\x00')
            return self.set_lan_config(1, LAN_PARAM_COMMUNITY_STRING, community_bytes)

        return True

    def get_ntp_config(self) -> Dict[str, Any]:
        """Get NTP configuration.

        Note: This is an OEM-specific command and may not be available on all BMCs.

        Args:
            None

        Returns:
            Dict containing NTP configuration
        """
        try:
            response = self.protocol.send_command(IPMI_NETFN_APP, IPMI_CMD_GET_NTP_CONFIG)

            if response['completion_code'] != 0:
                Logger.error(f"Failed to get NTP configuration: {response['completion_code']:#x}")
                return {}

            data = response['data']
            if len(data) < 5:
                Logger.error("Invalid NTP configuration response")
                return {}

            # Parse NTP server addresses
            # Note: This is a simplified example and may need to be adjusted for specific BMC implementations
            return {
                'ntp_enabled': bool(data[0] & 0x01),
                'server1': f"{data[1]}.{data[2]}.{data[3]}.{data[4]}",
                'server2': f"{data[5]}.{data[6]}.{data[7]}.{data[8]}" if len(data) >= 9 else ""
            }
        except Exception as e:
            Logger.error(f"Error getting NTP configuration: {str(e)}")
            return {}

    def set_ntp_config(self, enabled: bool = None, server1: str = None, server2: str = None) -> bool:
        """Set NTP configuration.

        Note: This is an OEM-specific command and may not be available on all BMCs.

        Args:
            enabled: Enable NTP
            server1: Primary NTP server
            server2: Secondary NTP server

        Returns:
            bool: True if successful
        """
        try:
            # Get current configuration
            current_config = self.get_ntp_config()

            # Update with new values if provided
            if enabled is not None:
                current_config['ntp_enabled'] = enabled

            if server1 is not None:
                current_config['server1'] = server1

            if server2 is not None:
                current_config['server2'] = server2

            # Construct request data
            request_data = bytes([0x01 if current_config.get('ntp_enabled', False) else 0x00])

            # Add server1 IP
            try:
                if current_config.get('server1'):
                    ip1 = ipaddress.IPv4Address(current_config['server1'])
                    request_data += bytes(ip1.packed)
                else:
                    request_data += b'\x00\x00\x00\x00'
            except ValueError:
                Logger.error(f"Invalid NTP server1 address: {current_config.get('server1')}")
                request_data += b'\x00\x00\x00\x00'

            # Add server2 IP
            try:
                if current_config.get('server2'):
                    ip2 = ipaddress.IPv4Address(current_config['server2'])
                    request_data += bytes(ip2.packed)
                else:
                    request_data += b'\x00\x00\x00\x00'
            except ValueError:
                Logger.error(f"Invalid NTP server2 address: {current_config.get('server2')}")
                request_data += b'\x00\x00\x00\x00'

            # Send command
            response = self.protocol.send_command(IPMI_NETFN_APP, IPMI_CMD_SET_NTP_CONFIG, request_data)

            if response['completion_code'] != 0:
                Logger.error(f"Failed to set NTP configuration: {response['completion_code']:#x}")
                return False

            return True
        except Exception as e:
            Logger.error(f"Error setting NTP configuration: {str(e)}")
            return False

    def get_syslog_config(self) -> Dict[str, Any]:
        """Get syslog configuration.

        Note: This is an OEM-specific command and may not be available on all BMCs.

        Args:
            None

        Returns:
            Dict containing syslog configuration
        """
        try:
            response = self.protocol.send_command(IPMI_NETFN_APP, IPMI_CMD_GET_SYSLOG_CONFIG)

            if response['completion_code'] != 0:
                Logger.error(f"Failed to get syslog configuration: {response['completion_code']:#x}")
                return {}

            data = response['data']
            if len(data) < 5:
                Logger.error("Invalid syslog configuration response")
                return {}

            # Parse syslog server addresses
            # Note: This is a simplified example and may need to be adjusted for specific BMC implementations
            return {
                'syslog_enabled': bool(data[0] & 0x01),
                'server1': f"{data[1]}.{data[2]}.{data[3]}.{data[4]}",
                'server2': f"{data[5]}.{data[6]}.{data[7]}.{data[8]}" if len(data) >= 9 else ""
            }
        except Exception as e:
            Logger.error(f"Error getting syslog configuration: {str(e)}")
            return {}

    def set_syslog_config(self, enabled: bool = None, server1: str = None, server2: str = None) -> bool:
        """Set syslog configuration.

        Note: This is an OEM-specific command and may not be available on all BMCs.

        Args:
            enabled: Enable syslog
            server1: Primary syslog server
            server2: Secondary syslog server

        Returns:
            bool: True if successful
        """
        try:
            # Get current configuration
            current_config = self.get_syslog_config()

            # Update with new values if provided
            if enabled is not None:
                current_config['syslog_enabled'] = enabled

            if server1 is not None:
                current_config['server1'] = server1

            if server2 is not None:
                current_config['server2'] = server2

            # Construct request data
            request_data = bytes([0x01 if current_config.get('syslog_enabled', False) else 0x00])

            # Add server1 IP
            try:
                if current_config.get('server1'):
                    ip1 = ipaddress.IPv4Address(current_config['server1'])
                    request_data += bytes(ip1.packed)
                else:
                    request_data += b'\x00\x00\x00\x00'
            except ValueError:
                Logger.error(f"Invalid syslog server1 address: {current_config.get('server1')}")
                request_data += b'\x00\x00\x00\x00'

            # Add server2 IP
            try:
                if current_config.get('server2'):
                    ip2 = ipaddress.IPv4Address(current_config['server2'])
                    request_data += bytes(ip2.packed)
                else:
                    request_data += b'\x00\x00\x00\x00'
            except ValueError:
                Logger.error(f"Invalid syslog server2 address: {current_config.get('server2')}")
                request_data += b'\x00\x00\x00\x00'

            # Send command
            response = self.protocol.send_command(IPMI_NETFN_APP, IPMI_CMD_SET_SYSLOG_CONFIG, request_data)

            if response['completion_code'] != 0:
                Logger.error(f"Failed to set syslog configuration: {response['completion_code']:#x}")
                return False

            return True
        except Exception as e:
            Logger.error(f"Error setting syslog configuration: {str(e)}")
            return False
