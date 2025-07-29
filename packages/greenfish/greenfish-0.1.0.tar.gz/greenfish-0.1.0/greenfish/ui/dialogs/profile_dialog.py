from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QComboBox, QPushButton, QTableWidget,
                             QTableWidgetItem, QMessageBox, QFileDialog,
                             QHeaderView, QTextEdit)
from PyQt6.QtCore import Qt, pyqtSignal
from typing import Dict, Any, Optional
from greenfish.config.config_manager import config_manager, ConnectionProfile
from greenfish.utils.logger import logger

class ProfileEditDialog(QDialog):
    """Dialog for creating/editing a connection profile."""

    def __init__(self, profile: Optional[ConnectionProfile] = None, parent=None):
        super().__init__(parent)
        self.profile = profile
        self.setWindowTitle("Connection Profile" if profile else "New Connection Profile")
        self.setMinimumWidth(400)

        # Create layout
        layout = QVBoxLayout(self)

        # Profile name
        name_layout = QHBoxLayout()
        name_label = QLabel("Profile Name:")
        self.name_input = QLineEdit()
        if profile:
            self.name_input.setText(profile.name)
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)

        # Base URL
        url_layout = QHBoxLayout()
        url_label = QLabel("Base URL:")
        self.url_input = QLineEdit()
        if profile:
            self.url_input.setText(profile.base_url)
        url_layout.addWidget(url_label)
        url_layout.addWidget(self.url_input)
        layout.addLayout(url_layout)

        # Username
        username_layout = QHBoxLayout()
        username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        if profile:
            self.username_input.setText(profile.username)
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        layout.addLayout(username_layout)

        # Password
        password_layout = QHBoxLayout()
        password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        if profile and profile.password:
            self.password_input.setText(profile.password)
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        layout.addLayout(password_layout)

        # Authentication type
        auth_layout = QHBoxLayout()
        auth_label = QLabel("Authentication:")
        self.auth_combo = QComboBox()
        self.auth_combo.addItems(["session", "basic"])
        if profile:
            index = self.auth_combo.findText(profile.auth_type)
            if index >= 0:
                self.auth_combo.setCurrentIndex(index)
        auth_layout.addWidget(auth_label)
        auth_layout.addWidget(self.auth_combo)
        layout.addLayout(auth_layout)

        # Description
        desc_layout = QVBoxLayout()
        desc_label = QLabel("Description:")
        self.desc_input = QTextEdit()
        self.desc_input.setMaximumHeight(100)
        if profile:
            self.desc_input.setText(profile.description)
        desc_layout.addWidget(desc_label)
        desc_layout.addWidget(self.desc_input)
        layout.addLayout(desc_layout)

        # Buttons
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

    def get_profile_data(self) -> Dict[str, Any]:
        """Get profile data from dialog inputs."""
        return {
            "name": self.name_input.text().strip(),
            "base_url": self.url_input.text().strip(),
            "username": self.username_input.text().strip(),
            "password": self.password_input.text(),
            "auth_type": self.auth_combo.currentText(),
            "description": self.desc_input.toPlainText().strip()
        }

