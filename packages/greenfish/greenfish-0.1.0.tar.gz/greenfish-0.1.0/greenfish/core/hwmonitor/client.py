"""Hardware Monitoring client implementation."""
from typing import Dict, Any, Optional, List, Union, Callable
import threading
import time
import datetime
import os
import json

from greenfish.utils.logger import Logger
from greenfish.core.hwmonitor.types import SensorReading, SensorType, HealthStatus
from greenfish.core.hwmonitor.alert import AlertManager, Alert, AlertRule, AlertLevel

class HardwareMonitorClient:
    """Hardware Monitor client for monitoring BMC hardware."""

    def __init__(self, config_dir: str = None):
        """Initialize Hardware Monitor client.

        Args:
            config_dir: Configuration directory
        """
        self.redfish_client = None
        self.ipmi_client = None
        self.connection_type = None
        self.connected = False
        self.sensor_cache = {}
        self.health_status = {}
        self.alert_manager = AlertManager(config_dir)
        self.polling_thread = None
        self.polling_interval = 60  # seconds
        self.polling_enabled = False
        self.sensor_callbacks = []
        self.health_callbacks = []

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
            self.sensor_cache = {}
            self.health_status = {}

            return True

        except Exception as e:
            Logger.error(f"Error connecting Hardware Monitor client: {str(e)}")
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
            self.sensor_cache = {}
            self.health_status = {}

            return True

        except Exception as e:
            Logger.error(f"Error connecting Hardware Monitor client: {str(e)}")
            self.connected = False
            return False

    def disconnect(self) -> bool:
        """Disconnect client.

        Returns:
            bool: True if successful
        """
        # Stop polling
        self.stop_polling()

        self.redfish_client = None
        self.ipmi_client = None
        self.connection_type = None
        self.connected = False
        self.sensor_cache = {}
        self.health_status = {}
        return True

    def is_connected(self) -> bool:
        """Check if client is connected.

        Returns:
            bool: True if connected
        """
        return self.connected

    def _get_redfish_sensors(self) -> List[SensorReading]:
        """Get sensors from Redfish.

        Returns:
            List[SensorReading]: List of sensor readings
        """
        sensors = []

        try:
            if not self.redfish_client or not self.connected:
                Logger.error("Not connected to Redfish")
                return []

            # Get thermal sensors
            thermal_data = self.redfish_client.get_thermal()
            if thermal_data:
                # Process temperature sensors
                for sensor in thermal_data.get("Temperatures", []):
                    sensor_reading = SensorReading.from_redfish(sensor)
                    sensors.append(sensor_reading)

                # Process fans
                for sensor in thermal_data.get("Fans", []):
                    sensor_reading = SensorReading.from_redfish(sensor)
                    sensors.append(sensor_reading)

            # Get power sensors
            power_data = self.redfish_client.get_power()
            if power_data:
                # Process power supplies
                for sensor in power_data.get("PowerSupplies", []):
                    # Create sensor for power supply status
                    status_sensor = {
                        "Id": f"{sensor.get('Id', '')}_Status",
                        "Name": f"{sensor.get('Name', '')} Status",
                        "Status": sensor.get("Status", {}),
                        "SensorType": "HealthState"
                    }
                    sensor_reading = SensorReading.from_redfish(status_sensor)
                    sensors.append(sensor_reading)

                    # Create sensor for power output
                    if "PowerOutputWatts" in sensor:
                        output_sensor = {
                            "Id": f"{sensor.get('Id', '')}_Output",
                            "Name": f"{sensor.get('Name', '')} Output",
                            "Reading": sensor.get("PowerOutputWatts"),
                            "ReadingUnits": "Watts",
                            "SensorType": "Power"
                        }
                        sensor_reading = SensorReading.from_redfish(output_sensor)
                        sensors.append(sensor_reading)

                    # Create sensor for input voltage
                    if "LineInputVoltage" in sensor:
                        voltage_sensor = {
                            "Id": f"{sensor.get('Id', '')}_Voltage",
                            "Name": f"{sensor.get('Name', '')} Input Voltage",
                            "Reading": sensor.get("LineInputVoltage"),
                            "ReadingUnits": "Volts",
                            "SensorType": "Voltage"
                        }
                        sensor_reading = SensorReading.from_redfish(voltage_sensor)
                        sensors.append(sensor_reading)

                # Process voltage sensors
                for sensor in power_data.get("Voltages", []):
                    sensor_reading = SensorReading.from_redfish(sensor)
                    sensors.append(sensor_reading)

            # Get additional sensors from Chassis
            chassis_list = self.redfish_client.get_chassis()
            for chassis in chassis_list:
                chassis_id = chassis.get("Id", "")

                # Get sensors collection
                sensors_uri = chassis.get("Sensors", {}).get("@odata.id")
                if sensors_uri:
                    sensors_data = self.redfish_client.get(sensors_uri)
                    if sensors_data and "Members" in sensors_data:
                        for member in sensors_data["Members"]:
                            sensor_uri = member.get("@odata.id")
                            if sensor_uri:
                                sensor_data = self.redfish_client.get(sensor_uri)
                                if sensor_data:
                                    sensor_reading = SensorReading.from_redfish(sensor_data)
                                    sensors.append(sensor_reading)

            return sensors

        except Exception as e:
            Logger.error(f"Error getting Redfish sensors: {str(e)}")
            return []

    def _get_ipmi_sensors(self) -> List[SensorReading]:
        """Get sensors from IPMI.

        Returns:
            List[SensorReading]: List of sensor readings
        """
        sensors = []

        try:
            if not self.ipmi_client or not self.connected:
                Logger.error("Not connected to IPMI")
                return []

            # Get sensor readings
            sensor_data = self.ipmi_client.get_sensor_readings()

            # Convert to SensorReading objects
            for sensor in sensor_data:
                sensor_reading = SensorReading.from_ipmi(sensor)
                sensors.append(sensor_reading)

            return sensors

        except Exception as e:
            Logger.error(f"Error getting IPMI sensors: {str(e)}")
            return []

    def get_sensors(self, sensor_type: Optional[SensorType] = None, use_cache: bool = False) -> List[SensorReading]:
        """Get sensor readings.

        Args:
            sensor_type: Filter by sensor type
            use_cache: Use cached sensor readings

        Returns:
            List[SensorReading]: List of sensor readings
        """
        try:
            if not self.connected:
                Logger.error("Not connected")
                return []

            # Check if using cache
            if use_cache and self.sensor_cache:
                sensors = list(self.sensor_cache.values())
            else:
                # Get sensors based on connection type
                if self.connection_type == "redfish":
                    sensors = self._get_redfish_sensors()
                elif self.connection_type == "ipmi":
                    sensors = self._get_ipmi_sensors()
                else:
                    sensors = []

                # Update cache
                for sensor in sensors:
                    self.sensor_cache[sensor.id] = sensor

                # Process alerts
                self._process_alerts(sensors)

                # Notify callbacks
                for callback in self.sensor_callbacks:
                    try:
                        callback(sensors)
                    except Exception as e:
                        Logger.error(f"Error in sensor callback: {str(e)}")

            # Filter by sensor type if specified
            if sensor_type:
                sensors = [s for s in sensors if s.sensor_type == sensor_type]

            return sensors

        except Exception as e:
            Logger.error(f"Error getting sensors: {str(e)}")
            return []

    def get_sensor(self, sensor_id: str, use_cache: bool = False) -> Optional[SensorReading]:
        """Get sensor reading by ID.

        Args:
            sensor_id: Sensor ID
            use_cache: Use cached sensor reading

        Returns:
            SensorReading: Sensor reading
        """
        try:
            if not self.connected:
                Logger.error("Not connected")
                return None

            # Check if using cache
            if use_cache and sensor_id in self.sensor_cache:
                return self.sensor_cache[sensor_id]

            # Get all sensors
            sensors = self.get_sensors(use_cache=False)

            # Find sensor with matching ID
            for sensor in sensors:
                if sensor.id == sensor_id:
                    return sensor

            return None

        except Exception as e:
            Logger.error(f"Error getting sensor: {str(e)}")
            return None

    def _get_redfish_health(self) -> Dict[str, HealthStatus]:
        """Get health status from Redfish.

        Returns:
            Dict[str, HealthStatus]: Health status by component
        """
        health_status = {}

        try:
            if not self.redfish_client or not self.connected:
                Logger.error("Not connected to Redfish")
                return {}

            # Get system health
            systems = self.redfish_client.get_systems()
            for system in systems:
                system_id = system.get("Id", "")
                status = system.get("Status", {})
                health = status.get("Health", "")
                health_status[f"System_{system_id}"] = HealthStatus.from_string(health)

                # Get processor health
                processors_uri = system.get("Processors", {}).get("@odata.id")
                if processors_uri:
                    processors = self.redfish_client.get(processors_uri)
                    if processors and "Members" in processors:
                        for i, member in enumerate(processors["Members"]):
                            processor_uri = member.get("@odata.id")
                            if processor_uri:
                                processor = self.redfish_client.get(processor_uri)
                                if processor:
                                    processor_id = processor.get("Id", f"CPU{i}")
                                    status = processor.get("Status", {})
                                    health = status.get("Health", "")
                                    health_status[f"Processor_{processor_id}"] = HealthStatus.from_string(health)

                # Get memory health
                memory_uri = system.get("Memory", {}).get("@odata.id")
                if memory_uri:
                    memory = self.redfish_client.get(memory_uri)
                    if memory and "Members" in memory:
                        for i, member in enumerate(memory["Members"]):
                            dimm_uri = member.get("@odata.id")
                            if dimm_uri:
                                dimm = self.redfish_client.get(dimm_uri)
                                if dimm:
                                    dimm_id = dimm.get("Id", f"DIMM{i}")
                                    status = dimm.get("Status", {})
                                    health = status.get("Health", "")
                                    health_status[f"Memory_{dimm_id}"] = HealthStatus.from_string(health)

            # Get chassis health
            chassis_list = self.redfish_client.get_chassis()
            for chassis in chassis_list:
                chassis_id = chassis.get("Id", "")
                status = chassis.get("Status", {})
                health = status.get("Health", "")
                health_status[f"Chassis_{chassis_id}"] = HealthStatus.from_string(health)

            # Get manager health
            managers = self.redfish_client.get_managers()
            for manager in managers:
                manager_id = manager.get("Id", "")
                status = manager.get("Status", {})
                health = status.get("Health", "")
                health_status[f"Manager_{manager_id}"] = HealthStatus.from_string(health)

            return health_status

        except Exception as e:
            Logger.error(f"Error getting Redfish health: {str(e)}")
            return {}

    def _get_ipmi_health(self) -> Dict[str, HealthStatus]:
        """Get health status from IPMI.

        Returns:
            Dict[str, HealthStatus]: Health status by component
        """
        health_status = {}

        try:
            if not self.ipmi_client or not self.connected:
                Logger.error("Not connected to IPMI")
                return {}

            # Get system health from SEL
            sel_entries = self.ipmi_client.sel.get_sel_info()
            if sel_entries:
                # Check if there are any critical SEL entries
                critical_entries = False
                warning_entries = False

                # Get recent SEL entries
                entries = self.ipmi_client.sel.get_sel_entries(count=10)

                for entry in entries:
                    severity = entry.get("severity", "").lower()
                    if severity in ["critical", "error", "fatal"]:
                        critical_entries = True
                        break
                    elif severity in ["warning", "non-critical"]:
                        warning_entries = True

                if critical_entries:
                    health_status["System"] = HealthStatus.CRITICAL
                elif warning_entries:
                    health_status["System"] = HealthStatus.WARNING
                else:
                    health_status["System"] = HealthStatus.OK

            # Get health from sensor readings
            sensors = self._get_ipmi_sensors()

            # Group sensors by type
            sensor_groups = {}
            for sensor in sensors:
                sensor_type = sensor.sensor_type.value
                if sensor_type not in sensor_groups:
                    sensor_groups[sensor_type] = []
                sensor_groups[sensor_type].append(sensor)

            # Determine health status for each sensor group
            for sensor_type, group_sensors in sensor_groups.items():
                critical_count = 0
                warning_count = 0
                ok_count = 0

                for sensor in group_sensors:
                    if sensor.status == HealthStatus.CRITICAL:
                        critical_count += 1
                    elif sensor.status == HealthStatus.WARNING:
                        warning_count += 1
                    elif sensor.status == HealthStatus.OK:
                        ok_count += 1

                if critical_count > 0:
                    health_status[sensor_type] = HealthStatus.CRITICAL
                elif warning_count > 0:
                    health_status[sensor_type] = HealthStatus.WARNING
                elif ok_count > 0:
                    health_status[sensor_type] = HealthStatus.OK
                else:
                    health_status[sensor_type] = HealthStatus.UNKNOWN

            return health_status

        except Exception as e:
            Logger.error(f"Error getting IPMI health: {str(e)}")
            return {}

    def get_health(self, use_cache: bool = False) -> Dict[str, HealthStatus]:
        """Get health status.

        Args:
            use_cache: Use cached health status

        Returns:
            Dict[str, HealthStatus]: Health status by component
        """
        try:
            if not self.connected:
                Logger.error("Not connected")
                return {}

            # Check if using cache
            if use_cache and self.health_status:
                return self.health_status

            # Get health based on connection type
            if self.connection_type == "redfish":
                health_status = self._get_redfish_health()
            elif self.connection_type == "ipmi":
                health_status = self._get_ipmi_health()
            else:
                health_status = {}

            # Determine overall health
            if health_status:
                critical_count = 0
                warning_count = 0
                ok_count = 0

                for component, status in health_status.items():
                    if status == HealthStatus.CRITICAL:
                        critical_count += 1
                    elif status == HealthStatus.WARNING:
                        warning_count += 1
                    elif status == HealthStatus.OK:
                        ok_count += 1

                if critical_count > 0:
                    health_status["Overall"] = HealthStatus.CRITICAL
                elif warning_count > 0:
                    health_status["Overall"] = HealthStatus.WARNING
                elif ok_count > 0:
                    health_status["Overall"] = HealthStatus.OK
                else:
                    health_status["Overall"] = HealthStatus.UNKNOWN

            # Update cache
            self.health_status = health_status

            # Notify callbacks
            for callback in self.health_callbacks:
                try:
                    callback(health_status)
                except Exception as e:
                    Logger.error(f"Error in health callback: {str(e)}")

            return health_status

        except Exception as e:
            Logger.error(f"Error getting health status: {str(e)}")
            return {}

    def _process_alerts(self, sensors: List[SensorReading]) -> List[Alert]:
        """Process sensor readings and generate alerts.

        Args:
            sensors: List of sensor readings

        Returns:
            List[Alert]: Generated alerts
        """
        alerts = []

        try:
            for sensor in sensors:
                # Process sensor with alert manager
                sensor_alerts = self.alert_manager.process_sensor_reading(sensor)
                alerts.extend(sensor_alerts)

            return alerts

        except Exception as e:
            Logger.error(f"Error processing alerts: {str(e)}")
            return []

    def start_polling(self, interval: int = 60) -> bool:
        """Start polling for sensor readings.

        Args:
            interval: Polling interval in seconds

        Returns:
            bool: True if successful
        """
        try:
            if not self.connected:
                Logger.error("Not connected")
                return False

            # Stop existing polling
            self.stop_polling()

            # Set polling interval
            self.polling_interval = interval
            self.polling_enabled = True

            # Start polling thread
            self.polling_thread = threading.Thread(target=self._polling_loop)
            self.polling_thread.daemon = True
            self.polling_thread.start()

            Logger.info(f"Started hardware monitoring polling (interval: {interval}s)")
            return True

        except Exception as e:
            Logger.error(f"Error starting polling: {str(e)}")
            return False

    def stop_polling(self) -> bool:
        """Stop polling for sensor readings.

        Returns:
            bool: True if successful
        """
        try:
            # Stop polling
            self.polling_enabled = False

            # Wait for thread to terminate
            if self.polling_thread and self.polling_thread.is_alive():
                self.polling_thread.join(timeout=2)

            self.polling_thread = None

            Logger.info("Stopped hardware monitoring polling")
            return True

        except Exception as e:
            Logger.error(f"Error stopping polling: {str(e)}")
            return False

    def _polling_loop(self) -> None:
        """Polling loop for sensor readings."""
        try:
            while self.polling_enabled and self.connected:
                # Get sensor readings
                self.get_sensors(use_cache=False)

                # Get health status
                self.get_health(use_cache=False)

                # Sleep for polling interval
                time.sleep(self.polling_interval)

        except Exception as e:
            Logger.error(f"Error in polling loop: {str(e)}")
            self.polling_enabled = False

    def register_sensor_callback(self, callback: Callable[[List[SensorReading]], None]) -> None:
        """Register callback for sensor updates.

        Args:
            callback: Callback function
        """
        self.sensor_callbacks.append(callback)

    def register_health_callback(self, callback: Callable[[Dict[str, HealthStatus]], None]) -> None:
        """Register callback for health status updates.

        Args:
            callback: Callback function
        """
        self.health_callbacks.append(callback)

    def get_alerts(self,
                  max_count: int = 100,
                  level: Optional[AlertLevel] = None,
                  acknowledged: Optional[bool] = None,
                  sensor_type: Optional[SensorType] = None) -> List[Alert]:
        """Get alerts with optional filtering.

        Args:
            max_count: Maximum number of alerts to return
            level: Filter by alert level
            acknowledged: Filter by acknowledged status
            sensor_type: Filter by sensor type

        Returns:
            List[Alert]: List of alerts
        """
        return self.alert_manager.get_alerts(max_count, level, acknowledged, sensor_type)

    def acknowledge_alert(self, alert_id: str, user: str = None) -> bool:
        """Acknowledge alert.

        Args:
            alert_id: Alert ID
            user: User who acknowledged

        Returns:
            bool: True if successful
        """
        return self.alert_manager.acknowledge_alert(alert_id, user)

    def clear_alerts(self, acknowledged_only: bool = False) -> int:
        """Clear alerts.

        Args:
            acknowledged_only: Clear only acknowledged alerts

        Returns:
            int: Number of alerts cleared
        """
        return self.alert_manager.clear_alerts(acknowledged_only)

    def get_alert_rules(self) -> List[AlertRule]:
        """Get alert rules.

        Returns:
            List[AlertRule]: List of alert rules
        """
        return self.alert_manager.get_rules()

    def add_alert_rule(self, rule: AlertRule) -> bool:
        """Add alert rule.

        Args:
            rule: Alert rule

        Returns:
            bool: True if successful
        """
        return self.alert_manager.add_rule(rule)

    def remove_alert_rule(self, rule_id: str) -> bool:
        """Remove alert rule.

        Args:
            rule_id: Rule ID

        Returns:
            bool: True if successful
        """
        return self.alert_manager.remove_rule(rule_id)

    def register_alert_callback(self, callback: Callable[[Alert], None]) -> None:
        """Register callback for new alerts.

        Args:
            callback: Callback function
        """
        self.alert_manager.register_alert_callback(callback)
