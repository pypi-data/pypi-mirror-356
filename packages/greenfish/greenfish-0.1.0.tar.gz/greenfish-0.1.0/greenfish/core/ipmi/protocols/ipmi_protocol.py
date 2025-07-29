"""IPMI 2.0 protocol implementation."""
import socket
import struct
import random
import time
import hmac
import hashlib
from typing import Dict, Any, List, Optional, Tuple, Union, Callable

from greenfish.utils.logger import Logger

# IPMI constants
IPMI_VERSION_2_0 = 0x20
RMCP_PORT = 623
RMCP_HEADER_SIZE = 4

# IPMI message types
IPMI_NETFN_APP = 0x06
IPMI_CMD_GET_DEVICE_ID = 0x01
IPMI_CMD_GET_CHANNEL_AUTH_CAP = 0x38
IPMI_CMD_GET_SESSION_CHALLENGE = 0x39
IPMI_CMD_ACTIVATE_SESSION = 0x3A
IPMI_CMD_SET_SESSION_PRIVILEGE = 0x3B
IPMI_CMD_CLOSE_SESSION = 0x3C

# Authentication types
IPMI_AUTH_NONE = 0x00
IPMI_AUTH_MD2 = 0x01
IPMI_AUTH_MD5 = 0x02
IPMI_AUTH_PASSWORD = 0x04
IPMI_AUTH_OEM = 0x05
IPMI_AUTH_RMCP_PLUS = 0x06

# Privilege levels
IPMI_PRIVILEGE_CALLBACK = 0x01
IPMI_PRIVILEGE_USER = 0x02
IPMI_PRIVILEGE_OPERATOR = 0x03
IPMI_PRIVILEGE_ADMINISTRATOR = 0x04
IPMI_PRIVILEGE_OEM = 0x05

