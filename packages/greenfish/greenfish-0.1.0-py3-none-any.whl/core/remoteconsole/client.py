"""Remote Console client implementation."""
from typing import Dict, Any, Optional, List, Union
import os
import time
import urllib.parse
import requests
import json
import subprocess
import tempfile
import platform
import socket

from greenfish.utils.logger import Logger
from greenfish.core.remoteconsole.types import RemoteConsole, ConsoleType, ConsoleState

class RemoteConsoleClient:
    """Remote Console client for interacting with BMCs."""

    def __init__(self):
        """Initialize Remote Console client."""
        self.redfish_client = None
        self.ipmi_client = None
        self.connection_type = None
        self.connected = False
        self.console_cache = {}
        self.active_consoles = {}

    def connect_redfish(self, redfish_client) -> bool:
        """Connect using Redfish client.

        Args:
            redfish_client: Redfish client

        Returns:
            bool: True if successful
        """
        try:
            if not redfish_client or not redfish_client.is_connected():
                Logger.error("Redfish client is not connected")
                return False

            self.redfish_client = redfish_client
            self.connection_type = "redfish"
            self.connected = True

            # Clear cache
            self.console_cache = {}

            return True

        except Exception as e:
            Logger.error(f"Error connecting Remote Console client: {str(e)}")
            self.connected = False
            return False

    def connect_ipmi(self, ipmi_client) -> bool:
        """Connect using IPMI client.

        Args:
            ipmi_client: IPMI client

        Returns:
            bool: True if successful
        """
        try:
            if not ipmi_client or not ipmi_client.is_connected():
                Logger.error("IPMI client is not connected")
                return False

            self.ipmi_client = ipmi_client
            self.connection_type = "ipmi"
            self.connected = True

            # Clear cache
            self.console_cache = {}

            return True

        except Exception as e:
            Logger.error(f"Error connecting Remote Console client: {str(e)}")
            self.connected = False
            return False

    def disconnect(self) -> bool:
        """Disconnect client.

        Returns:
            bool: True if successful
        """
        # Disconnect all active consoles
        for console_id in list(self.active_consoles.keys()):
            self.disconnect_console(console_id)

        self.redfish_client = None
        self.ipmi_client = None
        self.connection_type = None
        self.connected = False
        self.console_cache = {}
        self.active_consoles = {}
        return True

    def is_connected(self) -> bool:
        """Check if client is connected.

        Returns:
            bool: True if connected
        """
        return self.connected

    def _get_redfish_console_collection(self) -> List[Dict[str, Any]]:
        """Get Redfish Console collection.

        Returns:
            List: Console collection
        """
        try:
            if not self.redfish_client or not self.connected:
                Logger.error("Not connected to Redfish")
                return []

            # Get Managers collection
            managers = self.redfish_client.get_managers()

            if not managers:
                Logger.error("No managers found")
                return []

            # Get first manager
            manager_id = managers[0].get("Id", "")

            # Check for GraphicalConsole
            console_list = []

            # Check for GraphicalConsole
            graphical_console = self.redfish_client.get(f"/redfish/v1/Managers/{manager_id}/GraphicalConsole")
            if graphical_console and not graphical_console.get("error"):
                graphical_console["Id"] = "GraphicalConsole"
                graphical_console["Name"] = "Graphical Console"
                console_list.append(graphical_console)

            # Check for SerialConsole
            serial_console = self.redfish_client.get(f"/redfish/v1/Managers/{manager_id}/SerialConsole")
            if serial_console and not serial_console.get("error"):
                serial_console["Id"] = "SerialConsole"
                serial_console["Name"] = "Serial Console"
                console_list.append(serial_console)

            # Check for VirtualMedia (some implementations expose console through VirtualMedia)
            virtual_media = self.redfish_client.get(f"/redfish/v1/Managers/{manager_id}/VirtualMedia")
            if virtual_media and "Members" in virtual_media:
                for member in virtual_media["Members"]:
                    media_uri = member.get("@odata.id", "")
                    if media_uri and "Console" in media_uri:
                        media = self.redfish_client.get(media_uri)
                        if media and not media.get("error"):
                            console_list.append(media)

            return console_list

        except Exception as e:
            Logger.error(f"Error getting Remote Console collection: {str(e)}")
            return []

    def _get_ipmi_console_info(self) -> List[Dict[str, Any]]:
        """Get IPMI Console information.

        Returns:
            List: Console information
        """
        try:
            if not self.ipmi_client or not self.connected:
                Logger.error("Not connected to IPMI")
                return []

            console_list = []

            # Get BMC information to determine vendor
            bmc_info = self.ipmi_client.get_bmc_info()

            # Add Serial-over-LAN console
            sol_console = {
                "id": "sol",
                "name": "Serial Over LAN",
                "type": "Serial",
                "status": "Available",
                "host": self.ipmi_client.host,
                "port": self.ipmi_client.port,
                "username": self.ipmi_client.username
            }
            console_list.append(sol_console)

            # Add KVM console based on vendor
            # This is vendor-specific and would need to be adapted
            manufacturer_id = bmc_info.get("manufacturer_id", 0)

            # Example vendor detection
            if manufacturer_id == 0x2A7C:  # Dell
                kvm_console = {
                    "id": "kvm",
                    "name": "KVM Console",
                    "type": "KVM",
                    "status": "Available",
                    "url": f"https://{self.ipmi_client.host}/console",
                    "host": self.ipmi_client.host,
                    "requires_plugin": True,
                    "plugin_type": "Java"
                }
                console_list.append(kvm_console)
            elif manufacturer_id == 0x47:  # HP
                kvm_console = {
                    "id": "kvm",
                    "name": "iLO Remote Console",
                    "type": "KVM",
                    "status": "Available",
                    "url": f"https://{self.ipmi_client.host}/html/console.html",
                    "host": self.ipmi_client.host,
                    "requires_plugin": False
                }
                console_list.append(kvm_console)
            elif manufacturer_id == 0x2A:  # IBM/Lenovo
                kvm_console = {
                    "id": "kvm",
                    "name": "IMM Remote Console",
                    "type": "KVM",
                    "status": "Available",
                    "url": f"https://{self.ipmi_client.host}/designs/imm/remcons.html",
                    "host": self.ipmi_client.host,
                    "requires_plugin": True,
                    "plugin_type": "Java"
                }
                console_list.append(kvm_console)
            elif manufacturer_id == 0x15D9:  # Supermicro
                kvm_console = {
                    "id": "kvm",
                    "name": "IKVM Console",
                    "type": "KVM",
                    "status": "Available",
                    "url": f"https://{self.ipmi_client.host}/cgi/url_redirect.cgi?url_name=ikvm&url_type=jwsk",
                    "host": self.ipmi_client.host,
                    "requires_plugin": True,
                    "plugin_type": "Java"
                }
                console_list.append(kvm_console)

            return console_list

        except Exception as e:
            Logger.error(f"Error getting IPMI Console info: {str(e)}")
            return []

    def list_consoles(self) -> List[RemoteConsole]:
        """List available remote consoles.

        Returns:
            List[RemoteConsole]: List of remote consoles
        """
        console_list = []

        try:
            if not self.connected:
                Logger.error("Not connected")
                return []

            if self.connection_type == "redfish":
                # Get consoles from Redfish
                redfish_consoles = self._get_redfish_console_collection()

                for console_data in redfish_consoles:
                    console = RemoteConsole.from_redfish(console_data)
                    console_list.append(console)

                    # Update cache
                    self.console_cache[console.id] = console

            elif self.connection_type == "ipmi":
                # Get consoles from IPMI
                ipmi_consoles = self._get_ipmi_console_info()

                for console_data in ipmi_consoles:
                    console = RemoteConsole(
                        id=console_data.get("id", ""),
                        name=console_data.get("name", ""),
                        console_type=ConsoleType.from_string(console_data.get("type", "")),
                        state=ConsoleState.DISCONNECTED,
                        url=console_data.get("url", ""),
                        host=console_data.get("host", ""),
                        port=console_data.get("port", 0),
                        username=console_data.get("username", ""),
                        requires_plugin=console_data.get("requires_plugin", False),
                        plugin_type=console_data.get("plugin_type", ""),
                        raw_data=console_data
                    )
                    console_list.append(console)

                    # Update cache
                    self.console_cache[console.id] = console

            return console_list

        except Exception as e:
            Logger.error(f"Error listing remote consoles: {str(e)}")
            return []

    def get_console_info(self, console_id: str) -> Optional[RemoteConsole]:
        """Get remote console information.

        Args:
            console_id: Console ID

        Returns:
            RemoteConsole: Remote console information
        """
        try:
            if not self.connected:
                Logger.error("Not connected")
                return None

            # Check cache first
            if console_id in self.console_cache:
                # Check if console is active
                if console_id in self.active_consoles:
                    console = self.console_cache[console_id]
                    console.state = ConsoleState.CONNECTED
                    return console
                return self.console_cache[console_id]

            # Refresh console list
            self.list_consoles()

            if console_id in self.console_cache:
                return self.console_cache[console_id]

            Logger.error(f"Remote console not found: {console_id}")
            return None

        except Exception as e:
            Logger.error(f"Error getting remote console info: {str(e)}")
            return None

    def connect_console(self, console_id: str, viewer_class=None) -> bool:
        """Connect to remote console.

        Args:
            console_id: Console ID
            viewer_class: Viewer class (optional)

        Returns:
            bool: True if successful
        """
        try:
            if not self.connected:
                Logger.error("Not connected")
                return False

            # Get console info
            console = self.get_console_info(console_id)

            if not console:
                Logger.error(f"Remote console not found: {console_id}")
                return False

            # Check if already connected
            if console_id in self.active_consoles:
                Logger.info(f"Console already connected: {console_id}")
                return True

            if self.connection_type == "redfish":
                # Connect using Redfish
                if console.console_type == ConsoleType.KVM:
                    # Launch KVM viewer
                    if viewer_class:
                        viewer = viewer_class(console.url)
                        success = viewer.launch()

                        if success:
                            self.active_consoles[console_id] = viewer
                            console.state = ConsoleState.CONNECTED
                            self.console_cache[console_id] = console
                            Logger.info(f"Connected to KVM console: {console_id}")
                            return True
                    else:
                        # Use system default browser
                        import webbrowser
                        webbrowser.open(console.url)
                        self.active_consoles[console_id] = True
                        console.state = ConsoleState.CONNECTED
                        self.console_cache[console_id] = console
                        Logger.info(f"Opened KVM console URL: {console_id}")
                        return True

                elif console.console_type == ConsoleType.SERIAL:
                    # Launch Serial viewer
                    if viewer_class:
                        viewer = viewer_class(console.url)
                        success = viewer.launch()

                        if success:
                            self.active_consoles[console_id] = viewer
                            console.state = ConsoleState.CONNECTED
                            self.console_cache[console_id] = console
                            Logger.info(f"Connected to Serial console: {console_id}")
                            return True
                    else:
                        # Use system default browser or terminal
                        import webbrowser
                        webbrowser.open(console.url)
                        self.active_consoles[console_id] = True
                        console.state = ConsoleState.CONNECTED
                        self.console_cache[console_id] = console
                        Logger.info(f"Opened Serial console URL: {console_id}")
                        return True

            elif self.connection_type == "ipmi":
                # Connect using IPMI
                if console.console_type == ConsoleType.KVM:
                    # Launch KVM viewer
                    if viewer_class:
                        viewer = viewer_class(console.url)
                        success = viewer.launch()

                        if success:
                            self.active_consoles[console_id] = viewer
                            console.state = ConsoleState.CONNECTED
                            self.console_cache[console_id] = console
                            Logger.info(f"Connected to KVM console: {console_id}")
                            return True
                    else:
                        # Use system default browser
                        import webbrowser
                        webbrowser.open(console.url)
                        self.active_consoles[console_id] = True
                        console.state = ConsoleState.CONNECTED
                        self.console_cache[console_id] = console
                        Logger.info(f"Opened KVM console URL: {console_id}")
                        return True

                elif console.console_type == ConsoleType.SERIAL:
                    # Launch SOL session
                    if console_id == "sol":
                        # Start SOL session
                        if self.ipmi_client and hasattr(self.ipmi_client, 'sol'):
                            # Create a SOL viewer
                            if viewer_class:
                                viewer = viewer_class()

                                # Define callbacks
                                def data_callback(data):
                                    viewer.receive_data(data)

                                def close_callback():
                                    viewer.close()

                                # Start SOL session
                                success = self.ipmi_client.sol.start_sol_session(
                                    data_callback=data_callback,
                                    close_callback=close_callback
                                )

                                if success:
                                    # Set up send data callback
                                    def send_data_callback(data):
                                        self.ipmi_client.sol.send_sol_data(data)

                                    viewer.set_send_callback(send_data_callback)

                                    # Launch viewer
                                    viewer_success = viewer.launch()

                                    if viewer_success:
                                        self.active_consoles[console_id] = viewer
                                        console.state = ConsoleState.CONNECTED
                                        self.console_cache[console_id] = console
                                        Logger.info(f"Connected to SOL console: {console_id}")
                                        return True
                                    else:
                                        # Stop SOL session if viewer failed
                                        self.ipmi_client.sol.stop_sol_session()

                                Logger.error(f"Failed to start SOL session")
                                return False
                            else:
                                # Use ipmitool directly
                                try:
                                    cmd = ["ipmitool",
                                           "-I", "lanplus",
                                           "-H", self.ipmi_client.host,
                                           "-U", self.ipmi_client.username,
                                           "-P", self.ipmi_client.password,
                                           "sol", "activate"]

                                    # Create temporary file for password
                                    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp:
                                        temp_path = temp.name
                                        temp.write(self.ipmi_client.password)

                                    try:
                                        # Replace password with file path in command
                                        password_index = cmd.index("-P") + 1
                                        cmd[password_index] = temp_path

                                        # Add password file flag
                                        cmd[password_index - 1] = "-f"

                                        # Execute command
                                        process = subprocess.Popen(cmd)

                                        # Store process
                                        self.active_consoles[console_id] = process
                                        console.state = ConsoleState.CONNECTED
                                        self.console_cache[console_id] = console
                                        Logger.info(f"Connected to SOL console: {console_id}")
                                        return True

                                    finally:
                                        # Remove temporary password file
                                        try:
                                            os.unlink(temp_path)
                                        except:
                                            pass

                                except Exception as e:
                                    Logger.error(f"Failed to start SOL session: {str(e)}")
                                    return False

            Logger.error(f"Unsupported console type: {console.console_type}")
            return False

        except Exception as e:
            Logger.error(f"Error connecting to remote console: {str(e)}")
            return False

    def disconnect_console(self, console_id: str) -> bool:
        """Disconnect from remote console.

        Args:
            console_id: Console ID

        Returns:
            bool: True if successful
        """
        try:
            if not self.connected:
                Logger.error("Not connected")
                return False

            # Check if console is active
            if console_id not in self.active_consoles:
                Logger.info(f"Console not connected: {console_id}")
                return True

            # Get console info
            console = self.get_console_info(console_id)

            if not console:
                Logger.error(f"Remote console not found: {console_id}")
                return False

            # Disconnect based on console type
            viewer = self.active_consoles[console_id]

            if hasattr(viewer, 'close'):
                # Close viewer
                viewer.close()
            elif isinstance(viewer, subprocess.Popen):
                # Terminate process
                viewer.terminate()
                try:
                    viewer.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    viewer.kill()

            # Update state
            console.state = ConsoleState.DISCONNECTED
            self.console_cache[console_id] = console

            # Remove from active consoles
            del self.active_consoles[console_id]

            Logger.info(f"Disconnected from console: {console_id}")
            return True

        except Exception as e:
            Logger.error(f"Error disconnecting from remote console: {str(e)}")
            return False

    def send_keystrokes(self, console_id: str, keystrokes: str) -> bool:
        """Send keystrokes to remote console.

        Args:
            console_id: Console ID
            keystrokes: Keystrokes to send

        Returns:
            bool: True if successful
        """
        try:
            if not self.connected:
                Logger.error("Not connected")
                return False

            # Check if console is active
            if console_id not in self.active_consoles:
                Logger.error(f"Console not connected: {console_id}")
                return False

            # Get console info
            console = self.get_console_info(console_id)

            if not console:
                Logger.error(f"Remote console not found: {console_id}")
                return False

            # Send keystrokes based on console type
            viewer = self.active_consoles[console_id]

            if hasattr(viewer, 'send_keystrokes'):
                # Send keystrokes to viewer
                viewer.send_keystrokes(keystrokes)
                return True
            elif console.console_type == ConsoleType.SERIAL and self.connection_type == "ipmi":
                # Send data to SOL session
                if hasattr(self.ipmi_client, 'sol'):
                    self.ipmi_client.sol.send_sol_data(keystrokes)
                    return True

            Logger.error(f"Sending keystrokes not supported for this console type")
            return False

        except Exception as e:
            Logger.error(f"Error sending keystrokes to remote console: {str(e)}")
            return False

    def send_special_key(self, console_id: str, key: str) -> bool:
        """Send special key to remote console.

        Args:
            console_id: Console ID
            key: Special key (e.g., "CTRL+ALT+DEL", "F1", etc.)

        Returns:
            bool: True if successful
        """
        try:
            if not self.connected:
                Logger.error("Not connected")
                return False

            # Check if console is active
            if console_id not in self.active_consoles:
                Logger.error(f"Console not connected: {console_id}")
                return False

            # Get console info
            console = self.get_console_info(console_id)

            if not console:
                Logger.error(f"Remote console not found: {console_id}")
                return False

            # Send special key based on console type
            viewer = self.active_consoles[console_id]

            if hasattr(viewer, 'send_special_key'):
                # Send special key to viewer
                viewer.send_special_key(key)
                return True
            elif console.console_type == ConsoleType.SERIAL and self.connection_type == "ipmi":
                # Map special keys to escape sequences for SOL
                key_map = {
                    "CTRL+C": "\x03",
                    "CTRL+D": "\x04",
                    "CTRL+Z": "\x1A",
                    "ESC": "\x1B",
                    "ENTER": "\r",
                    "BACKSPACE": "\x08"
                }

                if key in key_map:
                    if hasattr(self.ipmi_client, 'sol'):
                        self.ipmi_client.sol.send_sol_data(key_map[key])
                        return True

            Logger.error(f"Sending special key not supported for this console type")
            return False

        except Exception as e:
            Logger.error(f"Error sending special key to remote console: {str(e)}")
            return False
