from PyQt6.QtWidgets import QLabel, QGridLayout, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt

from greenfish.ui.widgets.metrics.base_panel import BaseMetricsPanel
from greenfish.utils.logger import Logger


class PowerMetricsPanel(BaseMetricsPanel):
    """Panel for displaying power metrics"""

    def __init__(self, parent=None):
        super().__init__(parent)

    def refresh(self):
        """Refresh power metrics data"""
        if not self.client or not self.resource_id:
            self.show_error("No Redfish client or chassis ID available")
            return

        self.show_loading()
        self.clear_content()

        try:
            # Get power metrics from the client
            power_data = self.client.get_power_metrics(self.resource_id)
            if not power_data:
                self.show_error("No power data available")
                return

            self.data = power_data
            self.hide_status()
            self.display_power_data()

        except Exception as e:
            Logger.error(f"Failed to get power metrics: {str(e)}")
            self.show_error(str(e))

    def display_power_data(self):
        """Display the power data in the panel"""
        if not self.data:
            return

        # Power Control section
        if 'PowerControl' in self.data and self.data['PowerControl']:
            power_control_section, section_layout = self.create_section("Power Control")

            for i, control in enumerate(self.data['PowerControl']):
                control_widget = QWidget()
                control_layout = QGridLayout(control_widget)
                control_layout.setContentsMargins(10, 5, 10, 5)

                row = 0

                # Add power control metrics
                if 'PowerConsumedWatts' in control:
                    control_layout.addWidget(QLabel("Power Consumed:"), row, 0)
                    control_layout.addWidget(QLabel(f"{control['PowerConsumedWatts']} Watts"), row, 1)
                    row += 1

                if 'PowerRequestedWatts' in control:
                    control_layout.addWidget(QLabel("Power Requested:"), row, 0)
                    control_layout.addWidget(QLabel(f"{control['PowerRequestedWatts']} Watts"), row, 1)
                    row += 1

                if 'PowerAvailableWatts' in control:
                    control_layout.addWidget(QLabel("Power Available:"), row, 0)
                    control_layout.addWidget(QLabel(f"{control['PowerAvailableWatts']} Watts"), row, 1)
                    row += 1

                if 'PowerCapacityWatts' in control:
                    control_layout.addWidget(QLabel("Power Capacity:"), row, 0)
                    control_layout.addWidget(QLabel(f"{control['PowerCapacityWatts']} Watts"), row, 1)
                    row += 1

                if 'PowerAllocatedWatts' in control:
                    control_layout.addWidget(QLabel("Power Allocated:"), row, 0)
                    control_layout.addWidget(QLabel(f"{control['PowerAllocatedWatts']} Watts"), row, 1)
                    row += 1

                # Power limits
                if 'PowerLimit' in control:
                    limit = control['PowerLimit']
                    control_layout.addWidget(QLabel("Power Limit:"), row, 0)
                    limit_value = f"{limit.get('LimitInWatts', 'N/A')} Watts"
                    control_layout.addWidget(QLabel(limit_value), row, 1)
                    row += 1

                # Power metrics
                if 'PowerMetrics' in control:
                    metrics = control['PowerMetrics']

                    if 'IntervalInMin' in metrics:
                        control_layout.addWidget(QLabel("Measurement Interval:"), row, 0)
                        control_layout.addWidget(QLabel(f"{metrics['IntervalInMin']} minutes"), row, 1)
                        row += 1

                    if 'MinConsumedWatts' in metrics:
                        control_layout.addWidget(QLabel("Min Consumed Power:"), row, 0)
                        control_layout.addWidget(QLabel(f"{metrics['MinConsumedWatts']} Watts"), row, 1)
                        row += 1

                    if 'MaxConsumedWatts' in metrics:
                        control_layout.addWidget(QLabel("Max Consumed Power:"), row, 0)
                        control_layout.addWidget(QLabel(f"{metrics['MaxConsumedWatts']} Watts"), row, 1)
                        row += 1

                    if 'AverageConsumedWatts' in metrics:
                        control_layout.addWidget(QLabel("Avg Consumed Power:"), row, 0)
                        control_layout.addWidget(QLabel(f"{metrics['AverageConsumedWatts']} Watts"), row, 1)
                        row += 1

                section_layout.addWidget(control_widget)

            self.content_layout.insertWidget(0, power_control_section)

        # Power Supplies section
        if 'PowerSupplies' in self.data and self.data['PowerSupplies']:
            supplies_section, section_layout = self.create_section("Power Supplies")

            for i, supply in enumerate(self.data['PowerSupplies']):
                supply_widget = QWidget()
                supply_layout = QGridLayout(supply_widget)
                supply_layout.setContentsMargins(10, 5, 10, 5)

                # Add title for this power supply
                name = supply.get('Name', f"Power Supply {i+1}")
                title = QLabel(name)
                title.setStyleSheet("font-weight: bold;")
                supply_layout.addWidget(title, 0, 0, 1, 2)

                row = 1

                # Add power supply metrics
                if 'PowerInputWatts' in supply:
                    supply_layout.addWidget(QLabel("Power Input:"), row, 0)
                    supply_layout.addWidget(QLabel(f"{supply['PowerInputWatts']} Watts"), row, 1)
                    row += 1

                if 'PowerOutputWatts' in supply:
                    supply_layout.addWidget(QLabel("Power Output:"), row, 0)
                    supply_layout.addWidget(QLabel(f"{supply['PowerOutputWatts']} Watts"), row, 1)
                    row += 1

                if 'PowerCapacityWatts' in supply:
                    supply_layout.addWidget(QLabel("Power Capacity:"), row, 0)
                    supply_layout.addWidget(QLabel(f"{supply['PowerCapacityWatts']} Watts"), row, 1)
                    row += 1

                if 'LineInputVoltage' in supply:
                    supply_layout.addWidget(QLabel("Input Voltage:"), row, 0)
                    supply_layout.addWidget(QLabel(f"{supply['LineInputVoltage']} V"), row, 1)
                    row += 1

                if 'EfficiencyPercent' in supply:
                    supply_layout.addWidget(QLabel("Efficiency:"), row, 0)
                    supply_layout.addWidget(QLabel(f"{supply['EfficiencyPercent']}%"), row, 1)
                    row += 1

                if 'Status' in supply:
                    status = supply['Status']
                    health = status.get('Health', 'Unknown')
                    state = status.get('State', 'Unknown')

                    supply_layout.addWidget(QLabel("Health:"), row, 0)
                    health_label = QLabel(health)

                    # Set color based on health
                    if health == 'OK':
                        health_label.setStyleSheet("color: green;")
                    elif health == 'Warning':
                        health_label.setStyleSheet("color: orange;")
                    elif health == 'Critical':
                        health_label.setStyleSheet("color: red;")

                    supply_layout.addWidget(health_label, row, 1)
                    row += 1

                    supply_layout.addWidget(QLabel("State:"), row, 0)
                    supply_layout.addWidget(QLabel(state), row, 1)
                    row += 1

                section_layout.addWidget(supply_widget)

                # Add separator if not the last item
                if i < len(self.data['PowerSupplies']) - 1:
                    separator = QWidget()
                    separator.setFixedHeight(1)
                    separator.setStyleSheet("background-color: #cccccc;")
                    section_layout.addWidget(separator)

            self.content_layout.insertWidget(1, supplies_section)

        # Redundancy section
        if 'Redundancy' in self.data and self.data['Redundancy']:
            redundancy_section, section_layout = self.create_section("Power Redundancy")

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
