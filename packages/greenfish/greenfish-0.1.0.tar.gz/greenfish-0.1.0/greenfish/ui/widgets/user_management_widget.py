"""User Management Interface Widget."""
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                           QLabel, QComboBox, QTableWidget, QTableWidgetItem,
                           QHeaderView, QMessageBox, QGroupBox, QDialog,
                           QFormLayout, QLineEdit, QCheckBox, QSpinBox,
                           QRadioButton, QButtonGroup, QDialogButtonBox)
from PyQt5.QtCore import Qt, pyqtSignal, QThread

from greenfish.utils.logger import Logger

class UserWorker(QThread):
    """Worker thread for user operations."""

    finished = pyqtSignal(bool, str)

    def __init__(self, client, operation, user_data=None):
        """Initialize worker thread.

        Args:
            client: User management client
            operation: Operation to perform
            user_data: User data for create/modify operations
        """
        super().__init__()
        self.client = client
        self.operation = operation
        self.user_data = user_data

    def run(self):
        """Run the operation."""
        try:
            result = False
            message = ""

            if self.operation == "create":
                # Create user
                result = self.client.create_user(
                    self.user_data["username"],
                    self.user_data["password"],
                    self.user_data["role"],
                    self.user_data["enabled"]
                )

                if result:
                    message = f"Successfully created user {self.user_data['username']}"
                else:
                    message = f"Failed to create user {self.user_data['username']}"

            elif self.operation == "modify":
                # Modify user
                result = self.client.modify_user(
                    self.user_data["id"],
                    self.user_data.get("username"),
                    self.user_data.get("password"),
                    self.user_data.get("role"),
                    self.user_data.get("enabled")
                )

                if result:
                    message = f"Successfully modified user {self.user_data.get('username', self.user_data['id'])}"
                else:
                    message = f"Failed to modify user {self.user_data.get('username', self.user_data['id'])}"

            elif self.operation == "delete":
                # Delete user
                result = self.client.delete_user(self.user_data["id"])

                if result:
                    message = f"Successfully deleted user {self.user_data.get('username', self.user_data['id'])}"
                else:
                    message = f"Failed to delete user {self.user_data.get('username', self.user_data['id'])}"

            elif self.operation == "enable":
                # Enable user
                result = self.client.enable_user(self.user_data["id"])

                if result:
                    message = f"Successfully enabled user {self.user_data.get('username', self.user_data['id'])}"
                else:
                    message = f"Failed to enable user {self.user_data.get('username', self.user_data['id'])}"

            elif self.operation == "disable":
                # Disable user
                result = self.client.disable_user(self.user_data["id"])

                if result:
                    message = f"Successfully disabled user {self.user_data.get('username', self.user_data['id'])}"
                else:
                    message = f"Failed to disable user {self.user_data.get('username', self.user_data['id'])}"

            self.finished.emit(result, message)

        except Exception as e:
            Logger.error(f"Error in user operation: {str(e)}")
            self.finished.emit(False, f"Error: {str(e)}")


class UserDialog(QDialog):
    """User dialog for creating/editing users."""

    def __init__(self, parent=None, user=None):
        """Initialize dialog.

        Args:
            parent: Parent widget
            user: User data for editing (None for new user)
        """
        super().__init__(parent)
        self.user = user
        self.init_ui()

    def init_ui(self):
        """Initialize UI components."""
        # Set dialog title
        if self.user:
            self.setWindowTitle("Edit User")
        else:
            self.setWindowTitle("Create User")

        # Main layout
        main_layout = QVBoxLayout(self)

        # Form layout
        form_layout = QFormLayout()

        # Username
        self.username_edit = QLineEdit()
        if self.user:
            self.username_edit.setText(self.user.get("username", ""))
            if self.user.get("username_readonly", False):
                self.username_edit.setReadOnly(True)

        form_layout.addRow("Username:", self.username_edit)

        # Password
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        form_layout.addRow("Password:", self.password_edit)

        # Confirm Password
        self.confirm_password_edit = QLineEdit()
        self.confirm_password_edit.setEchoMode(QLineEdit.Password)
        form_layout.addRow("Confirm Password:", self.confirm_password_edit)

        # Role
        self.role_combo = QComboBox()
        self.role_combo.addItem("Administrator")
        self.role_combo.addItem("Operator")
        self.role_combo.addItem("ReadOnly")

        if self.user:
            role = self.user.get("role", "")
            if role == "Administrator":
                self.role_combo.setCurrentIndex(0)
            elif role == "Operator":
                self.role_combo.setCurrentIndex(1)
            elif role == "ReadOnly":
                self.role_combo.setCurrentIndex(2)

        form_layout.addRow("Role:", self.role_combo)

        # Enabled
        self.enabled_check = QCheckBox("Enabled")
        self.enabled_check.setChecked(self.user.get("enabled", True) if self.user else True)
        form_layout.addRow("", self.enabled_check)

        # Add form layout to main layout
        main_layout.addLayout(form_layout)

        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        main_layout.addWidget(button_box)

        # Set dialog size
        self.setMinimumWidth(300)

    def get_user_data(self):
        """Get user data from dialog.

        Returns:
            dict: User data
        """
        # Get role
        role = ""
        if self.role_combo.currentIndex() == 0:
            role = "Administrator"
        elif self.role_combo.currentIndex() == 1:
            role = "Operator"
        elif self.role_combo.currentIndex() == 2:
            role = "ReadOnly"

        # Build user data
        user_data = {
            "username": self.username_edit.text(),
            "password": self.password_edit.text(),
            "role": role,
            "enabled": self.enabled_check.isChecked()
        }

        # Add ID if editing
        if self.user:
            user_data["id"] = self.user.get("id", "")

        return user_data

    def validate(self):
        """Validate dialog inputs.

        Returns:
            tuple: (valid, message)
        """
        # Check username
        if not self.username_edit.text():
            return False, "Username is required"

        # Check password
        if not self.user and not self.password_edit.text():
            return False, "Password is required for new users"

        # Check password confirmation
        if self.password_edit.text() and self.password_edit.text() != self.confirm_password_edit.text():
            return False, "Passwords do not match"

        return True, ""

    def accept(self):
        """Handle dialog acceptance."""
        # Validate inputs
        valid, message = self.validate()

        if valid:
            super().accept()
        else:
            QMessageBox.warning(self, "Validation Error", message)


