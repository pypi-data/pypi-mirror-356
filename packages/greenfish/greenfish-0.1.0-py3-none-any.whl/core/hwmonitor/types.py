"""Hardware Monitoring types and enumerations."""
from enum import Enum, auto
from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass
import datetime

class SensorType(Enum):
    """Sensor types."""
    TEMPERATURE = "Temperature"
    VOLTAGE = "Voltage"
    CURRENT = "Current"
    FAN = "Fan"
    POWER = "Power"
    ENERGY = "Energy"
    FREQUENCY = "Frequency"
    HUMIDITY = "Humidity"
    PRESSURE = "Pressure"
    FLUID_LEVEL = "FluidLevel"
    PRESENCE = "Presence"
    HEALTH_STATE = "HealthState"
    UTILIZATION = "Utilization"
    UNKNOWN = "Unknown"

    @classmethod
    def from_string(cls, value: str) -> 'SensorType':
        """Convert string to SensorType.

        Args:
            value: String value

        Returns:
            SensorType: Corresponding enum value
        """
        value_map = {
            "temperature": cls.TEMPERATURE,
            "voltage": cls.VOLTAGE,
            "current": cls.CURRENT,
            "fan": cls.FAN,
            "power": cls.POWER,
            "energy": cls.ENERGY,
            "frequency": cls.FREQUENCY,
            "humidity": cls.HUMIDITY,
            "pressure": cls.PRESSURE,
            "fluidlevel": cls.FLUID_LEVEL,
            "presence": cls.PRESENCE,
            "health": cls.HEALTH_STATE,
            "state": cls.HEALTH_STATE,
            "utilization": cls.UTILIZATION
        }

        if not value:
            return cls.UNKNOWN

        cleaned_value = value.lower().replace(" ", "").replace("_", "")
        return value_map.get(cleaned_value, cls.UNKNOWN)

class HealthStatus(Enum):
    """Health status values."""
    OK = "OK"
    WARNING = "Warning"
    CRITICAL = "Critical"
    UNKNOWN = "Unknown"

    @classmethod
    def from_string(cls, value: str) -> 'HealthStatus':
        """Convert string to HealthStatus.

        Args:
            value: String value

        Returns:
            HealthStatus: Corresponding enum value
        """
        value_map = {
            "ok": cls.OK,
            "good": cls.OK,
            "normal": cls.OK,
            "enabled": cls.OK,
            "warning": cls.WARNING,
            "degraded": cls.WARNING,
            "caution": cls.WARNING,
            "critical": cls.CRITICAL,
            "error": cls.CRITICAL,
            "severe": cls.CRITICAL,
            "failed": cls.CRITICAL,
            "disabled": cls.CRITICAL
        }

        if not value:
            return cls.UNKNOWN

        cleaned_value = value.lower().replace(" ", "").replace("_", "")
        return value_map.get(cleaned_value, cls.UNKNOWN)

