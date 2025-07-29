"""Hardware Monitoring alert system."""
from enum import Enum, auto
from typing import Dict, Any, Optional, List, Union, Callable
from dataclasses import dataclass, field
import datetime
import re
import threading
import time
import json
import os

from greenfish.utils.logger import Logger
from greenfish.core.hwmonitor.types import SensorReading, SensorType, HealthStatus

class AlertLevel(Enum):
    """Alert severity levels."""
    INFO = "Info"
    WARNING = "Warning"
    CRITICAL = "Critical"

    @classmethod
    def from_health_status(cls, status: HealthStatus) -> 'AlertLevel':
        """Convert HealthStatus to AlertLevel.

        Args:
            status: Health status

        Returns:
            AlertLevel: Corresponding alert level
        """
        if status == HealthStatus.OK:
            return cls.INFO
        elif status == HealthStatus.WARNING:
            return cls.WARNING
        elif status == HealthStatus.CRITICAL:
            return cls.CRITICAL
        else:
            return cls.INFO

@dataclass
class AlertRule:
    """Alert rule configuration."""
    id: str
    name: str
    description: str
    enabled: bool = True
    sensor_type: Optional[SensorType] = None
    sensor_id: Optional[str] = None
    sensor_name_pattern: Optional[str] = None
    condition: Optional[str] = None
    threshold: Optional[float] = None
    level: AlertLevel = AlertLevel.WARNING
    action: Optional[str] = None
    parameters: Dict[str, Any] = field(default_factory=dict)

    def matches(self, sensor: SensorReading) -> bool:
        """Check if sensor matches this rule.

        Args:
            sensor: Sensor reading

        Returns:
            bool: True if sensor matches rule
        """
        # Check if rule is enabled
        if not self.enabled:
            return False

        # Check sensor type
        if self.sensor_type and sensor.sensor_type != self.sensor_type:
            return False

        # Check sensor ID
        if self.sensor_id and sensor.id != self.sensor_id:
            return False

        # Check sensor name pattern
        if self.sensor_name_pattern:
            try:
                pattern = re.compile(self.sensor_name_pattern, re.IGNORECASE)
                if not pattern.search(sensor.name):
                    return False
            except Exception as e:
                Logger.error(f"Invalid regex pattern in alert rule {self.id}: {str(e)}")
                return False

        # Check condition
        if self.condition and self.threshold is not None:
            # Only apply condition if sensor reading is numeric
            if isinstance(sensor.reading, (int, float)):
                if self.condition == ">" and sensor.reading <= self.threshold:
                    return False
                elif self.condition == ">=" and sensor.reading < self.threshold:
                    return False
                elif self.condition == "<" and sensor.reading >= self.threshold:
                    return False
                elif self.condition == "<=" and sensor.reading > self.threshold:
                    return False
                elif self.condition == "==" and sensor.reading != self.threshold:
                    return False
                elif self.condition == "!=" and sensor.reading == self.threshold:
                    return False
            else:
                # Non-numeric reading, can't apply condition
                return False

        # All checks passed
        return True

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AlertRule':
        """Create AlertRule from dictionary.

        Args:
            data: Dictionary data

        Returns:
            AlertRule: Alert rule object
        """
        sensor_type = None
        if "sensor_type" in data:
            sensor_type = SensorType.from_string(data["sensor_type"])

        level = AlertLevel.WARNING
        if "level" in data:
            try:
                level = AlertLevel(data["level"])
            except ValueError:
                level = AlertLevel.WARNING

        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            description=data.get("description", ""),
            enabled=data.get("enabled", True),
            sensor_type=sensor_type,
            sensor_id=data.get("sensor_id"),
            sensor_name_pattern=data.get("sensor_name_pattern"),
            condition=data.get("condition"),
            threshold=data.get("threshold"),
            level=level,
            action=data.get("action"),
            parameters=data.get("parameters", {})
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary.

        Returns:
            Dict: Dictionary representation
        """
        result = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "enabled": self.enabled,
            "level": self.level.value
        }

        if self.sensor_type:
            result["sensor_type"] = self.sensor_type.value

        if self.sensor_id:
            result["sensor_id"] = self.sensor_id

        if self.sensor_name_pattern:
            result["sensor_name_pattern"] = self.sensor_name_pattern

        if self.condition:
            result["condition"] = self.condition

        if self.threshold is not None:
            result["threshold"] = self.threshold

        if self.action:
            result["action"] = self.action

        if self.parameters:
            result["parameters"] = self.parameters

        return result

@dataclass
class Alert:
    """Alert data class."""
    id: str
    timestamp: datetime.datetime
    level: AlertLevel
    message: str
    sensor_id: Optional[str] = None
    sensor_name: Optional[str] = None
    sensor_reading: Optional[Union[float, str, bool]] = None
    sensor_type: Optional[SensorType] = None
    rule_id: Optional[str] = None
    acknowledged: bool = False
    acknowledged_by: Optional[str] = None
    acknowledged_time: Optional[datetime.datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary.

        Returns:
            Dict: Dictionary representation
        """
        result = {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "level": self.level.value,
            "message": self.message,
            "acknowledged": self.acknowledged
        }

        if self.sensor_id:
            result["sensor_id"] = self.sensor_id

        if self.sensor_name:
            result["sensor_name"] = self.sensor_name

        if self.sensor_reading is not None:
            result["sensor_reading"] = self.sensor_reading

        if self.sensor_type:
            result["sensor_type"] = self.sensor_type.value

        if self.rule_id:
            result["rule_id"] = self.rule_id

        if self.acknowledged_by:
            result["acknowledged_by"] = self.acknowledged_by

        if self.acknowledged_time:
            result["acknowledged_time"] = self.acknowledged_time.isoformat()

        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Alert':
        """Create Alert from dictionary.

        Args:
            data: Dictionary data

        Returns:
            Alert: Alert object
        """
        # Parse timestamp
        timestamp = datetime.datetime.now()
        if "timestamp" in data:
            try:
                timestamp = datetime.datetime.fromisoformat(data["timestamp"])
            except ValueError:
                pass

        # Parse level
        level = AlertLevel.INFO
        if "level" in data:
            try:
                level = AlertLevel(data["level"])
            except ValueError:
                level = AlertLevel.INFO

        # Parse sensor type
        sensor_type = None
        if "sensor_type" in data:
            sensor_type = SensorType.from_string(data["sensor_type"])

        # Parse acknowledged time
        acknowledged_time = None
        if "acknowledged_time" in data:
            try:
                acknowledged_time = datetime.datetime.fromisoformat(data["acknowledged_time"])
            except ValueError:
                pass

        return cls(
            id=data.get("id", ""),
            timestamp=timestamp,
            level=level,
            message=data.get("message", ""),
            sensor_id=data.get("sensor_id"),
            sensor_name=data.get("sensor_name"),
            sensor_reading=data.get("sensor_reading"),
            sensor_type=sensor_type,
            rule_id=data.get("rule_id"),
            acknowledged=data.get("acknowledged", False),
            acknowledged_by=data.get("acknowledged_by"),
            acknowledged_time=acknowledged_time
        )