class UserManagementWidget(QWidget):
    """User Management Interface widget."""

    def __init__(self, parent=None):
        """Initialize widget.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.client = None
        self.users = []
        self.worker = None

        self.init_ui()

    def init_ui(self):
        """Initialize UI components."""
        # Main layout
        main_layout = QVBoxLayout(self)

        # Controls
        controls_layout = QHBoxLayout()

        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh_users)

        self.connection_combo = QComboBox()
        self.connection_combo.addItem("Select Connection Type")
        self.connection_combo.addItem("Redfish")
        self.connection_combo.addItem("IPMI")
        self.connection_combo.currentIndexChanged.connect(self.on_connection_changed)

        self.create_button = QPushButton("Create User")
        self.create_button.clicked.connect(self.create_user)

        controls_layout.addWidget(QLabel("Connection:"))
        controls_layout.addWidget(self.connection_combo)
        controls_layout.addStretch()
        controls_layout.addWidget(self.create_button)
        controls_layout.addWidget(self.refresh_button)

        # Users table
        self.users_table = QTableWidget()
        self.users_table.setColumnCount(6)
        self.users_table.setHorizontalHeaderLabels([
            "ID", "Username", "Role", "Enabled", "Status", "Actions"
        ])
        self.users_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.users_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)
        self.users_table.verticalHeader().setVisible(False)
        self.users_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.users_table.setSelectionMode(QTableWidget.SingleSelection)
        self.users_table.setEditTriggers(QTableWidget.NoEditTriggers)

        # Status label
        self.status_label = QLabel()

        # Add widgets to main layout
        main_layout.addLayout(controls_layout)
        main_layout.addWidget(self.users_table)
        main_layout.addWidget(self.status_label)

    def set_client(self, client):
        """Set user management client.

        Args:
            client: User management client
        """
        self.client = client
        self.refresh_users()

    def refresh_users(self):
        """Refresh user list."""
        if not self.client or not self.client.is_connected():
            self.status_label.setText("Not connected to a server")
            self.users_table.setRowCount(0)
            self.users = []
            return

        try:
            # Get user list
            self.users = self.client.list_users()

            # Update table
            self.update_users_table()

            self.status_label.setText(f"Found {len(self.users)} users")

        except Exception as e:
            Logger.error(f"Error refreshing users: {str(e)}")
            self.status_label.setText(f"Error: {str(e)}")

    def update_users_table(self):
        """Update users table with current user list."""
        self.users_table.setRowCount(0)

        for user in self.users:
            row = self.users_table.rowCount()
            self.users_table.insertRow(row)

            # ID
            id_item = QTableWidgetItem(str(user.get("id", "")))
            self.users_table.setItem(row, 0, id_item)

            # Username
            username_item = QTableWidgetItem(user.get("username", ""))
            self.users_table.setItem(row, 1, username_item)

            # Role
            role_item = QTableWidgetItem(user.get("role", ""))
            self.users_table.setItem(row, 2, role_item)

            # Enabled
            enabled_item = QTableWidgetItem("Yes" if user.get("enabled", False) else "No")
            self.users_table.setItem(row, 3, enabled_item)

            # Status
            status_item = QTableWidgetItem(user.get("status", ""))
            self.users_table.setItem(row, 4, status_item)

            # Actions
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(2, 2, 2, 2)

            edit_button = QPushButton("Edit")
            edit_button.setProperty("user_index", row)
            edit_button.clicked.connect(lambda _, idx=row: self.edit_user(idx))

            delete_button = QPushButton("Delete")
            delete_button.setProperty("user_index", row)
            delete_button.clicked.connect(lambda _, idx=row: self.delete_user(idx))
            delete_button.setEnabled(not user.get("readonly", False))

            toggle_button = QPushButton("Disable" if user.get("enabled", False) else "Enable")
            toggle_button.setProperty("user_index", row)
            toggle_button.clicked.connect(lambda _, idx=row: self.toggle_user(idx))
            toggle_button.setEnabled(not user.get("readonly", False))

            actions_layout.addWidget(edit_button)
            actions_layout.addWidget(toggle_button)
            actions_layout.addWidget(delete_button)

            self.users_table.setCellWidget(row, 5, actions_widget)

    def create_user(self):
        """Create a new user."""
        if not self.client or not self.client.is_connected():
            QMessageBox.warning(self, "Not Connected", "Please connect to a server first")
            return

        # Show user dialog
        dialog = UserDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            # Get user data
            user_data = dialog.get_user_data()

            # Disable UI during operation
            self.setEnabled(False)
            self.status_label.setText(f"Creating user {user_data['username']}...")

            # Start worker thread
            self.worker = UserWorker(self.client, "create", user_data)
            self.worker.finished.connect(self.on_operation_finished)
            self.worker.start()

    def edit_user(self, index):
        """Edit a user.

        Args:
            index: User index in table
        """
        if 0 <= index < len(self.users):
            user = self.users[index]

            # Show user dialog
            dialog = UserDialog(self, user)
            if dialog.exec_() == QDialog.Accepted:
                # Get user data
                user_data = dialog.get_user_data()

                # Disable UI during operation
                self.setEnabled(False)
                self.status_label.setText(f"Modifying user {user_data['username']}...")

                # Start worker thread
                self.worker = UserWorker(self.client, "modify", user_data)
                self.worker.finished.connect(self.on_operation_finished)
                self.worker.start()

    def delete_user(self, index):
        """Delete a user.

        Args:
            index: User index in table
        """
        if 0 <= index < len(self.users):
            user = self.users[index]

            # Confirm deletion
            reply = QMessageBox.question(
                self, "Delete User",
                f"Are you sure you want to delete user {user.get('username', '')}?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                # Disable UI during operation
                self.setEnabled(False)
                self.status_label.setText(f"Deleting user {user.get('username', '')}...")

                # Start worker thread
                self.worker = UserWorker(self.client, "delete", user)
                self.worker.finished.connect(self.on_operation_finished)
                self.worker.start()

    def toggle_user(self, index):
        """Toggle user enabled status.

        Args:
            index: User index in table
        """
        if 0 <= index < len(self.users):
            user = self.users[index]

            # Determine operation
            operation = "disable" if user.get("enabled", False) else "enable"

            # Confirm operation
            action_text = "disable" if operation == "disable" else "enable"
            reply = QMessageBox.question(
                self, f"{action_text.capitalize()} User",
                f"Are you sure you want to {action_text} user {user.get('username', '')}?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                # Disable UI during operation
                self.setEnabled(False)
                self.status_label.setText(f"{action_text.capitalize()}ing user {user.get('username', '')}...")

                # Start worker thread
                self.worker = UserWorker(self.client, operation, user)
                self.worker.finished.connect(self.on_operation_finished)
                self.worker.start()

    def on_operation_finished(self, success, message):
        """Handle operation completion.

        Args:
            success: Whether operation was successful
            message: Result message
        """
        # Re-enable UI
        self.setEnabled(True)

        # Show result
        self.status_label.setText(message)

        if success:
            # Refresh user list
            self.refresh_users()
        else:
            # Show error message
            QMessageBox.critical(self, "Operation Failed", message)

    def on_connection_changed(self, index):
        """Handle connection type change.

        Args:
            index: Selected index
        """
        if index == 0:
            # No connection selected
            self.client = None
            self.users_table.setRowCount(0)
            self.users = []
            self.status_label.setText("No connection selected")
        elif index == 1:
            # Redfish connection
            if hasattr(self.parent(), "get_redfish_client"):
                redfish_client = self.parent().get_redfish_client()
                if redfish_client and redfish_client.is_connected():
                    from greenfish.core.user import UserManagementClient
                    self.client = UserManagementClient()
                    self.client.connect_redfish(redfish_client)
                    self.refresh_users()
                else:
                    self.status_label.setText("Redfish client not connected")
            else:
                self.status_label.setText("Redfish client not available")
        elif index == 2:
            # IPMI connection
            if hasattr(self.parent(), "get_ipmi_client"):
                ipmi_client = self.parent().get_ipmi_client()
                if ipmi_client and ipmi_client.is_connected():
                    from greenfish.core.user import UserManagementClient
                    self.client = UserManagementClient()
                    self.client.connect_ipmi(ipmi_client)
                    self.refresh_users()
                else:
                    self.status_label.setText("IPMI client not connected")
            else:
                self.status_label.setText("IPMI client not available")
