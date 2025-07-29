from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QComboBox, QMessageBox, QCheckBox, QWidget)
from PyQt6.QtCore import Qt, pyqtSignal
from typing import Dict, Optional
from greenfish.utils.logger import logger
from greenfish.ui.dialogs.profile_dialog import ProfileDialog
from greenfish.config.config_manager import config_manager, ConnectionProfile

class ConnectionDialog(QDialog):
    """Dialog for establishing Redfish connections."""

    # Signal emitted when connection is established
    connection_established = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("New Connection")
        self.setMinimumWidth(400)

        # Create layout
        layout = QVBoxLayout(self)

        # URL input
        url_layout = QHBoxLayout()
        url_label = QLabel("URL:")
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("http://192.168.0.1")
        url_layout.addWidget(url_label)
        url_layout.addWidget(self.url_input)
        layout.addLayout(url_layout)

        # Device type selection
        device_layout = QHBoxLayout()
        device_label = QLabel("Device Type:")
        self.device_combo = QComboBox()
        self.device_combo.addItems(["Redfish Server", "TP-Link Router"])
        self.device_combo.currentTextChanged.connect(self.on_device_changed)
        device_layout.addWidget(device_label)
        device_layout.addWidget(self.device_combo)
        layout.addLayout(device_layout)

        # Username container (optional for TP-Link)
        self.username_container = QWidget()
        username_layout = QHBoxLayout(self.username_container)
        username_layout.setContentsMargins(0, 0, 0, 0)
        username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Optional for TP-Link routers")
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        layout.addWidget(self.username_container)

        # Password input
        password_layout = QHBoxLayout()
        password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        layout.addLayout(password_layout)

        # Authentication method container (only for Redfish)
        self.auth_container = QWidget()
        auth_layout = QHBoxLayout(self.auth_container)
        auth_layout.setContentsMargins(0, 0, 0, 0)
        auth_label = QLabel("Auth Method:")
        self.auth_combo = QComboBox()
        self.auth_combo.addItems(["session", "basic"])
        auth_layout.addWidget(auth_label)
        auth_layout.addWidget(self.auth_combo)
        layout.addWidget(self.auth_container)

        # Add remember checkbox
        remember_layout = QHBoxLayout()
        self.remember_check = QCheckBox("Remember connection")
        remember_layout.addWidget(self.remember_check)
        remember_layout.addStretch()
        layout.addLayout(remember_layout)

        # Buttons
        button_layout = QHBoxLayout()
        self.connect_button = QPushButton("Connect")
        self.connect_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        profiles_button = QPushButton("Profiles...")
        profiles_button.clicked.connect(self.show_profiles)
        button_layout.addWidget(self.connect_button)
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(profiles_button)
        layout.addLayout(button_layout)

        # Apply solid color styling
        self.setStyleSheet("""
            QDialog {
                background-color: rgb(255, 255, 220);
            }
            QLabel {
                color: #333333;
            }
            QLineEdit {
                padding: 5px;
                border: 1px solid #CCCCCC;
                border-radius: 3px;
                background-color: rgb(255, 255, 255);
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
            QComboBox {
                padding: 5px;
                border: 1px solid #CCCCCC;
                border-radius: 3px;
                background-color: rgb(255, 255, 255);
            }
        """)

        # Set initial state
        self.on_device_changed(self.device_combo.currentText())

    def on_device_changed(self, device_type: str):
        """Handle device type change."""
        is_redfish = device_type == "Redfish Server"

        # Show/hide Redfish-specific fields
        self.username_container.setVisible(is_redfish)
        self.auth_container.setVisible(is_redfish)

        # Update URL placeholder
        if is_redfish:
            self.url_input.setPlaceholderText("https://hostname:port")
        else:
            self.url_input.setPlaceholderText("http://192.168.0.1")
            self.username_input.clear()  # Clear username for TP-Link

        logger.info(f"Device type changed to: {device_type}")

    def get_connection_params(self) -> Dict[str, str]:
        """Get connection parameters from dialog inputs."""
        device_type = self.device_combo.currentText()
        params = {
            "base_url": self.url_input.text().strip(),
            "password": self.password_input.text()
        }

        if device_type == "Redfish Server":
            params.update({
                "username": self.username_input.text().strip(),
                "auth": self.auth_combo.currentText()
            })
        else:
            # For TP-Link, use empty username
            params.update({
                "username": "",
                "auth": "basic"  # TP-Link uses basic auth
            })

        # Log connection attempt (without password)
        log_params = params.copy()
        log_params["password"] = "********"  # Mask password in logs
        logger.debug(f"Connection parameters: {log_params}")

        return params

    def show_profiles(self):
        """Show connection profiles dialog."""
        dialog = ProfileDialog(self)
        dialog.profile_selected.connect(self.use_profile)
        dialog.exec()

    def use_profile(self, profile: ConnectionProfile):
        """Use selected connection profile."""
        self.url_input.setText(profile.base_url)
        self.username_input.setText(profile.username)
        if profile.password:
            self.password_input.setText(profile.password)

        # Set authentication type
        index = self.auth_combo.findText(profile.auth_type)
        if index >= 0:
            self.auth_combo.setCurrentIndex(index)

        # Set device type (default to Redfish Server)
        self.device_combo.setCurrentIndex(0)

        # Automatically connect
        self.accept()

    def accept(self) -> None:
        """Handle dialog acceptance."""
        params = self.get_connection_params()

        # Validate inputs
        if not params["base_url"]:
            logger.error("URL field is empty")
            QMessageBox.warning(self, "Error", "Please enter a URL")
            return
        if not params["password"]:
            logger.error("Password field is empty")
            QMessageBox.warning(self, "Error", "Please enter a password")
            return

        # Log connection attempt
        logger.info(f"Attempting to connect to {params['base_url']}")

        # Save connection as profile if "Remember" is checked
        if hasattr(self, 'remember_check') and self.remember_check.isChecked():
            # Create profile name from URL
            url = self.url_input.text().strip()
            name = url.replace("http://", "").replace("https://", "").split("/")[0]

            # Create new profile
            profile = ConnectionProfile(
                name=name,
                base_url=url,
                username=self.username_input.text().strip(),
                password=self.password_input.text() if self.password_input.text() else None,
                auth_type=self.auth_combo.currentText()
            )

            # Add to config manager
            config_manager.add_profile(profile)

        # Emit connection parameters
        self.connection_established.emit(params)
        super().accept()
