"""Virtual Media client implementation."""
from typing import Dict, Any, Optional, List, Union
import os
import time
import urllib.parse
import requests
import json

from greenfish.utils.logger import Logger
from greenfish.core.virtualmedia.types import VirtualMedia, MediaType, MediaState

class VirtualMediaClient:
    """Virtual Media client for interacting with BMCs."""

    def __init__(self):
        """Initialize Virtual Media client."""
        self.redfish_client = None
        self.ipmi_client = None
        self.connection_type = None
        self.connected = False
        self.media_cache = {}

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
            self.media_cache = {}

            return True

        except Exception as e:
            Logger.error(f"Error connecting Virtual Media client: {str(e)}")
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
            self.media_cache = {}

            return True

        except Exception as e:
            Logger.error(f"Error connecting Virtual Media client: {str(e)}")
            self.connected = False
            return False

    def disconnect(self) -> bool:
        """Disconnect client.

        Returns:
            bool: True if successful
        """
        self.redfish_client = None
        self.ipmi_client = None
        self.connection_type = None
        self.connected = False
        self.media_cache = {}
        return True

    def is_connected(self) -> bool:
        """Check if client is connected.

        Returns:
            bool: True if connected
        """
        return self.connected

    def _get_redfish_virtual_media_collection(self) -> List[Dict[str, Any]]:
        """Get Redfish Virtual Media collection.

        Returns:
            List: Virtual Media collection
        """
        try:
            if not self.redfish_client or not self.connected:
                Logger.error("Not connected to Redfish")
                return []

            # Get Systems collection
            systems = self.redfish_client.get_systems()

            if not systems:
                Logger.error("No systems found")
                return []

            # Get first system
            system_id = systems[0].get("Id", "")

            # Get Manager for this system
            managers = self.redfish_client.get_managers()

            if not managers:
                Logger.error("No managers found")
                return []

            # Find manager for this system
            manager_id = None
            for manager in managers:
                if "Links" in manager and "ManagedSystems" in manager["Links"]:
                    managed_systems = manager["Links"]["ManagedSystems"]
                    for system in managed_systems:
                        if system_id in system.get("@odata.id", ""):
                            manager_id = manager.get("Id", "")
                            break

            if not manager_id:
                # Use first manager if no match found
                manager_id = managers[0].get("Id", "")

            # Get Virtual Media collection
            vm_collection = self.redfish_client.get(f"/redfish/v1/Managers/{manager_id}/VirtualMedia")

            if not vm_collection or "Members" not in vm_collection:
                Logger.error("Virtual Media collection not found")
                return []

            # Get each Virtual Media resource
            media_list = []

            for member in vm_collection["Members"]:
                media_uri = member.get("@odata.id", "")

                if media_uri:
                    media = self.redfish_client.get(media_uri)

                    if media:
                        media_list.append(media)

            return media_list

        except Exception as e:
            Logger.error(f"Error getting Virtual Media collection: {str(e)}")
            return []

    def _get_ipmi_virtual_media_info(self) -> List[Dict[str, Any]]:
        """Get IPMI Virtual Media information.

        Returns:
            List: Virtual Media information
        """
        try:
            if not self.ipmi_client or not self.connected:
                Logger.error("Not connected to IPMI")
                return []

            # Execute ipmitool command to get virtual media info
            result = self.ipmi_client.protocol.execute_ipmitool("raw", ["0x30", "0x42"])

            if not result["success"]:
                Logger.error(f"Failed to get IPMI Virtual Media info: {result['error']}")
                return []

            # Parse output
            output = result["output"]

            # This is a simplified example, as IPMI Virtual Media commands are vendor-specific
            # In a real implementation, this would need to be adapted to the specific BMC vendor

            # Example output format (this is hypothetical):
            # 01 00 01 00 00 00 00 00 00 00 00 00 00 00 00 00
            # Where:
            # - First byte: Number of virtual media devices
            # - Second byte: First device type (00 = CD/DVD)
            # - Third byte: First device status (01 = Connected)
            # - And so on for other devices

            media_list = []

            # Parse the output based on vendor-specific format
            # This is just a placeholder implementation
            bytes_data = [int(b, 16) for b in output.split()]

            if len(bytes_data) >= 1:
                num_devices = bytes_data[0]

                for i in range(num_devices):
                    if len(bytes_data) >= 3 + i * 2:
                        device_type = bytes_data[1 + i * 2]
                        device_status = bytes_data[2 + i * 2]

                        media_info = {
                            "id": f"vm{i}",
                            "name": f"Virtual Media {i}",
                            "type": self._get_media_type_from_ipmi(device_type),
                            "status": "inserted" if device_status == 1 else "ejected",
                            "inserted": device_status == 1
                        }

                        media_list.append(media_info)

            return media_list

        except Exception as e:
            Logger.error(f"Error getting IPMI Virtual Media info: {str(e)}")
            return []

    def _get_media_type_from_ipmi(self, type_code: int) -> str:
        """Get media type from IPMI type code.

        Args:
            type_code: IPMI type code

        Returns:
            str: Media type
        """
        # This mapping is vendor-specific and would need to be adapted
        media_types = {
            0: "CD",
            1: "DVD",
            2: "USB",
            3: "Floppy"
        }

        return media_types.get(type_code, "Unknown")

    def list_media(self) -> List[VirtualMedia]:
        """List available virtual media.

        Returns:
            List[VirtualMedia]: List of virtual media
        """
        media_list = []

        try:
            if not self.connected:
                Logger.error("Not connected")
                return []

            if self.connection_type == "redfish":
                # Get media from Redfish
                redfish_media = self._get_redfish_virtual_media_collection()

                for media_data in redfish_media:
                    media = VirtualMedia.from_redfish(media_data)
                    media_list.append(media)

                    # Update cache
                    self.media_cache[media.id] = media

            elif self.connection_type == "ipmi":
                # Get media from IPMI
                ipmi_media = self._get_ipmi_virtual_media_info()

                for media_data in ipmi_media:
                    media = VirtualMedia.from_ipmi(media_data)
                    media_list.append(media)

                    # Update cache
                    self.media_cache[media.id] = media

            return media_list

        except Exception as e:
            Logger.error(f"Error listing virtual media: {str(e)}")
            return []

    def get_media_info(self, media_id: str) -> Optional[VirtualMedia]:
        """Get virtual media information.

        Args:
            media_id: Media ID

        Returns:
            VirtualMedia: Virtual media information
        """
        try:
            if not self.connected:
                Logger.error("Not connected")
                return None

            # Check cache first
            if media_id in self.media_cache:
                return self.media_cache[media_id]

            if self.connection_type == "redfish":
                # Get media from Redfish
                redfish_media = self._get_redfish_virtual_media_collection()

                for media_data in redfish_media:
                    if media_data.get("Id") == media_id:
                        media = VirtualMedia.from_redfish(media_data)

                        # Update cache
                        self.media_cache[media.id] = media

                        return media

            elif self.connection_type == "ipmi":
                # Get media from IPMI
                ipmi_media = self._get_ipmi_virtual_media_info()

                for media_data in ipmi_media:
                    if media_data.get("id") == media_id:
                        media = VirtualMedia.from_ipmi(media_data)

                        # Update cache
                        self.media_cache[media.id] = media

                        return media

            Logger.error(f"Virtual media not found: {media_id}")
            return None

        except Exception as e:
            Logger.error(f"Error getting virtual media info: {str(e)}")
            return None

    def insert_media(self, media_id: str, image_url: str, write_protected: bool = True) -> bool:
        """Insert virtual media.

        Args:
            media_id: Media ID
            image_url: Image URL
            write_protected: Whether media is write-protected

        Returns:
            bool: True if successful
        """
        try:
            if not self.connected:
                Logger.error("Not connected")
                return False

            if self.connection_type == "redfish":
                # Get media info
                media_info = self.get_media_info(media_id)

                if not media_info:
                    Logger.error(f"Virtual media not found: {media_id}")
                    return False

                # Construct URI
                uri = f"/redfish/v1/Managers/{media_info.raw_data.get('@odata.id', '').split('/')[4]}/VirtualMedia/{media_id}/Actions/VirtualMedia.InsertMedia"

                # Construct payload
                payload = {
                    "Image": image_url,
                    "WriteProtected": write_protected
                }

                # Send request
                response = self.redfish_client.post(uri, payload)

                if not response or response.get("error"):
                    Logger.error(f"Failed to insert media: {response.get('error', {}).get('message', 'Unknown error')}")
                    return False

                # Clear cache entry to force refresh
                if media_id in self.media_cache:
                    del self.media_cache[media_id]

                Logger.info(f"Inserted virtual media {media_id} with image {image_url}")
                return True

            elif self.connection_type == "ipmi":
                # IPMI virtual media operations are vendor-specific
                # This is a simplified example

                # Get device number from media ID
                device_num = 0
                if media_id.startswith("vm"):
                    try:
                        device_num = int(media_id[2:])
                    except ValueError:
                        Logger.error(f"Invalid media ID format: {media_id}")
                        return False

                # Execute ipmitool command to insert media
                # This command is vendor-specific and would need to be adapted
                result = self.ipmi_client.protocol.execute_ipmitool("raw", ["0x30", "0x43", f"0x{device_num:02x}", "0x01", urllib.parse.quote(image_url)])

                if not result["success"]:
                    Logger.error(f"Failed to insert IPMI virtual media: {result['error']}")
                    return False

                # Clear cache entry to force refresh
                if media_id in self.media_cache:
                    del self.media_cache[media_id]

                Logger.info(f"Inserted IPMI virtual media {media_id} with image {image_url}")
                return True

            return False

        except Exception as e:
            Logger.error(f"Error inserting virtual media: {str(e)}")
            return False

    def eject_media(self, media_id: str) -> bool:
        """Eject virtual media.

        Args:
            media_id: Media ID

        Returns:
            bool: True if successful
        """
        try:
            if not self.connected:
                Logger.error("Not connected")
                return False

            if self.connection_type == "redfish":
                # Get media info
                media_info = self.get_media_info(media_id)

                if not media_info:
                    Logger.error(f"Virtual media not found: {media_id}")
                    return False

                # Construct URI
                uri = f"/redfish/v1/Managers/{media_info.raw_data.get('@odata.id', '').split('/')[4]}/VirtualMedia/{media_id}/Actions/VirtualMedia.EjectMedia"

                # Send request
                response = self.redfish_client.post(uri, {})

                if not response or response.get("error"):
                    Logger.error(f"Failed to eject media: {response.get('error', {}).get('message', 'Unknown error')}")
                    return False

                # Clear cache entry to force refresh
                if media_id in self.media_cache:
                    del self.media_cache[media_id]

                Logger.info(f"Ejected virtual media {media_id}")
                return True

            elif self.connection_type == "ipmi":
                # IPMI virtual media operations are vendor-specific
                # This is a simplified example

                # Get device number from media ID
                device_num = 0
                if media_id.startswith("vm"):
                    try:
                        device_num = int(media_id[2:])
                    except ValueError:
                        Logger.error(f"Invalid media ID format: {media_id}")
                        return False

                # Execute ipmitool command to eject media
                # This command is vendor-specific and would need to be adapted
                result = self.ipmi_client.protocol.execute_ipmitool("raw", ["0x30", "0x43", f"0x{device_num:02x}", "0x00"])

                if not result["success"]:
                    Logger.error(f"Failed to eject IPMI virtual media: {result['error']}")
                    return False

                # Clear cache entry to force refresh
                if media_id in self.media_cache:
                    del self.media_cache[media_id]

                Logger.info(f"Ejected IPMI virtual media {media_id}")
                return True

            return False

        except Exception as e:
            Logger.error(f"Error ejecting virtual media: {str(e)}")
            return False
