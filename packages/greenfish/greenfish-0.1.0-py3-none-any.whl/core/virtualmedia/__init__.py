"""Virtual Media Management module for Redfish Desktop."""
from greenfish.core.virtualmedia.client import VirtualMediaClient
from greenfish.core.virtualmedia.types import MediaType, MediaState, VirtualMedia
from greenfish.core.virtualmedia.operations import VirtualMediaOperations

__all__ = ['VirtualMediaClient', 'MediaType', 'MediaState', 'VirtualMediaOperations', 'VirtualMedia']
