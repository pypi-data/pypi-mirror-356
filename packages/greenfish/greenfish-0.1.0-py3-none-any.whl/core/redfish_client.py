import redfish
from typing import Optional, Dict, Any, Union, List
import json
import time
import os
import requests
from greenfish.utils.logger import logger

class RedfishClient:
    def __init__(self, base_url: str, username: str, password: str,
                 default_prefix: str = '/redfish/v1/', **kwargs):
        """Initialize Redfish client with connection parameters."""
        self.client = redfish.redfish_client(
            base_url=base_url,
            username=username,
            password=password,
            default_prefix=default_prefix,
            **kwargs
        )
        self.connected = False
        self.active_tasks = {}
        self.base_url = base_url.rstrip('/')
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.auth_token = None
        self.tasks = []

        logger.debug(f"Initialized RedfishClient for {base_url}")

    def connect(self, auth: str = "session") -> bool:
        """Connect to Redfish service with specified authentication method."""
        try:
            logger.info(f"Connecting to {self.base_url} using {auth} authentication")

            # Try to get service root
            response = self.session.get(
                f"{self.base_url}/redfish/v1/",
                auth=(self.username, self.password) if auth == "basic" else None,
                verify=False  # Skip SSL verification
            )

            if response.status_code == 401:
                logger.error("Authentication failed - Invalid credentials")
                raise Exception("Authentication failed - Invalid credentials")
            elif response.status_code == 403:
                logger.error("Access forbidden - Check your permissions")
                raise Exception("Access forbidden - Check your permissions")
            elif response.status_code != 200:
                logger.error(f"Service root not available - HTTP {response.status_code}")
                raise Exception(f"Service not able to provide the service root, return code: {response.status_code}")

            # Store auth token if using session auth
            if auth == "session":
                self.auth_token = response.headers.get('X-Auth-Token')
                if self.auth_token:
                    self.session.headers.update({'X-Auth-Token': self.auth_token})
                    logger.debug("Session token obtained and stored")

            self.connected = True
            logger.success("Successfully connected to Redfish service")

            return True
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Connection failed: {str(e)}")
            raise Exception(f"Failed to connect to {self.base_url}")
        except Exception as e:
            logger.error(f"Connection error: {str(e)}")
            raise

    def disconnect(self) -> None:
        """Disconnect from Redfish service."""
        if self.auth_token:
            # Delete session if we have one
            try:
                self.session.delete(f"{self.base_url}/redfish/v1/SessionService/Sessions/{self.auth_token}")
                logger.info("Session deleted successfully")
            except:
                logger.warning("Failed to delete session")

        self.session.close()
        self.connected = False
        self.auth_token = None
        logger.info("Disconnected from Redfish service")

    def get(self, path: str, args: Optional[Dict] = None) -> Dict[str, Any]:
        """Perform GET request on specified path."""
        if not self.connected:
            logger.error("Not connected to Redfish service")
            raise Exception("Not connected to Redfish service")

        response = self.client.get(path, args=args)
        if response.status >= 400:
            raise Exception(f"GET request failed: {response.status} - {response.text}")
        return response.dict

    def post(self, path: str, body: Union[Dict, list, bytes, str],
             args: Optional[Dict] = None) -> Dict[str, Any]:
        """Perform POST request on specified path."""
        if not self.connected:
            logger.error("Not connected to Redfish service")
            raise Exception("Not connected to Redfish service")

        response = self.client.post(path, body=body, args=args)
        if response.status >= 400:
            raise Exception(f"POST request failed: {response.status} - {response.text}")

        # Check for task creation
        if response.is_processing:
            task = response.monitor(self.client)
            task_id = task.dict.get("Id", "Unknown")
            self.active_tasks[task_id] = task.dict
            return {"is_task": True, "task_id": task_id, "task": task.dict}

        return response.dict

    def patch(self, path: str, body: Dict, args: Optional[Dict] = None) -> Dict[str, Any]:
        """Perform PATCH request on specified path."""
        if not self.connected:
            logger.error("Not connected to Redfish service")
            raise Exception("Not connected to Redfish service")

        response = self.client.patch(path, body=body, args=args)
        if response.status >= 400:
            raise Exception(f"PATCH request failed: {response.status} - {response.text}")

        # Check for task creation
        if response.is_processing:
            task = response.monitor(self.client)
            task_id = task.dict.get("Id", "Unknown")
            self.active_tasks[task_id] = task.dict
            return {"is_task": True, "task_id": task_id, "task": task.dict}

        return response.dict

    def put(self, path: str, body: Dict, args: Optional[Dict] = None) -> Dict[str, Any]:
        """Perform PUT request on specified path."""
        if not self.connected:
            logger.error("Not connected to Redfish service")
            raise Exception("Not connected to Redfish service")

        response = self.client.put(path, body=body, args=args)
        if response.status >= 400:
            raise Exception(f"PUT request failed: {response.status} - {response.text}")

        # Check for task creation
        if response.is_processing:
            task = response.monitor(self.client)
            task_id = task.dict.get("Id", "Unknown")
            self.active_tasks[task_id] = task.dict
            return {"is_task": True, "task_id": task_id, "task": task.dict}

        return response.dict

    def delete(self, path: str, args: Optional[Dict] = None) -> None:
        """Perform DELETE request on specified path."""
        if not self.connected:
            logger.error("Not connected to Redfish service")
            raise Exception("Not connected to Redfish service")

        response = self.client.delete(path, args=args)
        if response.status >= 400:
            raise Exception(f"DELETE request failed: {response.status} - {response.text}")

        # Check for task creation
        if response.is_processing:
            task = response.monitor(self.client)
            task_id = task.dict.get("Id", "Unknown")
            self.active_tasks[task_id] = task.dict
            return {"is_task": True, "task_id": task_id, "task": task.dict}

    def get_systems(self) -> Dict[str, Any]:
        """Get all systems information."""
        return self.get("/redfish/v1/Systems")

    def get_system(self, system_id: str = "1") -> Dict[str, Any]:
        """Get specific system information."""
        if not self.connected:
            logger.error("Not connected to Redfish service")
            raise Exception("Not connected to Redfish service")

        try:
            logger.info(f"Fetching system information for system {system_id}")
            response = self.session.get(f"{self.base_url}/redfish/v1/Systems/{system_id}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to get system information: {str(e)}")
            raise

    def get_chassis(self) -> Dict[str, Any]:
        """Get all chassis information."""
        return self.get("/redfish/v1/Chassis")

    def get_managers(self) -> Dict[str, Any]:
        """Get all managers information."""
        return self.get("/redfish/v1/Managers")

    def get_storage(self) -> Dict[str, Any]:
        """Get all storage information."""
        return self.get("/redfish/v1/Systems/1/Storage")

    def get_network_interfaces(self) -> Dict[str, Any]:
        """Get all network interfaces information."""
        return self.get("/redfish/v1/Systems/1/EthernetInterfaces")

    def reset_system(self, system_id: str = "1", reset_type: str = "GracefulShutdown") -> Dict[str, Any]:
        """Reset system with specified reset type."""
        if not self.connected:
            logger.error("Not connected to Redfish service")
            raise Exception("Not connected to Redfish service")

        try:
            logger.info(f"Resetting system {system_id} with type {reset_type}")
            response = self.session.post(
                f"{self.base_url}/redfish/v1/Systems/{system_id}/Actions/ComputerSystem.Reset",
                json={"ResetType": reset_type}
            )
            response.raise_for_status()

            # Check if operation resulted in a task
            if "Location" in response.headers:
                task_uri = response.headers["Location"]
                logger.info(f"Reset operation created task: {task_uri}")
                return {
                    "is_task": True,
                    "task_id": task_uri.split("/")[-1],
                    "task": self.get_task(task_uri)
                }

            logger.success(f"System {system_id} reset successfully")
            return {"is_task": False}

        except Exception as e:
            logger.error(f"Failed to reset system: {str(e)}")
            raise

    def get_tasks(self) -> List[Dict[str, Any]]:
        """Get all active tasks."""
        # First update task status
        self.update_tasks()
        return list(self.active_tasks.values())

    def update_tasks(self) -> None:
        """Update status of active tasks."""
        if not self.connected:
            logger.error("Not connected to Redfish service")
            raise Exception("Not connected to Redfish service")

        try:
            logger.info("Updating task list")
            self.tasks = self.get_tasks()
            logger.debug(f"Found {len(self.tasks)} tasks")
        except Exception as e:
            logger.error(f"Failed to update tasks: {str(e)}")
            raise

    def get_task(self, task_id: str) -> Dict[str, Any]:
        """Get specific task information."""
        if task_id in self.active_tasks:
            # Update task status first
            try:
                task_data = self.get(f"/redfish/v1/TaskService/Tasks/{task_id}")
                self.active_tasks[task_id] = task_data
            except Exception:
                # Return cached task data on error
                pass

            return self.active_tasks[task_id]
        else:
            # Try to get task directly
            try:
                task_data = self.get(f"/redfish/v1/TaskService/Tasks/{task_id}")
                self.active_tasks[task_id] = task_data
                return task_data
            except Exception as e:
                raise Exception(f"Task {task_id} not found: {str(e)}")

    def monitor_task(self, task_id: str, poll_interval: int = 5, timeout: int = 600) -> Dict[str, Any]:
        """Monitor a task until completion or timeout."""
        start_time = time.time()

        while time.time() - start_time < timeout:
            task_data = self.get_task(task_id)

            task_state = task_data.get("TaskState")
            if task_state in ["Completed", "Cancelled", "Exception"]:
                return task_data

            # Wait for next poll
            time.sleep(poll_interval)

        # Timeout reached
        raise TimeoutError(f"Task monitoring timed out after {timeout} seconds")

    def cancel_task(self, task_id: str) -> None:
        """Cancel a running task."""
        # Check if task exists
        if task_id not in self.active_tasks:
            raise Exception(f"Task {task_id} not found")

        # Cancel task
        try:
            self.delete(f"/redfish/v1/TaskService/Tasks/{task_id}")

            # Update task status
            self.active_tasks[task_id]["TaskState"] = "Cancelled"
        except Exception as e:
            raise Exception(f"Failed to cancel task {task_id}: {str(e)}")

    def get_bios_settings(self, system_id: str = "1") -> Dict[str, Any]:
        """Get BIOS settings for a system."""
        try:
            # First, get the BIOS registry resource
            system = self.get(f"/redfish/v1/Systems/{system_id}")

            # Check if BIOS endpoint is available
            if "Bios" not in system:
                raise Exception("BIOS endpoint not found in system resources")

            # Get the BIOS URI from the system resource
            bios_uri = system["Bios"]["@odata.id"]

            # Get BIOS settings
            bios_settings = self.get(bios_uri)

            # Get BIOS registry for attribute info if available
            attribute_registry = None
            if "AttributeRegistry" in bios_settings:
                try:
                    reg_name = bios_settings["AttributeRegistry"]
                    # Try to get registry - this may fail if not implemented on server
                    registry = self.get(f"/redfish/v1/Registries/{reg_name}")
                    if "Location" in registry and len(registry["Location"]) > 0:
                        reg_uri = registry["Location"][0]["Uri"]
                        attribute_registry = self.get(reg_uri)
                except Exception:
                    # Registry might not be available, continue without it
                    pass

            return {
                "settings": bios_settings,
                "registry": attribute_registry
            }
        except Exception as e:
            raise Exception(f"Error retrieving BIOS settings: {str(e)}")

    def get_bios_pending_settings(self, system_id: str = "1") -> Dict[str, Any]:
        """Get pending BIOS settings that require a reboot."""
        try:
            # First, get the BIOS settings resource
            system = self.get(f"/redfish/v1/Systems/{system_id}")

            # Check if BIOS endpoint is available
            if "Bios" not in system:
                raise Exception("BIOS endpoint not found in system resources")

            # Get the BIOS URI from the system resource
            bios_uri = system["Bios"]["@odata.id"]

            # Check for pending settings URI
            bios_settings = self.get(bios_uri)

            # Look for @Redfish.Settings with PendingSettings
            if "@Redfish.Settings" in bios_settings:
                settings_obj = bios_settings["@Redfish.Settings"]
                if "SettingsObject" in settings_obj:
                    pending_uri = settings_obj["SettingsObject"]["@odata.id"]
                    return self.get(pending_uri)

            # If we reach here, no pending settings were found
            return {"Attributes": {}}
        except Exception as e:
            raise Exception(f"Error retrieving pending BIOS settings: {str(e)}")

    def update_bios_settings(self, attributes: Dict[str, Any], system_id: str = "1") -> Dict[str, Any]:
        """Update BIOS settings for a system."""
        try:
            # First, get the BIOS settings resource
            system = self.get(f"/redfish/v1/Systems/{system_id}")

            # Check if BIOS endpoint is available
            if "Bios" not in system:
                raise Exception("BIOS endpoint not found in system resources")

            # Get the BIOS URI from the system resource
            bios_uri = system["Bios"]["@odata.id"]

            # Create PATCH payload with attributes
            payload = {"Attributes": attributes}

            # Update BIOS settings
            response = self.patch(bios_uri, body=payload)

            # Return response or task
            return response
        except Exception as e:
            raise Exception(f"Error updating BIOS settings: {str(e)}")

    def get_firmware_inventory(self) -> Dict[str, Any]:
        """Get firmware inventory."""
        try:
            # Get update service
            update_service = self.get("/redfish/v1/UpdateService")

            # Get firmware inventory URI
            if "FirmwareInventory" not in update_service:
                raise Exception("Firmware inventory not supported")

            firmware_uri = update_service["FirmwareInventory"]["@odata.id"]

            # Get firmware inventory
            firmware_inventory = self.get(firmware_uri)

            # Get details for each firmware item
            inventory_items = []
            if "Members" in firmware_inventory:
                for item in firmware_inventory["Members"]:
                    if "@odata.id" in item:
                        try:
                            item_uri = item["@odata.id"]
                            item_data = self.get(item_uri)
                            inventory_items.append(item_data)
                        except Exception:
                            # Skip items that can't be retrieved
                            pass

            return {
                "update_service": update_service,
                "items": inventory_items
            }
        except Exception as e:
            raise Exception(f"Error retrieving firmware inventory: {str(e)}")

    def get_update_service_info(self) -> Dict[str, Any]:
        """Get information about update service capabilities."""
        try:
            # Get update service
            update_service = self.get("/redfish/v1/UpdateService")
            return update_service
        except Exception as e:
            raise Exception(f"Error retrieving update service info: {str(e)}")

    def upload_firmware_image(self, image_path: str) -> Dict[str, Any]:
        """Upload firmware image to the Redfish service."""
        try:
            # Get update service
            update_service = self.get("/redfish/v1/UpdateService")

            # Check for HTTP push update capability
            if not update_service.get("HttpPushUri"):
                raise Exception("HTTP push update not supported by this Redfish service")

            # Get the push URI
            push_uri = update_service["HttpPushUri"]

            # Check if file exists
            if not os.path.isfile(image_path):
                raise Exception(f"Firmware image not found: {image_path}")

            # Read the image file
            with open(image_path, "rb") as f:
                image_data = f.read()

            # Send the firmware image
            headers = {"Content-Type": "application/octet-stream"}
            response = self.client.post(push_uri, body=image_data, headers=headers)

            if response.status >= 400:
                raise Exception(f"Firmware upload failed: {response.status} - {response.text}")

            # Check for task
            if response.is_processing:
                task = response.monitor(self.client)
                task_id = task.dict.get("Id", "Unknown")
                self.active_tasks[task_id] = task.dict
                return {"is_task": True, "task_id": task_id, "task": task.dict}

            return response.dict
        except Exception as e:
            raise Exception(f"Error uploading firmware image: {str(e)}")

    def update_firmware(self, image_uri: str, targets: List[str] = None) -> Dict[str, Any]:
        """Apply a firmware update to specified targets."""
        try:
            # Get update service
            update_service = self.get("/redfish/v1/UpdateService")

            # Check for simple update action
            if "Actions" not in update_service or "#UpdateService.SimpleUpdate" not in update_service["Actions"]:
                raise Exception("SimpleUpdate action not supported by this Redfish service")

            # Get the simple update action URI
            simple_update_uri = update_service["Actions"]["#UpdateService.SimpleUpdate"]["target"]

            # Prepare update payload
            payload = {
                "ImageURI": image_uri
            }

            if targets:
                payload["Targets"] = targets

            # Perform the update
            response = self.client.post(simple_update_uri, body=payload)

            if response.status >= 400:
                raise Exception(f"Firmware update failed: {response.status} - {response.text}")

            # Check for task
            if response.is_processing:
                task = response.monitor(self.client)
                task_id = task.dict.get("Id", "Unknown")
                self.active_tasks[task_id] = task.dict
                return {"is_task": True, "task_id": task_id, "task": task.dict}

            return response.dict
        except Exception as e:
            raise Exception(f"Error applying firmware update: {str(e)}")

    def get_account_service(self) -> Dict[str, Any]:
        """Get account service information."""
        try:
            logger.info("Fetching account service information")
            return self.get("/redfish/v1/AccountService")
        except Exception as e:
            logger.error(f"Failed to get account service: {str(e)}")
            raise

    def get_accounts(self) -> List[Dict[str, Any]]:
        """Get all user accounts."""
        try:
            logger.info("Fetching user accounts")
            accounts = self.get("/redfish/v1/AccountService/Accounts")

            # Get detailed information for each account
            account_list = []
            if "Members" in accounts:
                for member in accounts["Members"]:
                    if "@odata.id" in member:
                        try:
                            account_uri = member["@odata.id"]
                            account_data = self.get(account_uri)
                            account_list.append(account_data)
                        except Exception:
                            # Skip accounts that can't be retrieved
                            pass

            logger.debug(f"Found {len(account_list)} user accounts")
            return account_list
        except Exception as e:
            logger.error(f"Failed to get accounts: {str(e)}")
            raise

    def get_account(self, account_id: str) -> Dict[str, Any]:
        """Get specific user account information."""
        try:
            logger.info(f"Fetching account information for ID: {account_id}")
            return self.get(f"/redfish/v1/AccountService/Accounts/{account_id}")
        except Exception as e:
            logger.error(f"Failed to get account {account_id}: {str(e)}")
            raise

    def create_account(self, username: str, password: str, role_id: str,
                      enabled: bool = True) -> Dict[str, Any]:
        """Create a new user account."""
        try:
            logger.info(f"Creating new account for user: {username}")
            payload = {
                "UserName": username,
                "Password": password,
                "RoleId": role_id,
                "Enabled": enabled
            }

            response = self.post("/redfish/v1/AccountService/Accounts", body=payload)
            logger.success(f"Account created successfully for user: {username}")
            return response
        except Exception as e:
            logger.error(f"Failed to create account: {str(e)}")
            raise

    def update_account(self, account_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update user account properties."""
        try:
            logger.info(f"Updating account {account_id}")
            response = self.patch(f"/redfish/v1/AccountService/Accounts/{account_id}",
                                body=updates)
            logger.success(f"Account {account_id} updated successfully")
            return response
        except Exception as e:
            logger.error(f"Failed to update account {account_id}: {str(e)}")
            raise

    def delete_account(self, account_id: str) -> None:
        """Delete a user account."""
        try:
            logger.info(f"Deleting account {account_id}")
            self.delete(f"/redfish/v1/AccountService/Accounts/{account_id}")
            logger.success(f"Account {account_id} deleted successfully")
        except Exception as e:
            logger.error(f"Failed to delete account {account_id}: {str(e)}")
            raise

    def get_roles(self) -> List[Dict[str, Any]]:
        """Get available user roles."""
        try:
            logger.info("Fetching available roles")
            roles = self.get("/redfish/v1/AccountService/Roles")

            # Get detailed information for each role
            role_list = []
            if "Members" in roles:
                for member in roles["Members"]:
                    if "@odata.id" in member:
                        try:
                            role_uri = member["@odata.id"]
                            role_data = self.get(role_uri)
                            role_list.append(role_data)
                        except Exception:
                            # Skip roles that can't be retrieved
                            pass

            logger.debug(f"Found {len(role_list)} roles")
            return role_list
        except Exception as e:
            logger.error(f"Failed to get roles: {str(e)}")
            raise

    def get_role(self, role_id: str) -> Dict[str, Any]:
        """Get specific role information."""
        try:
            logger.info(f"Fetching role information for ID: {role_id}")
            return self.get(f"/redfish/v1/AccountService/Roles/{role_id}")
        except Exception as e:
            logger.error(f"Failed to get role {role_id}: {str(e)}")
            raise

    def get_secure_boot(self, system_id: str = "1") -> Dict[str, Any]:
        """Get Secure Boot information."""
        try:
            logger.info(f"Fetching Secure Boot information for system {system_id}")
            system = self.get(f"/redfish/v1/Systems/{system_id}")

            if "SecureBoot" not in system:
                raise Exception("Secure Boot not supported on this system")

            secure_boot_uri = system["SecureBoot"]["@odata.id"]
            secure_boot = self.get(secure_boot_uri)

            logger.debug(f"Secure Boot state: {secure_boot.get('SecureBootEnable', False)}")
            return secure_boot
        except Exception as e:
            logger.error(f"Failed to get Secure Boot information: {str(e)}")
            raise

    def get_secure_boot_databases(self, system_id: str = "1") -> List[Dict[str, Any]]:
        """Get Secure Boot certificate databases."""
        try:
            logger.info(f"Fetching Secure Boot databases for system {system_id}")
            system = self.get(f"/redfish/v1/Systems/{system_id}")

            if "SecureBoot" not in system:
                raise Exception("Secure Boot not supported on this system")

            secure_boot_uri = system["SecureBoot"]["@odata.id"]
            secure_boot = self.get(secure_boot_uri)

            if "SecureBootDatabases" not in secure_boot:
                raise Exception("Secure Boot databases not supported")

            databases_uri = secure_boot["SecureBootDatabases"]["@odata.id"]
            databases = self.get(databases_uri)

            # Get detailed information for each database
            database_list = []
            if "Members" in databases:
                for member in databases["Members"]:
                    if "@odata.id" in member:
                        try:
                            db_uri = member["@odata.id"]
                            db_data = self.get(db_uri)
                            database_list.append(db_data)
                        except Exception:
                            # Skip databases that can't be retrieved
                            pass

            logger.debug(f"Found {len(database_list)} Secure Boot databases")
            return database_list
        except Exception as e:
            logger.error(f"Failed to get Secure Boot databases: {str(e)}")
            raise

    def enable_secure_boot(self, enable: bool, system_id: str = "1") -> Dict[str, Any]:
        """Enable or disable Secure Boot."""
        try:
            logger.info(f"{'Enabling' if enable else 'Disabling'} Secure Boot for system {system_id}")
            system = self.get(f"/redfish/v1/Systems/{system_id}")

            if "SecureBoot" not in system:
                raise Exception("Secure Boot not supported on this system")

            secure_boot_uri = system["SecureBoot"]["@odata.id"]

            # Update Secure Boot state
            payload = {"SecureBootEnable": enable}
            response = self.patch(secure_boot_uri, body=payload)

            logger.success(f"Secure Boot {'enabled' if enable else 'disabled'} successfully")
            return response
        except Exception as e:
            logger.error(f"Failed to {'enable' if enable else 'disable'} Secure Boot: {str(e)}")
            raise

    def reset_secure_boot(self, system_id: str = "1") -> Dict[str, Any]:
        """Reset Secure Boot keys to default."""
        try:
            logger.info(f"Resetting Secure Boot keys for system {system_id}")
            system = self.get(f"/redfish/v1/Systems/{system_id}")

            if "SecureBoot" not in system:
                raise Exception("Secure Boot not supported on this system")

            secure_boot_uri = system["SecureBoot"]["@odata.id"]

            # Get SecureBoot resource to find ResetKeys action
            secure_boot = self.get(secure_boot_uri)

            if "Actions" not in secure_boot or "#SecureBoot.ResetKeys" not in secure_boot["Actions"]:
                raise Exception("Reset keys action not supported")

            reset_uri = secure_boot["Actions"]["#SecureBoot.ResetKeys"]["target"]

            # Reset keys to default
            response = self.post(reset_uri, body={"ResetKeysType": "ResetAllKeysToDefault"})

            logger.success("Secure Boot keys reset successfully")
            return response
        except Exception as e:
            logger.error(f"Failed to reset Secure Boot keys: {str(e)}")
            raise

    def clear_secure_boot_keys(self, system_id: str = "1") -> Dict[str, Any]:
        """Clear all Secure Boot keys."""
        try:
            logger.info(f"Clearing Secure Boot keys for system {system_id}")
            system = self.get(f"/redfish/v1/Systems/{system_id}")

            if "SecureBoot" not in system:
                raise Exception("Secure Boot not supported on this system")

            secure_boot_uri = system["SecureBoot"]["@odata.id"]

            # Get SecureBoot resource to find ResetKeys action
            secure_boot = self.get(secure_boot_uri)

            if "Actions" not in secure_boot or "#SecureBoot.ResetKeys" not in secure_boot["Actions"]:
                raise Exception("Reset keys action not supported")

            reset_uri = secure_boot["Actions"]["#SecureBoot.ResetKeys"]["target"]

            # Clear all keys
            response = self.post(reset_uri, body={"ResetKeysType": "DeleteAllKeys"})

            logger.success("Secure Boot keys cleared successfully")
            return response
        except Exception as e:
            logger.error(f"Failed to clear Secure Boot keys: {str(e)}")
            raise

    def get_event_service(self) -> Dict[str, Any]:
        """Get event service information."""
        try:
            logger.info("Fetching event service information")
            return self.get("/redfish/v1/EventService")
        except Exception as e:
            logger.error(f"Failed to get event service: {str(e)}")
            raise

    def get_event_subscriptions(self) -> List[Dict[str, Any]]:
        """Get all event subscriptions."""
        try:
            logger.info("Fetching event subscriptions")
            subs = self.get("/redfish/v1/EventService/Subscriptions")
            sub_list = []
            if "Members" in subs:
                for member in subs["Members"]:
                    if "@odata.id" in member:
                        try:
                            sub_uri = member["@odata.id"]
                            sub_data = self.get(sub_uri)
                            sub_list.append(sub_data)
                        except Exception:
                            pass
            logger.debug(f"Found {len(sub_list)} event subscriptions")
            return sub_list
        except Exception as e:
            logger.error(f"Failed to get event subscriptions: {str(e)}")
            raise

    def create_event_subscription(self, destination: str, event_types: list = None, protocol: str = "Redfish") -> Dict[str, Any]:
        """Create a new event subscription."""
        try:
            logger.info(f"Creating event subscription to {destination}")
            payload = {
                "Destination": destination,
                "Protocol": protocol
            }
            if event_types:
                payload["EventTypes"] = event_types
            response = self.post("/redfish/v1/EventService/Subscriptions", body=payload)
            logger.success(f"Event subscription created for {destination}")
            return response
        except Exception as e:
            logger.error(f"Failed to create event subscription: {str(e)}")
            raise

    def delete_event_subscription(self, subscription_id: str) -> None:
        """Delete an event subscription."""
        try:
            logger.info(f"Deleting event subscription {subscription_id}")
            self.delete(f"/redfish/v1/EventService/Subscriptions/{subscription_id}")
            logger.success(f"Event subscription {subscription_id} deleted successfully")
        except Exception as e:
            logger.error(f"Failed to delete event subscription {subscription_id}: {str(e)}")
            raise

    def get_log_service(self, resource_type: str = "Systems", resource_id: str = "1") -> Dict[str, Any]:
        """Get log service information for a specific resource."""
        try:
            logger.info(f"Fetching log service for {resource_type}/{resource_id}")
            resource_uri = f"/redfish/v1/{resource_type}/{resource_id}"
            resource = self.get(resource_uri)

            if "LogServices" not in resource:
                raise Exception(f"Log services not available for {resource_type}/{resource_id}")

            log_services_uri = resource["LogServices"]["@odata.id"]
            return self.get(log_services_uri)
        except Exception as e:
            logger.error(f"Failed to get log service: {str(e)}")
            raise

    def get_log_entries(self, resource_type: str = "Systems", resource_id: str = "1",
                       log_service_id: str = "Log") -> List[Dict[str, Any]]:
        """Get log entries from a specific log service."""
        try:
            logger.info(f"Fetching log entries for {resource_type}/{resource_id}/{log_service_id}")
            log_uri = f"/redfish/v1/{resource_type}/{resource_id}/LogServices/{log_service_id}/Entries"
            logs = self.get(log_uri)

            # Extract all log entries
            entries = []
            if "Members" in logs:
                for entry in logs["Members"]:
                    entries.append(entry)

            logger.debug(f"Found {len(entries)} log entries")
            return entries
        except Exception as e:
            logger.error(f"Failed to get log entries: {str(e)}")
            raise

    def get_log_entry(self, entry_id: str, resource_type: str = "Systems",
                     resource_id: str = "1", log_service_id: str = "Log") -> Dict[str, Any]:
        """Get a specific log entry."""
        try:
            logger.info(f"Fetching log entry {entry_id}")
            entry_uri = f"/redfish/v1/{resource_type}/{resource_id}/LogServices/{log_service_id}/Entries/{entry_id}"
            return self.get(entry_uri)
        except Exception as e:
            logger.error(f"Failed to get log entry {entry_id}: {str(e)}")
            raise

    def clear_logs(self, resource_type: str = "Systems", resource_id: str = "1",
                  log_service_id: str = "Log") -> Dict[str, Any]:
        """Clear all log entries from a specific log service."""
        try:
            logger.info(f"Clearing logs for {resource_type}/{resource_id}/{log_service_id}")
            log_service_uri = f"/redfish/v1/{resource_type}/{resource_id}/LogServices/{log_service_id}"
            log_service = self.get(log_service_uri)

            if "Actions" not in log_service or "#LogService.ClearLog" not in log_service["Actions"]:
                raise Exception("Clear log action not supported")

            clear_uri = log_service["Actions"]["#LogService.ClearLog"]["target"]
            response = self.post(clear_uri, body={})

            logger.success(f"Logs cleared successfully for {resource_type}/{resource_id}/{log_service_id}")
            return response
        except Exception as e:
            logger.error(f"Failed to clear logs: {str(e)}")
            raise

    def get_available_log_services(self, resource_type: str = "Systems", resource_id: str = "1") -> List[Dict[str, Any]]:
        """Get all available log services for a resource."""
        try:
            logger.info(f"Fetching available log services for {resource_type}/{resource_id}")
            log_services = self.get_log_service(resource_type, resource_id)

            services = []
            if "Members" in log_services:
                for member in log_services["Members"]:
                    if "@odata.id" in member:
                        try:
                            service_uri = member["@odata.id"]
                            service_data = self.get(service_uri)
                            services.append(service_data)
                        except Exception:
                            # Skip services that can't be retrieved
                            pass

            logger.debug(f"Found {len(services)} log services")
            return services
        except Exception as e:
            logger.error(f"Failed to get available log services: {str(e)}")
            raise

    def get_system_metrics(self, system_id: str = "1") -> Dict[str, Any]:
        """Get system metrics and telemetry data."""
        try:
            logger.info(f"Fetching system metrics for system {system_id}")

            metrics = {}

            # Get system information
            system = self.get_system(system_id)

            # Extract power metrics if available
            try:
                if "Power" in system:
                    power_uri = system["Power"]["@odata.id"]
                    power_data = self.get(power_uri)
                    metrics["power"] = power_data
            except Exception as e:
                logger.warning(f"Failed to get power metrics: {str(e)}")

            # Extract thermal metrics if available
            try:
                if "Thermal" in system:
                    thermal_uri = system["Thermal"]["@odata.id"]
                    thermal_data = self.get(thermal_uri)
                    metrics["thermal"] = thermal_data
            except Exception as e:
                logger.warning(f"Failed to get thermal metrics: {str(e)}")

            # Extract processor metrics if available
            try:
                if "Processors" in system:
                    processors_uri = system["Processors"]["@odata.id"]
                    processors_data = self.get(processors_uri)
                    metrics["processors"] = processors_data
            except Exception as e:
                logger.warning(f"Failed to get processor metrics: {str(e)}")

            # Extract memory metrics if available
            try:
                if "Memory" in system:
                    memory_uri = system["Memory"]["@odata.id"]
                    memory_data = self.get(memory_uri)
                    metrics["memory"] = memory_data
            except Exception as e:
                logger.warning(f"Failed to get memory metrics: {str(e)}")

            # Extract network metrics if available
            try:
                if "EthernetInterfaces" in system:
                    network_uri = system["EthernetInterfaces"]["@odata.id"]
                    network_data = self.get(network_uri)
                    metrics["network"] = network_data
            except Exception as e:
                logger.warning(f"Failed to get network metrics: {str(e)}")

            # Extract storage metrics if available
            try:
                if "Storage" in system:
                    storage_uri = system["Storage"]["@odata.id"]
                    storage_data = self.get(storage_uri)
                    metrics["storage"] = storage_data
            except Exception as e:
                logger.warning(f"Failed to get storage metrics: {str(e)}")

            logger.debug(f"Collected metrics for {len(metrics)} subsystems")
            return metrics
        except Exception as e:
            logger.error(f"Failed to get system metrics: {str(e)}")
            raise

    def get_power_metrics(self, chassis_id: str = "1") -> Dict[str, Any]:
        """Get detailed power metrics for a chassis."""
        try:
            logger.info(f"Fetching power metrics for chassis {chassis_id}")

            # Get chassis information
            chassis = self.get(f"/redfish/v1/Chassis/{chassis_id}")

            if "Power" not in chassis:
                raise Exception("Power metrics not available for this chassis")

            power_uri = chassis["Power"]["@odata.id"]
            power_data = self.get(power_uri)

            return power_data
        except Exception as e:
            logger.error(f"Failed to get power metrics: {str(e)}")
            raise

    def get_thermal_metrics(self, chassis_id: str = "1") -> Dict[str, Any]:
        """Get detailed thermal metrics for a chassis."""
        try:
            logger.info(f"Fetching thermal metrics for chassis {chassis_id}")

            # Get chassis information
            chassis = self.get(f"/redfish/v1/Chassis/{chassis_id}")

            if "Thermal" not in chassis:
                raise Exception("Thermal metrics not available for this chassis")

            thermal_uri = chassis["Thermal"]["@odata.id"]
            thermal_data = self.get(thermal_uri)

            return thermal_data
        except Exception as e:
            logger.error(f"Failed to get thermal metrics: {str(e)}")
            raise

    def get_telemetry_service(self) -> Dict[str, Any]:
        """Get telemetry service information if available."""
        try:
            logger.info("Fetching telemetry service information")
            return self.get("/redfish/v1/TelemetryService")
        except Exception as e:
            logger.error(f"Failed to get telemetry service: {str(e)}")
            raise

    def get_metric_report_definitions(self) -> List[Dict[str, Any]]:
        """Get available metric report definitions."""
        try:
            logger.info("Fetching metric report definitions")

            # Get telemetry service
            telemetry = self.get_telemetry_service()

            if "MetricReportDefinitions" not in telemetry:
                raise Exception("Metric report definitions not available")

            definitions_uri = telemetry["MetricReportDefinitions"]["@odata.id"]
            definitions = self.get(definitions_uri)

            # Get detailed information for each definition
            definition_list = []
            if "Members" in definitions:
                for member in definitions["Members"]:
                    if "@odata.id" in member:
                        try:
                            def_uri = member["@odata.id"]
                            def_data = self.get(def_uri)
                            definition_list.append(def_data)
                        except Exception:
                            # Skip definitions that can't be retrieved
                            pass

            logger.debug(f"Found {len(definition_list)} metric report definitions")
            return definition_list
        except Exception as e:
            logger.error(f"Failed to get metric report definitions: {str(e)}")
            raise

    def get_metric_reports(self) -> List[Dict[str, Any]]:
        """Get available metric reports."""
        try:
            logger.info("Fetching metric reports")

            # Get telemetry service
            telemetry = self.get_telemetry_service()

            if "MetricReports" not in telemetry:
                raise Exception("Metric reports not available")

            reports_uri = telemetry["MetricReports"]["@odata.id"]
            reports = self.get(reports_uri)

            # Get detailed information for each report
            report_list = []
            if "Members" in reports:
                for member in reports["Members"]:
                    if "@odata.id" in member:
                        try:
                            report_uri = member["@odata.id"]
                            report_data = self.get(report_uri)
                            report_list.append(report_data)
                        except Exception:
                            # Skip reports that can't be retrieved
                            pass

            logger.debug(f"Found {len(report_list)} metric reports")
            return report_list
        except Exception as e:
            logger.error(f"Failed to get metric reports: {str(e)}")
            raise

    def get_metric_report(self, report_id: str) -> Dict[str, Any]:
        """Get a specific metric report."""
        try:
            logger.info(f"Fetching metric report {report_id}")
            return self.get(f"/redfish/v1/TelemetryService/MetricReports/{report_id}")
        except Exception as e:
            logger.error(f"Failed to get metric report {report_id}: {str(e)}")
            raise

    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()