class ProfileDialog(QDialog):
    """Dialog for managing connection profiles."""

    profile_selected = pyqtSignal(ConnectionProfile)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Connection Profiles")
        self.setMinimumSize(600, 400)

        # Create layout
        layout = QVBoxLayout(self)

        # Create toolbar
        toolbar = QHBoxLayout()

        # Add profile button
        self.add_button = QPushButton("Add Profile")
        self.add_button.clicked.connect(self.add_profile)
        toolbar.addWidget(self.add_button)

        # Edit profile button
        self.edit_button = QPushButton("Edit Profile")
        self.edit_button.clicked.connect(self.edit_profile)
        toolbar.addWidget(self.edit_button)

        # Delete profile button
        self.delete_button = QPushButton("Delete Profile")
        self.delete_button.clicked.connect(self.delete_profile)
        toolbar.addWidget(self.delete_button)

        toolbar.addStretch()

        # Import/Export buttons
        self.import_button = QPushButton("Import")
        self.import_button.clicked.connect(self.import_profiles)
        toolbar.addWidget(self.import_button)

        self.export_button = QPushButton("Export")
        self.export_button.clicked.connect(self.export_profiles)
        toolbar.addWidget(self.export_button)

        layout.addLayout(toolbar)

        # Create profiles table
        self.profiles_table = QTableWidget()
        self.profiles_table.setColumnCount(5)
        self.profiles_table.setHorizontalHeaderLabels(["Name", "URL", "Username", "Auth Type", "Last Used"])
        self.profiles_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.profiles_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.profiles_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.profiles_table.verticalHeader().setVisible(False)
        self.profiles_table.setAlternatingRowColors(True)
        self.profiles_table.itemDoubleClicked.connect(self.on_profile_double_clicked)
        layout.addWidget(self.profiles_table)

        # Connect/Close buttons
        button_layout = QHBoxLayout()
        self.connect_button = QPushButton("Connect")
        self.connect_button.clicked.connect(self.connect_profile)
        button_layout.addWidget(self.connect_button)

        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.reject)
        button_layout.addWidget(self.close_button)
        layout.addLayout(button_layout)

        # Load profiles
        self.refresh_profiles()

        # Apply styling
        self.setStyleSheet("""
            QDialog {
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
        """)

    def refresh_profiles(self):
        """Refresh the profiles table."""
        profiles = config_manager.get_profiles()

        self.profiles_table.setRowCount(len(profiles))
        for row, profile in enumerate(profiles):
            self.profiles_table.setItem(row, 0, QTableWidgetItem(profile.name))
            self.profiles_table.setItem(row, 1, QTableWidgetItem(profile.base_url))
            self.profiles_table.setItem(row, 2, QTableWidgetItem(profile.username))
            self.profiles_table.setItem(row, 3, QTableWidgetItem(profile.auth_type))
            last_used = profile.last_used or "Never"
            self.profiles_table.setItem(row, 4, QTableWidgetItem(last_used))

            # Store profile ID in first column's data
            self.profiles_table.item(row, 0).setData(Qt.ItemDataRole.UserRole, profile.id)

        # Adjust column widths
        self.profiles_table.resizeColumnsToContents()
        self.profiles_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

    def add_profile(self):
        """Add a new connection profile."""
        dialog = ProfileEditDialog(parent=self)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        profile_data = dialog.get_profile_data()

        # Validate required fields
        if not profile_data["name"] or not profile_data["base_url"]:
            QMessageBox.warning(self, "Validation Error", "Profile name and URL are required.")
            return

        # Create new profile
        profile = ConnectionProfile(
            name=profile_data["name"],
            base_url=profile_data["base_url"],
            username=profile_data["username"],
            password=profile_data["password"],
            auth_type=profile_data["auth_type"],
            description=profile_data["description"]
        )

        # Add to config manager
        config_manager.add_profile(profile)

        # Refresh table
        self.refresh_profiles()

    def edit_profile(self):
        """Edit selected connection profile."""
        selected_row = self.profiles_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "No Selection", "Please select a profile to edit.")
            return

        # Get profile ID
        profile_id = self.profiles_table.item(selected_row, 0).data(Qt.ItemDataRole.UserRole)
        profile = config_manager.get_profile(profile_id)

        if not profile:
            QMessageBox.critical(self, "Error", "Failed to find selected profile.")
            return

        # Show edit dialog
        dialog = ProfileEditDialog(profile, parent=self)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        profile_data = dialog.get_profile_data()

        # Validate required fields
        if not profile_data["name"] or not profile_data["base_url"]:
            QMessageBox.warning(self, "Validation Error", "Profile name and URL are required.")
            return

        # Update profile
        profile.name = profile_data["name"]
        profile.base_url = profile_data["base_url"]
        profile.username = profile_data["username"]
        profile.password = profile_data["password"]
        profile.auth_type = profile_data["auth_type"]
        profile.description = profile_data["description"]

        # Save changes
        config_manager.update_profile(profile)

        # Refresh table
        self.refresh_profiles()

    def delete_profile(self):
        """Delete selected connection profile."""
        selected_row = self.profiles_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "No Selection", "Please select a profile to delete.")
            return

        # Get profile ID
        profile_id = self.profiles_table.item(selected_row, 0).data(Qt.ItemDataRole.UserRole)
        profile_name = self.profiles_table.item(selected_row, 0).text()

        # Confirm deletion
        confirm = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete the profile '{profile_name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm != QMessageBox.StandardButton.Yes:
            return

        # Delete profile
        if config_manager.delete_profile(profile_id):
            # Refresh table
            self.refresh_profiles()
        else:
            QMessageBox.critical(self, "Error", "Failed to delete profile.")

    def connect_profile(self):
        """Connect using selected profile."""
        selected_row = self.profiles_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "No Selection", "Please select a profile to connect.")
            return

        # Get profile ID
        profile_id = self.profiles_table.item(selected_row, 0).data(Qt.ItemDataRole.UserRole)
        profile = config_manager.get_profile(profile_id)

        if not profile:
            QMessageBox.critical(self, "Error", "Failed to find selected profile.")
            return

        # Update last used timestamp
        config_manager.update_profile_last_used(profile_id)

        # Emit signal with selected profile
        self.profile_selected.emit(profile)
        self.accept()

    def on_profile_double_clicked(self, item):
        """Handle double-click on profile item."""
        self.connect_profile()

    def import_profiles(self):
        """Import profiles from a file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Import Profiles",
            "",
            "JSON Files (*.json);;All Files (*)"
        )

        if not file_path:
            return

        if config_manager.import_profiles(file_path):
            self.refresh_profiles()
            QMessageBox.information(self, "Import Successful", "Connection profiles imported successfully.")
        else:
            QMessageBox.critical(self, "Import Failed", "Failed to import connection profiles.")

    def export_profiles(self):
        """Export profiles to a file."""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Profiles",
            "",
            "JSON Files (*.json);;All Files (*)"
        )

        if not file_path:
            return

        if config_manager.export_profiles(file_path):
            QMessageBox.information(self, "Export Successful", "Connection profiles exported successfully.")
        else:
            QMessageBox.critical(self, "Export Failed", "Failed to export connection profiles.")
