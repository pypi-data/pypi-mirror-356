from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QGroupBox, QTableWidget, QTableWidgetItem,
                             QMessageBox, QCheckBox)
from PyQt6.QtCore import Qt
from typing import Dict, Any, Optional
from greenfish.utils.logger import logger

class SecureBootWidget(QWidget):
    """Widget for managing Secure Boot configuration."""

    def __init__(self, redfish_client=None, parent=None):
        super().__init__(parent)
        self.redfish_client = redfish_client

        # Create layout
        layout = QVBoxLayout(self)

        # Status group
        status_group = QGroupBox("Secure Boot Status")
        status_layout = QVBoxLayout(status_group)

        # Enable/disable checkbox
        self.enable_check = QCheckBox("Enable Secure Boot")
        self.enable_check.stateChanged.connect(self.on_enable_changed)
        status_layout.addWidget(self.enable_check)

        # Current state label
        self.state_label = QLabel()
        status_layout.addWidget(self.state_label)

        layout.addWidget(status_group)

        # Key management group
        keys_group = QGroupBox("Key Management")
        keys_layout = QVBoxLayout(keys_group)

        # Key management buttons
        button_layout = QHBoxLayout()

        self.reset_button = QPushButton("Reset Keys to Default")
        self.reset_button.clicked.connect(self.reset_keys)
        button_layout.addWidget(self.reset_button)

        self.clear_button = QPushButton("Clear All Keys")
        self.clear_button.clicked.connect(self.clear_keys)
        button_layout.addWidget(self.clear_button)

        keys_layout.addLayout(button_layout)

        layout.addWidget(keys_group)

        # Database group
        db_group = QGroupBox("Certificate Databases")
        db_layout = QVBoxLayout(db_group)

        # Database table
        self.db_table = QTableWidget()
        self.db_table.setColumnCount(3)
        self.db_table.setHorizontalHeaderLabels(["Database", "Type", "Certificates"])
        self.db_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.db_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.db_table.verticalHeader().setVisible(False)
        db_layout.addWidget(self.db_table)

        layout.addWidget(db_group)

        # Refresh button
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh_data)
        layout.addWidget(self.refresh_button)

        # Apply styling
        self.setStyleSheet("""
            QWidget {
                background-color: rgb(255, 255, 220);
            }
            QGroupBox {
                font-weight: bold;
                border: 1px solid #CCCCCC;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
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

    def set_redfish_client(self, client):
        """Set the Redfish client."""
        self.redfish_client = client
        self.refresh_data()

    def refresh_data(self):
        """Refresh Secure Boot data."""
        if not self.redfish_client:
            return

        try:
            # Get Secure Boot information
            secure_boot = self.redfish_client.get_secure_boot()

            # Update enable checkbox
            enabled = secure_boot.get("SecureBootEnable", False)
            self.enable_check.setChecked(enabled)

            # Update state label
            current_state = secure_boot.get("SecureBootCurrentBoot", "Unknown")
            mode = secure_boot.get("SecureBootMode", "Unknown")
            self.state_label.setText(
                f"Current State: {current_state}\n"
                f"Mode: {mode}"
            )

            # Get database information
            try:
                databases = self.redfish_client.get_secure_boot_databases()

                # Update database table
                self.db_table.setRowCount(len(databases))
                for row, db in enumerate(databases):
                    self.db_table.setItem(row, 0, QTableWidgetItem(db.get("Name", "")))
                    self.db_table.setItem(row, 1, QTableWidgetItem(db.get("DatabaseId", "")))
                    cert_count = len(db.get("Certificates", {}).get("Members", []))
                    self.db_table.setItem(row, 2, QTableWidgetItem(str(cert_count)))

                # Adjust column widths
                self.db_table.resizeColumnsToContents()

            except Exception as e:
                logger.warning(f"Failed to get Secure Boot databases: {str(e)}")
                self.db_table.setRowCount(0)

            logger.success("Secure Boot data refreshed successfully")

        except Exception as e:
            logger.error(f"Failed to refresh Secure Boot data: {str(e)}")
            QMessageBox.critical(self, "Error", str(e))

    def on_enable_changed(self, state):
        """Handle Secure Boot enable/disable."""
        if not self.redfish_client:
            return

        try:
            enable = state == Qt.CheckState.Checked.value

            # Confirm action
            confirm = QMessageBox.question(
                self,
                "Confirm Secure Boot Change",
                f"Are you sure you want to {'enable' if enable else 'disable'} Secure Boot?\n\n"
                "Note: This change requires a system reboot to take effect.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if confirm != QMessageBox.StandardButton.Yes:
                # Revert checkbox state
                self.enable_check.setChecked(not enable)
                return

            # Update Secure Boot state
            self.redfish_client.enable_secure_boot(enable)

            # Show reboot message
            QMessageBox.information(
                self,
                "Secure Boot Updated",
                "Secure Boot state updated successfully.\n\n"
                "A system reboot is required for changes to take effect."
            )

        except Exception as e:
            logger.error(f"Failed to update Secure Boot state: {str(e)}")
            QMessageBox.critical(self, "Error", str(e))
            # Revert checkbox state
            self.enable_check.setChecked(not enable)

    def reset_keys(self):
        """Reset Secure Boot keys to default."""
        if not self.redfish_client:
            return

        try:
            # Confirm action
            confirm = QMessageBox.question(
                self,
                "Confirm Reset Keys",
                "Are you sure you want to reset all Secure Boot keys to their default values?\n\n"
                "This will remove any custom keys and restore the original manufacturer keys.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if confirm != QMessageBox.StandardButton.Yes:
                return

            # Reset keys
            self.redfish_client.reset_secure_boot()

            # Refresh data
            self.refresh_data()

            QMessageBox.information(
                self,
                "Keys Reset",
                "Secure Boot keys have been reset to their default values."
            )

        except Exception as e:
            logger.error(f"Failed to reset Secure Boot keys: {str(e)}")
            QMessageBox.critical(self, "Error", str(e))

    def clear_keys(self):
        """Clear all Secure Boot keys."""
        if not self.redfish_client:
            return

        try:
            # Confirm action
            confirm = QMessageBox.question(
                self,
                "Confirm Clear Keys",
                "Are you sure you want to clear all Secure Boot keys?\n\n"
                "WARNING: This will delete all keys and may prevent the system from booting!",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if confirm != QMessageBox.StandardButton.Yes:
                return

            # Clear keys
            self.redfish_client.clear_secure_boot_keys()

            # Refresh data
            self.refresh_data()

            QMessageBox.warning(
                self,
                "Keys Cleared",
                "All Secure Boot keys have been cleared.\n\n"
                "WARNING: The system may not boot until new keys are installed!"
            )

        except Exception as e:
            logger.error(f"Failed to clear Secure Boot keys: {str(e)}")
            QMessageBox.critical(self, "Error", str(e))
