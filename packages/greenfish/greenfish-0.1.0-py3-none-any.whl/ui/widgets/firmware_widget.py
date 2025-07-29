from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
                             QFileDialog, QMessageBox, QLineEdit, QGroupBox)
from PyQt6.QtCore import Qt
from typing import Dict, Any, List

class FirmwareWidget(QWidget):
    """Widget for managing firmware inventory and updates."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.firmware_data = {}
        self.selected_file = ""
        self.setup_ui()

    def setup_ui(self):
        """Setup the user interface."""
        main_layout = QVBoxLayout(self)

        # Firmware inventory group
        inventory_group = QGroupBox("Firmware Inventory")
        inventory_layout = QVBoxLayout(inventory_group)

        # Inventory table
        self.inventory_table = QTableWidget()
        self.inventory_table.setColumnCount(5)
        self.inventory_table.setHorizontalHeaderLabels(["Name", "Version", "Updated", "State", "Description"])
        self.inventory_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.inventory_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.inventory_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        inventory_layout.addWidget(self.inventory_table)

        # Refresh button
        refresh_button = QPushButton("Refresh Inventory")
        refresh_button.clicked.connect(self.refresh_clicked)
        inventory_layout.addWidget(refresh_button)

        main_layout.addWidget(inventory_group)

        # Firmware update group
        update_group = QGroupBox("Firmware Update")
        update_layout = QVBoxLayout(update_group)

        # Update using local file
        local_update_group = QGroupBox("Update from Local File")
        local_update_layout = QVBoxLayout(local_update_group)

        # File selection
        file_layout = QHBoxLayout()
        self.file_path = QLineEdit()
        self.file_path.setReadOnly(True)
        self.file_path.setPlaceholderText("No file selected")

        browse_button = QPushButton("Browse...")
        browse_button.clicked.connect(self.browse_file)

        file_layout.addWidget(self.file_path)
        file_layout.addWidget(browse_button)
        local_update_layout.addLayout(file_layout)

        # Upload button
        self.upload_button = QPushButton("Upload and Update")
        self.upload_button.setEnabled(False)
        self.upload_button.clicked.connect(self.upload_clicked)
        local_update_layout.addWidget(self.upload_button)

        update_layout.addWidget(local_update_group)

        # Update using URI
        uri_update_group = QGroupBox("Update from URI")
        uri_update_layout = QVBoxLayout(uri_update_group)

        # URI input
        uri_layout = QHBoxLayout()
        self.uri_input = QLineEdit()
        self.uri_input.setPlaceholderText("Enter firmware image URI (http://, ftp://, etc.)")
        uri_layout.addWidget(self.uri_input)
        uri_update_layout.addLayout(uri_layout)

        # Update button
        self.update_button = QPushButton("Update from URI")
        self.update_button.clicked.connect(self.update_from_uri_clicked)
        uri_update_layout.addWidget(self.update_button)

        update_layout.addWidget(uri_update_group)

        main_layout.addWidget(update_group)

        # Status label
        self.status_label = QLabel("No firmware data loaded")
        main_layout.addWidget(self.status_label)

        # Set styling
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
            QTableWidget {
                background-color: rgb(255, 255, 255);
                border: 1px solid #CCCCCC;
                border-radius: 3px;
            }
            QTableWidget::item {
                padding: 4px;
            }
            QHeaderView::section {
                background-color: rgb(240, 240, 220);
                padding: 4px;
                border: 1px solid #CCCCCC;
                border-left: none;
                border-top: none;
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
            QLineEdit {
                padding: 5px;
                border: 1px solid #CCCCCC;
                border-radius: 3px;
                background-color: rgb(255, 255, 255);
            }
        """)

    def load_firmware_data(self, firmware_data: Dict[str, Any]):
        """Load firmware data into the widget."""
        self.firmware_data = firmware_data
        self.update_inventory_table()
        self.status_label.setText(f"Loaded firmware inventory ({len(firmware_data.get('items', []))} items)")

    def update_inventory_table(self):
        """Update the inventory table with firmware data."""
        items = self.firmware_data.get("items", [])

        # Update inventory table
        self.inventory_table.setRowCount(len(items))

        for row, item in enumerate(items):
            # Name
            name_item = QTableWidgetItem(item.get("Name", "Unknown"))
            name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.inventory_table.setItem(row, 0, name_item)

            # Version
            version_item = QTableWidgetItem(item.get("Version", "Unknown"))
            version_item.setFlags(version_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.inventory_table.setItem(row, 1, version_item)

            # Last updated
            updated_item = QTableWidgetItem(item.get("ReleaseDate", "Unknown"))
            updated_item.setFlags(updated_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.inventory_table.setItem(row, 2, updated_item)

            # State
            state = "Unknown"
            if "Status" in item:
                state = item["Status"].get("State", "Unknown")
            state_item = QTableWidgetItem(state)
            state_item.setFlags(state_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.inventory_table.setItem(row, 3, state_item)

            # Description
            desc_item = QTableWidgetItem(item.get("Description", ""))
            desc_item.setFlags(desc_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.inventory_table.setItem(row, 4, desc_item)

    def browse_file(self):
        """Open file browser to select firmware image."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Firmware Image",
            "",
            "Firmware Images (*.bin *.img *.iso *.tar *.gz *.zip);;All Files (*)"
        )

        if file_path:
            self.file_path.setText(file_path)
            self.selected_file = file_path
            self.upload_button.setEnabled(True)
        else:
            self.upload_button.setEnabled(False)

    def refresh_clicked(self):
        """Signal to refresh firmware data."""
        # This will be connected to the parent widget's refresh method
        pass

    def upload_clicked(self):
        """Signal to upload and apply firmware update."""
        # This will be connected to the parent widget's upload method
        if not self.selected_file:
            QMessageBox.warning(self, "Error", "Please select a firmware image file")
            return

        confirm = QMessageBox.question(
            self,
            "Confirm Firmware Update",
            "Are you sure you want to upload and apply this firmware update?\n\n"
            "WARNING: Updating firmware may cause system instability or downtime if not performed correctly.\n"
            "Please make sure this update is compatible with your system.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm != QMessageBox.StandardButton.Yes:
            return

        # Signal will be connected to upload_firmware in parent

    def update_from_uri_clicked(self):
        """Signal to update firmware from URI."""
        # This will be connected to the parent widget's update method
        uri = self.uri_input.text().strip()

        if not uri:
            QMessageBox.warning(self, "Error", "Please enter a firmware image URI")
            return

        confirm = QMessageBox.question(
            self,
            "Confirm Firmware Update",
            f"Are you sure you want to apply firmware update from URI:\n{uri}\n\n"
            "WARNING: Updating firmware may cause system instability or downtime if not performed correctly.\n"
            "Please make sure this update is compatible with your system.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm != QMessageBox.StandardButton.Yes:
            return

        # Signal will be connected to update_firmware_from_uri in parent