class AlertManager:
    """Alert manager for handling hardware monitoring alerts."""

    def __init__(self, config_dir: str = None):
        """Initialize alert manager.

        Args:
            config_dir: Configuration directory
        """
        self.rules: List[AlertRule] = []
        self.alerts: List[Alert] = []
        self.alert_callbacks: List[Callable[[Alert], None]] = []
        self.config_dir = config_dir
        self.max_alerts = 1000
        self.alert_lock = threading.Lock()
        self.rule_lock = threading.Lock()

        # Load rules from configuration
        self._load_rules()

        # Load existing alerts
        self._load_alerts()

    def _load_rules(self) -> None:
        """Load alert rules from configuration."""
        if not self.config_dir:
            return

        rules_file = os.path.join(self.config_dir, "alert_rules.json")

        if not os.path.exists(rules_file):
            # Create default rules
            self._create_default_rules()
            return

        try:
            with open(rules_file, "r") as f:
                rules_data = json.load(f)

            with self.rule_lock:
                self.rules = []
                for rule_data in rules_data:
                    rule = AlertRule.from_dict(rule_data)
                    self.rules.append(rule)

            Logger.info(f"Loaded {len(self.rules)} alert rules")

        except Exception as e:
            Logger.error(f"Error loading alert rules: {str(e)}")
            # Create default rules
            self._create_default_rules()

    def _create_default_rules(self) -> None:
        """Create default alert rules."""
        with self.rule_lock:
            # Temperature rules
            self.rules.append(AlertRule(
                id="temp_warning",
                name="Temperature Warning",
                description="Alert when temperature exceeds warning threshold",
                sensor_type=SensorType.TEMPERATURE,
                condition=">",
                threshold=80.0,
                level=AlertLevel.WARNING
            ))

            self.rules.append(AlertRule(
                id="temp_critical",
                name="Temperature Critical",
                description="Alert when temperature exceeds critical threshold",
                sensor_type=SensorType.TEMPERATURE,
                condition=">",
                threshold=90.0,
                level=AlertLevel.CRITICAL
            ))

            # Fan rules
            self.rules.append(AlertRule(
                id="fan_warning",
                name="Fan Speed Warning",
                description="Alert when fan speed is below warning threshold",
                sensor_type=SensorType.FAN,
                condition="<",
                threshold=500.0,
                level=AlertLevel.WARNING
            ))

            self.rules.append(AlertRule(
                id="fan_critical",
                name="Fan Speed Critical",
                description="Alert when fan speed is below critical threshold",
                sensor_type=SensorType.FAN,
                condition="<",
                threshold=200.0,
                level=AlertLevel.CRITICAL
            ))

            # Voltage rules
            self.rules.append(AlertRule(
                id="voltage_warning",
                name="Voltage Warning",
                description="Alert when voltage is outside normal range",
                sensor_type=SensorType.VOLTAGE,
                level=AlertLevel.WARNING
            ))

            # Health state rule
            self.rules.append(AlertRule(
                id="health_state",
                name="Health State Alert",
                description="Alert when health state changes",
                sensor_type=SensorType.HEALTH_STATE,
                level=AlertLevel.WARNING
            ))

        # Save default rules
        self._save_rules()

        Logger.info("Created default alert rules")

    def _save_rules(self) -> None:
        """Save alert rules to configuration."""
        if not self.config_dir:
            return

        rules_file = os.path.join(self.config_dir, "alert_rules.json")

        try:
            # Create directory if it doesn't exist
            os.makedirs(self.config_dir, exist_ok=True)

            with self.rule_lock:
                rules_data = [rule.to_dict() for rule in self.rules]

            with open(rules_file, "w") as f:
                json.dump(rules_data, f, indent=2)

            Logger.info(f"Saved {len(self.rules)} alert rules")

        except Exception as e:
            Logger.error(f"Error saving alert rules: {str(e)}")

    def _load_alerts(self) -> None:
        """Load existing alerts from storage."""
        if not self.config_dir:
            return

        alerts_file = os.path.join(self.config_dir, "alerts.json")

        if not os.path.exists(alerts_file):
            return

        try:
            with open(alerts_file, "r") as f:
                alerts_data = json.load(f)

            with self.alert_lock:
                self.alerts = []
                for alert_data in alerts_data:
                    alert = Alert.from_dict(alert_data)
                    self.alerts.append(alert)

            Logger.info(f"Loaded {len(self.alerts)} alerts")

        except Exception as e:
            Logger.error(f"Error loading alerts: {str(e)}")

    def _save_alerts(self) -> None:
        """Save alerts to storage."""
        if not self.config_dir:
            return

        alerts_file = os.path.join(self.config_dir, "alerts.json")

        try:
            # Create directory if it doesn't exist
            os.makedirs(self.config_dir, exist_ok=True)

            with self.alert_lock:
                alerts_data = [alert.to_dict() for alert in self.alerts]

            with open(alerts_file, "w") as f:
                json.dump(alerts_data, f, indent=2)

        except Exception as e:
            Logger.error(f"Error saving alerts: {str(e)}")

    def add_rule(self, rule: AlertRule) -> bool:
        """Add alert rule.

        Args:
            rule: Alert rule

        Returns:
            bool: True if successful
        """
        try:
            with self.rule_lock:
                # Check if rule with same ID already exists
                for i, existing_rule in enumerate(self.rules):
                    if existing_rule.id == rule.id:
                        # Replace existing rule
                        self.rules[i] = rule
                        break
                else:
                    # Add new rule
                    self.rules.append(rule)

            # Save rules
            self._save_rules()

            return True

        except Exception as e:
            Logger.error(f"Error adding alert rule: {str(e)}")
            return False

    def remove_rule(self, rule_id: str) -> bool:
        """Remove alert rule.

        Args:
            rule_id: Rule ID

        Returns:
            bool: True if successful
        """
        try:
            with self.rule_lock:
                # Find rule with matching ID
                for i, rule in enumerate(self.rules):
                    if rule.id == rule_id:
                        # Remove rule
                        del self.rules[i]
                        break
                else:
                    # Rule not found
                    return False

            # Save rules
            self._save_rules()

            return True

        except Exception as e:
            Logger.error(f"Error removing alert rule: {str(e)}")
            return False

    def get_rules(self) -> List[AlertRule]:
        """Get all alert rules.

        Returns:
            List[AlertRule]: List of alert rules
        """
        with self.rule_lock:
            return self.rules.copy()

    def get_rule(self, rule_id: str) -> Optional[AlertRule]:
        """Get alert rule by ID.

        Args:
            rule_id: Rule ID

        Returns:
            AlertRule: Alert rule
        """
        with self.rule_lock:
            for rule in self.rules:
                if rule.id == rule_id:
                    return rule

        return None

    def register_alert_callback(self, callback: Callable[[Alert], None]) -> None:
        """Register callback for new alerts.

        Args:
            callback: Callback function
        """
        self.alert_callbacks.append(callback)

    def process_sensor_reading(self, sensor: SensorReading) -> List[Alert]:
        """Process sensor reading and generate alerts.

        Args:
            sensor: Sensor reading

        Returns:
            List[Alert]: List of generated alerts
        """
        generated_alerts = []

        try:
            # Get matching rules
            matching_rules = []
            with self.rule_lock:
                for rule in self.rules:
                    if rule.matches(sensor):
                        matching_rules.append(rule)

            # Generate alerts for matching rules
            for rule in matching_rules:
                # Create alert ID
                alert_id = f"{sensor.id}_{rule.id}_{int(time.time())}"

                # Create alert message
                if rule.condition and rule.threshold is not None and isinstance(sensor.reading, (int, float)):
                    message = f"{sensor.name} {rule.condition} {rule.threshold}"
                    if sensor.units:
                        message += f" {sensor.units}"
                else:
                    message = f"{sensor.name} triggered alert rule '{rule.name}'"

                # Create alert
                alert = Alert(
                    id=alert_id,
                    timestamp=datetime.datetime.now(),
                    level=rule.level,
                    message=message,
                    sensor_id=sensor.id,
                    sensor_name=sensor.name,
                    sensor_reading=sensor.reading,
                    sensor_type=sensor.sensor_type,
                    rule_id=rule.id
                )

                # Add alert to list
                with self.alert_lock:
                    self.alerts.append(alert)

                    # Trim alerts if exceeding maximum
                    if len(self.alerts) > self.max_alerts:
                        # Remove oldest alerts (non-acknowledged first)
                        self.alerts.sort(key=lambda a: (a.acknowledged, a.timestamp))
                        self.alerts = self.alerts[-self.max_alerts:]

                # Add to generated alerts
                generated_alerts.append(alert)

                # Notify callbacks
                for callback in self.alert_callbacks:
                    try:
                        callback(alert)
                    except Exception as e:
                        Logger.error(f"Error in alert callback: {str(e)}")

            # Save alerts if any were generated
            if generated_alerts:
                self._save_alerts()

            return generated_alerts

        except Exception as e:
            Logger.error(f"Error processing sensor reading: {str(e)}")
            return []

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
        with self.alert_lock:
            # Apply filters
            filtered_alerts = self.alerts

            if level is not None:
                filtered_alerts = [a for a in filtered_alerts if a.level == level]

            if acknowledged is not None:
                filtered_alerts = [a for a in filtered_alerts if a.acknowledged == acknowledged]

            if sensor_type is not None:
                filtered_alerts = [a for a in filtered_alerts if a.sensor_type == sensor_type]

            # Sort by timestamp (newest first)
            filtered_alerts.sort(key=lambda a: a.timestamp, reverse=True)

            # Limit count
            return filtered_alerts[:max_count]

    def acknowledge_alert(self, alert_id: str, user: str = None) -> bool:
        """Acknowledge alert.

        Args:
            alert_id: Alert ID
            user: User who acknowledged

        Returns:
            bool: True if successful
        """
        try:
            with self.alert_lock:
                # Find alert with matching ID
                for alert in self.alerts:
                    if alert.id == alert_id:
                        # Acknowledge alert
                        alert.acknowledged = True
                        alert.acknowledged_by = user
                        alert.acknowledged_time = datetime.datetime.now()
                        break
                else:
                    # Alert not found
                    return False

            # Save alerts
            self._save_alerts()

            return True

        except Exception as e:
            Logger.error(f"Error acknowledging alert: {str(e)}")
            return False

    def clear_alerts(self, acknowledged_only: bool = False) -> int:
        """Clear alerts.

        Args:
            acknowledged_only: Clear only acknowledged alerts

        Returns:
            int: Number of alerts cleared
        """
        try:
            count = 0
            with self.alert_lock:
                if acknowledged_only:
                    # Remove only acknowledged alerts
                    original_count = len(self.alerts)
                    self.alerts = [a for a in self.alerts if not a.acknowledged]
                    count = original_count - len(self.alerts)
                else:
                    # Remove all alerts
                    count = len(self.alerts)
                    self.alerts = []

            # Save alerts
            self._save_alerts()

            return count

        except Exception as e:
            Logger.error(f"Error clearing alerts: {str(e)}")
            return 0
