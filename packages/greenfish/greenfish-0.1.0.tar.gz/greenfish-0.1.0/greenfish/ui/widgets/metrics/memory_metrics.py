from PyQt6.QtWidgets import QLabel, QGridLayout, QWidget, QProgressBar
from PyQt6.QtCore import Qt

from greenfish.ui.widgets.metrics.base_panel import BaseMetricsPanel
from greenfish.utils.logger import Logger


class MemoryMetricsPanel(BaseMetricsPanel):
    """Panel for displaying memory metrics"""

    def __init__(self, parent=None):
        super().__init__(parent)

    def refresh(self):
        """Refresh memory metrics data"""
        if not self.client or not self.resource_id:
            self.show_error("No Redfish client or system ID available")
            return

        self.show_loading()
        self.clear_content()

        try:
            # Get system info from the client
            system_data = self.client.get_system(self.resource_id)
            if not system_data or 'Memory' not in system_data:
                self.show_error("No memory data available")
                return

            # Get the memory collection
            memory_url = system_data['Memory']['@odata.id']
            memory_data = self.client.get_resource(memory_url)

            if not memory_data or 'Members' not in memory_data:
                self.show_error("No memory members found")
                return

            # Get detailed information for each memory module
            memory_modules = []
            for member in memory_data['Members']:
                memory_url = member['@odata.id']
                memory_module = self.client.get_resource(memory_url)
                if memory_module:
                    memory_modules.append(memory_module)

            if not memory_modules:
                self.show_error("No memory module details available")
                return

            self.data = memory_modules
            self.hide_status()
            self.display_memory_data()

            # Also get system memory summary if available
            self.display_memory_summary(system_data)

        except Exception as e:
            Logger.error(f"Failed to get memory metrics: {str(e)}")
            self.show_error(str(e))

    def display_memory_summary(self, system_data):
        """Display memory summary information"""
        if not system_data or 'MemorySummary' not in system_data:
            return

        summary = system_data['MemorySummary']
        if not summary:
            return

        # Create a section for memory summary
        summary_section, section_layout = self.create_section("Memory Summary")

        summary_widget = QWidget()
        summary_layout = QGridLayout(summary_widget)
        summary_layout.setContentsMargins(10, 5, 10, 5)

        row = 0

        # Total system memory
        if 'TotalSystemMemoryGiB' in summary:
            summary_layout.addWidget(QLabel("Total System Memory:"), row, 0)
            summary_layout.addWidget(QLabel(f"{summary['TotalSystemMemoryGiB']} GiB"), row, 1)
            row += 1

        # Memory status
        if 'Status' in summary:
            status = summary['Status']
            health = status.get('Health', 'Unknown')
            state = status.get('State', 'Unknown')

            summary_layout.addWidget(QLabel("Health:"), row, 0)
            health_label = QLabel(health)

            # Set color based on health
            if health == 'OK':
                health_label.setStyleSheet("color: green;")
            elif health == 'Warning':
                health_label.setStyleSheet("color: orange;")
            elif health == 'Critical':
                health_label.setStyleSheet("color: red;")

            summary_layout.addWidget(health_label, row, 1)
            row += 1

            summary_layout.addWidget(QLabel("State:"), row, 0)
            summary_layout.addWidget(QLabel(state), row, 1)
            row += 1

        section_layout.addWidget(summary_widget)
        self.content_layout.insertWidget(0, summary_section)

    def display_memory_data(self):
        """Display the memory module data in the panel"""
        if not self.data:
            return

        # Create a section for memory modules
        modules_section, section_layout = self.create_section("Memory Modules")

        for i, module in enumerate(self.data):
            module_widget = QWidget()
            module_layout = QGridLayout(module_widget)
            module_layout.setContentsMargins(10, 5, 10, 5)

            # Add title for this memory module
            name = module.get('Name', f"Memory Module {i+1}")
            title = QLabel(name)
            title.setStyleSheet("font-weight: bold;")
            module_layout.addWidget(title, 0, 0, 1, 2)

            row = 1

            # Basic information
            if 'CapacityMiB' in module:
                capacity_gib = module['CapacityMiB'] / 1024
                module_layout.addWidget(QLabel("Capacity:"), row, 0)
                module_layout.addWidget(QLabel(f"{capacity_gib:.1f} GiB"), row, 1)
                row += 1

            if 'OperatingSpeedMhz' in module:
                module_layout.addWidget(QLabel("Speed:"), row, 0)
                module_layout.addWidget(QLabel(f"{module['OperatingSpeedMhz']} MHz"), row, 1)
                row += 1

            if 'MemoryDeviceType' in module:
                module_layout.addWidget(QLabel("Type:"), row, 0)
                module_layout.addWidget(QLabel(module['MemoryDeviceType']), row, 1)
                row += 1

            if 'DataWidthBits' in module:
                module_layout.addWidget(QLabel("Data Width:"), row, 0)
                module_layout.addWidget(QLabel(f"{module['DataWidthBits']} bits"), row, 1)
                row += 1

            if 'Manufacturer' in module:
                module_layout.addWidget(QLabel("Manufacturer:"), row, 0)
                module_layout.addWidget(QLabel(module['Manufacturer']), row, 1)
                row += 1

            if 'SerialNumber' in module:
                module_layout.addWidget(QLabel("Serial Number:"), row, 0)
                module_layout.addWidget(QLabel(module['SerialNumber']), row, 1)
                row += 1

            if 'PartNumber' in module:
                module_layout.addWidget(QLabel("Part Number:"), row, 0)
                module_layout.addWidget(QLabel(module['PartNumber']), row, 1)
                row += 1

            # Status
            if 'Status' in module:
                status = module['Status']
                health = status.get('Health', 'Unknown')
                state = status.get('State', 'Unknown')

                module_layout.addWidget(QLabel("Health:"), row, 0)
                health_label = QLabel(health)

                # Set color based on health
                if health == 'OK':
                    health_label.setStyleSheet("color: green;")
                elif health == 'Warning':
                    health_label.setStyleSheet("color: orange;")
                elif health == 'Critical':
                    health_label.setStyleSheet("color: red;")

                module_layout.addWidget(health_label, row, 1)
                row += 1

                module_layout.addWidget(QLabel("State:"), row, 0)
                module_layout.addWidget(QLabel(state), row, 1)
                row += 1

            # Additional memory metrics if available
            if 'MemoryMetrics' in module and '@odata.id' in module['MemoryMetrics']:
                try:
                    metrics_url = module['MemoryMetrics']['@odata.id']
                    metrics_data = self.client.get_resource(metrics_url)

                    if metrics_data:
                        # Add a separator
                        separator = QWidget()
                        separator.setFixedHeight(1)
                        separator.setStyleSheet("background-color: #cccccc;")
                        module_layout.addWidget(separator, row, 0, 1, 2)
                        row += 1

                        metrics_title = QLabel("Memory Metrics")
                        metrics_title.setStyleSheet("font-weight: bold;")
                        module_layout.addWidget(metrics_title, row, 0, 1, 2)
                        row += 1

                        # Memory bandwidth
                        if 'BandwidthPercent' in metrics_data:
                            module_layout.addWidget(QLabel("Bandwidth Usage:"), row, 0)
                            module_layout.addWidget(QLabel(f"{metrics_data['BandwidthPercent']}%"), row, 1)
                            row += 1

                            # Add a progress bar for bandwidth
                            progress = QProgressBar()
                            progress.setMinimum(0)
                            progress.setMaximum(100)
                            progress.setValue(int(metrics_data['BandwidthPercent']))

                            # Set color based on utilization
                            if metrics_data['BandwidthPercent'] > 90:
                                progress.setStyleSheet("QProgressBar::chunk { background-color: red; }")
                            elif metrics_data['BandwidthPercent'] > 70:
                                progress.setStyleSheet("QProgressBar::chunk { background-color: orange; }")
                            else:
                                progress.setStyleSheet("QProgressBar::chunk { background-color: green; }")

                            module_layout.addWidget(progress, row, 0, 1, 2)
                            row += 1

                        # Memory temperature
                        if 'TemperatureCelsius' in metrics_data:
                            module_layout.addWidget(QLabel("Temperature:"), row, 0)
                            module_layout.addWidget(QLabel(f"{metrics_data['TemperatureCelsius']}°C"), row, 1)
                            row += 1

                        # Error information
                        if 'CurrentPeriod' in metrics_data:
                            period = metrics_data['CurrentPeriod']

                            if 'CorrectedECCErrorCount' in period:
                                module_layout.addWidget(QLabel("Corrected ECC Errors:"), row, 0)
                                module_layout.addWidget(QLabel(str(period['CorrectedECCErrorCount'])), row, 1)
                                row += 1

                            if 'UncorrectedECCErrorCount' in period:
                                module_layout.addWidget(QLabel("Uncorrected ECC Errors:"), row, 0)
                                error_label = QLabel(str(period['UncorrectedECCErrorCount']))

                                # Highlight uncorrected errors
                                if period['UncorrectedECCErrorCount'] > 0:
                                    error_label.setStyleSheet("color: red; font-weight: bold;")

                                module_layout.addWidget(error_label, row, 1)
                                row += 1

                except Exception as e:
                    Logger.error(f"Failed to get memory metrics data: {str(e)}")

            section_layout.addWidget(module_widget)

            # Add separator if not the last item
            if i < len(self.data) - 1:
                separator = QWidget()
                separator.setFixedHeight(1)
                separator.setStyleSheet("background-color: #cccccc;")
                section_layout.addWidget(separator)

        self.content_layout.insertWidget(1, modules_section)
