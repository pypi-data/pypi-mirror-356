"""IPMI integration module for Redfish Desktop."""
from greenfish.core.ipmi.protocols import IPMIProtocol
from greenfish.core.ipmi.client import IPMIClient

__all__ = ['IPMIProtocol', 'IPMIClient']
