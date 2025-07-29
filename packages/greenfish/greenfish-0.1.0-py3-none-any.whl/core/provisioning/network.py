"""Network configuration module for bare metal provisioning."""
from typing import Dict, Any, Optional, List, Union
import os
import json
import ipaddress
import re
import subprocess
import platform
import tempfile
import shutil
from pathlib import Path

from greenfish.utils.logger import Logger

class NetworkConfiguration:
    """Network configuration for bare metal provisioning."""

    def __init__(self):
        """Initialize network configuration."""
        self.config_dir = None
        self.configs = {}

    def setup_config_environment(self, config_dir: str) -> bool:
        """Set up configuration environment.

        Args:
            config_dir: Directory for configuration files

        Returns:
            bool: True if setup successful
        """
        try:
            self.config_dir = Path(config_dir).resolve()

            # Create directory structure if it doesn't exist
            os.makedirs(self.config_dir / "templates", exist_ok=True)
            os.makedirs(self.config_dir / "dhcp", exist_ok=True)
            os.makedirs(self.config_dir / "dns", exist_ok=True)

            # Create default templates
            self._create_default_templates()

            # Load existing configurations
            self._load_configs()

            Logger.info(f"Network configuration environment set up at {self.config_dir}")
            return True

        except Exception as e:
            Logger.error(f"Failed to set up network configuration environment: {str(e)}")
            return False

    def _create_default_templates(self) -> None:
        """Create default network configuration templates."""
        # DHCP server template
        dhcp_template = {
            "name": "Basic DHCP Server",
            "description": "Basic DHCP server configuration",
            "config": {
                "subnet": "192.168.1.0",
                "netmask": "255.255.255.0",
                "range_start": "192.168.1.100",
                "range_end": "192.168.1.200",
                "gateway": "192.168.1.1",
                "dns_servers": ["8.8.8.8", "8.8.4.4"],
                "domain_name": "local",
                "lease_time": 86400
            }
        }

        # DNS server template
        dns_template = {
            "name": "Basic DNS Server",
            "description": "Basic DNS server configuration",
            "config": {
                "domain": "local",
                "forwarders": ["8.8.8.8", "8.8.4.4"],
                "records": [
                    {"name": "router", "type": "A", "value": "192.168.1.1"},
                    {"name": "server", "type": "A", "value": "192.168.1.2"}
                ]
            }
        }

        # Save templates
        with open(self.config_dir / "templates" / "dhcp_basic.json", "w") as f:
            json.dump(dhcp_template, f, indent=2)

        with open(self.config_dir / "templates" / "dns_basic.json", "w") as f:
            json.dump(dns_template, f, indent=2)

    def _load_configs(self) -> None:
        """Load existing configurations."""
        self.configs = {}

        try:
            for config_type in ["dhcp", "dns"]:
                config_dir = self.config_dir / config_type

                if not config_dir.exists():
                    continue

                for config_file in config_dir.glob("*.json"):
                    try:
                        with open(config_file, "r") as f:
                            config = json.load(f)

                        config_id = f"{config_type}_{config_file.stem}"
                        self.configs[config_id] = config

                    except Exception as e:
                        Logger.error(f"Failed to load configuration from {config_file}: {str(e)}")

        except Exception as e:
            Logger.error(f"Failed to load configurations: {str(e)}")

    def get_available_templates(self) -> List[Dict[str, Any]]:
        """Get available configuration templates.

        Returns:
            List of templates
        """
        templates = []

        try:
            template_dir = self.config_dir / "templates"

            if not template_dir.exists():
                return templates

            for template_file in template_dir.glob("*.json"):
                try:
                    with open(template_file, "r") as f:
                        template = json.load(f)

                    template["id"] = template_file.stem
                    template["type"] = "dhcp" if "dhcp" in template_file.stem else "dns"
                    templates.append(template)

                except Exception as e:
                    Logger.error(f"Failed to load template from {template_file}: {str(e)}")

        except Exception as e:
            Logger.error(f"Failed to get templates: {str(e)}")

        return templates

    def create_dhcp_config(self, name: str, config: Dict[str, Any]) -> str:
        """Create a new DHCP configuration.

        Args:
            name: Configuration name
            config: DHCP configuration

        Returns:
            str: Configuration ID
        """
        try:
            # Validate configuration
            if not self._validate_dhcp_config(config):
                Logger.error("Invalid DHCP configuration")
                return ""

            # Create configuration
            config_id = f"dhcp_{name.lower().replace(' ', '_')}"

            dhcp_config = {
                "id": config_id,
                "name": name,
                "type": "dhcp",
                "config": config
            }

            # Save configuration
            config_path = self.config_dir / "dhcp" / f"{name.lower().replace(' ', '_')}.json"

            with open(config_path, "w") as f:
                json.dump(dhcp_config, f, indent=2)

            # Add to configurations
            self.configs[config_id] = dhcp_config

            Logger.info(f"Created DHCP configuration {name}")
            return config_id

        except Exception as e:
            Logger.error(f"Failed to create DHCP configuration: {str(e)}")
            return ""

    def _validate_dhcp_config(self, config: Dict[str, Any]) -> bool:
        """Validate DHCP configuration.

        Args:
            config: DHCP configuration

        Returns:
            bool: True if valid
        """
        try:
            # Check required fields
            required_fields = ["subnet", "netmask", "range_start", "range_end", "gateway"]

            for field in required_fields:
                if field not in config:
                    Logger.error(f"Missing required field: {field}")
                    return False

            # Validate subnet
            try:
                subnet = ipaddress.IPv4Network(f"{config['subnet']}/{config['netmask']}", strict=False)
            except ValueError:
                Logger.error(f"Invalid subnet: {config['subnet']}/{config['netmask']}")
                return False

            # Validate IP addresses
            for field in ["range_start", "range_end", "gateway"]:
                try:
                    ip = ipaddress.IPv4Address(config[field])

                    # Check if IP is in subnet
                    if ip not in subnet:
                        Logger.error(f"IP address {config[field]} is not in subnet {subnet}")
                        return False

                except ValueError:
                    Logger.error(f"Invalid IP address: {config[field]}")
                    return False

            # Validate range
            start_ip = ipaddress.IPv4Address(config["range_start"])
            end_ip = ipaddress.IPv4Address(config["range_end"])

            if start_ip > end_ip:
                Logger.error(f"Invalid range: {start_ip} > {end_ip}")
                return False

            return True

        except Exception as e:
            Logger.error(f"Error validating DHCP configuration: {str(e)}")
            return False

    def create_dns_config(self, name: str, config: Dict[str, Any]) -> str:
        """Create a new DNS configuration.

        Args:
            name: Configuration name
            config: DNS configuration

        Returns:
            str: Configuration ID
        """
        try:
            # Validate configuration
            if not self._validate_dns_config(config):
                Logger.error("Invalid DNS configuration")
                return ""

            # Create configuration
            config_id = f"dns_{name.lower().replace(' ', '_')}"

            dns_config = {
                "id": config_id,
                "name": name,
                "type": "dns",
                "config": config
            }

            # Save configuration
            config_path = self.config_dir / "dns" / f"{name.lower().replace(' ', '_')}.json"

            with open(config_path, "w") as f:
                json.dump(dns_config, f, indent=2)

            # Add to configurations
            self.configs[config_id] = dns_config

            Logger.info(f"Created DNS configuration {name}")
            return config_id

        except Exception as e:
            Logger.error(f"Failed to create DNS configuration: {str(e)}")
            return ""

    def _validate_dns_config(self, config: Dict[str, Any]) -> bool:
        """Validate DNS configuration.

        Args:
            config: DNS configuration

        Returns:
            bool: True if valid
        """
        try:
            # Check required fields
            if "domain" not in config:
                Logger.error("Missing required field: domain")
                return False

            # Validate domain
            domain_pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$'

            if not re.match(domain_pattern, config["domain"]):
                Logger.error(f"Invalid domain: {config['domain']}")
                return False

            # Validate forwarders
            if "forwarders" in config:
                for forwarder in config["forwarders"]:
                    try:
                        ipaddress.IPv4Address(forwarder)
                    except ValueError:
                        Logger.error(f"Invalid forwarder IP: {forwarder}")
                        return False

            # Validate records
            if "records" in config:
                for record in config["records"]:
                    if "name" not in record or "type" not in record or "value" not in record:
                        Logger.error("Missing required fields in DNS record")
                        return False

                    # Validate record type
                    valid_types = ["A", "AAAA", "CNAME", "MX", "NS", "PTR", "SOA", "SRV", "TXT"]

                    if record["type"] not in valid_types:
                        Logger.error(f"Invalid record type: {record['type']}")
                        return False

                    # Validate record value based on type
                    if record["type"] == "A":
                        try:
                            ipaddress.IPv4Address(record["value"])
                        except ValueError:
                            Logger.error(f"Invalid A record value: {record['value']}")
                            return False

                    elif record["type"] == "AAAA":
                        try:
                            ipaddress.IPv6Address(record["value"])
                        except ValueError:
                            Logger.error(f"Invalid AAAA record value: {record['value']}")
                            return False

            return True

        except Exception as e:
            Logger.error(f"Error validating DNS configuration: {str(e)}")
            return False

    def delete_config(self, config_id: str) -> bool:
        """Delete a configuration.

        Args:
            config_id: Configuration ID

        Returns:
            bool: True if successful
        """
        try:
            if config_id not in self.configs:
                Logger.error(f"Configuration not found: {config_id}")
                return False

            config = self.configs[config_id]
            config_type = config.get("type", "")
            name = config.get("name", "")

            # Delete configuration file
            config_path = self.config_dir / config_type / f"{name.lower().replace(' ', '_')}.json"

            if config_path.exists():
                os.remove(config_path)

            # Remove from configurations
            del self.configs[config_id]

            Logger.info(f"Deleted {config_type} configuration {name}")
            return True

        except Exception as e:
            Logger.error(f"Failed to delete configuration: {str(e)}")
            return False

    def get_configs(self, config_type: str = None) -> List[Dict[str, Any]]:
        """Get configurations.

        Args:
            config_type: Configuration type (dhcp or dns)

        Returns:
            List of configurations
        """
        if config_type:
            return [config for config in self.configs.values() if config.get("type") == config_type]
        else:
            return list(self.configs.values())

    def get_config(self, config_id: str) -> Dict[str, Any]:
        """Get configuration by ID.

        Args:
            config_id: Configuration ID

        Returns:
            Dict: Configuration
        """
        return self.configs.get(config_id, {})

    def generate_dhcp_config_file(self, config_id: str, output_path: str = None) -> str:
        """Generate DHCP configuration file.

        Args:
            config_id: Configuration ID
            output_path: Output path (optional)

        Returns:
            str: Path to generated file
        """
        try:
            if config_id not in self.configs or self.configs[config_id].get("type") != "dhcp":
                Logger.error(f"DHCP configuration not found: {config_id}")
                return ""

            config = self.configs[config_id]
            dhcp_config = config.get("config", {})

            # Generate configuration content
            content = f"""# DHCP Server Configuration
# Generated by Redfish Desktop

subnet {dhcp_config.get('subnet')} netmask {dhcp_config.get('netmask')} {{
  range {dhcp_config.get('range_start')} {dhcp_config.get('range_end')};
  option routers {dhcp_config.get('gateway')};
  option domain-name "{dhcp_config.get('domain_name', 'local')}";
  option domain-name-servers {', '.join(dhcp_config.get('dns_servers', []))};
  default-lease-time {dhcp_config.get('lease_time', 86400)};
  max-lease-time {dhcp_config.get('lease_time', 86400) * 2};
}}
"""

            # Add static mappings if present
            if "static_mappings" in dhcp_config:
                content += "\n# Static mappings\n"

                for mapping in dhcp_config["static_mappings"]:
                    content += f"host {mapping.get('name')} {{\n"
                    content += f"  hardware ethernet {mapping.get('mac')};\n"
                    content += f"  fixed-address {mapping.get('ip')};\n"
                    content += "}\n"

            # Write to file
            if output_path:
                output_file = output_path
            else:
                output_file = self.config_dir / "dhcp" / f"{config['name'].lower().replace(' ', '_')}.conf"

            with open(output_file, "w") as f:
                f.write(content)

            Logger.info(f"Generated DHCP configuration file: {output_file}")
            return str(output_file)

        except Exception as e:
            Logger.error(f"Failed to generate DHCP configuration file: {str(e)}")
            return ""

    def generate_dns_config_file(self, config_id: str, output_path: str = None) -> str:
        """Generate DNS configuration file.

        Args:
            config_id: Configuration ID
            output_path: Output path (optional)

        Returns:
            str: Path to generated file
        """
        try:
            if config_id not in self.configs or self.configs[config_id].get("type") != "dns":
                Logger.error(f"DNS configuration not found: {config_id}")
                return ""

            config = self.configs[config_id]
            dns_config = config.get("config", {})

            # Generate configuration content
            content = f"""// DNS Server Configuration
// Generated by Redfish Desktop

options {{
  directory "/var/cache/bind";
  forwarders {{
    {'; '.join(dns_config.get('forwarders', []))};
  }};
  allow-query {{ any; }};
  recursion yes;
}};

zone "{dns_config.get('domain')}" {{
  type master;
  file "/etc/bind/zones/db.{dns_config.get('domain')}";
}};
"""

            # Write to file
            if output_path:
                output_file = output_path
            else:
                output_file = self.config_dir / "dns" / f"{config['name'].lower().replace(' ', '_')}.conf"

            with open(output_file, "w") as f:
                f.write(content)

            # Generate zone file
            zone_dir = self.config_dir / "dns" / "zones"
            os.makedirs(zone_dir, exist_ok=True)

            zone_content = f"""$TTL 86400
@       IN      SOA     ns1.{dns_config.get('domain')}. admin.{dns_config.get('domain')}. (
                        {int(time.time())}     ; Serial
                        3600                    ; Refresh
                        1800                    ; Retry
                        604800                  ; Expire
                        86400 )                 ; Minimum TTL

@       IN      NS      ns1.{dns_config.get('domain')}.
@       IN      A       127.0.0.1
ns1     IN      A       127.0.0.1
"""

            # Add records
            if "records" in dns_config:
                for record in dns_config["records"]:
                    zone_content += f"{record.get('name')}\tIN\t{record.get('type')}\t{record.get('value')}\n"

            # Write zone file
            zone_file = zone_dir / f"db.{dns_config.get('domain')}"

            with open(zone_file, "w") as f:
                f.write(zone_content)

            Logger.info(f"Generated DNS configuration file: {output_file}")
            Logger.info(f"Generated DNS zone file: {zone_file}")
            return str(output_file)

        except Exception as e:
            Logger.error(f"Failed to generate DNS configuration file: {str(e)}")
            return ""
