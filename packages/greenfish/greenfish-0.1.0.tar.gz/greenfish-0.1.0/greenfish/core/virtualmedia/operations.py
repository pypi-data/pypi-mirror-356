"""Virtual Media operations module."""
from typing import Dict, Any, Optional, List, Union, Callable
import os
import time
import re
import urllib.parse
import requests
import tempfile
import shutil
from pathlib import Path

from greenfish.utils.logger import Logger
from greenfish.core.virtualmedia.types import VirtualMedia, MediaType, MediaState

class VirtualMediaOperations:
    """Virtual Media operations."""

    def __init__(self, client):
        """Initialize Virtual Media operations.

        Args:
            client: Virtual Media client
        """
        self.client = client

    def insert_media(self, media_id: str, image_url: str, write_protected: bool = True) -> bool:
        """Insert virtual media.

        Args:
            media_id: Media ID
            image_url: Image URL
            write_protected: Whether media is write-protected

        Returns:
            bool: True if successful
        """
        return self.client.insert_media(media_id, image_url, write_protected)

    def eject_media(self, media_id: str) -> bool:
        """Eject virtual media.

        Args:
            media_id: Media ID

        Returns:
            bool: True if successful
        """
        return self.client.eject_media(media_id)

    def get_media_info(self, media_id: str) -> Optional[VirtualMedia]:
        """Get virtual media information.

        Args:
            media_id: Media ID

        Returns:
            VirtualMedia: Virtual media information
        """
        return self.client.get_media_info(media_id)

    def list_media(self) -> List[VirtualMedia]:
        """List available virtual media.

        Returns:
            List[VirtualMedia]: List of virtual media
        """
        return self.client.list_media()

    def create_iso_image(self,
                         files: List[str],
                         output_path: str = None,
                         volume_id: str = "REDFISH_VM") -> str:
        """Create ISO image from files.

        Args:
            files: List of files to include
            output_path: Output path (optional)
            volume_id: Volume ID

        Returns:
            str: Path to created ISO
        """
        try:
            import subprocess

            # Create temporary directory
            temp_dir = tempfile.mkdtemp()

            try:
                # Copy files to temporary directory
                for file_path in files:
                    if os.path.exists(file_path):
                        shutil.copy(file_path, temp_dir)
                    else:
                        Logger.error(f"File not found: {file_path}")

                # Generate output path if not provided
                if not output_path:
                    output_path = os.path.join(tempfile.gettempdir(), f"{volume_id}_{int(time.time())}.iso")

                # Create ISO image
                cmd = [
                    "mkisofs",
                    "-o", output_path,
                    "-J",
                    "-r",
                    "-V", volume_id,
                    temp_dir
                ]

                result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                if result.returncode == 0:
                    Logger.info(f"Created ISO image: {output_path}")
                    return output_path
                else:
                    Logger.error(f"Failed to create ISO image: {result.stderr.decode()}")
                    return ""

            finally:
                # Clean up temporary directory
                shutil.rmtree(temp_dir)

        except Exception as e:
            Logger.error(f"Error creating ISO image: {str(e)}")
            return ""

    def create_img_image(self,
                         size_mb: int,
                         output_path: str = None,
                         filesystem: str = "fat32",
                         label: str = "REDFISH_VM") -> str:
        """Create IMG image with specified filesystem.

        Args:
            size_mb: Size in megabytes
            output_path: Output path (optional)
            filesystem: Filesystem type (fat32, ntfs, ext4)
            label: Volume label

        Returns:
            str: Path to created IMG
        """
        try:
            import subprocess

            # Generate output path if not provided
            if not output_path:
                output_path = os.path.join(tempfile.gettempdir(), f"{label}_{int(time.time())}.img")

            # Create empty file
            with open(output_path, "wb") as f:
                f.seek(size_mb * 1024 * 1024 - 1)
                f.write(b"\0")

            # Format the image
            if filesystem.lower() == "fat32":
                cmd = ["mkfs.vfat", "-F", "32", "-n", label, output_path]
            elif filesystem.lower() == "ntfs":
                cmd = ["mkfs.ntfs", "--quick", "--label", label, output_path]
            elif filesystem.lower() == "ext4":
                cmd = ["mkfs.ext4", "-L", label, output_path]
            else:
                Logger.error(f"Unsupported filesystem: {filesystem}")
                return ""

            result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            if result.returncode == 0:
                Logger.info(f"Created IMG image: {output_path}")
                return output_path
            else:
                Logger.error(f"Failed to create IMG image: {result.stderr.decode()}")
                return ""

        except Exception as e:
            Logger.error(f"Error creating IMG image: {str(e)}")
            return ""

    def mount_image(self, image_path: str, mount_point: str = None) -> str:
        """Mount image file to access contents.

        Args:
            image_path: Path to image file
            mount_point: Mount point (optional)

        Returns:
            str: Mount point
        """
        try:
            import subprocess

            # Generate mount point if not provided
            if not mount_point:
                mount_point = os.path.join(tempfile.gettempdir(), f"redfish_vm_{int(time.time())}")

            # Create mount point if it doesn't exist
            os.makedirs(mount_point, exist_ok=True)

            # Mount image
            cmd = ["mount", "-o", "loop", image_path, mount_point]
            result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            if result.returncode == 0:
                Logger.info(f"Mounted image {image_path} at {mount_point}")
                return mount_point
            else:
                Logger.error(f"Failed to mount image: {result.stderr.decode()}")
                return ""

        except Exception as e:
            Logger.error(f"Error mounting image: {str(e)}")
            return ""

    def unmount_image(self, mount_point: str) -> bool:
        """Unmount image file.

        Args:
            mount_point: Mount point

        Returns:
            bool: True if successful
        """
        try:
            import subprocess

            # Unmount image
            cmd = ["umount", mount_point]
            result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            if result.returncode == 0:
                Logger.info(f"Unmounted image from {mount_point}")
                return True
            else:
                Logger.error(f"Failed to unmount image: {result.stderr.decode()}")
                return False

        except Exception as e:
            Logger.error(f"Error unmounting image: {str(e)}")
            return False

    def copy_files_to_image(self, image_path: str, files: List[str], target_dir: str = "/") -> bool:
        """Copy files to image.

        Args:
            image_path: Path to image file
            files: List of files to copy
            target_dir: Target directory in image

        Returns:
            bool: True if successful
        """
        try:
            # Mount image
            mount_point = self.mount_image(image_path)

            if not mount_point:
                return False

            try:
                # Create target directory if it doesn't exist
                target_path = os.path.join(mount_point, target_dir.lstrip("/"))
                os.makedirs(target_path, exist_ok=True)

                # Copy files
                for file_path in files:
                    if os.path.exists(file_path):
                        shutil.copy(file_path, target_path)
                    else:
                        Logger.error(f"File not found: {file_path}")

                Logger.info(f"Copied {len(files)} files to image")
                return True

            finally:
                # Unmount image
                self.unmount_image(mount_point)

        except Exception as e:
            Logger.error(f"Error copying files to image: {str(e)}")
            return False

    def extract_files_from_image(self, image_path: str, source_files: List[str], output_dir: str) -> bool:
        """Extract files from image.

        Args:
            image_path: Path to image file
            source_files: List of files to extract (relative to image root)
            output_dir: Output directory

        Returns:
            bool: True if successful
        """
        try:
            # Mount image
            mount_point = self.mount_image(image_path)

            if not mount_point:
                return False

            try:
                # Create output directory if it doesn't exist
                os.makedirs(output_dir, exist_ok=True)

                # Extract files
                for file_path in source_files:
                    source_path = os.path.join(mount_point, file_path.lstrip("/"))

                    if os.path.exists(source_path):
                        if os.path.isdir(source_path):
                            shutil.copytree(source_path, os.path.join(output_dir, os.path.basename(file_path)))
                        else:
                            shutil.copy(source_path, output_dir)
                    else:
                        Logger.error(f"File not found in image: {file_path}")

                Logger.info(f"Extracted {len(source_files)} files from image")
                return True

            finally:
                # Unmount image
                self.unmount_image(mount_point)

        except Exception as e:
            Logger.error(f"Error extracting files from image: {str(e)}")
            return False

    def download_image(self, url: str, output_path: str = None) -> str:
        """Download image from URL.

        Args:
            url: Image URL
            output_path: Output path (optional)

        Returns:
            str: Path to downloaded image
        """
        try:
            # Generate output path if not provided
            if not output_path:
                parsed_url = urllib.parse.urlparse(url)
                filename = os.path.basename(parsed_url.path)
                output_path = os.path.join(tempfile.gettempdir(), filename)

            # Download image
            response = requests.get(url, stream=True)
            response.raise_for_status()

            with open(output_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            Logger.info(f"Downloaded image from {url} to {output_path}")
            return output_path

        except Exception as e:
            Logger.error(f"Error downloading image: {str(e)}")
            return ""

    def upload_image(self, image_path: str, url: str) -> bool:
        """Upload image to URL.

        Args:
            image_path: Path to image file
            url: Upload URL

        Returns:
            bool: True if successful
        """
        try:
            # Check if file exists
            if not os.path.exists(image_path):
                Logger.error(f"Image file not found: {image_path}")
                return False

            # Upload image
            with open(image_path, "rb") as f:
                response = requests.put(url, data=f)
                response.raise_for_status()

            Logger.info(f"Uploaded image {image_path} to {url}")
            return True

        except Exception as e:
            Logger.error(f"Error uploading image: {str(e)}")
            return False
