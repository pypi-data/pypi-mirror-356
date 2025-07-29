from PyQt6.QtWidgets import (QLabel, QGridLayout, QWidget, QVBoxLayout,
                             QComboBox, QPushButton, QTableWidget, QTableWidgetItem,
                             QHeaderView, QHBoxLayout)
from PyQt6.QtCore import Qt

from greenfish.ui.widgets.metrics.base_panel import BaseMetricsPanel
from greenfish.utils.logger import Logger


class TelemetryPanel(BaseMetricsPanel):
    """Panel for displaying telemetry data and metric reports"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.metric_reports = []
        self.report_definitions = []

    def refresh(self):
        """Refresh telemetry data"""
        if not self.client:
            self.show_error("No Redfish client available")
            return

        self.show_loading()
        self.clear_content()

        try:
            # Check if telemetry service is available
            telemetry_service = self.client.get_telemetry_service()
            if not telemetry_service:
                self.show_error("Telemetry service not available on this system")
                return

            # Get metric report definitions
            self.report_definitions = self.client.get_metric_report_definitions()
            if not self.report_definitions:
                self.show_error("No metric report definitions available")
                return

            # Get available metric reports
            self.metric_reports = self.client.get_metric_reports()
            if not self.metric_reports:
                self.show_error("No metric reports available")
                return

            self.hide_status()
            self.display_telemetry_data()

        except Exception as e:
            Logger.error(f"Failed to get telemetry data: {str(e)}")
            self.show_error(str(e))

    def display_telemetry_data(self):
        """Display the telemetry data in the panel"""
        if not self.metric_reports and not self.report_definitions:
            return

        # Create a section for metric report selection
        selection_section, selection_layout = self.create_section("Metric Reports")

        # Create a widget for report selection
        selection_widget = QWidget()
        selection_layout_inner = QHBoxLayout(selection_widget)
        selection_layout_inner.setContentsMargins(10, 5, 10, 5)

        # Create a dropdown for selecting reports
        self.report_combo = QComboBox()
        for report in self.metric_reports:
            if 'Id' in report and 'Name' in report:
                self.report_combo.addItem(report['Name'], report['Id'])

        # Add a refresh button
        refresh_button = QPushButton("View Report")
        refresh_button.clicked.connect(self.load_selected_report)

        selection_layout_inner.addWidget(QLabel("Select Report:"))
        selection_layout_inner.addWidget(self.report_combo, 1)
        selection_layout_inner.addWidget(refresh_button)

        selection_layout.addWidget(selection_widget)
        self.content_layout.insertWidget(0, selection_section)

        # Create a section for the report details
        self.report_section, self.report_layout = self.create_section("Report Details")

        # Add a placeholder message
        placeholder = QLabel("Select a report and click 'View Report' to view details")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.report_layout.addWidget(placeholder)

        self.content_layout.insertWidget(1, self.report_section)

        # Load the first report if available
        if self.report_combo.count() > 0:
            self.load_selected_report()

    def load_selected_report(self):
        """Load the selected metric report"""
        if self.report_combo.count() == 0:
            return

        # Clear the previous report content
        while self.report_layout.count():
            item = self.report_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Get the selected report ID
        report_id = self.report_combo.currentData()
        if not report_id:
            return

        try:
            # Get the report data
            report_data = self.client.get_metric_report(report_id)
            if not report_data:
                placeholder = QLabel(f"Failed to load report: {report_id}")
                placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.report_layout.addWidget(placeholder)
                return

            # Display the report metadata
            metadata_widget = QWidget()
            metadata_layout = QGridLayout(metadata_widget)
            metadata_layout.setContentsMargins(10, 5, 10, 5)

            row = 0

            if 'Id' in report_data:
                metadata_layout.addWidget(QLabel("ID:"), row, 0)
                metadata_layout.addWidget(QLabel(report_data['Id']), row, 1)
                row += 1

            if 'Name' in report_data:
                metadata_layout.addWidget(QLabel("Name:"), row, 0)
                metadata_layout.addWidget(QLabel(report_data['Name']), row, 1)
                row += 1

            if 'Description' in report_data:
                metadata_layout.addWidget(QLabel("Description:"), row, 0)
                metadata_layout.addWidget(QLabel(report_data['Description']), row, 1)
                row += 1

            if 'MetricReportDefinition' in report_data and '@odata.id' in report_data['MetricReportDefinition']:
                metadata_layout.addWidget(QLabel("Definition:"), row, 0)
                metadata_layout.addWidget(QLabel(report_data['MetricReportDefinition']['@odata.id'].split('/')[-1]), row, 1)
                row += 1

            if 'ReportingInterval' in report_data:
                metadata_layout.addWidget(QLabel("Reporting Interval:"), row, 0)
                metadata_layout.addWidget(QLabel(report_data['ReportingInterval']), row, 1)
                row += 1

            if 'Timestamp' in report_data:
                metadata_layout.addWidget(QLabel("Timestamp:"), row, 0)
                metadata_layout.addWidget(QLabel(report_data['Timestamp']), row, 1)
                row += 1

            self.report_layout.addWidget(metadata_widget)

            # Display the metric values
            if 'MetricValues' in report_data and report_data['MetricValues']:
                # Create a table for the metric values
                table_widget = QTableWidget()
                table_widget.setColumnCount(5)  # MetricId, MetricValue, Timestamp, MetricProperty, Status
                table_widget.setHorizontalHeaderLabels(["Metric ID", "Value", "Timestamp", "Property", "Status"])
                table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

                # Add rows for each metric value
                table_widget.setRowCount(len(report_data['MetricValues']))

                for i, metric in enumerate(report_data['MetricValues']):
                    # Metric ID
                    if 'MetricId' in metric:
                        table_widget.setItem(i, 0, QTableWidgetItem(metric['MetricId']))

                    # Metric Value
                    if 'MetricValue' in metric:
                        table_widget.setItem(i, 1, QTableWidgetItem(str(metric['MetricValue'])))

                    # Timestamp
                    if 'Timestamp' in metric:
                        table_widget.setItem(i, 2, QTableWidgetItem(metric['Timestamp']))

                    # Metric Property
                    if 'MetricProperty' in metric:
                        table_widget.setItem(i, 3, QTableWidgetItem(metric['MetricProperty']))

                    # Status
                    if 'Status' in metric:
                        status = metric['Status']
                        health = status.get('Health', 'Unknown')
                        state = status.get('State', 'Unknown')
                        status_text = f"{health} ({state})"
                        status_item = QTableWidgetItem(status_text)

                        # Set color based on health
                        if health == 'OK':
                            status_item.setForeground(Qt.GlobalColor.green)
                        elif health == 'Warning':
                            status_item.setForeground(Qt.GlobalColor.yellow)
                        elif health == 'Critical':
                            status_item.setForeground(Qt.GlobalColor.red)

                        table_widget.setItem(i, 4, status_item)

                self.report_layout.addWidget(table_widget)
            else:
                no_metrics = QLabel("No metric values available in this report")
                no_metrics.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.report_layout.addWidget(no_metrics)

        except Exception as e:
            Logger.error(f"Failed to load metric report: {str(e)}")
            error_label = QLabel(f"Error loading report: {str(e)}")
            error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            error_label.setStyleSheet("color: red;")
            self.report_layout.addWidget(error_label)
