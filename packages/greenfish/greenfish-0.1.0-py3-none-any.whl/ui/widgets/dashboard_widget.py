from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QProgressBar, QGroupBox, QFrame, QSizePolicy)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPalette
from typing import Dict, Any, List

class StatusCard(QFrame):
    """Widget for displaying a status card with title and value."""

    def __init__(self, title: str, value: str = "N/A", parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFrameShadow(QFrame.Shadow.Raised)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setMinimumHeight(100)

        # Setup layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        # Title label
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        layout.addWidget(self.title_label)

        # Value label
        self.value_label = QLabel(value)
        self.value_label.setStyleSheet("font-size: 18px; padding-top: 5px;")
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.value_label)

        # Set styling
        self.setStyleSheet("""
            StatusCard {
                background-color: rgb(255, 255, 220);
                border: 1px solid #CCCCCC;
                border-radius: 5px;
            }
        """)

    def set_value(self, value: str):
        """Update the card value."""
        self.value_label.setText(value)

    def set_status_color(self, status: str):
        """Update card color based on status."""
        if status.lower() == "ok" or status.lower() == "good":
            self.setStyleSheet("""
                StatusCard {
                    background-color: rgb(220, 255, 220);
                    border: 1px solid #CCCCCC;
                    border-radius: 5px;
                }
            """)
        elif status.lower() == "warning":
            self.setStyleSheet("""
                StatusCard {
                    background-color: rgb(255, 245, 200);
                    border: 1px solid #CCCCCC;
                    border-radius: 5px;
                }
            """)
        elif status.lower() == "critical" or status.lower() == "error":
            self.setStyleSheet("""
                StatusCard {
                    background-color: rgb(255, 220, 220);
                    border: 1px solid #CCCCCC;
                    border-radius: 5px;
                }
            """)
        else:
            self.setStyleSheet("""
                StatusCard {
                    background-color: rgb(255, 255, 220);
                    border: 1px solid #CCCCCC;
                    border-radius: 5px;
                }
            """)

class DashboardWidget(QWidget):
    """Widget for displaying system status dashboard."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        """Setup the user interface."""
        main_layout = QVBoxLayout(self)

        # System health section
        health_group = QGroupBox("System Health")
        health_layout = QHBoxLayout(health_group)

        # Create status cards
        self.system_status = StatusCard("System Status")
        self.power_status = StatusCard("Power Status")
        self.storage_status = StatusCard("Storage Status")
        self.thermal_status = StatusCard("Thermal Status")

        health_layout.addWidget(self.system_status)
        health_layout.addWidget(self.power_status)
        health_layout.addWidget(self.storage_status)
        health_layout.addWidget(self.thermal_status)

        main_layout.addWidget(health_group)

        # Resource utilization
        utilization_group = QGroupBox("Resource Utilization")
        utilization_layout = QVBoxLayout(utilization_group)

        # CPU utilization
        cpu_layout = QHBoxLayout()
        cpu_label = QLabel("CPU:")
        self.cpu_bar = QProgressBar()
        self.cpu_bar.setValue(0)
        cpu_layout.addWidget(cpu_label)
        cpu_layout.addWidget(self.cpu_bar)
        utilization_layout.addLayout(cpu_layout)

        # Memory utilization
        memory_layout = QHBoxLayout()
        memory_label = QLabel("Memory:")
        self.memory_bar = QProgressBar()
        self.memory_bar.setValue(0)
        memory_layout.addWidget(memory_label)
        memory_layout.addWidget(self.memory_bar)
        utilization_layout.addLayout(memory_layout)

        main_layout.addWidget(utilization_group)

        # Recent alerts section
        alerts_group = QGroupBox("Recent Alerts")
        alerts_layout = QVBoxLayout(alerts_group)

        self.alerts_label = QLabel("No recent alerts")
        alerts_layout.addWidget(self.alerts_label)

        main_layout.addWidget(alerts_group)

        # Set widget styling
        self.setStyleSheet("""
            QGroupBox {
                background-color: rgb(255, 255, 220);
                border: 1px solid #CCCCCC;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QLabel {
                color: #333333;
            }
            QProgressBar {
                border: 1px solid #CCCCCC;
                border-radius: 3px;
                background-color: rgb(240, 240, 240);
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: rgb(120, 180, 220);
            }
        """)

    def update_dashboard(self, system_data: Dict[str, Any]):
        """Update dashboard with system information."""
        # Update system status
        system_status = system_data.get("Status", {}).get("Health", "N/A")
        self.system_status.set_value(system_status)
        self.system_status.set_status_color(system_status)

        # Update power status
        power_state = system_data.get("PowerState", "N/A")
        self.power_status.set_value(power_state)
        self.power_status.set_status_color("OK" if power_state == "On" else "Warning")

        # Update storage status
        if "Storage" in system_data:
            storage_status = "OK"
            self.storage_status.set_value(storage_status)
            self.storage_status.set_status_color(storage_status)

        # Update thermal status
        if "Thermal" in system_data:
            thermal_status = system_data["Thermal"].get("Status", {}).get("Health", "N/A")
            self.thermal_status.set_value(thermal_status)
            self.thermal_status.set_status_color(thermal_status)

        # Update resource utilization
        # Note: Redfish doesn't always provide CPU/Memory utilization directly
        # These would need to be calculated or estimated based on available data

        # Update alerts
        self.update_alerts(system_data)

    def update_alerts(self, system_data: Dict[str, Any]):
        """Update alerts based on system data."""
        alerts = []

        # Check for system status alerts
        if system_data.get("Status", {}).get("Health") not in ["OK", "Good"]:
            alerts.append(f"System health: {system_data.get('Status', {}).get('Health', 'Unknown')}")

        # Check for thermal alerts
        if "Thermal" in system_data:
            thermal = system_data["Thermal"]
            if thermal.get("Status", {}).get("Health") not in ["OK", "Good"]:
                alerts.append(f"Thermal issue: {thermal.get('Status', {}).get('Health', 'Unknown')}")

        # Update alerts display
        if alerts:
            alert_text = "<ul>"
            for alert in alerts:
                alert_text += f"<li>{alert}</li>"
            alert_text += "</ul>"
            self.alerts_label.setText(alert_text)
        else:
            self.alerts_label.setText("No active alerts")
