from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
                             QComboBox, QLineEdit, QCheckBox, QMessageBox, QTabWidget,
                             QSpinBox, QGroupBox, QScrollArea)
from PyQt6.QtCore import Qt
from typing import Dict, Any, Optional

class BiosConfigWidget(QWidget):
    """Widget for displaying and modifying BIOS settings."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.bios_data = {}
        self.modified_attributes = {}
        self.setup_ui()

    def setup_ui(self):
        """Setup the user interface."""
        main_layout = QVBoxLayout(self)

        # Create tab widget for different setting categories
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        # Add default "All Settings" tab
        self.all_settings_tab = QWidget()
        self.all_settings_layout = QVBoxLayout(self.all_settings_tab)

        # Create table for BIOS settings
        self.settings_table = QTableWidget()
        self.settings_table.setColumnCount(3)
        self.settings_table.setHorizontalHeaderLabels(["Setting", "Value", "Description"])
        self.settings_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.settings_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.all_settings_layout.addWidget(self.settings_table)

        self.tabs.addTab(self.all_settings_tab, "All Settings")

        # Pending settings tab
        self.pending_tab = QWidget()
        self.pending_layout = QVBoxLayout(self.pending_tab)

        self.pending_table = QTableWidget()
        self.pending_table.setColumnCount(3)
        self.pending_table.setHorizontalHeaderLabels(["Setting", "Pending Value", "Current Value"])
        self.pending_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.pending_layout.addWidget(self.pending_table)

        self.tabs.addTab(self.pending_tab, "Pending Changes")

        # Buttons row
        button_layout = QHBoxLayout()

        self.refresh_button = QPushButton("Refresh")
        button_layout.addWidget(self.refresh_button)

        self.apply_button = QPushButton("Apply Changes")
        self.apply_button.setEnabled(False)
        button_layout.addWidget(self.apply_button)

        self.reset_button = QPushButton("Reset")
        self.reset_button.setEnabled(False)
        button_layout.addWidget(self.reset_button)

        main_layout.addLayout(button_layout)

        # Status label
        self.status_label = QLabel("No BIOS data loaded")
        main_layout.addWidget(self.status_label)

        # Connect signals
        self.refresh_button.clicked.connect(self.refresh_clicked)
        self.apply_button.clicked.connect(self.apply_changes)
        self.reset_button.clicked.connect(self.reset_changes)

        # Set styling
        self.setStyleSheet("""
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
            QTabWidget::pane {
                border: 1px solid #CCCCCC;
                border-radius: 3px;
            }
            QTabBar::tab {
                background-color: rgb(240, 240, 220);
                border: 1px solid #CCCCCC;
                border-bottom: none;
                border-top-left-radius: 3px;
                border-top-right-radius: 3px;
                padding: 5px 10px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: rgb(255, 255, 220);
                border-bottom: 1px solid rgb(255, 255, 220);
            }
            QTabBar::tab:!selected {
                margin-top: 2px;
            }
        """)

    def load_bios_data(self, bios_data: Dict[str, Any]):
        """Load BIOS data into the widget."""
        self.bios_data = bios_data
        self.modified_attributes = {}  # Reset modified attributes

        # Clear any existing category tabs (except first two)
        while self.tabs.count() > 2:
            self.tabs.removeTab(2)

        # Update settings table
        self.update_settings_table()

        # Check if we have registry data for categories
        registry = bios_data.get("registry", None)
        if registry and "RegistryEntries" in registry:
            # Create tabs for each category
            categories = {}

            # Group attributes by category
            registry_entries = registry["RegistryEntries"]
            if "Attributes" in registry_entries:
                for attr in registry_entries["Attributes"]:
                    if "AttributeName" in attr and "MenuPath" in attr:
                        category = attr.get("MenuPath", "Other")
                        if category not in categories:
                            categories[category] = []
                        categories[category].append(attr)

            # Create a tab for each category
            for category, attrs in categories.items():
                # Skip if empty
                if not attrs:
                    continue

                # Create tab
                tab = QWidget()
                tab_layout = QVBoxLayout(tab)

                # Create scroll area for potentially long lists
                scroll = QScrollArea()
                scroll.setWidgetResizable(True)
                scroll_content = QWidget()
                scroll_layout = QVBoxLayout(scroll_content)

                # Add attributes to this category
                for attr in attrs:
                    attr_name = attr.get("AttributeName")
                    attr_display = attr.get("DisplayName", attr_name)
                    attr_desc = attr.get("HelpText", "")
                    attr_type = attr.get("Type", "String")

                    # Get current value
                    current_value = self.bios_data["settings"].get("Attributes", {}).get(attr_name, "N/A")

                    # Create a group box for this setting
                    group = QGroupBox(attr_display)
                    group_layout = QVBoxLayout(group)

                    # Add description
                    if attr_desc:
                        desc_label = QLabel(attr_desc)
                        desc_label.setWordWrap(True)
                        group_layout.addWidget(desc_label)

                    # Create editor based on type
                    editor = None

                    if attr_type == "Enumeration" and "Value" in attr:
                        # Create combobox for enumeration
                        editor = QComboBox()
                        for val in attr["Value"]:
                            value_name = val.get("ValueName")
                            value_display = val.get("ValueDisplayName", value_name)
                            editor.addItem(value_display, value_name)

                        # Set current value
                        index = editor.findData(current_value)
                        if index >= 0:
                            editor.setCurrentIndex(index)

                        editor.currentIndexChanged.connect(
                            lambda index, attr=attr_name, combo=editor: self.setting_changed(attr, combo.currentData())
                        )

                    elif attr_type == "Boolean":
                        # Create checkbox for boolean
                        editor = QCheckBox("Enabled")
                        editor.setChecked(current_value)

                        editor.stateChanged.connect(
                            lambda state, attr=attr_name: self.setting_changed(attr, state == Qt.CheckState.Checked)
                        )

                    elif attr_type == "Integer":
                        # Create spinbox for integer
                        editor = QSpinBox()

                        # Set range if available
                        if "LowerBound" in attr:
                            editor.setMinimum(attr["LowerBound"])
                        if "UpperBound" in attr:
                            editor.setMaximum(attr["UpperBound"])

                        # Set current value
                        try:
                            editor.setValue(int(current_value))
                        except (ValueError, TypeError):
                            pass

                        editor.valueChanged.connect(
                            lambda value, attr=attr_name: self.setting_changed(attr, value)
                        )

                    else:
                        # Default to text input for other types
                        editor = QLineEdit(str(current_value))

                        editor.textChanged.connect(
                            lambda text, attr=attr_name: self.setting_changed(attr, text)
                        )

                    # Add editor to group
                    if editor:
                        editor_layout = QHBoxLayout()
                        value_label = QLabel("Value:")
                        editor_layout.addWidget(value_label)
                        editor_layout.addWidget(editor)
                        group_layout.addLayout(editor_layout)

                    # Add to scroll layout
                    scroll_layout.addWidget(group)

                # Add spacer at the end
                scroll_layout.addStretch()

                # Set scroll content
                scroll.setWidget(scroll_content)
                tab_layout.addWidget(scroll)

                # Add tab
                self.tabs.addTab(tab, category)

        # Update status
        self.status_label.setText(f"Loaded BIOS settings ({len(self.bios_data.get('settings', {}).get('Attributes', {}))} attributes)")

    def update_settings_table(self):
        """Update the settings table with current BIOS data."""
        settings = self.bios_data.get("settings", {}).get("Attributes", {})

        # Update main settings table
        self.settings_table.setRowCount(len(settings))

        row = 0
        for name, value in settings.items():
            # Setting name
            name_item = QTableWidgetItem(name)
            name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.settings_table.setItem(row, 0, name_item)

            # Setting value (editable)
            value_item = QTableWidgetItem(str(value))
            self.settings_table.setItem(row, 1, value_item)

            # Description (from registry if available)
            desc = self.get_attribute_description(name)
            desc_item = QTableWidgetItem(desc)
            desc_item.setFlags(desc_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.settings_table.setItem(row, 2, desc_item)

            row += 1

        # Connect to item changed signal
        self.settings_table.itemChanged.connect(self.table_item_changed)

    def update_pending_table(self, pending_settings: Dict[str, Any]):
        """Update the pending settings table."""
        current_settings = self.bios_data.get("settings", {}).get("Attributes", {})
        pending_attributes = pending_settings.get("Attributes", {})

        # Clear table
        self.pending_table.setRowCount(len(pending_attributes))

        row = 0
        for name, value in pending_attributes.items():
            # Only show if different from current
            current_value = current_settings.get(name, "N/A")
            if str(value) != str(current_value):
                # Setting name
                name_item = QTableWidgetItem(name)
                name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.pending_table.setItem(row, 0, name_item)

                # Pending value
                pending_item = QTableWidgetItem(str(value))
                pending_item.setFlags(pending_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.pending_table.setItem(row, 1, pending_item)

                # Current value
                current_item = QTableWidgetItem(str(current_value))
                current_item.setFlags(current_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.pending_table.setItem(row, 2, current_item)

                row += 1

        # Update actual row count (in case we skipped some)
        self.pending_table.setRowCount(row)

    def get_attribute_description(self, attr_name: str) -> str:
        """Get attribute description from registry if available."""
        registry = self.bios_data.get("registry", None)
        if registry and "RegistryEntries" in registry:
            registry_entries = registry["RegistryEntries"]
            if "Attributes" in registry_entries:
                for attr in registry_entries["Attributes"]:
                    if attr.get("AttributeName") == attr_name:
                        return attr.get("HelpText", "")
        return ""

    def table_item_changed(self, item):
        """Handle changes to table items."""
        # Only process value column changes (column 1)
        if item.column() == 1:
            row = item.row()
            attr_name = self.settings_table.item(row, 0).text()
            attr_value = item.text()

            # Convert value based on registry type if possible
            converted_value = self.convert_value_by_type(attr_name, attr_value)

            # Update modified attributes
            self.setting_changed(attr_name, converted_value)

    def convert_value_by_type(self, attr_name: str, value: str) -> Any:
        """Convert string value to appropriate type based on registry."""
        # Get attribute type from registry
        registry = self.bios_data.get("registry", None)
        if registry and "RegistryEntries" in registry:
            registry_entries = registry["RegistryEntries"]
            if "Attributes" in registry_entries:
                for attr in registry_entries["Attributes"]:
                    if attr.get("AttributeName") == attr_name:
                        attr_type = attr.get("Type", "String")

                        if attr_type == "Boolean":
                            return value.lower() in ("true", "1", "yes", "y", "on")
                        elif attr_type == "Integer":
                            try:
                                return int(value)
                            except ValueError:
                                pass
                        # Enumeration and other types as string
                        return value

        # Default to string if no type info
        return value

    def setting_changed(self, attr_name: str, value: Any):
        """Handle setting changes."""
        original_value = self.bios_data.get("settings", {}).get("Attributes", {}).get(attr_name)

        if str(value) != str(original_value):
            # Value changed, add to modified attributes
            self.modified_attributes[attr_name] = value
        else:
            # Value unchanged, remove from modified attributes
            if attr_name in self.modified_attributes:
                del self.modified_attributes[attr_name]

        # Update button states
        self.apply_button.setEnabled(len(self.modified_attributes) > 0)
        self.reset_button.setEnabled(len(self.modified_attributes) > 0)

        # Update status
        if len(self.modified_attributes) > 0:
            self.status_label.setText(f"Modified {len(self.modified_attributes)} settings")
        else:
            self.status_label.setText("No pending changes")

    def refresh_clicked(self):
        """Signal to refresh BIOS data."""
        # This will be connected to the parent widget's refresh method
        pass

    def apply_changes(self):
        """Signal to apply BIOS changes."""
        # This will be connected to the parent widget's apply method
        pass

    def reset_changes(self):
        """Reset all pending changes."""
        self.modified_attributes = {}

        # Reload BIOS data to reset UI
        self.load_bios_data(self.bios_data)

        # Update status
        self.status_label.setText("Changes reset")

        # Disable buttons
        self.apply_button.setEnabled(False)
        self.reset_button.setEnabled(False)

    def get_modified_attributes(self) -> Dict[str, Any]:
        """Get the modified attributes."""
        return self.modified_attributes.copy()
