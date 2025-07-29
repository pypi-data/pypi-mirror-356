from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
                             QTableWidgetItem, QPushButton, QComboBox, QLabel,
                             QMessageBox, QHeaderView, QSplitter, QTextEdit)
from PyQt6.QtCore import Qt, QDateTime
from PyQt6.QtGui import QColor, QBrush
from typing import Dict, Any, List, Optional
import json
from greenfish.utils.logger import logger

class LogWidget(QWidget):
    """Widget for viewing and managing system logs."""

    def __init__(self, redfish_client=None, parent=None):
        super().__init__(parent)
        self.redfish_client = redfish_client
        self.current_resource_type = "Systems"
        self.current_resource_id = "1"
        self.current_log_service = "Log"
        self.log_services = []

        # Create layout
        layout = QVBoxLayout(self)

        # Create controls
        controls_layout = QHBoxLayout()

        # Resource type selector
        resource_type_layout = QHBoxLayout()
        resource_type_label = QLabel("Resource Type:")
        self.resource_type_combo = QComboBox()
        self.resource_type_combo.addItems(["Systems", "Managers", "Chassis"])
        self.resource_type_combo.currentTextChanged.connect(self.on_resource_type_changed)
        resource_type_layout.addWidget(resource_type_label)
        resource_type_layout.addWidget(self.resource_type_combo)
        controls_layout.addLayout(resource_type_layout)

        # Resource ID selector
        resource_id_layout = QHBoxLayout()
        resource_id_label = QLabel("Resource ID:")
        self.resource_id_combo = QComboBox()
        self.resource_id_combo.addItem("1")
        self.resource_id_combo.currentTextChanged.connect(self.on_resource_id_changed)
        resource_id_layout.addWidget(resource_id_label)
        resource_id_layout.addWidget(self.resource_id_combo)
        controls_layout.addLayout(resource_id_layout)

        # Log service selector
        log_service_layout = QHBoxLayout()
        log_service_label = QLabel("Log Service:")
        self.log_service_combo = QComboBox()
        self.log_service_combo.currentTextChanged.connect(self.on_log_service_changed)
        log_service_layout.addWidget(log_service_label)
        log_service_layout.addWidget(self.log_service_combo)
        controls_layout.addLayout(log_service_layout)

        controls_layout.addStretch()

        # Clear logs button
        self.clear_button = QPushButton("Clear Logs")
        self.clear_button.clicked.connect(self.clear_logs)
        controls_layout.addWidget(self.clear_button)

        # Refresh button
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh_logs)
        controls_layout.addWidget(self.refresh_button)

        layout.addLayout(controls_layout)

        # Create splitter for log table and details
        splitter = QSplitter(Qt.Orientation.Vertical)

        # Create log table
        self.log_table = QTableWidget()
        self.log_table.setColumnCount(5)
        self.log_table.setHorizontalHeaderLabels(["ID", "Severity", "Message", "Created", "Entry Type"])
        self.log_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.log_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.log_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.log_table.verticalHeader().setVisible(False)
        self.log_table.setAlternatingRowColors(True)
        self.log_table.itemSelectionChanged.connect(self.on_log_selected)
        splitter.addWidget(self.log_table)

        # Create log details view
        self.details_view = QTextEdit()
        self.details_view.setReadOnly(True)
        splitter.addWidget(self.details_view)

        # Set initial splitter sizes
        splitter.setSizes([400, 200])
        layout.addWidget(splitter)

        # Apply styling
        self.setStyleSheet("""
            QWidget {
                background-color: rgb(255, 255, 220);
            }
            QTableWidget {
                background-color: white;
                alternate-background-color: rgb(250, 250, 240);
            }
            QPushButton {
                padding: 5px 15px;
                background-color: rgb(200, 200, 180);
                border: 1px solid #CCCCCC;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: rgb(180, 180, 160);
            }
            QTextEdit {
                background-color: white;
                font-family: monospace;
            }
        """)

    def set_redfish_client(self, client):
        """Set the Redfish client and refresh logs."""
        self.redfish_client = client
        self.populate_log_services()
        self.refresh_logs()

    def populate_log_services(self):
        """Populate available log services."""
        if not self.redfish_client:
            return

        try:
            # Get available log services
            self.log_services = self.redfish_client.get_available_log_services(
                self.current_resource_type,
                self.current_resource_id
            )

            # Update log service combo
            self.log_service_combo.clear()
            for service in self.log_services:
                service_id = service.get("Id", "")
                if service_id:
                    self.log_service_combo.addItem(service_id)

            # Set default if available
            if self.log_service_combo.count() > 0:
                self.current_log_service = self.log_service_combo.itemText(0)
            else:
                self.current_log_service = "Log"  # Default

        except Exception as e:
            logger.error(f"Failed to populate log services: {str(e)}")
            QMessageBox.critical(self, "Error", f"Failed to get log services: {str(e)}")

    def refresh_logs(self):
        """Refresh log entries."""
        if not self.redfish_client:
            return

        try:
            # Clear current logs
            self.log_table.setRowCount(0)
            self.details_view.clear()

            # Get log entries
            entries = self.redfish_client.get_log_entries(
                self.current_resource_type,
                self.current_resource_id,
                self.current_log_service
            )

            # Populate table
            self.log_table.setRowCount(len(entries))
            for row, entry in enumerate(entries):
                # Extract entry ID
                entry_id = entry.get("Id", "")
                self.log_table.setItem(row, 0, QTableWidgetItem(entry_id))

                # Extract severity and set color
                severity = entry.get("Severity", "")
                severity_item = QTableWidgetItem(severity)
                if severity == "Critical":
                    severity_item.setForeground(QBrush(QColor(255, 0, 0)))  # Red
                elif severity == "Warning":
                    severity_item.setForeground(QBrush(QColor(255, 165, 0)))  # Orange
                self.log_table.setItem(row, 1, severity_item)

                # Extract message
                message = entry.get("Message", "")
                self.log_table.setItem(row, 2, QTableWidgetItem(message))

                # Extract created time
                created = entry.get("Created", "")
                self.log_table.setItem(row, 3, QTableWidgetItem(created))

                # Extract entry type
                entry_type = entry.get("EntryType", "")
                self.log_table.setItem(row, 4, QTableWidgetItem(entry_type))

            # Adjust column widths
            self.log_table.resizeColumnsToContents()
            self.log_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)

            logger.success("Log entries refreshed successfully")

        except Exception as e:
            logger.error(f"Failed to refresh logs: {str(e)}")
            QMessageBox.critical(self, "Error", f"Failed to get log entries: {str(e)}")

    def on_log_selected(self):
        """Handle log entry selection."""
        selected_rows = self.log_table.selectedItems()
        if not selected_rows:
            self.details_view.clear()
            return

        # Get the selected row
        row = self.log_table.currentRow()
        if row < 0:
            return

        # Get entry ID
        entry_id = self.log_table.item(row, 0).text()

        try:
            # Get full entry details
            entry = self.redfish_client.get_log_entry(
                entry_id,
                self.current_resource_type,
                self.current_resource_id,
                self.current_log_service
            )

            # Format JSON for display
            formatted_json = json.dumps(entry, indent=4)
            self.details_view.setText(formatted_json)

        except Exception as e:
            logger.error(f"Failed to get log entry details: {str(e)}")
            self.details_view.setText(f"Error retrieving details: {str(e)}")

    def clear_logs(self):
        """Clear all logs in the current log service."""
        if not self.redfish_client:
            return

        # Confirm action
        confirm = QMessageBox.question(
            self,
            "Confirm Clear Logs",
            f"Are you sure you want to clear all logs in the {self.current_log_service} service?\n\n"
            "This action cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm != QMessageBox.StandardButton.Yes:
            return

        try:
            # Clear logs
            self.redfish_client.clear_logs(
                self.current_resource_type,
                self.current_resource_id,
                self.current_log_service
            )

            # Refresh logs
            self.refresh_logs()

            QMessageBox.information(
                self,
                "Logs Cleared",
                "Logs have been cleared successfully."
            )

        except Exception as e:
            logger.error(f"Failed to clear logs: {str(e)}")
            QMessageBox.critical(self, "Error", f"Failed to clear logs: {str(e)}")

    def on_resource_type_changed(self, resource_type):
        """Handle resource type change."""
        self.current_resource_type = resource_type
        self.populate_log_services()
        self.refresh_logs()

    def on_resource_id_changed(self, resource_id):
        """Handle resource ID change."""
        self.current_resource_id = resource_id
        self.populate_log_services()
        self.refresh_logs()

    def on_log_service_changed(self, log_service):
        """Handle log service change."""
        self.current_log_service = log_service
        self.refresh_logs()
