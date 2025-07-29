import os
import json
from typing import Dict, Any, Optional
import appdirs

# Define default settings
DEFAULT_SETTINGS = {
    "theme": "light",
    "connection_profiles": [],
    "auto_reconnect": False,
    "refresh_interval": 30
}

class Settings:
    """Settings manager for the application."""

    def __init__(self):
        """Initialize settings."""
        # Determine config directory
        self.config_dir = appdirs.user_config_dir("RedFishDesktop")
        self.config_file = os.path.join(self.config_dir, "settings.json")

        # Create config directory if it doesn't exist
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)

        # Load settings
        self.settings = self.load_settings()

    def load_settings(self) -> Dict[str, Any]:
        """Load settings from file."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                # If error loading settings, use defaults
                return DEFAULT_SETTINGS.copy()
        else:
            # If file doesn't exist, use defaults
            return DEFAULT_SETTINGS.copy()

    def save_settings(self) -> None:
        """Save settings to file."""
        try:
            with open(self.config_file, "w") as f:
                json.dump(self.settings, f, indent=2)
        except IOError:
            # Ignore errors saving settings
            pass

    def get(self, key: str, default: Any = None) -> Any:
        """Get a setting value."""
        return self.settings.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set a setting value."""
        self.settings[key] = value
        self.save_settings()

    def get_theme(self) -> str:
        """Get the current theme."""
        return self.settings.get("theme", "light")

    def set_theme(self, theme: str) -> None:
        """Set the current theme."""
        self.settings["theme"] = theme
        self.save_settings()

    def get_auto_reconnect(self) -> bool:
        """Get auto-reconnect setting."""
        return self.settings.get("auto_reconnect", False)

    def set_auto_reconnect(self, value: bool) -> None:
        """Set auto-reconnect setting."""
        self.settings["auto_reconnect"] = value
        self.save_settings()

    def get_refresh_interval(self) -> int:
        """Get refresh interval in seconds."""
        return self.settings.get("refresh_interval", 30)

    def set_refresh_interval(self, value: int) -> None:
        """Set refresh interval in seconds."""
        self.settings["refresh_interval"] = value
        self.save_settings()

    def get_connection_profiles(self) -> list:
        """Get saved connection profiles."""
        return self.settings.get("connection_profiles", [])

    def add_connection_profile(self, profile: Dict[str, Any]) -> None:
        """Add a connection profile."""
        profiles = self.get_connection_profiles()

        # Replace profile if it already exists (by name)
        for i, p in enumerate(profiles):
            if p.get("name") == profile.get("name"):
                profiles[i] = profile
                break
        else:
            # Add new profile
            profiles.append(profile)

        self.settings["connection_profiles"] = profiles
        self.save_settings()

    def remove_connection_profile(self, name: str) -> None:
        """Remove a connection profile."""
        profiles = self.get_connection_profiles()

        # Remove profile if it exists
        self.settings["connection_profiles"] = [p for p in profiles if p.get("name") != name]
        self.save_settings()

# Create a global settings instance
settings = Settings()
