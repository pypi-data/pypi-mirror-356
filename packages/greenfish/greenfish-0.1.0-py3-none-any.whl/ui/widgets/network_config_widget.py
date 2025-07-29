"""Network Configuration Widget."""
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                           QLabel, QComboBox, QTableWidget, QTableWidgetItem,
                           QHeaderView, QMessageBox, QGroupBox, QTabWidget,
                           QFormLayout, QLineEdit, QCheckBox, QSpinBox,
                           QRadioButton, QButtonGroup, QGridLayout)
from PyQt5.QtCore import Qt, pyqtSignal, QThread

from greenfish.utils.logger import Logger

class NetworkWorker(QThread):
    """Worker thread for network operations."""

    finished = pyqtSignal(bool, str)

    def __init__(self, client, operation, interface=None, config=None):
        """Initialize worker thread.

        Args:
            client: Network client
            operation: Operation to perform
            interface: Network interface
            config: Network configuration
        """
        super().__init__()
        self.client = client
        self.operation = operation
        self.interface = interface
        self.config = config

    def run(self):
        """Run the operation."""
        try:
            result = False
            message = ""

            if self.operation == "apply":
                # Apply network configuration
                result = self.client.apply_network_config(
                    self.interface, self.config
                )

                if result:
                    message = f"Successfully applied network configuration to {self.interface}"
                else:
                    message = f"Failed to apply network configuration to {self.interface}"

            elif self.operation == "reset":
                # Reset network configuration
                result = self.client.reset_network_config(self.interface)

                if result:
                    message = f"Successfully reset network configuration for {self.interface}"
                else:
                    message = f"Failed to reset network configuration for {self.interface}"

            self.finished.emit(result, message)

        except Exception as e:
            Logger.error(f"Error in network operation: {str(e)}")
            self.finished.emit(False, f"Error: {str(e)}")