class IPMIProtocol:
    """IPMI 2.0 protocol handler."""

    def __init__(self, host: str, port: int = RMCP_PORT, username: str = "", password: str = ""):
        """Initialize IPMI protocol handler.

        Args:
            host: BMC hostname or IP address
            port: IPMI port (default: 623)
            username: Username for authentication
            password: Password for authentication
        """
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.socket = None
        self.session_id = 0
        self.sequence_number = 0
        self.auth_type = IPMI_AUTH_MD5  # Default to MD5 authentication
        self.privilege_level = IPMI_PRIVILEGE_ADMINISTRATOR
        self.session_active = False
        self.timeout = 5.0  # Socket timeout in seconds

    def connect(self) -> bool:
        """Establish connection to BMC.

        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            # Create socket
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.settimeout(self.timeout)

            # Get channel authentication capabilities
            auth_cap = self._get_channel_auth_capabilities()
            if not auth_cap:
                Logger.error("Failed to get channel authentication capabilities")
                return False

            # Get session challenge
            challenge = self._get_session_challenge()
            if not challenge:
                Logger.error("Failed to get session challenge")
                return False

            # Activate session
            if not self._activate_session(challenge):
                Logger.error("Failed to activate session")
                return False

            # Set session privilege level
            if not self._set_session_privilege():
                Logger.error("Failed to set session privilege level")
                return False

            self.session_active = True
            return True

        except Exception as e:
            Logger.error(f"IPMI connection error: {str(e)}")
            if self.socket:
                self.socket.close()
                self.socket = None
            return False

    def disconnect(self) -> None:
        """Close connection to BMC."""
        if self.session_active:
            try:
                self._close_session()
            except Exception as e:
                Logger.error(f"Error closing IPMI session: {str(e)}")

        if self.socket:
            self.socket.close()
            self.socket = None

        self.session_active = False

    def send_command(self, netfn: int, command: int, data: bytes = b'') -> Dict[str, Any]:
        """Send IPMI command and return response.

        Args:
            netfn: Network function code
            command: Command code
            data: Command data bytes

        Returns:
            Dict containing completion code and response data
        """
        if not self.socket or not self.session_active:
            raise RuntimeError("Not connected to BMC")

        # Build IPMI message
        msg = self._build_ipmi_message(netfn, command, data)

        # Send message
        self.socket.sendto(msg, (self.host, self.port))

        # Receive response
        response, _ = self.socket.recvfrom(1024)

        # Parse response
        return self._parse_ipmi_response(response, netfn, command)

    def get_device_id(self) -> Dict[str, Any]:
        """Get BMC device ID information.

        Returns:
            Dict containing BMC device information
        """
        response = self.send_command(IPMI_NETFN_APP, IPMI_CMD_GET_DEVICE_ID)
        if response['completion_code'] != 0:
            raise RuntimeError(f"Failed to get device ID: {response['completion_code']:#x}")

        data = response['data']
        if len(data) < 12:
            raise RuntimeError("Invalid device ID response")

        # Parse device ID response
        device_id = data[0]
        device_revision = data[1] & 0x0F
        firmware_revision_1 = data[2]
        firmware_revision_2 = data[3]
        ipmi_version = data[4]
        manufacturer_id = (data[7] << 16) | (data[6] << 8) | data[5]
        product_id = (data[9] << 8) | data[8]

        return {
            'device_id': device_id,
            'device_revision': device_revision,
            'firmware_revision': f"{firmware_revision_1}.{firmware_revision_2:02x}",
            'ipmi_version': f"{ipmi_version >> 4}.{ipmi_version & 0x0F}",
            'manufacturer_id': manufacturer_id,
            'product_id': product_id
        }

    def _get_channel_auth_capabilities(self) -> Dict[str, Any]:
        """Get channel authentication capabilities.

        Returns:
            Dict containing authentication capabilities
        """
        # Build request data
        data = bytes([
            0x0E,  # Channel number (E = current channel)
            self.privilege_level  # Requested privilege level
        ])

        # Send request
        response = self._send_rmcp_message(IPMI_NETFN_APP, IPMI_CMD_GET_CHANNEL_AUTH_CAP, data)
        if response['completion_code'] != 0:
            Logger.error(f"Get channel auth capabilities failed: {response['completion_code']:#x}")
            return {}

        # Parse response
        data = response['data']
        if len(data) < 8:
            Logger.error("Invalid channel auth capabilities response")
            return {}

        channel_number = data[0]
        auth_type_support = data[1]

        return {
            'channel_number': channel_number,
            'auth_type_support': auth_type_support,
            'auth_types': {
                'none': bool(auth_type_support & (1 << IPMI_AUTH_NONE)),
                'md2': bool(auth_type_support & (1 << IPMI_AUTH_MD2)),
                'md5': bool(auth_type_support & (1 << IPMI_AUTH_MD5)),
                'password': bool(auth_type_support & (1 << IPMI_AUTH_PASSWORD)),
                'oem': bool(auth_type_support & (1 << IPMI_AUTH_OEM)),
                'rmcp_plus': bool(auth_type_support & (1 << IPMI_AUTH_RMCP_PLUS))
            }
        }

    def _get_session_challenge(self) -> bytes:
        """Get session challenge.

        Returns:
            Challenge bytes or empty bytes on failure
        """
        # Build request data
        data = bytes([
            self.auth_type  # Authentication type
        ])

        # Add username padded to 16 bytes
        username_bytes = self.username.encode('ascii')
        username_bytes = username_bytes[:16].ljust(16, b'\0')
        data += username_bytes

        # Send request
        response = self._send_rmcp_message(IPMI_NETFN_APP, IPMI_CMD_GET_SESSION_CHALLENGE, data)
        if response['completion_code'] != 0:
            Logger.error(f"Get session challenge failed: {response['completion_code']:#x}")
            return b''

        # Parse response
        data = response['data']
        if len(data) < 20:
            Logger.error("Invalid session challenge response")
            return b''

        self.session_id = struct.unpack("<I", data[0:4])[0]
        challenge = data[4:20]

        return challenge

    def _activate_session(self, challenge: bytes) -> bool:
        """Activate session using challenge.

        Args:
            challenge: Challenge bytes from get_session_challenge

        Returns:
            bool: True if session activated successfully
        """
        # Generate random initial sequence number
        self.sequence_number = random.randint(0, 0xFFFFFFFF)

        # Calculate authentication code
        auth_code = self._calculate_auth_code(challenge)

        # Build request data
        data = bytes([
            self.auth_type,  # Authentication type
            self.privilege_level  # Requested privilege level
        ])

        # Add challenge string
        data += challenge

        # Add initial outbound sequence number
        data += struct.pack("<I", self.sequence_number)

        # Send request
        response = self._send_rmcp_message(IPMI_NETFN_APP, IPMI_CMD_ACTIVATE_SESSION, data, auth_code)
        if response['completion_code'] != 0:
            Logger.error(f"Activate session failed: {response['completion_code']:#x}")
            return False

        # Parse response
        data = response['data']
        if len(data) < 10:
            Logger.error("Invalid activate session response")
            return False

        # Update session ID and sequence number
        self.session_id = struct.unpack("<I", data[1:5])[0]
        self.sequence_number = struct.unpack("<I", data[5:9])[0]

        return True

    def _set_session_privilege(self) -> bool:
        """Set session privilege level.

        Returns:
            bool: True if privilege level set successfully
        """
        # Build request data
        data = bytes([
            0x00,  # Reserved
            self.privilege_level  # Requested privilege level
        ])

        # Send request
        response = self.send_command(IPMI_NETFN_APP, IPMI_CMD_SET_SESSION_PRIVILEGE, data)
        if response['completion_code'] != 0:
            Logger.error(f"Set session privilege failed: {response['completion_code']:#x}")
            return False

        # Parse response
        data = response['data']
        if len(data) < 1:
            Logger.error("Invalid set session privilege response")
            return False

        # Check if requested privilege level was granted
        granted_level = data[0]
        if granted_level != self.privilege_level:
            Logger.warning(f"Requested privilege level {self.privilege_level} not granted, got {granted_level}")

        return True

    def _close_session(self) -> bool:
        """Close the current session.

        Returns:
            bool: True if session closed successfully
        """
        # Build request data with session ID
        data = struct.pack("<I", self.session_id)

        # Send request
        response = self.send_command(IPMI_NETFN_APP, IPMI_CMD_CLOSE_SESSION, data)

        # Check completion code
        return response['completion_code'] == 0

    def _send_rmcp_message(self, netfn: int, command: int, data: bytes, auth_code: bytes = None) -> Dict[str, Any]:
        """Send RMCP message without session.

        Args:
            netfn: Network function code
            command: Command code
            data: Command data bytes
            auth_code: Authentication code (optional)

        Returns:
            Dict containing completion code and response data
        """
        if not self.socket:
            raise RuntimeError("Socket not initialized")

        # Build RMCP header
        rmcp_header = bytes([
            0x06,  # RMCP Version 1.0
            0x00,  # Reserved
            0x00,  # Reserved
            0x07   # RMCP message class (IPMI)
        ])

        # Build IPMI header
        ipmi_header = bytes([
            0x00,  # Authentication type (none)
            0x00, 0x00, 0x00, 0x00,  # Session ID (0 for pre-session commands)
            0x00, 0x00, 0x00, 0x00,  # Sequence number (0 for pre-session commands)
            (netfn << 2) | 0x00,  # Network function and LUN
            0x00,  # Checksum
            0x20,  # Requester address (BMC)
            0x20,  # Responder address (BMC)
            command  # Command code
        ])

        # Calculate header checksum
        header_checksum = (-sum(ipmi_header[9:12])) & 0xFF
        ipmi_header = ipmi_header[:10] + bytes([header_checksum]) + ipmi_header[11:]

        # Calculate data checksum
        data_checksum = (-sum(ipmi_header[11:] + data)) & 0xFF

        # Build complete message
        message = rmcp_header + ipmi_header + data + bytes([data_checksum])

        # Send message
        self.socket.sendto(message, (self.host, self.port))

        # Receive response
        response, _ = self.socket.recvfrom(1024)

        # Parse response
        return self._parse_rmcp_response(response)

    def _build_ipmi_message(self, netfn: int, command: int, data: bytes) -> bytes:
        """Build IPMI message with session information.

        Args:
            netfn: Network function code
            command: Command code
            data: Command data bytes

        Returns:
            Complete IPMI message bytes
        """
        # Build RMCP header
        rmcp_header = bytes([
            0x06,  # RMCP Version 1.0
            0x00,  # Reserved
            0x00,  # Reserved
            0x07   # RMCP message class (IPMI)
        ])

        # Increment sequence number
        self.sequence_number = (self.sequence_number + 1) & 0xFFFFFFFF

        # Build IPMI header
        ipmi_header = bytes([
            self.auth_type,  # Authentication type
        ])

        # Add session ID
        ipmi_header += struct.pack("<I", self.session_id)

        # Add sequence number
        ipmi_header += struct.pack("<I", self.sequence_number)

        # Calculate authentication code if needed
        auth_code = b'\x00' * 16  # Placeholder for auth code
        if self.auth_type != IPMI_AUTH_NONE:
            # In a real implementation, calculate the auth code here
            pass

        # Add authentication code
        ipmi_header += auth_code

        # Add message header
        ipmi_header += bytes([
            (netfn << 2) | 0x00,  # Network function and LUN
            0x00,  # Checksum (placeholder)
            0x20,  # Requester address (BMC)
            0x20,  # Responder address (BMC)
            command  # Command code
        ])

        # Calculate header checksum
        header_checksum = (-sum(ipmi_header[-5:-2])) & 0xFF
        ipmi_header = ipmi_header[:-4] + bytes([header_checksum]) + ipmi_header[-3:]

        # Calculate data checksum
        data_checksum = (-sum(ipmi_header[-3:] + data)) & 0xFF

        # Build complete message
        return rmcp_header + ipmi_header + data + bytes([data_checksum])

    def _parse_rmcp_response(self, response: bytes) -> Dict[str, Any]:
        """Parse RMCP response.

        Args:
            response: Response bytes

        Returns:
            Dict containing completion code and response data
        """
        if len(response) < RMCP_HEADER_SIZE + 10:
            raise RuntimeError("Invalid RMCP response")

        # Skip RMCP header
        ipmi_msg = response[RMCP_HEADER_SIZE:]

        # Parse IPMI message
        if ipmi_msg[0] != 0x00:  # Auth type
            Logger.warning(f"Unexpected authentication type: {ipmi_msg[0]:#x}")

        # Find start of IPMI response data
        data_start = 9  # Skip auth type, session ID, sequence number

        # Extract completion code
        completion_code = ipmi_msg[data_start + 4]

        # Extract response data
        data = ipmi_msg[data_start + 5:-1]  # Exclude checksum

        return {
            'completion_code': completion_code,
            'data': data
        }

    def _parse_ipmi_response(self, response: bytes, netfn: int, command: int) -> Dict[str, Any]:
        """Parse IPMI response with session information.

        Args:
            response: Response bytes
            netfn: Expected network function code
            command: Expected command code

        Returns:
            Dict containing completion code and response data
        """
        if len(response) < RMCP_HEADER_SIZE + 21:
            raise RuntimeError("Invalid IPMI response")

        # Skip RMCP header
        ipmi_msg = response[RMCP_HEADER_SIZE:]

        # Verify authentication type
        if ipmi_msg[0] != self.auth_type:
            Logger.warning(f"Authentication type mismatch: expected {self.auth_type:#x}, got {ipmi_msg[0]:#x}")

        # Verify session ID
        session_id = struct.unpack("<I", ipmi_msg[1:5])[0]
        if session_id != self.session_id:
            Logger.warning(f"Session ID mismatch: expected {self.session_id:#x}, got {session_id:#x}")

        # Skip auth type, session ID, sequence number, auth code
        data_start = 21

        # Verify network function
        resp_netfn = (ipmi_msg[data_start] >> 2) & 0x3F
        expected_resp_netfn = (netfn | 0x01)  # Response netfn is request netfn + 1
        if resp_netfn != expected_resp_netfn:
            Logger.warning(f"Network function mismatch: expected {expected_resp_netfn:#x}, got {resp_netfn:#x}")

        # Verify command
        resp_cmd = ipmi_msg[data_start + 3]
        if resp_cmd != command:
            Logger.warning(f"Command mismatch: expected {command:#x}, got {resp_cmd:#x}")

        # Extract completion code
        completion_code = ipmi_msg[data_start + 4]

        # Extract response data
        data = ipmi_msg[data_start + 5:-1]  # Exclude checksum

        return {
            'completion_code': completion_code,
            'data': data
        }

    def _calculate_auth_code(self, challenge: bytes) -> bytes:
        """Calculate authentication code.

        Args:
            challenge: Challenge bytes

        Returns:
            Authentication code bytes
        """
        if self.auth_type == IPMI_AUTH_NONE:
            return b'\x00' * 16

        elif self.auth_type == IPMI_AUTH_MD5:
            # MD5 hash of password + session ID + challenge + password
            password_bytes = self.password.encode('ascii')
            session_id_bytes = struct.pack("<I", self.session_id)

            auth_data = password_bytes + session_id_bytes + challenge + password_bytes
            return hashlib.md5(auth_data).digest()

        else:
            Logger.warning(f"Unsupported authentication type: {self.auth_type}")
            return b'\x00' * 16