@dataclass
class SensorReading:
    """Sensor reading data class."""
    id: str
    name: str
    sensor_type: SensorType
    reading: Optional[Union[float, str, bool]]
    units: Optional[str] = None
    status: HealthStatus = HealthStatus.UNKNOWN
    location: Optional[str] = None
    upper_critical: Optional[float] = None
    upper_warning: Optional[float] = None
    lower_warning: Optional[float] = None
    lower_critical: Optional[float] = None
    min_reading: Optional[float] = None
    max_reading: Optional[float] = None
    timestamp: Optional[datetime.datetime] = None
    raw_data: Optional[Dict[str, Any]] = None

    @classmethod
    def from_redfish(cls, data: Dict[str, Any]) -> 'SensorReading':
        """Create SensorReading from Redfish data.

        Args:
            data: Redfish sensor data

        Returns:
            SensorReading: Sensor reading object
        """
        # Extract sensor ID
        sensor_id = data.get("Id", data.get("MemberId", ""))

        # Extract sensor name
        name = data.get("Name", "")

        # Extract reading value
        reading = None
        if "Reading" in data:
            reading = data["Reading"]
        elif "ReadingCelsius" in data:
            reading = data["ReadingCelsius"]
        elif "ReadingVolts" in data:
            reading = data["ReadingVolts"]
        elif "ReadingRPM" in data:
            reading = data["ReadingRPM"]
        elif "ReadingWatts" in data:
            reading = data["ReadingWatts"]
        elif "State" in data:
            reading = data["State"]

        # Extract units
        units = data.get("ReadingUnits", None)

        # Extract sensor type
        sensor_type_str = data.get("SensorType", "")
        if not sensor_type_str and "ReadingCelsius" in data:
            sensor_type_str = "Temperature"
        elif not sensor_type_str and "ReadingVolts" in data:
            sensor_type_str = "Voltage"
        elif not sensor_type_str and "ReadingRPM" in data:
            sensor_type_str = "Fan"
        elif not sensor_type_str and "ReadingWatts" in data:
            sensor_type_str = "Power"

        sensor_type = SensorType.from_string(sensor_type_str)

        # Extract health status
        status_data = data.get("Status", {})
        health_str = status_data.get("Health", status_data.get("State", ""))
        status = HealthStatus.from_string(health_str)

        # Extract thresholds
        thresholds = data.get("Thresholds", {})
        upper_critical = None
        upper_warning = None
        lower_warning = None
        lower_critical = None

        if thresholds:
            for threshold in thresholds.get("UpperCritical", []):
                if threshold.get("Activation", "") == "Increasing":
                    upper_critical = threshold.get("Reading")

            for threshold in thresholds.get("UpperWarning", []):
                if threshold.get("Activation", "") == "Increasing":
                    upper_warning = threshold.get("Reading")

            for threshold in thresholds.get("LowerWarning", []):
                if threshold.get("Activation", "") == "Decreasing":
                    lower_warning = threshold.get("Reading")

            for threshold in thresholds.get("LowerCritical", []):
                if threshold.get("Activation", "") == "Decreasing":
                    lower_critical = threshold.get("Reading")

        # Extract location
        location = None
        physical_context = data.get("PhysicalContext", "")
        physical_sub_context = data.get("PhysicalSubContext", "")

        if physical_context and physical_sub_context:
            location = f"{physical_context} {physical_sub_context}"
        elif physical_context:
            location = physical_context

        # Create sensor reading object
        return cls(
            id=sensor_id,
            name=name,
            sensor_type=sensor_type,
            reading=reading,
            units=units,
            status=status,
            location=location,
            upper_critical=upper_critical,
            upper_warning=upper_warning,
            lower_warning=lower_warning,
            lower_critical=lower_critical,
            timestamp=datetime.datetime.now(),
            raw_data=data
        )

    @classmethod
    def from_ipmi(cls, data: Dict[str, Any]) -> 'SensorReading':
        """Create SensorReading from IPMI data.

        Args:
            data: IPMI sensor data

        Returns:
            SensorReading: Sensor reading object
        """
        # Extract sensor ID
        sensor_id = str(data.get("sensor_number", ""))

        # Extract sensor name
        name = data.get("sensor_name", "")

        # Extract reading value
        reading = data.get("reading", None)

        # Extract units
        units = data.get("units", None)

        # Extract sensor type
        sensor_type_str = data.get("sensor_type", "")
        sensor_type = SensorType.from_string(sensor_type_str)

        # Extract health status
        status_str = data.get("status", "")
        status = HealthStatus.from_string(status_str)

        # Extract thresholds
        upper_critical = data.get("upper_critical", None)
        upper_warning = data.get("upper_non_critical", None)
        lower_warning = data.get("lower_non_critical", None)
        lower_critical = data.get("lower_critical", None)

        # Extract min/max readings
        min_reading = data.get("min_reading", None)
        max_reading = data.get("max_reading", None)

        # Create sensor reading object
        return cls(
            id=sensor_id,
            name=name,
            sensor_type=sensor_type,
            reading=reading,
            units=units,
            status=status,
            upper_critical=upper_critical,
            upper_warning=upper_warning,
            lower_warning=lower_warning,
            lower_critical=lower_critical,
            min_reading=min_reading,
            max_reading=max_reading,
            timestamp=datetime.datetime.now(),
            raw_data=data
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary.

        Returns:
            Dict: Dictionary representation
        """
        result = {
            "id": self.id,
            "name": self.name,
            "sensor_type": self.sensor_type.value,
            "reading": self.reading,
            "status": self.status.value
        }

        if self.units:
            result["units"] = self.units

        if self.location:
            result["location"] = self.location

        if self.upper_critical is not None:
            result["upper_critical"] = self.upper_critical

        if self.upper_warning is not None:
            result["upper_warning"] = self.upper_warning

        if self.lower_warning is not None:
            result["lower_warning"] = self.lower_warning

        if self.lower_critical is not None:
            result["lower_critical"] = self.lower_critical

        if self.min_reading is not None:
            result["min_reading"] = self.min_reading

        if self.max_reading is not None:
            result["max_reading"] = self.max_reading

        if self.timestamp:
            result["timestamp"] = self.timestamp.isoformat()

        return result