class NetworkConfigWidget(QWidget):
    """Network Configuration widget."""

    def __init__(self, parent=None):
        """Initialize widget.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.client = None
        self.interfaces = []
        self.worker = None

        self.init_ui()

    def init_ui(self):
        """Initialize UI components."""
        # Main layout
        main_layout = QVBoxLayout(self)

        # Controls
        controls_layout = QHBoxLayout()

        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh_interfaces)

        self.connection_combo = QComboBox()
        self.connection_combo.addItem("Select Connection Type")
        self.connection_combo.addItem("Redfish")
        self.connection_combo.addItem("IPMI")
        self.connection_combo.currentIndexChanged.connect(self.on_connection_changed)

        controls_layout.addWidget(QLabel("Connection:"))
        controls_layout.addWidget(self.connection_combo)
        controls_layout.addStretch()
        controls_layout.addWidget(self.refresh_button)

        # Tab widget for interfaces
        self.tabs = QTabWidget()

        # Status label
        self.status_label = QLabel()

        # Add widgets to main layout
        main_layout.addLayout(controls_layout)
        main_layout.addWidget(self.tabs)
        main_layout.addWidget(self.status_label)

    def set_client(self, client):
        """Set network client.

        Args:
            client: Network client
        """
        self.client = client
        self.refresh_interfaces()

    def refresh_interfaces(self):
        """Refresh network interfaces."""
        if not self.client or not self.client.is_connected():
            self.status_label.setText("Not connected to a server")
            self.clear_tabs()
            self.interfaces = []
            return

        try:
            # Get network interfaces
            self.interfaces = self.client.get_network_interfaces()

            # Update tabs
            self.update_tabs()

            self.status_label.setText(f"Found {len(self.interfaces)} network interfaces")

        except Exception as e:
            Logger.error(f"Error refreshing network interfaces: {str(e)}")
            self.status_label.setText(f"Error: {str(e)}")

    def clear_tabs(self):
        """Clear all tabs."""
        while self.tabs.count() > 0:
            self.tabs.removeTab(0)

    def update_tabs(self):
        """Update tabs with current interfaces."""
        self.clear_tabs()

        for interface in self.interfaces:
            # Create tab for interface
            interface_widget = QWidget()
            interface_layout = QVBoxLayout(interface_widget)

            # Interface details
            details_group = QGroupBox("Interface Details")
            details_layout = QFormLayout()

            # ID
            id_label = QLabel(interface.get("id", ""))
            details_layout.addRow("ID:", id_label)

            # Name
            name_label = QLabel(interface.get("name", ""))
            details_layout.addRow("Name:", name_label)

            # MAC Address
            mac_label = QLabel(interface.get("mac_address", ""))
            details_layout.addRow("MAC Address:", mac_label)

            # Status
            status_label = QLabel(interface.get("status", ""))
            details_layout.addRow("Status:", status_label)

            # Speed
            speed_label = QLabel(f"{interface.get('speed', 0)} Mbps")
            details_layout.addRow("Speed:", speed_label)

            # MTU
            mtu_label = QLabel(str(interface.get("mtu", 0)))
            details_layout.addRow("MTU:", mtu_label)

            details_group.setLayout(details_layout)

            # IP Configuration
            ip_group = QGroupBox("IP Configuration")
            ip_layout = QVBoxLayout()

            # DHCP/Static selection
            ip_mode_group = QWidget()
            ip_mode_layout = QHBoxLayout(ip_mode_group)
            ip_mode_layout.setContentsMargins(0, 0, 0, 0)

            self.dhcp_radio = QRadioButton("DHCP")
            self.static_radio = QRadioButton("Static IP")

            ip_mode_group_buttons = QButtonGroup(ip_mode_group)
            ip_mode_group_buttons.addButton(self.dhcp_radio)
            ip_mode_group_buttons.addButton(self.static_radio)

            # Set current mode
            if interface.get("dhcp_enabled", True):
                self.dhcp_radio.setChecked(True)
            else:
                self.static_radio.setChecked(True)

            # Connect signals
            self.dhcp_radio.toggled.connect(self.on_ip_mode_changed)
            self.static_radio.toggled.connect(self.on_ip_mode_changed)

            ip_mode_layout.addWidget(self.dhcp_radio)
            ip_mode_layout.addWidget(self.static_radio)
            ip_mode_layout.addStretch()

            ip_layout.addWidget(ip_mode_group)

            # Static IP settings
            static_group = QGroupBox("Static IP Settings")
            static_layout = QFormLayout()

            # IP Address
            self.ip_edit = QLineEdit(interface.get("ip_address", ""))
            static_layout.addRow("IP Address:", self.ip_edit)

            # Subnet Mask
            self.subnet_edit = QLineEdit(interface.get("subnet_mask", ""))
            static_layout.addRow("Subnet Mask:", self.subnet_edit)

            # Gateway
            self.gateway_edit = QLineEdit(interface.get("gateway", ""))
            static_layout.addRow("Gateway:", self.gateway_edit)

            # DNS Servers
            self.dns1_edit = QLineEdit("")
            self.dns2_edit = QLineEdit("")

            # Set DNS servers if available
            dns_servers = interface.get("dns_servers", [])
            if len(dns_servers) > 0:
                self.dns1_edit.setText(dns_servers[0])
            if len(dns_servers) > 1:
                self.dns2_edit.setText(dns_servers[1])

            static_layout.addRow("Primary DNS:", self.dns1_edit)
            static_layout.addRow("Secondary DNS:", self.dns2_edit)

            static_group.setLayout(static_layout)
            ip_layout.addWidget(static_group)

            # Enable/disable static settings based on current mode
            static_group.setEnabled(not interface.get("dhcp_enabled", True))

            # VLAN settings
            vlan_group = QGroupBox("VLAN Settings")
            vlan_layout = QFormLayout()

            # VLAN Enabled
            self.vlan_check = QCheckBox("Enable VLAN")
            self.vlan_check.setChecked(interface.get("vlan_enabled", False))
            self.vlan_check.toggled.connect(self.on_vlan_toggled)

            # VLAN ID
            self.vlan_id_spin = QSpinBox()
            self.vlan_id_spin.setRange(1, 4094)
            self.vlan_id_spin.setValue(interface.get("vlan_id", 1))
            self.vlan_id_spin.setEnabled(interface.get("vlan_enabled", False))

            vlan_layout.addRow("", self.vlan_check)
            vlan_layout.addRow("VLAN ID:", self.vlan_id_spin)

            vlan_group.setLayout(vlan_layout)
            ip_layout.addWidget(vlan_group)

            ip_group.setLayout(ip_layout)

            # Actions
            actions_group = QGroupBox("Actions")
            actions_layout = QHBoxLayout()

            self.apply_button = QPushButton("Apply Settings")
            self.apply_button.clicked.connect(lambda: self.apply_settings(interface))

            self.reset_button = QPushButton("Reset")
            self.reset_button.clicked.connect(lambda: self.reset_settings(interface))

            actions_layout.addWidget(self.apply_button)
            actions_layout.addWidget(self.reset_button)

            actions_group.setLayout(actions_layout)

            # Add groups to interface layout
            interface_layout.addWidget(details_group)
            interface_layout.addWidget(ip_group)
            interface_layout.addWidget(actions_group)
            interface_layout.addStretch()

            # Add tab
            self.tabs.addTab(interface_widget, interface.get("name", f"Interface {interface.get('id', '')}"))

    def on_ip_mode_changed(self, checked):
        """Handle IP mode change.

        Args:
            checked: Whether the radio button is checked
        """
        if not checked:
            return

        # Get current tab widget
        current_widget = self.tabs.currentWidget()
        if not current_widget:
            return

        # Find static group
        static_group = None
        for i in range(current_widget.layout().count()):
            item = current_widget.layout().itemAt(i)
            if item and item.widget() and isinstance(item.widget(), QGroupBox):
                if item.widget().title() == "IP Configuration":
                    ip_group = item.widget()
                    for j in range(ip_group.layout().count()):
                        sub_item = ip_group.layout().itemAt(j)
                        if sub_item and sub_item.widget() and isinstance(sub_item.widget(), QGroupBox):
                            if sub_item.widget().title() == "Static IP Settings":
                                static_group = sub_item.widget()
                                break
                    break

        if static_group:
            # Enable/disable static settings based on mode
            static_group.setEnabled(self.static_radio.isChecked())

    def on_vlan_toggled(self, checked):
        """Handle VLAN toggle.

        Args:
            checked: Whether the checkbox is checked
        """
        # Get current tab widget
        current_widget = self.tabs.currentWidget()
        if not current_widget:
            return

        # Find VLAN ID spinbox
        for i in range(current_widget.layout().count()):
            item = current_widget.layout().itemAt(i)
            if item and item.widget() and isinstance(item.widget(), QGroupBox):
                if item.widget().title() == "IP Configuration":
                    ip_group = item.widget()
                    for j in range(ip_group.layout().count()):
                        sub_item = ip_group.layout().itemAt(j)
                        if sub_item and sub_item.widget() and isinstance(sub_item.widget(), QGroupBox):
                            if sub_item.widget().title() == "VLAN Settings":
                                vlan_group = sub_item.widget()
                                for k in range(vlan_group.layout().rowCount()):
                                    label = vlan_group.layout().itemAt(k, QFormLayout.LabelRole)
                                    field = vlan_group.layout().itemAt(k, QFormLayout.FieldRole)
                                    if label and field and label.widget() and isinstance(label.widget(), QLabel):
                                        if label.widget().text() == "VLAN ID:":
                                            field.widget().setEnabled(checked)
                                            break
                                break
                    break

    def apply_settings(self, interface):
        """Apply network settings.

        Args:
            interface: Network interface
        """
        # Get current tab widget
        current_widget = self.tabs.currentWidget()
        if not current_widget:
            return

        # Build configuration
        config = {}

        # DHCP/Static
        config["dhcp_enabled"] = self.dhcp_radio.isChecked()

        # Static IP settings
        if not config["dhcp_enabled"]:
            config["ip_address"] = self.ip_edit.text()
            config["subnet_mask"] = self.subnet_edit.text()
            config["gateway"] = self.gateway_edit.text()

            # DNS servers
            dns_servers = []
            if self.dns1_edit.text():
                dns_servers.append(self.dns1_edit.text())
            if self.dns2_edit.text():
                dns_servers.append(self.dns2_edit.text())

            config["dns_servers"] = dns_servers

        # VLAN settings
        config["vlan_enabled"] = self.vlan_check.isChecked()
        if config["vlan_enabled"]:
            config["vlan_id"] = self.vlan_id_spin.value()

        # Validate IP address format
        if not config["dhcp_enabled"]:
            import re
            ip_pattern = r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$"

            if not re.match(ip_pattern, config["ip_address"]):
                QMessageBox.warning(self, "Invalid IP Address", "Please enter a valid IP address")
                return

            if not re.match(ip_pattern, config["subnet_mask"]):
                QMessageBox.warning(self, "Invalid Subnet Mask", "Please enter a valid subnet mask")
                return

            if config["gateway"] and not re.match(ip_pattern, config["gateway"]):
                QMessageBox.warning(self, "Invalid Gateway", "Please enter a valid gateway address")
                return

            for dns in config["dns_servers"]:
                if not re.match(ip_pattern, dns):
                    QMessageBox.warning(self, "Invalid DNS Server", "Please enter valid DNS server addresses")
                    return

        # Confirm changes
        reply = QMessageBox.question(
            self, "Apply Network Settings",
            f"Are you sure you want to apply these network settings to {interface.get('name', '')}?\n\n"
            "This may cause temporary network disruption.",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            # Disable UI during operation
            self.setEnabled(False)
            self.status_label.setText(f"Applying network settings to {interface.get('name', '')}...")

            # Start worker thread
            self.worker = NetworkWorker(
                self.client, "apply", interface.get("id", ""), config
            )
            self.worker.finished.connect(self.on_operation_finished)
            self.worker.start()

    def reset_settings(self, interface):
        """Reset network settings.

        Args:
            interface: Network interface
        """
        # Confirm reset
        reply = QMessageBox.question(
            self, "Reset Network Settings",
            f"Are you sure you want to reset the network settings for {interface.get('name', '')}?\n\n"
            "This will restore the default configuration and may cause temporary network disruption.",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            # Disable UI during operation
            self.setEnabled(False)
            self.status_label.setText(f"Resetting network settings for {interface.get('name', '')}...")

            # Start worker thread
            self.worker = NetworkWorker(
                self.client, "reset", interface.get("id", "")
            )
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
            # Refresh interfaces
            self.refresh_interfaces()
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
            self.clear_tabs()
            self.interfaces = []
            self.status_label.setText("No connection selected")
        elif index == 1:
            # Redfish connection
            if hasattr(self.parent(), "get_redfish_client"):
                redfish_client = self.parent().get_redfish_client()
                if redfish_client and redfish_client.is_connected():
                    from greenfish.core.network import NetworkClient
                    self.client = NetworkClient()
                    self.client.connect_redfish(redfish_client)
                    self.refresh_interfaces()
                else:
                    self.status_label.setText("Redfish client not connected")
            else:
                self.status_label.setText("Redfish client not available")
        elif index == 2:
            # IPMI connection
            if hasattr(self.parent(), "get_ipmi_client"):
                ipmi_client = self.parent().get_ipmi_client()
                if ipmi_client and ipmi_client.is_connected():
                    from greenfish.core.network import NetworkClient
                    self.client = NetworkClient()
                    self.client.connect_ipmi(ipmi_client)
                    self.refresh_interfaces()
                else:
                    self.status_label.setText("IPMI client not connected")
            else:
                self.status_label.setText("IPMI client not available")
