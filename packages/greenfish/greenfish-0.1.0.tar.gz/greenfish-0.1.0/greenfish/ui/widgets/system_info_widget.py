from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QTreeWidget, QTreeWidgetItem, QGroupBox)
from PyQt6.QtCore import Qt
from typing import Dict, Any

class SystemInfoWidget(QWidget):
    """Widget for displaying system information from Redfish."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        """Setup the user interface."""
        layout = QVBoxLayout(self)

        # System overview group
        overview_group = QGroupBox("System Overview")
        overview_layout = QVBoxLayout(overview_group)

        # System info labels
        self.model_label = QLabel("Model: ")
        self.manufacturer_label = QLabel("Manufacturer: ")
        self.serial_label = QLabel("Serial Number: ")
        self.power_state_label = QLabel("Power State: ")

        overview_layout.addWidget(self.model_label)
        overview_layout.addWidget(self.manufacturer_label)
        overview_layout.addWidget(self.serial_label)
        overview_layout.addWidget(self.power_state_label)

        # Power control buttons
        power_layout = QHBoxLayout()
        self.power_on_button = QPushButton("Power On")
        self.power_off_button = QPushButton("Power Off")
        self.reset_button = QPushButton("Reset")
        power_layout.addWidget(self.power_on_button)
        power_layout.addWidget(self.power_off_button)
        power_layout.addWidget(self.reset_button)
        overview_layout.addLayout(power_layout)

        layout.addWidget(overview_group)

        # Hardware details tree
        details_group = QGroupBox("Hardware Details")
        details_layout = QVBoxLayout(details_group)

        self.details_tree = QTreeWidget()
        self.details_tree.setHeaderLabels(["Property", "Value"])
        self.details_tree.setColumnWidth(0, 200)
        details_layout.addWidget(self.details_tree)

        layout.addWidget(details_group)

        # Apply solid color styling
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
            QPushButton {
                padding: 5px 15px;
                background-color: rgb(200, 200, 180);
                border: 1px solid #CCCCCC;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: rgb(180, 180, 160);
            }
            QTreeWidget {
                background-color: rgb(255, 255, 255);
                border: 1px solid #CCCCCC;
                border-radius: 3px;
            }
            QTreeWidget::item {
                padding: 2px;
            }
        """)

    def update_system_info(self, system_data: Dict[str, Any]):
        """Update the widget with system information."""
        # Update overview labels
        self.model_label.setText(f"Model: {system_data.get('Model', 'N/A')}")
        self.manufacturer_label.setText(f"Manufacturer: {system_data.get('Manufacturer', 'N/A')}")
        self.serial_label.setText(f"Serial Number: {system_data.get('SerialNumber', 'N/A')}")
        self.power_state_label.setText(f"Power State: {system_data.get('PowerState', 'N/A')}")

        # Update hardware details tree
        self.details_tree.clear()

        # Add processor information
        if 'Processors' in system_data:
            processor_item = QTreeWidgetItem(self.details_tree, ["Processors"])
            for proc in system_data['Processors'].get('Members', []):
                proc_item = QTreeWidgetItem(processor_item, [
                    f"Processor {proc.get('Id', 'N/A')}",
                    f"{proc.get('Model', 'N/A')} - {proc.get('TotalCores', 'N/A')} cores"
                ])

        # Add memory information
        if 'Memory' in system_data:
            memory_item = QTreeWidgetItem(self.details_tree, ["Memory"])
            for mem in system_data['Memory'].get('Members', []):
                mem_item = QTreeWidgetItem(memory_item, [
                    f"Memory {mem.get('Id', 'N/A')}",
                    f"{mem.get('CapacityMiB', 'N/A')} MiB - {mem.get('MemoryType', 'N/A')}"
                ])

        # Add storage information
        if 'Storage' in system_data:
            storage_item = QTreeWidgetItem(self.details_tree, ["Storage"])
            for storage in system_data['Storage'].get('Members', []):
                storage_item = QTreeWidgetItem(storage_item, [
                    f"Storage {storage.get('Id', 'N/A')}",
                    f"{storage.get('Model', 'N/A')}"
                ])

        # Expand all items
        self.details_tree.expandAll()
