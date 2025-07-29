from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
                             QPushButton, QDialog, QLabel, QLineEdit, QMessageBox, QComboBox)
from PyQt6.QtCore import Qt
from typing import Dict, Any, Optional
from greenfish.utils.logger import logger

class EventSubscriptionDialog(QDialog):
    """Dialog for creating a new event subscription."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("New Event Subscription")
        self.setMinimumWidth(400)
        layout = QVBoxLayout(self)

        # Destination input
        dest_layout = QHBoxLayout()
        dest_label = QLabel("Destination URL:")
        self.dest_input = QLineEdit()
        dest_layout.addWidget(dest_label)
        dest_layout.addWidget(self.dest_input)
        layout.addLayout(dest_layout)

        # Protocol selection
        proto_layout = QHBoxLayout()
        proto_label = QLabel("Protocol:")
        self.proto_combo = QComboBox()
        self.proto_combo.addItems(["Redfish", "SNMPv2c", "SNMPv3"])
        proto_layout.addWidget(proto_label)
        proto_layout.addWidget(self.proto_combo)
        layout.addLayout(proto_layout)

        # Event types input (comma separated)
        event_layout = QHBoxLayout()
        event_label = QLabel("Event Types (comma separated):")
        self.event_input = QLineEdit()
        event_layout.addWidget(event_label)
        event_layout.addWidget(self.event_input)
        layout.addLayout(event_layout)

        # Buttons
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Create")
        self.save_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

    def get_data(self) -> Dict[str, Any]:
        return {
            "Destination": self.dest_input.text().strip(),
            "Protocol": self.proto_combo.currentText(),
            "EventTypes": [e.strip() for e in self.event_input.text().split(",") if e.strip()]
        }

class EventSubscriptionWidget(QWidget):
    """Widget for managing Redfish event subscriptions."""
    def __init__(self, redfish_client=None, parent=None):
        super().__init__(parent)
        self.redfish_client = redfish_client
        layout = QVBoxLayout(self)

        # Toolbar
        toolbar = QHBoxLayout()
        self.add_button = QPushButton("Add Subscription")
        self.add_button.clicked.connect(self.add_subscription)
        toolbar.addWidget(self.add_button)
        self.delete_button = QPushButton("Delete Subscription")
        self.delete_button.clicked.connect(self.delete_subscription)
        toolbar.addWidget(self.delete_button)
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh_subscriptions)
        toolbar.addWidget(self.refresh_button)
        toolbar.addStretch()
        layout.addLayout(toolbar)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Destination", "Protocol", "Event Types"])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.verticalHeader().setVisible(False)
        layout.addWidget(self.table)

        self.setStyleSheet("""
            QWidget { background-color: rgb(255, 255, 220); }
            QTableWidget { background-color: white; }
            QPushButton {
                padding: 5px 15px;
                background-color: rgb(200, 200, 180);
                border: 1px solid #CCCCCC;
                border-radius: 3px;
            }
            QPushButton:hover { background-color: rgb(180, 180, 160); }
        """)

    def set_redfish_client(self, client):
        self.redfish_client = client
        self.refresh_subscriptions()

    def refresh_subscriptions(self):
        if not self.redfish_client:
            return
        try:
            subs = self.redfish_client.get_event_subscriptions()
            self.table.setRowCount(len(subs))
            for row, sub in enumerate(subs):
                self.table.setItem(row, 0, QTableWidgetItem(sub.get("Id", "")))
                self.table.setItem(row, 1, QTableWidgetItem(sub.get("Destination", "")))
                self.table.setItem(row, 2, QTableWidgetItem(sub.get("Protocol", "")))
                event_types = ", ".join(sub.get("EventTypes", []))
                self.table.setItem(row, 3, QTableWidgetItem(event_types))
            self.table.resizeColumnsToContents()
            logger.success("Event subscriptions refreshed successfully")
        except Exception as e:
            logger.error(f"Failed to refresh event subscriptions: {str(e)}")
            QMessageBox.critical(self, "Error", str(e))

    def add_subscription(self):
        if not self.redfish_client:
            return
        dialog = EventSubscriptionDialog(self)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return
        data = dialog.get_data()
        if not data["Destination"]:
            QMessageBox.warning(self, "Input Error", "Destination URL is required.")
            return
        try:
            self.redfish_client.create_event_subscription(
                destination=data["Destination"],
                event_types=data["EventTypes"],
                protocol=data["Protocol"]
            )
            self.refresh_subscriptions()
        except Exception as e:
            logger.error(f"Failed to add event subscription: {str(e)}")
            QMessageBox.critical(self, "Error", str(e))

    def delete_subscription(self):
        if not self.redfish_client:
            return
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Warning", "Please select a subscription to delete.")
            return
        sub_id = self.table.item(row, 0).text()
        confirm = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete subscription '{sub_id}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm != QMessageBox.StandardButton.Yes:
            return
        try:
            self.redfish_client.delete_event_subscription(sub_id)
            self.refresh_subscriptions()
        except Exception as e:
            logger.error(f"Failed to delete event subscription: {str(e)}")
            QMessageBox.critical(self, "Error", str(e))
