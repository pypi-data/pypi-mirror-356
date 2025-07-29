"""iPXE client implementation for bare metal provisioning."""
from typing import Dict, Any, Optional, List, Union
import os
import subprocess
import tempfile
import shutil
import re
import ftplib
import http.server
import socketserver
import threading
import time
from pathlib import Path

from greenfish.utils.logger import Logger

class IPXEClient:
    """iPXE client for bare metal provisioning."""

    def __init__(self):
        """Initialize iPXE client."""
        self.server_thread = None
        self.http_server = None
        self.tftp_server = None
        self.http_port = 8000
        self.tftp_port = 69
        self.ipxe_root = None
        self.running = False

    def setup_ipxe_environment(self, ipxe_root: str) -> bool:
        """Set up iPXE environment.

        Args:
            ipxe_root: Root directory for iPXE files

        Returns:
            bool: True if setup successful
        """
        try:
            self.ipxe_root = Path(ipxe_root).resolve()

            # Create directory structure if it doesn't exist
            os.makedirs(self.ipxe_root / "boot", exist_ok=True)
            os.makedirs(self.ipxe_root / "images", exist_ok=True)
            os.makedirs(self.ipxe_root / "scripts", exist_ok=True)

            # Create default iPXE script
            self._create_default_script()

            Logger.info(f"iPXE environment set up at {self.ipxe_root}")
            return True

        except Exception as e:
            Logger.error(f"Failed to set up iPXE environment: {str(e)}")
            return False

    def _create_default_script(self) -> None:
        """Create default iPXE script."""
        default_script = """#!ipxe

echo ========================================
echo Redfish Desktop iPXE Boot Menu
echo ========================================
echo

:menu
menu iPXE Boot Menu
item --gap -- ------------------------- OS Installation -------------------------
item centos8   Install CentOS 8
item ubuntu20  Install Ubuntu 20.04
item --gap -- ------------------------- Utilities -----------------------------
item memtest   Run Memtest86+
item shell     iPXE Shell
item exit      Exit to BIOS
choose --timeout 60000 --default exit selected || goto exit

goto ${selected}

:centos8
echo Booting CentOS 8 installer...
kernel http://${next-server}:${http-port}/images/centos8/vmlinuz initrd=initrd.img inst.repo=http://${next-server}:${http-port}/images/centos8 ip=dhcp
initrd http://${next-server}:${http-port}/images/centos8/initrd.img
boot || goto failed

:ubuntu20
echo Booting Ubuntu 20.04 installer...
kernel http://${next-server}:${http-port}/images/ubuntu20/vmlinuz initrd=initrd ip=dhcp url=http://${next-server}:${http-port}/images/ubuntu20/ubuntu.iso autoinstall
initrd http://${next-server}:${http-port}/images/ubuntu20/initrd
boot || goto failed

:memtest
echo Booting Memtest86+...
kernel http://${next-server}:${http-port}/boot/memtest86.bin
boot || goto failed

:shell
echo Dropping to iPXE shell...
shell || goto menu

:exit
echo Exiting to BIOS...
exit

:failed
echo Boot failed, dropping to shell
shell
"""

        # Write default script
        with open(self.ipxe_root / "scripts" / "default.ipxe", "w") as f:
            f.write(default_script)

    def add_os_image(self, os_name: str, iso_path: str) -> bool:
        """Add OS image for provisioning.

        Args:
            os_name: Operating system name
            iso_path: Path to ISO image

        Returns:
            bool: True if successful
        """
        try:
            if not os.path.exists(iso_path):
                Logger.error(f"ISO file not found: {iso_path}")
                return False

            # Create directory for OS
            os_dir = self.ipxe_root / "images" / os_name
            os.makedirs(os_dir, exist_ok=True)

            # Copy ISO to images directory
            shutil.copy(iso_path, os_dir / f"{os_name}.iso")

            Logger.info(f"Added OS image for {os_name}")
            return True

        except Exception as e:
            Logger.error(f"Failed to add OS image: {str(e)}")
            return False

    def extract_boot_files(self, os_name: str) -> bool:
        """Extract boot files from ISO image.

        Args:
            os_name: Operating system name

        Returns:
            bool: True if successful
        """
        try:
            iso_path = self.ipxe_root / "images" / os_name / f"{os_name}.iso"
            if not os.path.exists(iso_path):
                Logger.error(f"ISO file not found: {iso_path}")
                return False

            os_dir = self.ipxe_root / "images" / os_name

            # Use 7z to extract boot files
            if os_name.startswith("centos") or os_name.startswith("rhel"):
                # Extract kernel and initrd for CentOS/RHEL
                subprocess.run([
                    "7z", "e", str(iso_path),
                    "-o" + str(os_dir),
                    "isolinux/vmlinuz", "isolinux/initrd.img"
                ], check=True)

            elif os_name.startswith("ubuntu") or os_name.startswith("debian"):
                # Extract kernel and initrd for Ubuntu/Debian
                subprocess.run([
                    "7z", "e", str(iso_path),
                    "-o" + str(os_dir),
                    "casper/vmlinuz", "casper/initrd"
                ], check=True)

            Logger.info(f"Extracted boot files for {os_name}")
            return True

        except Exception as e:
            Logger.error(f"Failed to extract boot files: {str(e)}")
            return False

    def create_kickstart_file(self, os_name: str, config: Dict[str, Any]) -> bool:
        """Create kickstart file for automated installation.

        Args:
            os_name: Operating system name
            config: Kickstart configuration

        Returns:
            bool: True if successful
        """
        try:
            os_dir = self.ipxe_root / "images" / os_name
            os.makedirs(os_dir, exist_ok=True)

            # Basic kickstart template for CentOS/RHEL
            if os_name.startswith("centos") or os_name.startswith("rhel"):
                ks_content = f"""# Kickstart file for {os_name}
# Generated by Redfish Desktop

# System language
lang {config.get('lang', 'en_US.UTF-8')}

# Keyboard layouts
keyboard {config.get('keyboard', 'us')}

# Network information
network --bootproto={config.get('network_type', 'dhcp')} --device={config.get('network_device', 'eth0')} --onboot=yes

# Root password
rootpw --iscrypted {config.get('root_password_hash', '$6$rounds=10000$randomsalt$randomhash')}

# System timezone
timezone {config.get('timezone', 'America/New_York')} --isUtc

# Use graphical install
{'' if config.get('text_mode', False) else 'graphical'}

# System bootloader configuration
bootloader --location=mbr --boot-drive={config.get('boot_drive', 'sda')}

# Partition clearing information
clearpart --all --initlabel

# Disk partitioning information
autopart

# System services
services --enabled="chronyd"

# System authorization information
auth --enableshadow --passalgo=sha512

# Reboot after installation
reboot

# Packages
%packages
@^{config.get('environment', 'minimal')}
%end

# Post-installation script
%post
echo "Redfish Desktop automated installation completed"
%end
"""

                # Write kickstart file
                with open(os_dir / "ks.cfg", "w") as f:
                    f.write(ks_content)

            # Preseed file for Ubuntu/Debian
            elif os_name.startswith("ubuntu") or os_name.startswith("debian"):
                preseed_content = f"""# Preseed file for {os_name}
# Generated by Redfish Desktop

# Localization
d-i debian-installer/locale string {config.get('lang', 'en_US.UTF-8')}
d-i keyboard-configuration/xkb-keymap select {config.get('keyboard', 'us')}

# Network configuration
d-i netcfg/choose_interface select {config.get('network_device', 'auto')}
d-i netcfg/get_hostname string {config.get('hostname', 'redfish-client')}
d-i netcfg/get_domain string {config.get('domain', 'local')}

# Mirror settings
d-i mirror/country string manual
d-i mirror/http/hostname string archive.ubuntu.com
d-i mirror/http/directory string /ubuntu

# Account setup
d-i passwd/root-login boolean true
d-i passwd/root-password-crypted password {config.get('root_password_hash', '$6$rounds=10000$randomsalt$randomhash')}

# Clock and time zone setup
d-i clock-setup/utc boolean true
d-i time/zone string {config.get('timezone', 'America/New_York')}

# Partitioning
d-i partman-auto/method string regular
d-i partman-auto/choose_recipe select atomic
d-i partman-partitioning/confirm_write_new_label boolean true
d-i partman/choose_partition select finish
d-i partman/confirm boolean true
d-i partman/confirm_nooverwrite boolean true

# Package selection
tasksel tasksel/first multiselect {config.get('environment', 'standard')}

# Boot loader installation
d-i grub-installer/only_debian boolean true
d-i grub-installer/with_other_os boolean true
d-i grub-installer/bootdev string default

# Finishing up the installation
d-i finish-install/reboot_in_progress note
"""

                # Write preseed file
                with open(os_dir / "preseed.cfg", "w") as f:
                    f.write(preseed_content)

            Logger.info(f"Created automated installation file for {os_name}")
            return True

        except Exception as e:
            Logger.error(f"Failed to create automated installation file: {str(e)}")
            return False

    def create_custom_ipxe_script(self, script_name: str, content: str) -> bool:
        """Create custom iPXE script.

        Args:
            script_name: Script name
            content: Script content

        Returns:
            bool: True if successful
        """
        try:
            script_path = self.ipxe_root / "scripts" / f"{script_name}.ipxe"

            with open(script_path, "w") as f:
                f.write(content)

            Logger.info(f"Created custom iPXE script: {script_name}")
            return True

        except Exception as e:
            Logger.error(f"Failed to create custom iPXE script: {str(e)}")
            return False

    def start_http_server(self, port: int = 8000) -> bool:
        """Start HTTP server for iPXE files.

        Args:
            port: HTTP port

        Returns:
            bool: True if successful
        """
        try:
            self.http_port = port

            # Create HTTP server
            handler = http.server.SimpleHTTPRequestHandler

            class IPXEHTTPServer(socketserver.TCPServer):
                allow_reuse_address = True

            # Change to iPXE root directory
            os.chdir(self.ipxe_root)

            self.http_server = IPXEHTTPServer(("", port), handler)

            # Start server in a separate thread
            self.server_thread = threading.Thread(target=self.http_server.serve_forever)
            self.server_thread.daemon = True
            self.server_thread.start()

            Logger.info(f"Started HTTP server on port {port}")
            self.running = True
            return True

        except Exception as e:
            Logger.error(f"Failed to start HTTP server: {str(e)}")
            return False

    def stop_servers(self) -> bool:
        """Stop all running servers.

        Returns:
            bool: True if successful
        """
        try:
            if self.http_server:
                self.http_server.shutdown()
                self.http_server = None

            if self.tftp_server:
                self.tftp_server.shutdown()
                self.tftp_server = None

            self.running = False
            Logger.info("Stopped all provisioning servers")
            return True

        except Exception as e:
            Logger.error(f"Failed to stop servers: {str(e)}")
            return False

    def is_running(self) -> bool:
        """Check if servers are running.

        Returns:
            bool: True if running
        """
        return self.running
