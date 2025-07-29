"""OS deployment module for bare metal provisioning."""
from typing import Dict, Any, Optional, List, Union
import os
import json
import time
import shutil
from pathlib import Path
import tempfile
import uuid

from greenfish.utils.logger import Logger
from greenfish.core.provisioning.ipxe import IPXEClient

class OSDeployment:
    """OS deployment for bare metal provisioning."""

    def __init__(self, ipxe_client: IPXEClient = None):
        """Initialize OS deployment.

        Args:
            ipxe_client: iPXE client instance
        """
        self.ipxe_client = ipxe_client or IPXEClient()
        self.deployment_dir = None
        self.deployments = {}

    def setup_deployment_environment(self, deployment_dir: str) -> bool:
        """Set up deployment environment.

        Args:
            deployment_dir: Directory for deployment files

        Returns:
            bool: True if setup successful
        """
        try:
            self.deployment_dir = Path(deployment_dir).resolve()

            # Create directory structure if it doesn't exist
            os.makedirs(self.deployment_dir / "templates", exist_ok=True)
            os.makedirs(self.deployment_dir / "configs", exist_ok=True)
            os.makedirs(self.deployment_dir / "logs", exist_ok=True)

            # Create default templates
            self._create_default_templates()

            # Load existing deployments
            self._load_deployments()

            Logger.info(f"Deployment environment set up at {self.deployment_dir}")
            return True

        except Exception as e:
            Logger.error(f"Failed to set up deployment environment: {str(e)}")
            return False

    def _create_default_templates(self) -> None:
        """Create default deployment templates."""
        # CentOS template
        centos_template = {
            "name": "CentOS 8 Server",
            "os_type": "centos8",
            "description": "CentOS 8 minimal server installation",
            "config": {
                "lang": "en_US.UTF-8",
                "keyboard": "us",
                "network_type": "dhcp",
                "network_device": "eth0",
                "timezone": "America/New_York",
                "text_mode": False,
                "boot_drive": "sda",
                "environment": "minimal"
            }
        }

        # Ubuntu template
        ubuntu_template = {
            "name": "Ubuntu 20.04 Server",
            "os_type": "ubuntu20",
            "description": "Ubuntu 20.04 LTS server installation",
            "config": {
                "lang": "en_US.UTF-8",
                "keyboard": "us",
                "network_device": "auto",
                "hostname": "redfish-client",
                "domain": "local",
                "timezone": "America/New_York",
                "environment": "standard"
            }
        }

        # Save templates
        with open(self.deployment_dir / "templates" / "centos8.json", "w") as f:
            json.dump(centos_template, f, indent=2)

        with open(self.deployment_dir / "templates" / "ubuntu20.json", "w") as f:
            json.dump(ubuntu_template, f, indent=2)

    def _load_deployments(self) -> None:
        """Load existing deployments."""
        self.deployments = {}

        try:
            config_dir = self.deployment_dir / "configs"

            if not config_dir.exists():
                return

            for config_file in config_dir.glob("*.json"):
                try:
                    with open(config_file, "r") as f:
                        deployment = json.load(f)

                    deployment_id = config_file.stem
                    self.deployments[deployment_id] = deployment

                except Exception as e:
                    Logger.error(f"Failed to load deployment from {config_file}: {str(e)}")

        except Exception as e:
            Logger.error(f"Failed to load deployments: {str(e)}")

    def get_available_templates(self) -> List[Dict[str, Any]]:
        """Get available deployment templates.

        Returns:
            List of templates
        """
        templates = []

        try:
            template_dir = self.deployment_dir / "templates"

            if not template_dir.exists():
                return templates

            for template_file in template_dir.glob("*.json"):
                try:
                    with open(template_file, "r") as f:
                        template = json.load(f)

                    template["id"] = template_file.stem
                    templates.append(template)

                except Exception as e:
                    Logger.error(f"Failed to load template from {template_file}: {str(e)}")

        except Exception as e:
            Logger.error(f"Failed to get templates: {str(e)}")

        return templates

    def create_deployment(self, template_id: str, name: str, config_overrides: Dict[str, Any] = None) -> str:
        """Create a new deployment from a template.

        Args:
            template_id: Template ID
            name: Deployment name
            config_overrides: Configuration overrides

        Returns:
            str: Deployment ID
        """
        try:
            # Load template
            template_path = self.deployment_dir / "templates" / f"{template_id}.json"

            if not template_path.exists():
                Logger.error(f"Template not found: {template_id}")
                return ""

            with open(template_path, "r") as f:
                template = json.load(f)

            # Create deployment
            deployment_id = str(uuid.uuid4())

            deployment = {
                "id": deployment_id,
                "name": name,
                "template_id": template_id,
                "os_type": template.get("os_type", ""),
                "description": template.get("description", ""),
                "status": "created",
                "created_at": int(time.time()),
                "updated_at": int(time.time()),
                "config": template.get("config", {})
            }

            # Apply config overrides
            if config_overrides:
                deployment["config"].update(config_overrides)

            # Save deployment
            config_path = self.deployment_dir / "configs" / f"{deployment_id}.json"

            with open(config_path, "w") as f:
                json.dump(deployment, f, indent=2)

            # Add to deployments
            self.deployments[deployment_id] = deployment

            Logger.info(f"Created deployment {name} with ID {deployment_id}")
            return deployment_id

        except Exception as e:
            Logger.error(f"Failed to create deployment: {str(e)}")
            return ""

    def update_deployment(self, deployment_id: str, updates: Dict[str, Any]) -> bool:
        """Update deployment configuration.

        Args:
            deployment_id: Deployment ID
            updates: Updates to apply

        Returns:
            bool: True if successful
        """
        try:
            if deployment_id not in self.deployments:
                Logger.error(f"Deployment not found: {deployment_id}")
                return False

            deployment = self.deployments[deployment_id]

            # Apply updates
            if "name" in updates:
                deployment["name"] = updates["name"]

            if "description" in updates:
                deployment["description"] = updates["description"]

            if "config" in updates:
                deployment["config"].update(updates["config"])

            deployment["updated_at"] = int(time.time())

            # Save deployment
            config_path = self.deployment_dir / "configs" / f"{deployment_id}.json"

            with open(config_path, "w") as f:
                json.dump(deployment, f, indent=2)

            Logger.info(f"Updated deployment {deployment['name']}")
            return True

        except Exception as e:
            Logger.error(f"Failed to update deployment: {str(e)}")
            return False

    def delete_deployment(self, deployment_id: str) -> bool:
        """Delete a deployment.

        Args:
            deployment_id: Deployment ID

        Returns:
            bool: True if successful
        """
        try:
            if deployment_id not in self.deployments:
                Logger.error(f"Deployment not found: {deployment_id}")
                return False

            deployment = self.deployments[deployment_id]

            # Delete deployment file
            config_path = self.deployment_dir / "configs" / f"{deployment_id}.json"

            if config_path.exists():
                os.remove(config_path)

            # Remove from deployments
            del self.deployments[deployment_id]

            Logger.info(f"Deleted deployment {deployment['name']}")
            return True

        except Exception as e:
            Logger.error(f"Failed to delete deployment: {str(e)}")
            return False

    def get_deployments(self) -> List[Dict[str, Any]]:
        """Get all deployments.

        Returns:
            List of deployments
        """
        return list(self.deployments.values())

    def get_deployment(self, deployment_id: str) -> Dict[str, Any]:
        """Get deployment by ID.

        Args:
            deployment_id: Deployment ID

        Returns:
            Dict: Deployment configuration
        """
        return self.deployments.get(deployment_id, {})

    def prepare_deployment(self, deployment_id: str, iso_path: str = None) -> bool:
        """Prepare deployment for execution.

        Args:
            deployment_id: Deployment ID
            iso_path: Path to ISO image (optional)

        Returns:
            bool: True if successful
        """
        try:
            if deployment_id not in self.deployments:
                Logger.error(f"Deployment not found: {deployment_id}")
                return False

            deployment = self.deployments[deployment_id]
            os_type = deployment.get("os_type", "")

            # Set up iPXE environment if not already set up
            if not self.ipxe_client.ipxe_root:
                ipxe_root = self.deployment_dir / "ipxe"
                self.ipxe_client.setup_ipxe_environment(ipxe_root)

            # Add OS image if provided
            if iso_path:
                self.ipxe_client.add_os_image(os_type, iso_path)
                self.ipxe_client.extract_boot_files(os_type)

            # Create kickstart/preseed file
            self.ipxe_client.create_kickstart_file(os_type, deployment["config"])

            # Update deployment status
            deployment["status"] = "prepared"
            deployment["updated_at"] = int(time.time())

            # Save deployment
            config_path = self.deployment_dir / "configs" / f"{deployment_id}.json"

            with open(config_path, "w") as f:
                json.dump(deployment, f, indent=2)

            Logger.info(f"Prepared deployment {deployment['name']}")
            return True

        except Exception as e:
            Logger.error(f"Failed to prepare deployment: {str(e)}")
            return False

    def start_deployment(self, deployment_id: str, http_port: int = 8000) -> bool:
        """Start deployment by starting the HTTP server.

        Args:
            deployment_id: Deployment ID
            http_port: HTTP port

        Returns:
            bool: True if successful
        """
        try:
            if deployment_id not in self.deployments:
                Logger.error(f"Deployment not found: {deployment_id}")
                return False

            deployment = self.deployments[deployment_id]

            # Start HTTP server
            if not self.ipxe_client.is_running():
                self.ipxe_client.start_http_server(http_port)

            # Update deployment status
            deployment["status"] = "running"
            deployment["updated_at"] = int(time.time())

            # Save deployment
            config_path = self.deployment_dir / "configs" / f"{deployment_id}.json"

            with open(config_path, "w") as f:
                json.dump(deployment, f, indent=2)

            Logger.info(f"Started deployment {deployment['name']}")
            return True

        except Exception as e:
            Logger.error(f"Failed to start deployment: {str(e)}")
            return False

    def stop_deployment(self, deployment_id: str) -> bool:
        """Stop deployment by stopping the HTTP server.

        Args:
            deployment_id: Deployment ID

        Returns:
            bool: True if successful
        """
        try:
            if deployment_id not in self.deployments:
                Logger.error(f"Deployment not found: {deployment_id}")
                return False

            deployment = self.deployments[deployment_id]

            # Stop HTTP server
            if self.ipxe_client.is_running():
                self.ipxe_client.stop_servers()

            # Update deployment status
            deployment["status"] = "stopped"
            deployment["updated_at"] = int(time.time())

            # Save deployment
            config_path = self.deployment_dir / "configs" / f"{deployment_id}.json"

            with open(config_path, "w") as f:
                json.dump(deployment, f, indent=2)

            Logger.info(f"Stopped deployment {deployment['name']}")
            return True

        except Exception as e:
            Logger.error(f"Failed to stop deployment: {str(e)}")
            return False
