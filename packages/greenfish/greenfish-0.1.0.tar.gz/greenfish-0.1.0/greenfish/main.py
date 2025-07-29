import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QSplitter, QTreeWidget, QTreeWidgetItem,
                             QMessageBox, QStatusBar, QTabWidget, QMenu, QMenuBar)
from PyQt6.QtCore import Qt, QSize, pyqtSlot, QTimer
from PyQt6.QtGui import QAction, QKeySequence

from greenfish.ui.dialogs.connection_dialog import ConnectionDialog
from greenfish.ui.dialogs.settings_dialog import SettingsDialog
from greenfish.ui.widgets.system_info_widget import SystemInfoWidget
from greenfish.ui.widgets.dashboard_widget import DashboardWidget
from greenfish.ui.widgets.task_monitor_widget import TaskMonitorWidget
from greenfish.ui.widgets.bios_config_widget import BiosConfigWidget
from greenfish.ui.widgets.firmware_widget import FirmwareWidget
from greenfish.ui.widgets.account_widget import AccountWidget
from greenfish.ui.widgets.secure_boot_widget import SecureBootWidget
from greenfish.ui.widgets.event_subscription_widget import EventSubscriptionWidget
from greenfish.ui.widgets.log_widget import LogWidget
from greenfish.core.redfish_client import RedfishClient
from greenfish.config.settings import settings
from greenfish.config.themes import ThemeManager
from greenfish.utils.logger import Logger
from greenfish.ui.dialogs.profile_dialog import ProfileDialog
from greenfish.ui.widgets.metrics import MetricsWidget
from greenfish.config.config_manager import ConfigManager
from greenfish.config.connection_profile import ConnectionProfile

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Redfish Desktop")
        self.setMinimumSize(1200, 800)

        # Removed transparency for glass effect

        # Create central widget with layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Create splitter for resizable sections
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Create navigation tree
        self.nav_tree = QTreeWidget()
        self.nav_tree.setHeaderLabels(["Redfish Resources"])
        self.nav_tree.setMinimumWidth(250)
        self.setup_navigation_tree()
        self.nav_tree.itemClicked.connect(self.handle_tree_item_click)
        splitter.addWidget(self.nav_tree)

        # Create content area with tabs
        self.content_tabs = QTabWidget()

        # Create and add dashboard tab
        self.dashboard = DashboardWidget()
        self.content_tabs.addTab(self.dashboard, "Dashboard")

        # Create and add system info tab
        self.system_info = SystemInfoWidget()
        self.content_tabs.addTab(self.system_info, "System Information")

        # Create and add BIOS configuration tab
        self.bios_config = BiosConfigWidget()
        self.content_tabs.addTab(self.bios_config, "BIOS Configuration")

        # Create and add firmware management tab
        self.firmware_widget = FirmwareWidget()
        self.content_tabs.addTab(self.firmware_widget, "Firmware Management")

        # Create and add task monitor tab
        self.task_monitor = TaskMonitorWidget()
        self.content_tabs.addTab(self.task_monitor, "Task Monitor")

        # Create and add account management tab
        self.account_widget = AccountWidget()
        self.content_tabs.addTab(self.account_widget, "User Accounts")

        # Create and add secure boot tab
        self.secure_boot = SecureBootWidget()
        self.content_tabs.addTab(self.secure_boot, "Secure Boot")

        # Create and add event subscription tab
        self.event_widget = EventSubscriptionWidget()
        self.content_tabs.addTab(self.event_widget, "Event Subscriptions")

        # Create and add log management tab
        self.log_widget = LogWidget()
        self.content_tabs.addTab(self.log_widget, "System Logs")

        # Create and add metrics tab
        self.metrics_widget = MetricsWidget()
        self.content_tabs.addTab(self.metrics_widget, "Metrics & Reporting")

        splitter.addWidget(self.content_tabs)

        # Set initial splitter sizes
        splitter.setSizes([250, 950])
        main_layout.addWidget(splitter)

        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Not connected")

        # Setup menu bar
        self.setup_menu()

        # Setup keyboard shortcuts
        self.setup_shortcuts()

        # Initialize Redfish client
        self.redfish_client = None

        # Initialize theme manager
        self.theme_manager = ThemeManager()

        # Apply theme from settings
        self.apply_theme(settings.get_theme())

        # Set up auto-refresh timer
        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self.refresh_data)
        self.start_refresh_timer()

    def apply_theme(self, theme_name):
        """Apply theme to the application."""
        stylesheet = self.theme_manager.get_stylesheet(theme_name)
        self.setStyleSheet(stylesheet)

    def setup_menu(self):
        # File menu
        file_menu = self.menuBar().addMenu("&File")

        new_connection = QAction("&New Connection", self)
        new_connection.setShortcut(QKeySequence("Ctrl+N"))
        new_connection.triggered.connect(self.show_connection_dialog)
        file_menu.addAction(new_connection)

        manage_profiles = QAction("&Manage Profiles", self)
        manage_profiles.triggered.connect(self.show_profile_dialog)
        file_menu.addAction(manage_profiles)

        save_config = QAction("&Save Configuration", self)
        save_config.setShortcut(QKeySequence("Ctrl+S"))
        file_menu.addAction(save_config)

        file_menu.addSeparator()

        exit_action = QAction("E&xit", self)
        exit_action.setShortcut(QKeySequence("Ctrl+Q"))
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # View menu
        view_menu = self.menuBar().addMenu("&View")

        refresh_action = QAction("&Refresh", self)
        refresh_action.setShortcut(QKeySequence("F5"))
        refresh_action.triggered.connect(self.refresh_data)
        view_menu.addAction(refresh_action)

        # Settings menu
        settings_menu = self.menuBar().addMenu("&Settings")

        preferences_action = QAction("&Preferences", self)
        preferences_action.setShortcut(QKeySequence("Ctrl+P"))
        preferences_action.triggered.connect(self.show_settings_dialog)
        settings_menu.addAction(preferences_action)

        # Add account management to Settings menu
        settings_menu.addSeparator()
        account_action = QAction("&User Accounts", self)
        account_action.triggered.connect(lambda: self.content_tabs.setCurrentWidget(self.account_widget))
        settings_menu.addAction(account_action)

        # System menu
        system_menu = self.menuBar().addMenu("&System")

        # Add BIOS configuration action
        bios_action = QAction("&BIOS Configuration", self)
        bios_action.triggered.connect(self.show_bios_config)
        system_menu.addAction(bios_action)

        # Add firmware management action
        firmware_action = QAction("&Firmware Management", self)
        firmware_action.triggered.connect(self.show_firmware_management)
        system_menu.addAction(firmware_action)

        # Add secure boot to System menu
        system_menu.addSeparator()
        secure_boot_action = QAction("&Secure Boot", self)
        secure_boot_action.triggered.connect(lambda: self.content_tabs.setCurrentWidget(self.secure_boot))
        system_menu.addAction(secure_boot_action)

        # Add event subscriptions to System menu
        event_action = QAction("&Event Subscriptions", self)
        event_action.triggered.connect(lambda: self.content_tabs.setCurrentWidget(self.event_widget))
        system_menu.addAction(event_action)

        # Add logs to System menu
        logs_action = QAction("System &Logs", self)
        logs_action.triggered.connect(lambda: self.content_tabs.setCurrentWidget(self.log_widget))
        system_menu.addAction(logs_action)

        system_menu.addSeparator()

        power_on = QAction("Power &On", self)
        power_on.triggered.connect(lambda: self.power_action("On"))
        system_menu.addAction(power_on)

        power_off = QAction("Power O&ff", self)
        power_off.triggered.connect(lambda: self.power_action("Off"))
        system_menu.addAction(power_off)

        reboot = QAction("&Reboot", self)
        reboot.triggered.connect(lambda: self.power_action("GracefulRestart"))
        system_menu.addAction(reboot)

        # Help menu
        help_menu = self.menuBar().addMenu("&Help")

        help_action = QAction("&Help", self)
        help_action.setShortcut(QKeySequence("F1"))
        help_menu.addAction(help_action)

    def setup_shortcuts(self):
        # Additional shortcuts
        search_action = QAction("Search", self)
        search_action.setShortcut(QKeySequence("Ctrl+F"))
        self.addAction(search_action)

        history_action = QAction("History", self)
        history_action.setShortcut(QKeySequence("Ctrl+H"))
        self.addAction(history_action)

    def setup_navigation_tree(self):
        """Setup the navigation tree with Redfish resources."""
        # Systems
        systems_item = QTreeWidgetItem(self.nav_tree, ["Systems"])
        QTreeWidgetItem(systems_item, ["System 1"])

        # BIOS
        bios_item = QTreeWidgetItem(systems_item, ["BIOS Settings"])

        # Firmware
        firmware_item = QTreeWidgetItem(self.nav_tree, ["Update Service"])
        QTreeWidgetItem(firmware_item, ["Firmware Inventory"])
        QTreeWidgetItem(firmware_item, ["Update Firmware"])

        # Chassis
        chassis_item = QTreeWidgetItem(self.nav_tree, ["Chassis"])
        QTreeWidgetItem(chassis_item, ["Chassis 1"])

        # Managers
        managers_item = QTreeWidgetItem(self.nav_tree, ["Managers"])
        QTreeWidgetItem(managers_item, ["Manager 1"])

        # Storage
        storage_item = QTreeWidgetItem(self.nav_tree, ["Storage"])
        QTreeWidgetItem(storage_item, ["Storage 1"])

        # Network
        network_item = QTreeWidgetItem(self.nav_tree, ["Network"])
        QTreeWidgetItem(network_item, ["Ethernet Interfaces"])

        # Tasks
        tasks_item = QTreeWidgetItem(self.nav_tree, ["Tasks"])
        QTreeWidgetItem(tasks_item, ["Active Tasks"])

        # Expand all items
        self.nav_tree.expandAll()

    def handle_tree_item_click(self, item, column):
        """Handle clicks on navigation tree items."""
        if not self.redfish_client or not self.redfish_client.connected:
            QMessageBox.warning(self, "Not Connected", "Please establish a connection first")
            return

        # Get the item text and parent text
        item_text = item.text(0)
        parent = item.parent()
        parent_text = parent.text(0) if parent else None

        try:
            if parent_text == "Systems" and item_text.startswith("System"):
                # Get system ID from item text
                system_id = item_text.split(" ")[1]
                self.load_system_info(system_id)
                self.content_tabs.setCurrentWidget(self.system_info)

            elif item_text == "BIOS Settings":
                self.load_bios_settings()
                self.content_tabs.setCurrentWidget(self.bios_config)

            elif parent_text == "Update Service" and item_text == "Firmware Inventory":
                self.load_firmware_inventory()
                self.content_tabs.setCurrentWidget(self.firmware_widget)

            elif parent_text == "Update Service" and item_text == "Update Firmware":
                self.load_firmware_inventory()
                self.content_tabs.setCurrentWidget(self.firmware_widget)

            elif parent_text == "Tasks" and item_text == "Active Tasks":
                # Refresh task list
                self.refresh_tasks()
                self.content_tabs.setCurrentWidget(self.task_monitor)

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def show_connection_dialog(self):
        """Show the connection dialog and handle connection."""
        dialog = ConnectionDialog(self)
        dialog.connection_established.connect(self.handle_connection)
        dialog.exec()

    def handle_connection(self, params):
        """Handle new Redfish connection."""
        try:
            # Create new Redfish client
            self.redfish_client = RedfishClient(
                base_url=params["base_url"],
                username=params["username"],
                password=params["password"]
            )

            # Connect to service
            self.redfish_client.connect(auth=params["auth"])

            # Update status
            success_msg = f"Connected to {params['base_url']}"
            Logger.success(success_msg)
            self.status_bar.showMessage(success_msg)

            # Refresh data
            self.refresh_data()

            # Update account widget
            self.account_widget.set_redfish_client(self.redfish_client)

            # Update secure boot widget
            self.secure_boot.set_redfish_client(self.redfish_client)

            # Update event subscription widget
            self.event_widget.set_redfish_client(self.redfish_client)

            # Update log widget
            self.log_widget.set_redfish_client(self.redfish_client)

            # Update metrics widget
            self.metrics_widget.set_client(self.redfish_client, self.redfish_client.get_system()[0]['Id'], self.redfish_client.get_chassis()[0]['Id'])

        except Exception as e:
            error_msg = f"Connection Error: {str(e)}"
            Logger.error(error_msg)
            QMessageBox.critical(self, "Connection Error", error_msg)
            self.status_bar.showMessage("Connection failed")

    def refresh_data(self):
        """Refresh the displayed data."""
        if not self.redfish_client or not self.redfish_client.connected:
            error_msg = "Please establish a connection first"
            Logger.warning(error_msg)
            QMessageBox.warning(self, "Not Connected", error_msg)
            return

        try:
            # Switch to dashboard tab
            self.content_tabs.setCurrentWidget(self.dashboard)

            # Get system information
            Logger.info("Fetching system information...")
            system_data = self.redfish_client.get_system()

            # Update dashboard
            self.dashboard.update_dashboard(system_data)

            # Update system info widget
            self.system_info.update_system_info(system_data)

            # Refresh tasks
            self.refresh_tasks()

            # Update metrics widget
            self.metrics_widget.refresh_metrics()

            # Update status
            success_msg = "Data refreshed successfully"
            Logger.success(success_msg)
            self.status_bar.showMessage(success_msg)

        except Exception as e:
            error_msg = f"Refresh Error: {str(e)}"
            Logger.error(error_msg)
            QMessageBox.critical(self, "Refresh Error", error_msg)
            self.status_bar.showMessage("Failed to refresh data")

    def load_system_info(self, system_id: str):
        """Load system information for specific system."""
        if not self.redfish_client or not self.redfish_client.connected:
            return

        # Get system data
        system_data = self.redfish_client.get_system(system_id)

        # Update system info widget
        self.system_info.update_system_info(system_data)

        # Update status
        self.status_bar.showMessage(f"Loaded system {system_id}")

    def refresh_tasks(self):
        """Refresh task list."""
        if not self.redfish_client or not self.redfish_client.connected:
            return

        # Update tasks in Redfish client
        self.redfish_client.update_tasks()

        # Get all tasks
        tasks = self.redfish_client.get_tasks()

        # Update task monitor widget
        for task in tasks:
            self.task_monitor.add_task(task)

    def power_action(self, action: str):
        """Perform power action on system."""
        if not self.redfish_client or not self.redfish_client.connected:
            QMessageBox.warning(self, "Not Connected", "Please establish a connection first")
            return

        try:
            # Confirm action
            confirm = QMessageBox.question(self, "Confirm Power Action",
                                          f"Are you sure you want to perform the '{action}' action?")
            if confirm != QMessageBox.StandardButton.Yes:
                return

            # Perform power action
            result = self.redfish_client.reset_system(reset_type=action)

            # Check if action resulted in a task
            if isinstance(result, dict) and result.get("is_task"):
                task_id = result.get("task_id")
                task = result.get("task")

                # Add task to monitor
                self.task_monitor.add_task(task)

                # Show task monitor tab
                self.content_tabs.setCurrentWidget(self.task_monitor)

                # Update status
                self.status_bar.showMessage(f"Power action '{action}' initiated (Task ID: {task_id})")
            else:
                # Refresh data
                self.refresh_data()

                # Update status
                self.status_bar.showMessage(f"Power action '{action}' completed successfully")

        except Exception as e:
            QMessageBox.critical(self, "Power Action Error", str(e))
            self.status_bar.showMessage(f"Failed to perform power action '{action}'")

    def show_bios_config(self):
        """Show BIOS configuration tab."""
        if not self.redfish_client or not self.redfish_client.connected:
            QMessageBox.warning(self, "Not Connected", "Please establish a connection first")
            return

        self.load_bios_settings()
        self.content_tabs.setCurrentWidget(self.bios_config)

    def load_bios_settings(self, system_id: str = "1"):
        """Load BIOS settings."""
        if not self.redfish_client or not self.redfish_client.connected:
            return

        try:
            # Get BIOS settings
            self.status_bar.showMessage("Loading BIOS settings...")
            bios_data = self.redfish_client.get_bios_settings(system_id)

            # Update BIOS config widget
            self.bios_config.load_bios_data(bios_data)

            # Get pending settings if available
            try:
                pending_settings = self.redfish_client.get_bios_pending_settings(system_id)
                self.bios_config.update_pending_table(pending_settings)
            except Exception:
                # Pending settings might not be available, ignore
                pass

            # Connect refresh button
            self.bios_config.refresh_button.clicked.disconnect()
            self.bios_config.refresh_button.clicked.connect(lambda: self.load_bios_settings(system_id))

            # Connect apply button
            self.bios_config.apply_button.clicked.disconnect()
            self.bios_config.apply_button.clicked.connect(lambda: self.apply_bios_settings(system_id))

            # Update status
            self.status_bar.showMessage("BIOS settings loaded successfully")

        except Exception as e:
            self.status_bar.showMessage(f"Failed to load BIOS settings: {str(e)}")
            raise

    def apply_bios_settings(self, system_id: str = "1"):
        """Apply modified BIOS settings."""
        if not self.redfish_client or not self.redfish_client.connected:
            return

        # Get modified attributes
        modified_attrs = self.bios_config.get_modified_attributes()
        if not modified_attrs:
            return

        # Confirm changes
        confirm = QMessageBox.question(
            self,
            "Confirm BIOS Changes",
            f"Are you sure you want to apply {len(modified_attrs)} BIOS setting changes?\n\n"
            "Note: A system reboot will be required for changes to take effect.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm != QMessageBox.StandardButton.Yes:
            return

        try:
            # Apply changes
            self.status_bar.showMessage("Applying BIOS changes...")
            result = self.redfish_client.update_bios_settings(modified_attrs, system_id)

            # Check if action resulted in a task
            if isinstance(result, dict) and result.get("is_task"):
                task_id = result.get("task_id")
                task = result.get("task")

                # Add task to monitor
                self.task_monitor.add_task(task)

                # Show task monitor tab
                self.content_tabs.setCurrentWidget(self.task_monitor)

                QMessageBox.information(
                    self,
                    "BIOS Update Task Created",
                    f"BIOS update task created (ID: {task_id}).\n\n"
                    "You can monitor the progress in the Task Monitor tab."
                )

                # Update status
                self.status_bar.showMessage(f"BIOS changes submitted (Task ID: {task_id})")
            else:
                QMessageBox.information(
                    self,
                    "BIOS Update Submitted",
                    "BIOS changes submitted successfully.\n\n"
                    "A system reboot will be required for changes to take effect."
                )

                # Update status
                self.status_bar.showMessage("BIOS changes submitted successfully")

                # Reload BIOS settings
                self.load_bios_settings(system_id)

        except Exception as e:
            QMessageBox.critical(self, "BIOS Update Error", str(e))
            self.status_bar.showMessage(f"Failed to apply BIOS changes: {str(e)}")

    def show_firmware_management(self):
        """Show firmware management tab."""
        if not self.redfish_client or not self.redfish_client.connected:
            QMessageBox.warning(self, "Not Connected", "Please establish a connection first")
            return

        self.load_firmware_inventory()
        self.content_tabs.setCurrentWidget(self.firmware_widget)

    def load_firmware_inventory(self):
        """Load firmware inventory data."""
        if not self.redfish_client or not self.redfish_client.connected:
            return

        try:
            # Get firmware inventory
            self.status_bar.showMessage("Loading firmware inventory...")
            firmware_data = self.redfish_client.get_firmware_inventory()

            # Update firmware widget
            self.firmware_widget.load_firmware_data(firmware_data)

            # Connect refresh button
            self.firmware_widget.refresh_button.clicked.disconnect()
            self.firmware_widget.refresh_button.clicked.connect(self.load_firmware_inventory)

            # Connect upload button
            self.firmware_widget.upload_button.clicked.connect(self.upload_firmware)

            # Connect update button
            self.firmware_widget.update_button.clicked.connect(self.update_firmware_from_uri)

            # Update status
            self.status_bar.showMessage("Firmware inventory loaded successfully")

        except Exception as e:
            self.status_bar.showMessage(f"Failed to load firmware inventory: {str(e)}")
            raise

    def upload_firmware(self):
        """Upload firmware image and apply update."""
        if not self.redfish_client or not self.redfish_client.connected:
            return

        file_path = self.firmware_widget.selected_file
        if not file_path:
            return

        try:
            # Upload firmware image
            self.status_bar.showMessage(f"Uploading firmware image: {file_path}...")
            result = self.redfish_client.upload_firmware_image(file_path)

            # Check if action resulted in a task
            if isinstance(result, dict) and result.get("is_task"):
                task_id = result.get("task_id")
                task = result.get("task")

                # Add task to monitor
                self.task_monitor.add_task(task)

                # Show task monitor tab
                self.content_tabs.setCurrentWidget(self.task_monitor)

                QMessageBox.information(
                    self,
                    "Firmware Update Task Created",
                    f"Firmware upload task created (ID: {task_id}).\n\n"
                    "You can monitor the progress in the Task Monitor tab."
                )

                # Update status
                self.status_bar.showMessage(f"Firmware upload initiated (Task ID: {task_id})")
            else:
                QMessageBox.information(
                    self,
                    "Firmware Uploaded",
                    "Firmware image uploaded successfully."
                )

                # Update status
                self.status_bar.showMessage("Firmware image uploaded successfully")

                # Refresh firmware inventory
                self.load_firmware_inventory()

        except Exception as e:
            QMessageBox.critical(self, "Firmware Upload Error", str(e))
            self.status_bar.showMessage(f"Failed to upload firmware: {str(e)}")

    def update_firmware_from_uri(self):
        """Update firmware from URI."""
        if not self.redfish_client or not self.redfish_client.connected:
            return

        uri = self.firmware_widget.uri_input.text().strip()
        if not uri:
            return

        try:
            # Update firmware
            self.status_bar.showMessage(f"Updating firmware from URI: {uri}...")
            result = self.redfish_client.update_firmware(uri)

            # Check if action resulted in a task
            if isinstance(result, dict) and result.get("is_task"):
                task_id = result.get("task_id")
                task = result.get("task")

                # Add task to monitor
                self.task_monitor.add_task(task)

                # Show task monitor tab
                self.content_tabs.setCurrentWidget(self.task_monitor)

                QMessageBox.information(
                    self,
                    "Firmware Update Task Created",
                    f"Firmware update task created (ID: {task_id}).\n\n"
                    "You can monitor the progress in the Task Monitor tab."
                )

                # Update status
                self.status_bar.showMessage(f"Firmware update initiated (Task ID: {task_id})")
            else:
                QMessageBox.information(
                    self,
                    "Firmware Update Submitted",
                    "Firmware update submitted successfully."
                )

                # Update status
                self.status_bar.showMessage("Firmware update submitted successfully")

                # Refresh firmware inventory
                self.load_firmware_inventory()

        except Exception as e:
            QMessageBox.critical(self, "Firmware Update Error", str(e))
            self.status_bar.showMessage(f"Failed to update firmware: {str(e)}")

    def show_settings_dialog(self):
        """Show the settings dialog."""
        dialog = SettingsDialog(self)
        dialog.settings_changed.connect(self.on_settings_changed)
        dialog.exec()

    def on_settings_changed(self):
        """Handle settings changes."""
        # Apply theme from settings
        self.apply_theme(settings.get_theme())

        # Update status
        self.status_bar.showMessage("Settings updated")

    def show_profile_dialog(self):
        """Show connection profiles dialog."""
        dialog = ProfileDialog(self)
        dialog.profile_selected.connect(self.connect_from_profile)
        dialog.exec()

    def connect_from_profile(self, profile):
        """Connect using a connection profile."""
        params = {
            "base_url": profile.base_url,
            "username": profile.username,
            "password": profile.password,
            "auth": profile.auth_type
        }
        self.handle_connection(params)

    def closeEvent(self, event):
        """Handle window close event."""
        if self.redfish_client and self.redfish_client.connected:
            self.redfish_client.disconnect()
        event.accept()

    def start_refresh_timer(self):
        """Start the auto-refresh timer based on settings"""
        # Get refresh interval from settings (in seconds)
        refresh_interval = settings.get('refresh_interval', 60)

        # Stop existing timer if running
        if self.refresh_timer.isActive():
            self.refresh_timer.stop()

        # Start timer if auto-refresh is enabled
        if settings.get('auto_refresh', True):
            self.refresh_timer.start(refresh_interval * 1000)  # Convert to milliseconds

def main():
    app = QApplication(sys.argv)

    # Enable high DPI scaling in PyQt6
    # PyQt6 handles high DPI scaling automatically

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
