"""Remote Console types and enumerations."""
from enum import Enum, auto
from typing import Dict, Any, Optional, List, Union

class ConsoleType(Enum):
    """Remote Console types."""

    KVM = "KVM"
    SERIAL = "Serial"
    SSH = "SSH"
    TELNET = "Telnet"
    VNC = "VNC"
    RDP = "RDP"
    UNKNOWN = "Unknown"

    @classmethod
    def from_string(cls, console_type: str) -> 'ConsoleType':
        """Convert string to ConsoleType.

        Args:
            console_type: Console type string

        Returns:
            ConsoleType: Corresponding console type
        """
        console_type = console_type.lower()

        if "kvm" in console_type:
            return cls.KVM
        elif "serial" in console_type:
            return cls.SERIAL
        elif "ssh" in console_type:
            return cls.SSH
        elif "telnet" in console_type:
            return cls.TELNET
        elif "vnc" in console_type:
            return cls.VNC
        elif "rdp" in console_type:
            return cls.RDP
        else:
            return cls.UNKNOWN

class ConsoleState(Enum):
    """Remote Console states."""

    CONNECTED = "Connected"
    DISCONNECTED = "Disconnected"
    CONNECTING = "Connecting"
    DISCONNECTING = "Disconnecting"
    ERROR = "Error"
    UNKNOWN = "Unknown"

    @classmethod
    def from_string(cls, state: str) -> 'ConsoleState':
        """Convert string to ConsoleState.

        Args:
            state: Console state string

        Returns:
            ConsoleState: Corresponding console state
        """
        state = state.lower()

        if "connect" in state and "ed" in state and "dis" not in state:
            return cls.CONNECTED
        elif "disconnect" in state and "ed" in state:
            return cls.DISCONNECTED
        elif "connect" in state and "ing" in state and "dis" not in state:
            return cls.CONNECTING
        elif "disconnect" in state and "ing" in state:
            return cls.DISCONNECTING
        elif "error" in state or "fail" in state:
            return cls.ERROR
        else:
            return cls.UNKNOWN

class RemoteConsole:
    """Remote Console object."""

    def __init__(self,
                 id: str = "",
                 name: str = "",
                 console_type: ConsoleType = ConsoleType.UNKNOWN,
                 state: ConsoleState = ConsoleState.UNKNOWN,
                 url: str = "",
                 host: str = "",
                 port: int = 0,
                 username: str = "",
                 password: str = "",
                 requires_plugin: bool = False,
                 plugin_type: str = "",
                 raw_data: Dict[str, Any] = None):
        """Initialize Remote Console object.

        Args:
            id: Console ID
            name: Console name
            console_type: Console type
            state: Console state
            url: Console URL
            host: Host address
            port: Port number
            username: Username
            password: Password
            requires_plugin: Whether console requires a plugin
            plugin_type: Plugin type
            raw_data: Raw data from server
        """
        self.id = id
        self.name = name
        self.console_type = console_type
        self.state = state
        self.url = url
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.requires_plugin = requires_plugin
        self.plugin_type = plugin_type
        self.raw_data = raw_data or {}

    def __str__(self) -> str:
        """Get string representation.

        Returns:
            str: String representation
        """
        return f"{self.name} ({self.console_type.value}): {self.state.value}"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary.

        Returns:
            Dict: Dictionary representation
        """
        return {
            "id": self.id,
            "name": self.name,
            "console_type": self.console_type.value,
            "state": self.state.value,
            "url": self.url,
            "host": self.host,
            "port": self.port,
            "username": self.username,
            "requires_plugin": self.requires_plugin,
            "plugin_type": self.plugin_type
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RemoteConsole':
        """Create from dictionary.

        Args:
            data: Dictionary data

        Returns:
            RemoteConsole: Remote console object
        """
        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            console_type=ConsoleType(data.get("console_type", ConsoleType.UNKNOWN.value)),
            state=ConsoleState(data.get("state", ConsoleState.UNKNOWN.value)),
            url=data.get("url", ""),
            host=data.get("host", ""),
            port=data.get("port", 0),
            username=data.get("username", ""),
            password=data.get("password", ""),
            requires_plugin=data.get("requires_plugin", False),
            plugin_type=data.get("plugin_type", ""),
            raw_data=data.get("raw_data", {})
        )

    @classmethod
    def from_redfish(cls, data: Dict[str, Any]) -> 'RemoteConsole':
        """Create from Redfish data.

        Args:
            data: Redfish data

        Returns:
            RemoteConsole: Remote console object
        """
        console_type = ConsoleType.UNKNOWN
        if "ConnectTypesSupported" in data and data["ConnectTypesSupported"]:
            console_type_str = data["ConnectTypesSupported"][0]
            console_type = ConsoleType.from_string(console_type_str)

        state = ConsoleState.UNKNOWN
        if "ServiceEnabled" in data:
            state = ConsoleState.CONNECTED if data["ServiceEnabled"] else ConsoleState.DISCONNECTED

        # Parse URL or connection details
        url = data.get("URI", "")
        host = ""
        port = 0

        if url:
            # Try to extract host and port from URL
            try:
                from urllib.parse import urlparse
                parsed_url = urlparse(url)
                host = parsed_url.hostname or ""
                port = parsed_url.port or 0
            except:
                pass

        return cls(
            id=data.get("Id", ""),
            name=data.get("Name", ""),
            console_type=console_type,
            state=state,
            url=url,
            host=host,
            port=port,
            username="",  # Redfish doesn't typically provide credentials
            password="",
            requires_plugin=data.get("RequiresPlugin", False),
            plugin_type=data.get("PluginType", ""),
            raw_data=data
        )
