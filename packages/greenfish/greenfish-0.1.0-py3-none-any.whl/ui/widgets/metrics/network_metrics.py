from PyQt6.QtWidgets import QLabel, QGridLayout, QWidget, QProgressBar
from PyQt6.QtCore import Qt

from greenfish.ui.widgets.metrics.base_panel import BaseMetricsPanel
from greenfish.utils.logger import Logger


class NetworkMetricsPanel(BaseMetricsPanel):
    """Panel for displaying network metrics"""

    def __init__(self, parent=None):
        super().__init__(parent)

    def refresh(self):
        """Refresh network metrics data"""
        if not self.client or not self.resource_id:
            self.show_error("No Redfish client or system ID available")
            return

        self.show_loading()
        self.clear_content()

        try:
            # Get system info from the client
            system_data = self.client.get_system(self.resource_id)
            if not system_data or 'EthernetInterfaces' not in system_data:
                self.show_error("No network data available")
                return

            # Get the ethernet interfaces collection
            interfaces_url = system_data['EthernetInterfaces']['@odata.id']
            interfaces_data = self.client.get_resource(interfaces_url)

            if not interfaces_data or 'Members' not in interfaces_data:
                self.show_error("No network interfaces found")
                return

            # Get detailed information for each interface
            interfaces = []
            for member in interfaces_data['Members']:
                interface_url = member['@odata.id']
                interface_data = self.client.get_resource(interface_url)
                if interface_data:
                    interfaces.append(interface_data)

            if not interfaces:
                self.show_error("No network interface details available")
                return

            self.data = interfaces
            self.hide_status()
            self.display_network_data()

        except Exception as e:
            Logger.error(f"Failed to get network metrics: {str(e)}")
            self.show_error(str(e))

    def display_network_data(self):
        """Display the network interface data in the panel"""
        if not self.data:
            return

        for i, interface in enumerate(self.data):
            # Create a section for each network interface
            interface_name = interface.get('Name', f"Network Interface {i+1}")
            interface_section, section_layout = self.create_section(interface_name)

            interface_widget = QWidget()
            interface_layout = QGridLayout(interface_widget)
            interface_layout.setContentsMargins(10, 5, 10, 5)

            row = 0

            # Basic interface information
            if 'Id' in interface:
                interface_layout.addWidget(QLabel("ID:"), row, 0)
                interface_layout.addWidget(QLabel(interface['Id']), row, 1)
                row += 1

            if 'Description' in interface:
                interface_layout.addWidget(QLabel("Description:"), row, 0)
                interface_layout.addWidget(QLabel(interface['Description']), row, 1)
                row += 1

            # MAC Address
            if 'MACAddress' in interface:
                interface_layout.addWidget(QLabel("MAC Address:"), row, 0)
                interface_layout.addWidget(QLabel(interface['MACAddress']), row, 1)
                row += 1

            # Link status
            if 'LinkStatus' in interface:
                interface_layout.addWidget(QLabel("Link Status:"), row, 0)
                status_label = QLabel(interface['LinkStatus'])

                # Set color based on link status
                if interface['LinkStatus'] == 'LinkUp':
                    status_label.setStyleSheet("color: green;")
                else:
                    status_label.setStyleSheet("color: red;")

                interface_layout.addWidget(status_label, row, 1)
                row += 1

            # Interface speed
            if 'SpeedMbps' in interface:
                interface_layout.addWidget(QLabel("Speed:"), row, 0)
                interface_layout.addWidget(QLabel(f"{interface['SpeedMbps']} Mbps"), row, 1)
                row += 1

            # Auto-negotiation
            if 'AutoNeg' in interface:
                interface_layout.addWidget(QLabel("Auto-Negotiation:"), row, 0)
                interface_layout.addWidget(QLabel("Enabled" if interface['AutoNeg'] else "Disabled"), row, 1)
                row += 1

            # Full duplex
            if 'FullDuplex' in interface:
                interface_layout.addWidget(QLabel("Duplex:"), row, 0)
                interface_layout.addWidget(QLabel("Full" if interface['FullDuplex'] else "Half"), row, 1)
                row += 1

            # MTU size
            if 'MTUSize' in interface:
                interface_layout.addWidget(QLabel("MTU Size:"), row, 0)
                interface_layout.addWidget(QLabel(str(interface['MTUSize'])), row, 1)
                row += 1

            # Status
            if 'Status' in interface:
                status = interface['Status']
                health = status.get('Health', 'Unknown')
                state = status.get('State', 'Unknown')

                interface_layout.addWidget(QLabel("Health:"), row, 0)
                health_label = QLabel(health)

                # Set color based on health
                if health == 'OK':
                    health_label.setStyleSheet("color: green;")
                elif health == 'Warning':
                    health_label.setStyleSheet("color: orange;")
                elif health == 'Critical':
                    health_label.setStyleSheet("color: red;")

                interface_layout.addWidget(health_label, row, 1)
                row += 1

                interface_layout.addWidget(QLabel("State:"), row, 0)
                interface_layout.addWidget(QLabel(state), row, 1)
                row += 1

            # Add a separator
            separator = QWidget()
            separator.setFixedHeight(1)
            separator.setStyleSheet("background-color: #cccccc;")
            interface_layout.addWidget(separator, row, 0, 1, 2)
            row += 1

            # IP configuration
            ip_title = QLabel("IP Configuration")
            ip_title.setStyleSheet("font-weight: bold;")
            interface_layout.addWidget(ip_title, row, 0, 1, 2)
            row += 1

            if 'IPv4Addresses' in interface and interface['IPv4Addresses']:
                for j, ipv4 in enumerate(interface['IPv4Addresses']):
                    if 'Address' in ipv4:
                        interface_layout.addWidget(QLabel(f"IPv4 Address {j+1}:"), row, 0)
                        interface_layout.addWidget(QLabel(ipv4['Address']), row, 1)
                        row += 1

                    if 'SubnetMask' in ipv4:
                        interface_layout.addWidget(QLabel(f"Subnet Mask {j+1}:"), row, 0)
                        interface_layout.addWidget(QLabel(ipv4['SubnetMask']), row, 1)
                        row += 1

                    if 'Gateway' in ipv4:
                        interface_layout.addWidget(QLabel(f"Gateway {j+1}:"), row, 0)
                        interface_layout.addWidget(QLabel(ipv4['Gateway']), row, 1)
                        row += 1

            if 'IPv6Addresses' in interface and interface['IPv6Addresses']:
                for j, ipv6 in enumerate(interface['IPv6Addresses']):
                    if 'Address' in ipv6:
                        interface_layout.addWidget(QLabel(f"IPv6 Address {j+1}:"), row, 0)
                        interface_layout.addWidget(QLabel(ipv6['Address']), row, 1)
                        row += 1

                    if 'PrefixLength' in ipv6:
                        interface_layout.addWidget(QLabel(f"Prefix Length {j+1}:"), row, 0)
                        interface_layout.addWidget(QLabel(str(ipv6['PrefixLength'])), row, 1)
                        row += 1

            # DNS information
            if 'NameServers' in interface and interface['NameServers']:
                # Add a separator
                separator = QWidget()
                separator.setFixedHeight(1)
                separator.setStyleSheet("background-color: #cccccc;")
                interface_layout.addWidget(separator, row, 0, 1, 2)
                row += 1

                dns_title = QLabel("DNS Configuration")
                dns_title.setStyleSheet("font-weight: bold;")
                interface_layout.addWidget(dns_title, row, 0, 1, 2)
                row += 1

                for j, dns in enumerate(interface['NameServers']):
                    interface_layout.addWidget(QLabel(f"DNS Server {j+1}:"), row, 0)
                    interface_layout.addWidget(QLabel(dns), row, 1)
                    row += 1

            # VLAN information
            if 'VLAN' in interface and interface['VLAN']:
                # Add a separator
                separator = QWidget()
                separator.setFixedHeight(1)
                separator.setStyleSheet("background-color: #cccccc;")
                interface_layout.addWidget(separator, row, 0, 1, 2)
                row += 1

                vlan_title = QLabel("VLAN Configuration")
                vlan_title.setStyleSheet("font-weight: bold;")
                interface_layout.addWidget(vlan_title, row, 0, 1, 2)
                row += 1

                vlan = interface['VLAN']

                if 'VLANId' in vlan:
                    interface_layout.addWidget(QLabel("VLAN ID:"), row, 0)
                    interface_layout.addWidget(QLabel(str(vlan['VLANId'])), row, 1)
                    row += 1

                if 'VLANEnable' in vlan:
                    interface_layout.addWidget(QLabel("VLAN Enabled:"), row, 0)
                    interface_layout.addWidget(QLabel("Yes" if vlan['VLANEnable'] else "No"), row, 1)
                    row += 1

            # Interface metrics if available
            if 'Statistics' in interface and interface['Statistics']:
                # Add a separator
                separator = QWidget()
                separator.setFixedHeight(1)
                separator.setStyleSheet("background-color: #cccccc;")
                interface_layout.addWidget(separator, row, 0, 1, 2)
                row += 1

                metrics_title = QLabel("Network Metrics")
                metrics_title.setStyleSheet("font-weight: bold;")
                interface_layout.addWidget(metrics_title, row, 0, 1, 2)
                row += 1

                stats = interface['Statistics']

                if 'RxBytes' in stats:
                    rx_mb = stats['RxBytes'] / (1024 * 1024)
                    interface_layout.addWidget(QLabel("Received:"), row, 0)
                    interface_layout.addWidget(QLabel(f"{rx_mb:.2f} MB"), row, 1)
                    row += 1

                if 'TxBytes' in stats:
                    tx_mb = stats['TxBytes'] / (1024 * 1024)
                    interface_layout.addWidget(QLabel("Transmitted:"), row, 0)
                    interface_layout.addWidget(QLabel(f"{tx_mb:.2f} MB"), row, 1)
                    row += 1

                if 'RxErrors' in stats:
                    interface_layout.addWidget(QLabel("Receive Errors:"), row, 0)
                    error_label = QLabel(str(stats['RxErrors']))

                    # Highlight errors
                    if stats['RxErrors'] > 0:
                        error_label.setStyleSheet("color: red;")

                    interface_layout.addWidget(error_label, row, 1)
                    row += 1

                if 'TxErrors' in stats:
                    interface_layout.addWidget(QLabel("Transmit Errors:"), row, 0)
                    error_label = QLabel(str(stats['TxErrors']))

                    # Highlight errors
                    if stats['TxErrors'] > 0:
                        error_label.setStyleSheet("color: red;")

                    interface_layout.addWidget(error_label, row, 1)
                    row += 1

                if 'RxDropped' in stats:
                    interface_layout.addWidget(QLabel("Dropped Packets (Rx):"), row, 0)
                    interface_layout.addWidget(QLabel(str(stats['RxDropped'])), row, 1)
                    row += 1

                if 'TxDropped' in stats:
                    interface_layout.addWidget(QLabel("Dropped Packets (Tx):"), row, 0)
                    interface_layout.addWidget(QLabel(str(stats['TxDropped'])), row, 1)
                    row += 1

            section_layout.addWidget(interface_widget)
            self.content_layout.insertWidget(i, interface_section)

            # Add separator between interfaces
            if i < len(self.data) - 1:
                separator = QWidget()
                separator.setFixedHeight(2)
                separator.setStyleSheet("background-color: #aaaaaa;")
                self.content_layout.insertWidget(i + 1, separator)
