"""IPMI user operations module."""
from typing import Dict, Any, List, Optional

from greenfish.utils.logger import Logger

# IPMI constants
IPMI_NETFN_APP = 0x06
IPMI_CMD_GET_USER_ACCESS = 0x44
IPMI_CMD_GET_USER_NAME = 0x45
IPMI_CMD_SET_USER_NAME = 0x46
IPMI_CMD_SET_USER_PASSWORD = 0x47
IPMI_CMD_SET_USER_ACCESS = 0x43
IPMI_CMD_GET_CHANNEL_ACCESS = 0x41
IPMI_CMD_SET_CHANNEL_ACCESS = 0x40

# User privilege levels
IPMI_PRIVILEGE_CALLBACK = 0x01
IPMI_PRIVILEGE_USER = 0x02
IPMI_PRIVILEGE_OPERATOR = 0x03
IPMI_PRIVILEGE_ADMINISTRATOR = 0x04
IPMI_PRIVILEGE_OEM = 0x05

# Password operations
IPMI_PASSWORD_SET_PASSWORD = 0x00
IPMI_PASSWORD_TEST_PASSWORD = 0x01
IPMI_PASSWORD_DISABLE_USER = 0x02
IPMI_PASSWORD_ENABLE_USER = 0x03

# Password types
IPMI_PASSWORD_TYPE_16_BYTES = 0x00
IPMI_PASSWORD_TYPE_20_BYTES = 0x01

