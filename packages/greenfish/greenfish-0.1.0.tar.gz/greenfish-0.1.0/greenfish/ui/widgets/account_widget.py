from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
                             QTableWidgetItem, QPushButton, QDialog, QLabel,
                             QLineEdit, QComboBox, QMessageBox, QCheckBox)
from PyQt6.QtCore import Qt
from typing import Dict, Any, Optional
from greenfish.utils.logger import logger

class AccountDialog(QDialog):
    """Dialog for creating/editing user accounts."""

    def __init__(self, roles: list, account_data: Optional[Dict[str, Any]] = None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("User Account")
        self.setMinimumWidth(400)

        # Create layout
        layout = QVBoxLayout(self)

        # Username input
        username_layout = QHBoxLayout()
        username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        if account_data:
            self.username_input.setText(account_data.get("UserName", ""))
            self.username_input.setEnabled(False)  # Can't change username
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        layout.addLayout(username_layout)

        # Password input
        password_layout = QHBoxLayout()
        password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        layout.addLayout(password_layout)

        # Role selection
        role_layout = QHBoxLayout()
        role_label = QLabel("Role:")
        self.role_combo = QComboBox()
        self.role_combo.addItems([role.get("Id", "") for role in roles])
        if account_data:
            current_role = account_data.get("RoleId", "")
            index = self.role_combo.findText(current_role)
            if index >= 0:
                self.role_combo.setCurrentIndex(index)
        role_layout.addWidget(role_label)
        role_layout.addWidget(self.role_combo)
        layout.addLayout(role_layout)

        # Enabled checkbox
        self.enabled_check = QCheckBox("Enabled")
        self.enabled_check.setChecked(account_data.get("Enabled", True) if account_data else True)
        layout.addWidget(self.enabled_check)

        # Buttons
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

    def get_account_data(self) -> Dict[str, Any]:
        """Get account data from dialog inputs."""
        data = {
            "UserName": self.username_input.text().strip(),
            "RoleId": self.role_combo.currentText(),
            "Enabled": self.enabled_check.isChecked()
        }

        # Only include password if it was entered
        password = self.password_input.text()
        if password:
            data["Password"] = password

        return data

class AccountWidget(QWidget):
    """Widget for managing user accounts."""

    def __init__(self, redfish_client=None, parent=None):
        super().__init__(parent)
        self.redfish_client = redfish_client
        self.roles = []

        # Create layout
        layout = QVBoxLayout(self)

        # Create toolbar
        toolbar = QHBoxLayout()

        # Add account button
        self.add_button = QPushButton("Add Account")
        self.add_button.clicked.connect(self.add_account)
        toolbar.addWidget(self.add_button)

        # Edit account button
        self.edit_button = QPushButton("Edit Account")
        self.edit_button.clicked.connect(self.edit_account)
        toolbar.addWidget(self.edit_button)

        # Delete account button
        self.delete_button = QPushButton("Delete Account")
        self.delete_button.clicked.connect(self.delete_account)
        toolbar.addWidget(self.delete_button)

        # Refresh button
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh_accounts)
        toolbar.addWidget(self.refresh_button)

        toolbar.addStretch()
        layout.addLayout(toolbar)

        # Create accounts table
        self.accounts_table = QTableWidget()
        self.accounts_table.setColumnCount(4)
        self.accounts_table.setHorizontalHeaderLabels(["Username", "Role", "Enabled", "ID"])
        self.accounts_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.accounts_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.accounts_table.verticalHeader().setVisible(False)
        layout.addWidget(self.accounts_table)

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
        """)

    def set_redfish_client(self, client):
        """Set the Redfish client."""
        self.redfish_client = client
        self.refresh_accounts()

    def refresh_accounts(self):
        """Refresh the accounts table."""
        if not self.redfish_client:
            return

        try:
            # Get available roles first
            self.roles = self.redfish_client.get_roles()

            # Get accounts
            accounts = self.redfish_client.get_accounts()

            # Update table
            self.accounts_table.setRowCount(len(accounts))
            for row, account in enumerate(accounts):
                self.accounts_table.setItem(row, 0, QTableWidgetItem(account.get("UserName", "")))
                self.accounts_table.setItem(row, 1, QTableWidgetItem(account.get("RoleId", "")))
                self.accounts_table.setItem(row, 2, QTableWidgetItem("Yes" if account.get("Enabled", False) else "No"))
                self.accounts_table.setItem(row, 3, QTableWidgetItem(account.get("Id", "")))

            # Adjust column widths
            self.accounts_table.resizeColumnsToContents()

            logger.success("Account list refreshed successfully")

        except Exception as e:
            logger.error(f"Failed to refresh accounts: {str(e)}")
            QMessageBox.critical(self, "Error", str(e))

    def add_account(self):
        """Add a new user account."""
        if not self.redfish_client:
            return

        try:
            # Show account dialog
            dialog = AccountDialog(self.roles, parent=self)
            if dialog.exec() != QDialog.DialogCode.Accepted:
                return

            # Get account data
            account_data = dialog.get_account_data()

            # Create account
            self.redfish_client.create_account(
                username=account_data["UserName"],
                password=account_data["Password"],
                role_id=account_data["RoleId"],
                enabled=account_data["Enabled"]
            )

            # Refresh accounts
            self.refresh_accounts()

        except Exception as e:
            logger.error(f"Failed to add account: {str(e)}")
            QMessageBox.critical(self, "Error", str(e))

    def edit_account(self):
        """Edit selected user account."""
        if not self.redfish_client:
            return

        # Get selected account
        current_row = self.accounts_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Warning", "Please select an account to edit")
            return

        try:
            # Get account ID
            account_id = self.accounts_table.item(current_row, 3).text()

            # Get current account data
            account_data = self.redfish_client.get_account(account_id)

            # Show account dialog
            dialog = AccountDialog(self.roles, account_data, parent=self)
            if dialog.exec() != QDialog.DialogCode.Accepted:
                return

            # Get updated data
            updates = dialog.get_account_data()

            # Remove username as it can't be changed
            updates.pop("UserName", None)

            # Update account
            self.redfish_client.update_account(account_id, updates)

            # Refresh accounts
            self.refresh_accounts()

        except Exception as e:
            logger.error(f"Failed to edit account: {str(e)}")
            QMessageBox.critical(self, "Error", str(e))

    def delete_account(self):
        """Delete selected user account."""
        if not self.redfish_client:
            return

        # Get selected account
        current_row = self.accounts_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Warning", "Please select an account to delete")
            return

        try:
            # Get account info
            account_id = self.accounts_table.item(current_row, 3).text()
            username = self.accounts_table.item(current_row, 0).text()

            # Confirm deletion
            confirm = QMessageBox.question(
                self,
                "Confirm Delete",
                f"Are you sure you want to delete the account '{username}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if confirm != QMessageBox.StandardButton.Yes:
                return

            # Delete account
            self.redfish_client.delete_account(account_id)

            # Refresh accounts
            self.refresh_accounts()

        except Exception as e:
            logger.error(f"Failed to delete account: {str(e)}")
            QMessageBox.critical(self, "Error", str(e))
