import uuid
from datetime import datetime
from typing import Dict, Any


class ConnectionProfile:
    """Class representing a saved connection profile."""

    def __init__(self, name: str, base_url: str, username: str, password: str = None,
                auth_type: str = "session", description: str = "", id: str = None):
        """Initialize a connection profile."""
        self.id = id or str(uuid.uuid4())
        self.name = name
        self.base_url = base_url
        self.username = username
        self.password = password  # Note: Password should be encrypted in a real app
        self.auth_type = auth_type
        self.description = description
        self.created = datetime.now().isoformat()
        self.last_used = None

    def to_dict(self, include_password: bool = False) -> Dict[str, Any]:
        """Convert profile to dictionary."""
        result = {
            "id": self.id,
            "name": self.name,
            "base_url": self.base_url,
            "username": self.username,
            "auth_type": self.auth_type,
            "description": self.description,
            "created": self.created,
            "last_used": self.last_used
        }

        if include_password and self.password:
            result["password"] = self.password

        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ConnectionProfile':
        """Create profile from dictionary."""
        profile = cls(
            name=data.get("name", ""),
            base_url=data.get("base_url", ""),
            username=data.get("username", ""),
            password=data.get("password"),
            auth_type=data.get("auth_type", "session"),
            description=data.get("description", ""),
            id=data.get("id")
        )

        profile.created = data.get("created", datetime.now().isoformat())
        profile.last_used = data.get("last_used")

        return profile