class UserOperations:
    """IPMI user operations handler."""

    def __init__(self, protocol):
        """Initialize user operations handler.

        Args:
            protocol: IPMI protocol handler
        """
        self.protocol = protocol

    def get_user_access(self, channel: int = 1, user_id: int = 1) -> Dict[str, Any]:
        """Get user access information.

        Args:
            channel: Channel number
            user_id: User ID

        Returns:
            Dict containing user access information
        """
        request_data = bytes([
            channel & 0x0F,
            user_id
        ])

        response = self.protocol.send_command(IPMI_NETFN_APP, IPMI_CMD_GET_USER_ACCESS, request_data)

        if response['completion_code'] != 0:
            Logger.error(f"Failed to get user access: {response['completion_code']:#x}")
            return {}

        data = response['data']
        if len(data) < 4:
            Logger.error("Invalid user access response")
            return {}

        return {
            'max_user_ids': data[0] & 0x3F,
            'enabled_user_ids': data[1] & 0x3F,
            'fixed_user_ids': data[2] & 0x3F,
            'user_access': {
                'callback_allowed': bool(data[3] & 0x01),
                'link_auth_allowed': bool(data[3] & 0x02),
                'ipmi_msg_allowed': bool(data[3] & 0x04),
                'privilege_level': data[3] >> 4
            }
        }

    def get_user_name(self, user_id: int) -> str:
        """Get user name.

        Args:
            user_id: User ID

        Returns:
            User name
        """
        request_data = bytes([user_id])

        response = self.protocol.send_command(IPMI_NETFN_APP, IPMI_CMD_GET_USER_NAME, request_data)

        if response['completion_code'] != 0:
            Logger.error(f"Failed to get user name: {response['completion_code']:#x}")
            return ""

        data = response['data']
        if not data:
            return ""

        # Convert bytes to string, strip null bytes
        try:
            name = data.decode('ascii').rstrip('\x00')
        except UnicodeDecodeError:
            name = data.hex()

        return name

    def set_user_name(self, user_id: int, name: str) -> bool:
        """Set user name.

        Args:
            user_id: User ID
            name: User name (max 16 bytes)

        Returns:
            bool: True if successful
        """
        # Encode name and pad to 16 bytes
        name_bytes = name.encode('ascii')[:16].ljust(16, b'\x00')

        request_data = bytes([user_id]) + name_bytes

        response = self.protocol.send_command(IPMI_NETFN_APP, IPMI_CMD_SET_USER_NAME, request_data)

        if response['completion_code'] != 0:
            Logger.error(f"Failed to set user name: {response['completion_code']:#x}")
            return False

        return True

    def set_user_password(self, user_id: int, password: str, operation: int = IPMI_PASSWORD_SET_PASSWORD,
                         password_type: int = IPMI_PASSWORD_TYPE_16_BYTES) -> bool:
        """Set user password.

        Args:
            user_id: User ID
            password: Password
            operation: Password operation
            password_type: Password type

        Returns:
            bool: True if successful
        """
        # Encode password and pad appropriately
        if password_type == IPMI_PASSWORD_TYPE_16_BYTES:
            password_bytes = password.encode('ascii')[:16].ljust(16, b'\x00')
        else:  # IPMI_PASSWORD_TYPE_20_BYTES
            password_bytes = password.encode('ascii')[:20].ljust(20, b'\x00')

        request_data = bytes([
            user_id,
            (operation & 0x03) | ((password_type & 0x01) << 4)
        ]) + password_bytes

        response = self.protocol.send_command(IPMI_NETFN_APP, IPMI_CMD_SET_USER_PASSWORD, request_data)

        if response['completion_code'] != 0:
            Logger.error(f"Failed to set user password: {response['completion_code']:#x}")
            return False

        return True

    def enable_user(self, user_id: int) -> bool:
        """Enable user.

        Args:
            user_id: User ID

        Returns:
            bool: True if successful
        """
        return self.set_user_password(user_id, "", IPMI_PASSWORD_ENABLE_USER)

    def disable_user(self, user_id: int) -> bool:
        """Disable user.

        Args:
            user_id: User ID

        Returns:
            bool: True if successful
        """
        return self.set_user_password(user_id, "", IPMI_PASSWORD_DISABLE_USER)

    def test_password(self, user_id: int, password: str) -> bool:
        """Test if password is correct.

        Args:
            user_id: User ID
            password: Password to test

        Returns:
            bool: True if password is correct
        """
        result = self.set_user_password(user_id, password, IPMI_PASSWORD_TEST_PASSWORD)
        return result

    def set_user_access(self, user_id: int, channel: int = 1, privilege: int = IPMI_PRIVILEGE_USER,
                       callback: bool = False, link_auth: bool = True, ipmi_msg: bool = True,
                       enable_user: bool = True) -> bool:
        """Set user access.

        Args:
            user_id: User ID
            channel: Channel number
            privilege: Privilege level
            callback: Enable callback
            link_auth: Enable link authentication
            ipmi_msg: Enable IPMI messaging
            enable_user: Enable user

        Returns:
            bool: True if successful
        """
        # Build access flags
        access = 0
        if callback:
            access |= 0x01
        if link_auth:
            access |= 0x02
        if ipmi_msg:
            access |= 0x04
        if enable_user:
            access |= 0x80

        # Build request data
        request_data = bytes([
            (channel & 0x0F) | 0x80,  # Channel number with change bit set
            (user_id & 0x3F) | (access & 0xC0),  # User ID with enable/disable bits
            (access & 0x3F) | ((privilege & 0x0F) << 4),  # Access flags with privilege
            0x00  # Reserved
        ])

        response = self.protocol.send_command(IPMI_NETFN_APP, IPMI_CMD_SET_USER_ACCESS, request_data)

        if response['completion_code'] != 0:
            Logger.error(f"Failed to set user access: {response['completion_code']:#x}")
            return False

        return True

    def get_channel_access(self, channel: int = 1, get_non_volatile: bool = False) -> Dict[str, Any]:
        """Get channel access information.

        Args:
            channel: Channel number
            get_non_volatile: Get non-volatile settings

        Returns:
            Dict containing channel access information
        """
        request_data = bytes([
            channel & 0x0F,
            0x01 if get_non_volatile else 0x00
        ])

        response = self.protocol.send_command(IPMI_NETFN_APP, IPMI_CMD_GET_CHANNEL_ACCESS, request_data)

        if response['completion_code'] != 0:
            Logger.error(f"Failed to get channel access: {response['completion_code']:#x}")
            return {}

        data = response['data']
        if len(data) < 2:
            Logger.error("Invalid channel access response")
            return {}

        return {
            'access_mode': data[0] & 0x07,
            'user_level_auth': bool(data[0] & 0x10),
            'per_message_auth': bool(data[0] & 0x20),
            'pef_alerting': bool(data[0] & 0x40),
            'channel_privilege': data[1] & 0x0F
        }

    def set_channel_access(self, channel: int = 1, access_mode: int = None, user_level_auth: bool = None,
                          per_message_auth: bool = None, pef_alerting: bool = None,
                          privilege: int = None, volatile: bool = True) -> bool:
        """Set channel access.

        Args:
            channel: Channel number
            access_mode: Access mode
            user_level_auth: Enable user level authentication
            per_message_auth: Enable per-message authentication
            pef_alerting: Enable PEF alerting
            privilege: Channel privilege level
            volatile: Set volatile settings

        Returns:
            bool: True if successful
        """
        # Build access flags
        access_byte = 0
        access_mask = 0

        if access_mode is not None:
            access_byte |= access_mode & 0x07
            access_mask |= 0x07

        if user_level_auth is not None:
            if user_level_auth:
                access_byte |= 0x10
            access_mask |= 0x10

        if per_message_auth is not None:
            if per_message_auth:
                access_byte |= 0x20
            access_mask |= 0x20

        if pef_alerting is not None:
            if pef_alerting:
                access_byte |= 0x40
            access_mask |= 0x40

        # Build privilege byte
        priv_byte = 0
        priv_mask = 0

        if privilege is not None:
            priv_byte |= privilege & 0x0F
            priv_mask |= 0x0F

        # Set change bits
        if access_mask:
            access_byte |= 0x80

        if priv_mask:
            priv_byte |= 0x80

        # Build request data
        request_data = bytes([
            channel & 0x0F,
            (0x01 if volatile else 0x02),  # 0x01 = volatile, 0x02 = non-volatile
            access_byte,
            priv_byte
        ])

        response = self.protocol.send_command(IPMI_NETFN_APP, IPMI_CMD_SET_CHANNEL_ACCESS, request_data)

        if response['completion_code'] != 0:
            Logger.error(f"Failed to set channel access: {response['completion_code']:#x}")
            return False

        return True

    def list_users(self, max_users: int = 16) -> List[Dict[str, Any]]:
        """List all users.

        Args:
            max_users: Maximum number of users to check

        Returns:
            List of user dictionaries
        """
        users = []

        for user_id in range(1, max_users + 1):
            # Get user access
            access = self.get_user_access(1, user_id)
            if not access:
                continue

            # Get user name
            name = self.get_user_name(user_id)
            if not name:
                continue

            # Create user entry
            user = {
                'id': user_id,
                'name': name,
                'privilege': access.get('user_access', {}).get('privilege_level', 0),
                'enabled': access.get('user_access', {}).get('ipmi_msg_allowed', False)
            }

            users.append(user)

        return users

    def create_user(self, name: str, password: str, privilege: int = IPMI_PRIVILEGE_USER,
                   channel: int = 1) -> bool:
        """Create a new user.

        Args:
            name: User name
            password: User password
            privilege: Privilege level
            channel: Channel number

        Returns:
            bool: True if successful
        """
        # Find first available user ID
        max_users = 16  # Default max users
        for user_id in range(1, max_users + 1):
            existing_name = self.get_user_name(user_id)
            if not existing_name:
                # Found an empty slot
                break
        else:
            Logger.error("No available user slots")
            return False

        # Set user name
        if not self.set_user_name(user_id, name):
            return False

        # Set user password
        if not self.set_user_password(user_id, password):
            return False

        # Set user access
        if not self.set_user_access(user_id, channel, privilege):
            return False

        # Enable user
        if not self.enable_user(user_id):
            return False

        return True

    def delete_user(self, user_id: int) -> bool:
        """Delete a user.

        Args:
            user_id: User ID

        Returns:
            bool: True if successful
        """
        # Disable user
        if not self.disable_user(user_id):
            return False

        # Clear user name
        if not self.set_user_name(user_id, ""):
            return False

        return True
