"""IPMI protocol implementation."""
from typing import Dict, Any, Optional, List, Union, Tuple
import subprocess
import re
import os
import tempfile
import time
import platform
from greenfish.utils.logger import Logger

class IPMIProtocol:
    """IPMI 2.0 protocol implementation using ipmitool."""

    def __init__(self):
        """Initialize IPMI protocol handler."""
        self.host = None
        self.port = None
        self.username = None
        self.password = None
        self.interface = None
        self.timeout = None
        self.kg_key = None
        self.privilege_level = None
        self.connected = False
        self._check_ipmitool()

    def _check_ipmitool(self) -> bool:
        """Check if ipmitool is available.

        Returns:
            bool: True if ipmitool is available
        """
        try:
            result = subprocess.run(
                ["ipmitool", "-V"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=5
            )

            if result.returncode == 0:
                Logger.debug(f"ipmitool found: {result.stdout.strip()}")
                return True
            else:
                Logger.error(f"ipmitool check failed: {result.stderr.strip()}")
                return False

        except FileNotFoundError:
            Logger.error("ipmitool not found in PATH")
            return False
        except Exception as e:
            Logger.error(f"Error checking for ipmitool: {str(e)}")
            return False

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
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.interface = interface
        self.timeout = timeout
        self.kg_key = kg_key
        self.privilege_level = privilege_level

        # Test connection by getting device ID
        try:
            result = self.send_command(0x06, 0x01)  # NetFn App, Cmd Get Device ID
            if result['completion_code'] == 0:
                self.connected = True
                return True
            else:
                Logger.error(f"IPMI connection test failed: {result['completion_code']:#x}")
                self.connected = False
                return False

        except Exception as e:
            Logger.error(f"IPMI connection error: {str(e)}")
            self.connected = False
            return False

    def disconnect(self) -> bool:
        """Disconnect from BMC.

        Returns:
            bool: True if disconnection successful
        """
        # No actual disconnection needed for ipmitool
        self.connected = False
        return True

    def _build_ipmitool_base_cmd(self) -> List[str]:
        """Build base ipmitool command with connection parameters.

        Returns:
            List[str]: Base command arguments
        """
        cmd = ["ipmitool"]

        # Add interface
        cmd.extend(["-I", self.interface])

        # Add connection details
        cmd.extend(["-H", self.host])
        cmd.extend(["-p", str(self.port)])
        cmd.extend(["-U", self.username])
        cmd.extend(["-P", self.password])

        # Add timeout
        cmd.extend(["-N", str(self.timeout)])

        # Add K_g key if provided
        if self.kg_key:
            cmd.extend(["-k", self.kg_key])

        # Add privilege level
        cmd.extend(["-L", self.privilege_level])

        return cmd

    def send_raw_command(self, raw_data: List[int]) -> Dict[str, Any]:
        """Send a raw IPMI command.

        Args:
            raw_data: List of bytes for the raw command

        Returns:
            Dict containing response data and completion code
        """
        if not self.host:
            return {'completion_code': 0xC0, 'data': [], 'error': 'Not connected'}

        try:
            cmd = self._build_ipmitool_base_cmd()
            cmd.append("raw")
            cmd.extend([str(b) for b in raw_data])

            Logger.debug(f"Executing IPMI command: {' '.join(cmd)}")

            # Create temporary file for password
            with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp:
                temp_path = temp.name
                temp.write(self.password)

            try:
                # Replace password with file path in command
                password_index = cmd.index("-P") + 1
                cmd[password_index] = temp_path

                # Add password file flag
                cmd[password_index - 1] = "-f"

                # Execute command
                result = subprocess.run(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=self.timeout + 5
                )

            finally:
                # Remove temporary password file
                try:
                    os.unlink(temp_path)
                except:
                    pass

            if result.returncode != 0:
                error_msg = result.stderr.strip()
                Logger.error(f"IPMI command failed: {error_msg}")
                return {'completion_code': 0xC0, 'data': [], 'error': error_msg}

            # Parse output
            output = result.stdout.strip()
            if not output:
                return {'completion_code': 0, 'data': []}

            # Convert hex output to bytes
            data_bytes = []
            for part in output.split():
                try:
                    data_bytes.append(int(part, 16))
                except ValueError:
                    pass

            return {'completion_code': 0, 'data': data_bytes}

        except subprocess.TimeoutExpired:
            Logger.error(f"IPMI command timed out after {self.timeout + 5} seconds")
            return {'completion_code': 0xC3, 'data': [], 'error': 'Timeout'}
        except Exception as e:
            Logger.error(f"IPMI command error: {str(e)}")
            return {'completion_code': 0xC0, 'data': [], 'error': str(e)}

    def send_command(self, netfn: int, cmd: int, data: bytes = b'') -> Dict[str, Any]:
        """Send an IPMI command.

        Args:
            netfn: Network function code
            cmd: Command code
            data: Command data bytes

        Returns:
            Dict containing response data and completion code
        """
        raw_data = [netfn, cmd]

        # Add data bytes if provided
        if isinstance(data, bytes) and data:
            raw_data.extend(list(data))
        elif isinstance(data, list):
            raw_data.extend(data)

        return self.send_raw_command(raw_data)

    def execute_ipmitool(self, subcommand: str, args: List[str] = None) -> Dict[str, Any]:
        """Execute an ipmitool subcommand.

        Args:
            subcommand: Ipmitool subcommand
            args: Additional arguments

        Returns:
            Dict containing command result
        """
        if not self.host:
            return {'success': False, 'output': '', 'error': 'Not connected'}

        try:
            cmd = self._build_ipmitool_base_cmd()
            cmd.append(subcommand)

            if args:
                cmd.extend(args)

            Logger.debug(f"Executing ipmitool command: {' '.join(cmd)}")

            # Create temporary file for password
            with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp:
                temp_path = temp.name
                temp.write(self.password)

            try:
                # Replace password with file path in command
                password_index = cmd.index("-P") + 1
                cmd[password_index] = temp_path

                # Add password file flag
                cmd[password_index - 1] = "-f"

                # Execute command
                result = subprocess.run(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=self.timeout + 5
                )

            finally:
                # Remove temporary password file
                try:
                    os.unlink(temp_path)
                except:
                    pass

            if result.returncode != 0:
                error_msg = result.stderr.strip()
                Logger.error(f"ipmitool command failed: {error_msg}")
                return {'success': False, 'output': '', 'error': error_msg}

            return {'success': True, 'output': result.stdout.strip(), 'error': ''}

        except subprocess.TimeoutExpired:
            Logger.error(f"ipmitool command timed out after {self.timeout + 5} seconds")
            return {'success': False, 'output': '', 'error': 'Timeout'}
        except Exception as e:
            Logger.error(f"ipmitool command error: {str(e)}")
            return {'success': False, 'output': '', 'error': str(e)}

    def parse_ipmitool_output(self, output: str, pattern: str) -> List[Dict[str, str]]:
        """Parse output from ipmitool commands.

        Args:
            output: Command output string
            pattern: Regex pattern for parsing

        Returns:
            List of dictionaries with parsed values
        """
        results = []

        try:
            # Split output into lines and process each line
            for line in output.strip().split('\n'):
                match = re.search(pattern, line)
                if match:
                    results.append(match.groupdict())
        except Exception as e:
            Logger.error(f"Error parsing ipmitool output: {str(e)}")

        return results
