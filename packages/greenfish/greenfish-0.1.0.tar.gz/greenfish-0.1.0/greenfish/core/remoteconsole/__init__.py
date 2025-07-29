"""Remote Console module for Redfish Desktop."""
from greenfish.core.remoteconsole.client import RemoteConsoleClient
from greenfish.core.remoteconsole.types import ConsoleType, ConsoleState
from greenfish.core.remoteconsole.viewers import KVMViewer, SerialViewer

__all__ = ['RemoteConsoleClient', 'ConsoleType', 'ConsoleState', 'KVMViewer', 'SerialViewer']
