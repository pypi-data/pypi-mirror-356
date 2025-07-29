import os
import json
from typing import Dict, Any, List, Optional
import uuid
from datetime import datetime
from greenfish.utils.logger import Logger
from greenfish.config.connection_profile import ConnectionProfile

class ConfigManager:
    """Class for managing application configuration and profiles."""

    def __init__(self, config_dir: str = None):
        """Initialize configuration manager."""
        # Set configuration directory
        if config_dir:
            self.config_dir = config_dir
        else:
            # Default to user's home directory
            home_dir = os.path.expanduser("~")
            self.config_dir = os.path.join(home_dir, ".redfish_desktop")

        # Create config directory if it doesn't exist
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)

        # Set file paths
        self.profiles_file = os.path.join(self.config_dir, "profiles.json")
        self.config_file = os.path.join(self.config_dir, "config.json")

        # Initialize profiles and config
        self.profiles = []
        self.config = {}

        # Load existing data
        self.load_profiles()
        self.load_config()

        Logger.debug(f"ConfigManager initialized with directory: {self.config_dir}")

    def load_profiles(self) -> None:
        """Load connection profiles from file."""
        if os.path.exists(self.profiles_file):
            try:
                with open(self.profiles_file, "r") as f:
                    profiles_data = json.load(f)

                self.profiles = [ConnectionProfile.from_dict(p) for p in profiles_data]
                Logger.debug(f"Loaded {len(self.profiles)} connection profiles")
            except Exception as e:
                Logger.error(f"Failed to load profiles: {str(e)}")
                self.profiles = []
        else:
            self.profiles = []

    def save_profiles(self) -> None:
        """Save connection profiles to file."""
        try:
            profiles_data = [p.to_dict(include_password=True) for p in self.profiles]

            with open(self.profiles_file, "w") as f:
                json.dump(profiles_data, f, indent=4)

            Logger.debug(f"Saved {len(self.profiles)} connection profiles")
        except Exception as e:
            Logger.error(f"Failed to save profiles: {str(e)}")

    def load_config(self) -> None:
        """Load configuration from file."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as f:
                    self.config = json.load(f)

                Logger.debug("Configuration loaded successfully")
            except Exception as e:
                Logger.error(f"Failed to load configuration: {str(e)}")
                self.config = {}
        else:
            self.config = {}

    def save_config(self) -> None:
        """Save configuration to file."""
        try:
            with open(self.config_file, "w") as f:
                json.dump(self.config, f, indent=4)

            Logger.debug("Configuration saved successfully")
        except Exception as e:
            Logger.error(f"Failed to save configuration: {str(e)}")

    def get_profiles(self) -> List[ConnectionProfile]:
        """Get all connection profiles."""
        return self.profiles

    def get_profile(self, profile_id: str) -> Optional[ConnectionProfile]:
        """Get a specific connection profile by ID."""
        for profile in self.profiles:
            if profile.id == profile_id:
                return profile

        return None

    def add_profile(self, profile: ConnectionProfile) -> None:
        """Add a new connection profile."""
        self.profiles.append(profile)
        self.save_profiles()

    def update_profile(self, profile: ConnectionProfile) -> bool:
        """Update an existing connection profile."""
        for i, p in enumerate(self.profiles):
            if p.id == profile.id:
                self.profiles[i] = profile
                self.save_profiles()
                return True

        return False

    def delete_profile(self, profile_id: str) -> bool:
        """Delete a connection profile."""
        for i, profile in enumerate(self.profiles):
            if profile.id == profile_id:
                del self.profiles[i]
                self.save_profiles()
                return True

        return False

    def update_profile_last_used(self, profile_id: str) -> bool:
        """Update the last used timestamp of a profile."""
        profile = self.get_profile(profile_id)
        if profile:
            profile.last_used = datetime.now().isoformat()
            self.save_profiles()
            return True

        return False

    def get_config_value(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        return self.config.get(key, default)

    def set_config_value(self, key: str, value: Any) -> None:
        """Set a configuration value."""
        self.config[key] = value
        self.save_config()

    def export_profiles(self, file_path: str) -> bool:
        """Export connection profiles to a file."""
        try:
            profiles_data = [p.to_dict(include_password=True) for p in self.profiles]

            with open(file_path, "w") as f:
                json.dump(profiles_data, f, indent=4)

            Logger.debug(f"Exported {len(self.profiles)} profiles to {file_path}")
            return True
        except Exception as e:
            Logger.error(f"Failed to export profiles: {str(e)}")
            return False

    def import_profiles(self, file_path: str) -> bool:
        """Import connection profiles from a file."""
        try:
            with open(file_path, "r") as f:
                profiles_data = json.load(f)

            # Create profiles from imported data
            imported_profiles = [ConnectionProfile.from_dict(p) for p in profiles_data]

            # Merge with existing profiles (avoid duplicates by ID)
            existing_ids = {p.id for p in self.profiles}
            for profile in imported_profiles:
                if profile.id not in existing_ids:
                    self.profiles.append(profile)
                    existing_ids.add(profile.id)

            self.save_profiles()
            Logger.debug(f"Imported profiles from {file_path}")
            return True
        except Exception as e:
            Logger.error(f"Failed to import profiles: {str(e)}")
            return False

    def export_config(self, file_path: str) -> bool:
        """Export configuration to a file."""
        try:
            with open(file_path, "w") as f:
                json.dump(self.config, f, indent=4)

            Logger.debug(f"Exported configuration to {file_path}")
            return True
        except Exception as e:
            Logger.error(f"Failed to export configuration: {str(e)}")
            return False

    def import_config(self, file_path: str) -> bool:
        """Import configuration from a file."""
        try:
            with open(file_path, "r") as f:
                imported_config = json.load(f)

            # Merge with existing config
            self.config.update(imported_config)
            self.save_config()

            Logger.debug(f"Imported configuration from {file_path}")
            return True
        except Exception as e:
            Logger.error(f"Failed to import configuration: {str(e)}")
            return False

# Create a global instance
config_manager = ConfigManager()
