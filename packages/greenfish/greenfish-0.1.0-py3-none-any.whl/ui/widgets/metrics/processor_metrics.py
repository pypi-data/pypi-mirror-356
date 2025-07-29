from PyQt6.QtWidgets import QLabel, QGridLayout, QWidget, QProgressBar
from PyQt6.QtCore import Qt

from greenfish.ui.widgets.metrics.base_panel import BaseMetricsPanel
from greenfish.utils.logger import Logger


class ProcessorMetricsPanel(BaseMetricsPanel):
    """Panel for displaying processor metrics"""

    def __init__(self, parent=None):
        super().__init__(parent)

    def refresh(self):
        """Refresh processor metrics data"""
        if not self.client or not self.resource_id:
            self.show_error("No Redfish client or system ID available")
            return

        self.show_loading()
        self.clear_content()

        try:
            # Get system info from the client
            system_data = self.client.get_system(self.resource_id)
            if not system_data or 'Processors' not in system_data:
                self.show_error("No processor data available")
                return

            # Get the processors collection
            processors_url = system_data['Processors']['@odata.id']
            processors_data = self.client.get_resource(processors_url)

            if not processors_data or 'Members' not in processors_data:
                self.show_error("No processor members found")
                return

            # Get detailed information for each processor
            processors = []
            for member in processors_data['Members']:
                processor_url = member['@odata.id']
                processor_data = self.client.get_resource(processor_url)
                if processor_data:
                    processors.append(processor_data)

            if not processors:
                self.show_error("No processor details available")
                return

            self.data = processors
            self.hide_status()
            self.display_processor_data()

        except Exception as e:
            Logger.error(f"Failed to get processor metrics: {str(e)}")
            self.show_error(str(e))

    def display_processor_data(self):
        """Display the processor data in the panel"""
        if not self.data:
            return

        for i, processor in enumerate(self.data):
            # Create a section for each processor
            proc_section, section_layout = self.create_section(f"Processor {i+1}")

            proc_widget = QWidget()
            proc_layout = QGridLayout(proc_widget)
            proc_layout.setContentsMargins(10, 5, 10, 5)

            row = 0

            # Basic information
            if 'Model' in processor:
                proc_layout.addWidget(QLabel("Model:"), row, 0)
                proc_layout.addWidget(QLabel(processor['Model']), row, 1)
                row += 1

            if 'Manufacturer' in processor:
                proc_layout.addWidget(QLabel("Manufacturer:"), row, 0)
                proc_layout.addWidget(QLabel(processor['Manufacturer']), row, 1)
                row += 1

            if 'ProcessorType' in processor:
                proc_layout.addWidget(QLabel("Type:"), row, 0)
                proc_layout.addWidget(QLabel(processor['ProcessorType']), row, 1)
                row += 1

            if 'ProcessorArchitecture' in processor:
                proc_layout.addWidget(QLabel("Architecture:"), row, 0)
                proc_layout.addWidget(QLabel(processor['ProcessorArchitecture']), row, 1)
                row += 1

            if 'InstructionSet' in processor:
                proc_layout.addWidget(QLabel("Instruction Set:"), row, 0)
                proc_layout.addWidget(QLabel(processor['InstructionSet']), row, 1)
                row += 1

            # Core information
            if 'TotalCores' in processor:
                proc_layout.addWidget(QLabel("Total Cores:"), row, 0)
                proc_layout.addWidget(QLabel(str(processor['TotalCores'])), row, 1)
                row += 1

            if 'TotalThreads' in processor:
                proc_layout.addWidget(QLabel("Total Threads:"), row, 0)
                proc_layout.addWidget(QLabel(str(processor['TotalThreads'])), row, 1)
                row += 1

            # Frequency information
            if 'MaxSpeedMHz' in processor:
                proc_layout.addWidget(QLabel("Max Speed:"), row, 0)
                proc_layout.addWidget(QLabel(f"{processor['MaxSpeedMHz']} MHz"), row, 1)
                row += 1

            # Status
            if 'Status' in processor:
                status = processor['Status']
                health = status.get('Health', 'Unknown')
                state = status.get('State', 'Unknown')

                proc_layout.addWidget(QLabel("Health:"), row, 0)
                health_label = QLabel(health)

                # Set color based on health
                if health == 'OK':
                    health_label.setStyleSheet("color: green;")
                elif health == 'Warning':
                    health_label.setStyleSheet("color: orange;")
                elif health == 'Critical':
                    health_label.setStyleSheet("color: red;")

                proc_layout.addWidget(health_label, row, 1)
                row += 1

                proc_layout.addWidget(QLabel("State:"), row, 0)
                proc_layout.addWidget(QLabel(state), row, 1)
                row += 1

            # Additional processor metrics if available
            if 'ProcessorMetrics' in processor and '@odata.id' in processor['ProcessorMetrics']:
                try:
                    metrics_url = processor['ProcessorMetrics']['@odata.id']
                    metrics_data = self.client.get_resource(metrics_url)

                    if metrics_data:
                        # Add a separator
                        separator = QWidget()
                        separator.setFixedHeight(1)
                        separator.setStyleSheet("background-color: #cccccc;")
                        proc_layout.addWidget(separator, row, 0, 1, 2)
                        row += 1

                        metrics_title = QLabel("Processor Metrics")
                        metrics_title.setStyleSheet("font-weight: bold;")
                        proc_layout.addWidget(metrics_title, row, 0, 1, 2)
                        row += 1

                        # CPU utilization
                        if 'AverageFrequencyMHz' in metrics_data:
                            proc_layout.addWidget(QLabel("Average Frequency:"), row, 0)
                            proc_layout.addWidget(QLabel(f"{metrics_data['AverageFrequencyMHz']} MHz"), row, 1)
                            row += 1

                        if 'ConsumedPowerWatt' in metrics_data:
                            proc_layout.addWidget(QLabel("Power Consumption:"), row, 0)
                            proc_layout.addWidget(QLabel(f"{metrics_data['ConsumedPowerWatt']} Watts"), row, 1)
                            row += 1

                        if 'ThrottlingCelsius' in metrics_data:
                            proc_layout.addWidget(QLabel("Throttling Temp:"), row, 0)
                            proc_layout.addWidget(QLabel(f"{metrics_data['ThrottlingCelsius']}°C"), row, 1)
                            row += 1

                        if 'TemperatureCelsius' in metrics_data:
                            proc_layout.addWidget(QLabel("Temperature:"), row, 0)
                            temp_value = QLabel(f"{metrics_data['TemperatureCelsius']}°C")
                            proc_layout.addWidget(temp_value, row, 1)
                            row += 1

                        # CPU utilization
                        if 'CPUUtilization' in metrics_data:
                            utilization = metrics_data['CPUUtilization']

                            if 'PercentProcessorIdle' in utilization:
                                idle = utilization['PercentProcessorIdle']
                                used = 100 - idle

                                proc_layout.addWidget(QLabel("CPU Utilization:"), row, 0)
                                proc_layout.addWidget(QLabel(f"{used:.1f}%"), row, 1)
                                row += 1

                                # Add a progress bar for utilization
                                progress = QProgressBar()
                                progress.setMinimum(0)
                                progress.setMaximum(100)
                                progress.setValue(int(used))

                                # Set color based on utilization
                                if used > 90:
                                    progress.setStyleSheet("QProgressBar::chunk { background-color: red; }")
                                elif used > 70:
                                    progress.setStyleSheet("QProgressBar::chunk { background-color: orange; }")
                                else:
                                    progress.setStyleSheet("QProgressBar::chunk { background-color: green; }")

                                proc_layout.addWidget(progress, row, 0, 1, 2)
                                row += 1

                except Exception as e:
                    Logger.error(f"Failed to get processor metrics data: {str(e)}")

            section_layout.addWidget(proc_widget)
            self.content_layout.insertWidget(i, proc_section)
