from PyQt6.QtWidgets import QLabel, QGridLayout, QWidget, QProgressBar
from PyQt6.QtCore import Qt

from greenfish.ui.widgets.metrics.base_panel import BaseMetricsPanel
from greenfish.utils.logger import Logger


class ThermalMetricsPanel(BaseMetricsPanel):
    """Panel for displaying thermal metrics"""

    def __init__(self, parent=None):
        super().__init__(parent)

    def refresh(self):
        """Refresh thermal metrics data"""
        if not self.client or not self.resource_id:
            self.show_error("No Redfish client or chassis ID available")
            return

        self.show_loading()
        self.clear_content()

        try:
            # Get thermal metrics from the client
            thermal_data = self.client.get_thermal_metrics(self.resource_id)
            if not thermal_data:
                self.show_error("No thermal data available")
                return

            self.data = thermal_data
            self.hide_status()
            self.display_thermal_data()

        except Exception as e:
            Logger.error(f"Failed to get thermal metrics: {str(e)}")
            self.show_error(str(e))

    def display_thermal_data(self):
        """Display the thermal data in the panel"""
        if not self.data:
            return

        # Temperatures section
        if 'Temperatures' in self.data and self.data['Temperatures']:
            temp_section, section_layout = self.create_section("Temperature Sensors")

            for i, sensor in enumerate(self.data['Temperatures']):
                sensor_widget = QWidget()
                sensor_layout = QGridLayout(sensor_widget)
                sensor_layout.setContentsMargins(10, 5, 10, 5)

                # Add title for this sensor
                name = sensor.get('Name', f"Sensor {i+1}")
                title = QLabel(name)
                title.setStyleSheet("font-weight: bold;")
                sensor_layout.addWidget(title, 0, 0, 1, 2)

                row = 1

                # Current reading
                if 'ReadingCelsius' in sensor:
                    reading = sensor['ReadingCelsius']
                    sensor_layout.addWidget(QLabel("Current Temperature:"), row, 0)
                    sensor_layout.addWidget(QLabel(f"{reading}°C"), row, 1)
                    row += 1

                    # Add a progress bar if we have min/max values
                    if 'MinReadingRangeTemp' in sensor and 'MaxReadingRangeTemp' in sensor:
                        min_temp = sensor['MinReadingRangeTemp']
                        max_temp = sensor['MaxReadingRangeTemp']

                        progress = QProgressBar()
                        progress.setMinimum(int(min_temp))
                        progress.setMaximum(int(max_temp))
                        progress.setValue(int(reading))

                        # Set color based on thresholds if available
                        if 'UpperThresholdCritical' in sensor and reading >= sensor['UpperThresholdCritical']:
                            progress.setStyleSheet("QProgressBar::chunk { background-color: red; }")
                        elif 'UpperThresholdNonCritical' in sensor and reading >= sensor['UpperThresholdNonCritical']:
                            progress.setStyleSheet("QProgressBar::chunk { background-color: orange; }")
                        else:
                            progress.setStyleSheet("QProgressBar::chunk { background-color: green; }")

                        sensor_layout.addWidget(progress, row, 0, 1, 2)
                        row += 1

                # Thresholds
                if 'UpperThresholdNonCritical' in sensor:
                    sensor_layout.addWidget(QLabel("Warning Threshold:"), row, 0)
                    sensor_layout.addWidget(QLabel(f"{sensor['UpperThresholdNonCritical']}°C"), row, 1)
                    row += 1

                if 'UpperThresholdCritical' in sensor:
                    sensor_layout.addWidget(QLabel("Critical Threshold:"), row, 0)
                    sensor_layout.addWidget(QLabel(f"{sensor['UpperThresholdCritical']}°C"), row, 1)
                    row += 1

                if 'UpperThresholdFatal' in sensor:
                    sensor_layout.addWidget(QLabel("Fatal Threshold:"), row, 0)
                    sensor_layout.addWidget(QLabel(f"{sensor['UpperThresholdFatal']}°C"), row, 1)
                    row += 1

                # Status
                if 'Status' in sensor:
                    status = sensor['Status']
                    health = status.get('Health', 'Unknown')
                    state = status.get('State', 'Unknown')

                    sensor_layout.addWidget(QLabel("Health:"), row, 0)
                    health_label = QLabel(health)

                    # Set color based on health
                    if health == 'OK':
                        health_label.setStyleSheet("color: green;")
                    elif health == 'Warning':
                        health_label.setStyleSheet("color: orange;")
                    elif health == 'Critical':
                        health_label.setStyleSheet("color: red;")

                    sensor_layout.addWidget(health_label, row, 1)
                    row += 1

                    sensor_layout.addWidget(QLabel("State:"), row, 0)
                    sensor_layout.addWidget(QLabel(state), row, 1)
                    row += 1

                section_layout.addWidget(sensor_widget)

                # Add separator if not the last item
                if i < len(self.data['Temperatures']) - 1:
                    separator = QWidget()
                    separator.setFixedHeight(1)
                    separator.setStyleSheet("background-color: #cccccc;")
                    section_layout.addWidget(separator)

            self.content_layout.insertWidget(0, temp_section)

        # Fans section
        if 'Fans' in self.data and self.data['Fans']:
            fans_section, section_layout = self.create_section("Fans")

            for i, fan in enumerate(self.data['Fans']):
                fan_widget = QWidget()
                fan_layout = QGridLayout(fan_widget)
                fan_layout.setContentsMargins(10, 5, 10, 5)

                # Add title for this fan
                name = fan.get('Name', f"Fan {i+1}")
                title = QLabel(name)
                title.setStyleSheet("font-weight: bold;")
                fan_layout.addWidget(title, 0, 0, 1, 2)

                row = 1

                # Current reading
                if 'Reading' in fan:
                    reading = fan['Reading']
                    units = fan.get('ReadingUnits', 'RPM')
                    fan_layout.addWidget(QLabel("Current Speed:"), row, 0)
                    fan_layout.addWidget(QLabel(f"{reading} {units}"), row, 1)
                    row += 1

                    # Add a progress bar if we have min/max values
                    if 'MinReadingRange' in fan and 'MaxReadingRange' in fan:
                        min_speed = fan['MinReadingRange']
                        max_speed = fan['MaxReadingRange']

                        progress = QProgressBar()
                        progress.setMinimum(int(min_speed))
                        progress.setMaximum(int(max_speed))
                        progress.setValue(int(reading))

                        fan_layout.addWidget(progress, row, 0, 1, 2)
                        row += 1

                # Status
                if 'Status' in fan:
                    status = fan['Status']
                    health = status.get('Health', 'Unknown')
                    state = status.get('State', 'Unknown')

                    fan_layout.addWidget(QLabel("Health:"), row, 0)
                    health_label = QLabel(health)

                    # Set color based on health
                    if health == 'OK':
                        health_label.setStyleSheet("color: green;")
                    elif health == 'Warning':
                        health_label.setStyleSheet("color: orange;")
                    elif health == 'Critical':
                        health_label.setStyleSheet("color: red;")

                    fan_layout.addWidget(health_label, row, 1)
                    row += 1

                    fan_layout.addWidget(QLabel("State:"), row, 0)
                    fan_layout.addWidget(QLabel(state), row, 1)
                    row += 1

                section_layout.addWidget(fan_widget)

                # Add separator if not the last item
                if i < len(self.data['Fans']) - 1:
                    separator = QWidget()
                    separator.setFixedHeight(1)
                    separator.setStyleSheet("background-color: #cccccc;")
                    section_layout.addWidget(separator)

            self.content_layout.insertWidget(1, fans_section)

        # Redundancy section
        if 'Redundancy' in self.data and self.data['Redundancy']:
            redundancy_section, section_layout = self.create_section("Cooling Redundancy")

            for i, redundancy in enumerate(self.data['Redundancy']):
                redundancy_widget = QWidget()
                redundancy_layout = QGridLayout(redundancy_widget)
                redundancy_layout.setContentsMargins(10, 5, 10, 5)

                row = 0

                # Add redundancy information
                if 'Name' in redundancy:
                    redundancy_layout.addWidget(QLabel("Name:"), row, 0)
                    redundancy_layout.addWidget(QLabel(redundancy['Name']), row, 1)
                    row += 1

                if 'Mode' in redundancy:
                    redundancy_layout.addWidget(QLabel("Mode:"), row, 0)
                    redundancy_layout.addWidget(QLabel(redundancy['Mode']), row, 1)
                    row += 1

                if 'MaxNumSupported' in redundancy:
                    redundancy_layout.addWidget(QLabel("Max Supported:"), row, 0)
                    redundancy_layout.addWidget(QLabel(str(redundancy['MaxNumSupported'])), row, 1)
                    row += 1

                if 'MinNumNeeded' in redundancy:
                    redundancy_layout.addWidget(QLabel("Min Needed:"), row, 0)
                    redundancy_layout.addWidget(QLabel(str(redundancy['MinNumNeeded'])), row, 1)
                    row += 1

                if 'Status' in redundancy:
                    status = redundancy['Status']
                    health = status.get('Health', 'Unknown')
                    state = status.get('State', 'Unknown')

                    redundancy_layout.addWidget(QLabel("Health:"), row, 0)
                    health_label = QLabel(health)

                    # Set color based on health
                    if health == 'OK':
                        health_label.setStyleSheet("color: green;")
                    elif health == 'Warning':
                        health_label.setStyleSheet("color: orange;")
                    elif health == 'Critical':
                        health_label.setStyleSheet("color: red;")

                    redundancy_layout.addWidget(health_label, row, 1)
                    row += 1

                    redundancy_layout.addWidget(QLabel("State:"), row, 0)
                    redundancy_layout.addWidget(QLabel(state), row, 1)
                    row += 1

                section_layout.addWidget(redundancy_widget)

            self.content_layout.insertWidget(2, redundancy_section)
