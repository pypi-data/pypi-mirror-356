"""Virtual Media types and enumerations."""
from enum import Enum, auto
from typing import Dict, Any, Optional, List, Union

class MediaType(Enum):
    """Virtual Media types."""

    CD = "CD"
    DVD = "DVD"
    USB = "USB"
    FLOPPY = "Floppy"
    ISO = "ISO"
    IMG = "IMG"
    UNKNOWN = "Unknown"

    @classmethod
    def from_string(cls, media_type: str) -> 'MediaType':
        """Convert string to MediaType.

        Args:
            media_type: Media type string

        Returns:
            MediaType: Corresponding media type
        """
        media_type = media_type.lower()

        if "cd" in media_type or "optical" in media_type:
            return cls.CD
        elif "dvd" in media_type:
            return cls.DVD
        elif "usb" in media_type:
            return cls.USB
        elif "floppy" in media_type:
            return cls.FLOPPY
        elif "iso" in media_type:
            return cls.ISO
        elif "img" in media_type:
            return cls.IMG
        else:
            return cls.UNKNOWN

class MediaState(Enum):
    """Virtual Media states."""

    INSERTED = "Inserted"
    EJECTED = "Ejected"
    CONNECTING = "Connecting"
    DISCONNECTING = "Disconnecting"
    ERROR = "Error"
    UNKNOWN = "Unknown"

    @classmethod
    def from_string(cls, state: str) -> 'MediaState':
        """Convert string to MediaState.

        Args:
            state: Media state string

        Returns:
            MediaState: Corresponding media state
        """
        state = state.lower()

        if "insert" in state:
            return cls.INSERTED
        elif "eject" in state or "disconnect" in state:
            return cls.EJECTED
        elif "connect" in state and "ing" in state:
            return cls.CONNECTING
        elif "disconnect" in state and "ing" in state:
            return cls.DISCONNECTING
        elif "error" in state or "fail" in state:
            return cls.ERROR
        else:
            return cls.UNKNOWN

class VirtualMedia:
    """Virtual Media object."""

    def __init__(self,
                 id: str = "",
                 name: str = "",
                 media_type: MediaType = MediaType.UNKNOWN,
                 state: MediaState = MediaState.UNKNOWN,
                 image_url: str = "",
                 inserted: bool = False,
                 write_protected: bool = True,
                 connected_via: str = "",
                 raw_data: Dict[str, Any] = None):
        """Initialize Virtual Media object.

        Args:
            id: Media ID
            name: Media name
            media_type: Media type
            state: Media state
            image_url: Image URL
            inserted: Whether media is inserted
            write_protected: Whether media is write-protected
            connected_via: Connection method
            raw_data: Raw data from server
        """
        self.id = id
        self.name = name
        self.media_type = media_type
        self.state = state
        self.image_url = image_url
        self.inserted = inserted
        self.write_protected = write_protected
        self.connected_via = connected_via
        self.raw_data = raw_data or {}

    def __str__(self) -> str:
        """Get string representation.

        Returns:
            str: String representation
        """
        return f"{self.name} ({self.media_type.value}): {'Inserted' if self.inserted else 'Ejected'}"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary.

        Returns:
            Dict: Dictionary representation
        """
        return {
            "id": self.id,
            "name": self.name,
            "media_type": self.media_type.value,
            "state": self.state.value,
            "image_url": self.image_url,
            "inserted": self.inserted,
            "write_protected": self.write_protected,
            "connected_via": self.connected_via
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'VirtualMedia':
        """Create from dictionary.

        Args:
            data: Dictionary data

        Returns:
            VirtualMedia: Virtual media object
        """
        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            media_type=MediaType(data.get("media_type", MediaType.UNKNOWN.value)),
            state=MediaState(data.get("state", MediaState.UNKNOWN.value)),
            image_url=data.get("image_url", ""),
            inserted=data.get("inserted", False),
            write_protected=data.get("write_protected", True),
            connected_via=data.get("connected_via", ""),
            raw_data=data.get("raw_data", {})
        )

    @classmethod
    def from_redfish(cls, data: Dict[str, Any]) -> 'VirtualMedia':
        """Create from Redfish data.

        Args:
            data: Redfish data

        Returns:
            VirtualMedia: Virtual media object
        """
        media_type = MediaType.UNKNOWN
        if "MediaTypes" in data and data["MediaTypes"]:
            media_type = MediaType.from_string(data["MediaTypes"][0])

        state = MediaState.UNKNOWN
        if "Inserted" in data:
            state = MediaState.INSERTED if data["Inserted"] else MediaState.EJECTED

        return cls(
            id=data.get("Id", ""),
            name=data.get("Name", ""),
            media_type=media_type,
            state=state,
            image_url=data.get("Image", ""),
            inserted=data.get("Inserted", False),
            write_protected=data.get("WriteProtected", True),
            connected_via=data.get("ConnectedVia", ""),
            raw_data=data
        )

    @classmethod
    def from_ipmi(cls, data: Dict[str, Any]) -> 'VirtualMedia':
        """Create from IPMI data.

        Args:
            data: IPMI data

        Returns:
            VirtualMedia: Virtual media object
        """
        media_type = MediaType.UNKNOWN
        if "type" in data:
            media_type = MediaType.from_string(data["type"])

        state = MediaState.UNKNOWN
        if "status" in data:
            state = MediaState.from_string(data["status"])

        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            media_type=media_type,
            state=state,
            image_url=data.get("url", ""),
            inserted=data.get("inserted", False),
            write_protected=data.get("write_protected", True),
            connected_via=data.get("connected_via", ""),
            raw_data=data
        )
