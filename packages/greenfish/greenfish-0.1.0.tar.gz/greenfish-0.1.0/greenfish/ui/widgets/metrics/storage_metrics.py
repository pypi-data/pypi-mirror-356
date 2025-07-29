from PyQt6.QtWidgets import QLabel, QGridLayout, QWidget, QProgressBar, QVBoxLayout
from PyQt6.QtCore import Qt

from greenfish.ui.widgets.metrics.base_panel import BaseMetricsPanel
from greenfish.utils.logger import Logger


class StorageMetricsPanel(BaseMetricsPanel):
    """Panel for displaying storage metrics"""

    def __init__(self, parent=None):
        super().__init__(parent)

    def refresh(self):
        """Refresh storage metrics data"""
        if not self.client or not self.resource_id:
            self.show_error("No Redfish client or system ID available")
            return

        self.show_loading()
        self.clear_content()

        try:
            # Get system info from the client
            system_data = self.client.get_system(self.resource_id)
            if not system_data or 'Storage' not in system_data:
                self.show_error("No storage data available")
                return

            # Get the storage collection
            storage_url = system_data['Storage']['@odata.id']
            storage_data = self.client.get_resource(storage_url)

            if not storage_data or 'Members' not in storage_data:
                self.show_error("No storage controllers found")
                return

            # Get detailed information for each storage controller
            controllers = []
            for member in storage_data['Members']:
                controller_url = member['@odata.id']
                controller_data = self.client.get_resource(controller_url)
                if controller_data:
                    controllers.append(controller_data)

            if not controllers:
                self.show_error("No storage controller details available")
                return

            self.data = controllers
            self.hide_status()
            self.display_storage_data()

        except Exception as e:
            Logger.error(f"Failed to get storage metrics: {str(e)}")
            self.show_error(str(e))

    def display_storage_data(self):
        """Display the storage data in the panel"""
        if not self.data:
            return

        for i, controller in enumerate(self.data):
            # Create a section for each storage controller
            controller_name = controller.get('Name', f"Storage Controller {i+1}")
            controller_section, section_layout = self.create_section(controller_name)

            # Display controller information
            controller_widget = QWidget()
            controller_layout = QGridLayout(controller_widget)
            controller_layout.setContentsMargins(10, 5, 10, 5)

            row = 0

            # Basic controller information
            if 'Id' in controller:
                controller_layout.addWidget(QLabel("ID:"), row, 0)
                controller_layout.addWidget(QLabel(controller['Id']), row, 1)
                row += 1

            if 'StorageControllers' in controller and controller['StorageControllers']:
                ctrl_info = controller['StorageControllers'][0]  # Get first controller info

                if 'Model' in ctrl_info:
                    controller_layout.addWidget(QLabel("Model:"), row, 0)
                    controller_layout.addWidget(QLabel(ctrl_info['Model']), row, 1)
                    row += 1

                if 'Manufacturer' in ctrl_info:
                    controller_layout.addWidget(QLabel("Manufacturer:"), row, 0)
                    controller_layout.addWidget(QLabel(ctrl_info['Manufacturer']), row, 1)
                    row += 1

                if 'SupportedControllerProtocols' in ctrl_info:
                    protocols = ', '.join(ctrl_info['SupportedControllerProtocols'])
                    controller_layout.addWidget(QLabel("Protocols:"), row, 0)
                    controller_layout.addWidget(QLabel(protocols), row, 1)
                    row += 1

                if 'Status' in ctrl_info:
                    status = ctrl_info['Status']
                    health = status.get('Health', 'Unknown')
                    state = status.get('State', 'Unknown')

                    controller_layout.addWidget(QLabel("Health:"), row, 0)
                    health_label = QLabel(health)

                    # Set color based on health
                    if health == 'OK':
                        health_label.setStyleSheet("color: green;")
                    elif health == 'Warning':
                        health_label.setStyleSheet("color: orange;")
                    elif health == 'Critical':
                        health_label.setStyleSheet("color: red;")

                    controller_layout.addWidget(health_label, row, 1)
                    row += 1

                    controller_layout.addWidget(QLabel("State:"), row, 0)
                    controller_layout.addWidget(QLabel(state), row, 1)
                    row += 1

            section_layout.addWidget(controller_widget)

            # Get drives for this controller
            if 'Drives' in controller and '@odata.id' in controller['Drives']:
                try:
                    drives_url = controller['Drives']['@odata.id']
                    drives_data = self.client.get_resource(drives_url)

                    if drives_data and 'Members' in drives_data and drives_data['Members']:
                        # Create a section for drives
                        drives_widget = QWidget()
                        drives_layout = QVBoxLayout(drives_widget)
                        drives_layout.setContentsMargins(0, 10, 0, 0)

                        drives_title = QLabel("Drives")
                        drives_title.setStyleSheet("font-weight: bold;")
                        drives_layout.addWidget(drives_title)

                        # Get detailed information for each drive
                        for j, drive_link in enumerate(drives_data['Members']):
                            drive_url = drive_link['@odata.id']
                            drive_data = self.client.get_resource(drive_url)

                            if drive_data:
                                drive_widget = QWidget()
                                drive_layout = QGridLayout(drive_widget)
                                drive_layout.setContentsMargins(10, 5, 10, 5)

                                # Add title for this drive
                                drive_name = drive_data.get('Name', f"Drive {j+1}")
                                drive_title = QLabel(drive_name)
                                drive_title.setStyleSheet("font-weight: bold;")
                                drive_layout.addWidget(drive_title, 0, 0, 1, 2)

                                drive_row = 1

                                # Basic drive information
                                if 'Model' in drive_data:
                                    drive_layout.addWidget(QLabel("Model:"), drive_row, 0)
                                    drive_layout.addWidget(QLabel(drive_data['Model']), drive_row, 1)
                                    drive_row += 1

                                if 'MediaType' in drive_data:
                                    drive_layout.addWidget(QLabel("Media Type:"), drive_row, 0)
                                    drive_layout.addWidget(QLabel(drive_data['MediaType']), drive_row, 1)
                                    drive_row += 1

                                if 'Protocol' in drive_data:
                                    drive_layout.addWidget(QLabel("Protocol:"), drive_row, 0)
                                    drive_layout.addWidget(QLabel(drive_data['Protocol']), drive_row, 1)
                                    drive_row += 1

                                if 'CapacityBytes' in drive_data:
                                    capacity_gb = drive_data['CapacityBytes'] / (1024 * 1024 * 1024)
                                    drive_layout.addWidget(QLabel("Capacity:"), drive_row, 0)
                                    drive_layout.addWidget(QLabel(f"{capacity_gb:.1f} GB"), drive_row, 1)
                                    drive_row += 1

                                if 'RotationSpeedRPM' in drive_data:
                                    drive_layout.addWidget(QLabel("Rotation Speed:"), drive_row, 0)
                                    drive_layout.addWidget(QLabel(f"{drive_data['RotationSpeedRPM']} RPM"), drive_row, 1)
                                    drive_row += 1

                                if 'SerialNumber' in drive_data:
                                    drive_layout.addWidget(QLabel("Serial Number:"), drive_row, 0)
                                    drive_layout.addWidget(QLabel(drive_data['SerialNumber']), drive_row, 1)
                                    drive_row += 1

                                if 'Status' in drive_data:
                                    status = drive_data['Status']
                                    health = status.get('Health', 'Unknown')
                                    state = status.get('State', 'Unknown')

                                    drive_layout.addWidget(QLabel("Health:"), drive_row, 0)
                                    health_label = QLabel(health)

                                    # Set color based on health
                                    if health == 'OK':
                                        health_label.setStyleSheet("color: green;")
                                    elif health == 'Warning':
                                        health_label.setStyleSheet("color: orange;")
                                    elif health == 'Critical':
                                        health_label.setStyleSheet("color: red;")

                                    drive_layout.addWidget(health_label, drive_row, 1)
                                    drive_row += 1

                                    drive_layout.addWidget(QLabel("State:"), drive_row, 0)
                                    drive_layout.addWidget(QLabel(state), drive_row, 1)
                                    drive_row += 1

                                # Predictive failure analysis
                                if 'PredictedMediaLifeLeftPercent' in drive_data:
                                    life_left = drive_data['PredictedMediaLifeLeftPercent']
                                    drive_layout.addWidget(QLabel("Life Left:"), drive_row, 0)
                                    drive_layout.addWidget(QLabel(f"{life_left}%"), drive_row, 1)
                                    drive_row += 1

                                    # Add a progress bar for life left
                                    progress = QProgressBar()
                                    progress.setMinimum(0)
                                    progress.setMaximum(100)
                                    progress.setValue(int(life_left))

                                    # Set color based on life left
                                    if life_left < 20:
                                        progress.setStyleSheet("QProgressBar::chunk { background-color: red; }")
                                    elif life_left < 50:
                                        progress.setStyleSheet("QProgressBar::chunk { background-color: orange; }")
                                    else:
                                        progress.setStyleSheet("QProgressBar::chunk { background-color: green; }")

                                    drive_layout.addWidget(progress, drive_row, 0, 1, 2)
                                    drive_row += 1

                                # Add the drive widget to the drives section
                                drives_layout.addWidget(drive_widget)

                                # Add separator if not the last item
                                if j < len(drives_data['Members']) - 1:
                                    separator = QWidget()
                                    separator.setFixedHeight(1)
                                    separator.setStyleSheet("background-color: #cccccc;")
                                    drives_layout.addWidget(separator)

                        section_layout.addWidget(drives_widget)

                except Exception as e:
                    Logger.error(f"Failed to get drive data: {str(e)}")

            # Get volumes for this controller
            if 'Volumes' in controller and '@odata.id' in controller['Volumes']:
                try:
                    volumes_url = controller['Volumes']['@odata.id']
                    volumes_data = self.client.get_resource(volumes_url)

                    if volumes_data and 'Members' in volumes_data and volumes_data['Members']:
                        # Create a section for volumes
                        volumes_widget = QWidget()
                        volumes_layout = QVBoxLayout(volumes_widget)
                        volumes_layout.setContentsMargins(0, 10, 0, 0)

                        volumes_title = QLabel("Volumes")
                        volumes_title.setStyleSheet("font-weight: bold;")
                        volumes_layout.addWidget(volumes_title)

                        # Get detailed information for each volume
                        for j, volume_link in enumerate(volumes_data['Members']):
                            volume_url = volume_link['@odata.id']
                            volume_data = self.client.get_resource(volume_url)

                            if volume_data:
                                volume_widget = QWidget()
                                volume_layout = QGridLayout(volume_widget)
                                volume_layout.setContentsMargins(10, 5, 10, 5)

                                # Add title for this volume
                                volume_name = volume_data.get('Name', f"Volume {j+1}")
                                volume_title = QLabel(volume_name)
                                volume_title.setStyleSheet("font-weight: bold;")
                                volume_layout.addWidget(volume_title, 0, 0, 1, 2)

                                vol_row = 1

                                # Basic volume information
                                if 'VolumeType' in volume_data:
                                    volume_layout.addWidget(QLabel("Type:"), vol_row, 0)
                                    volume_layout.addWidget(QLabel(volume_data['VolumeType']), vol_row, 1)
                                    vol_row += 1

                                if 'RAIDType' in volume_data:
                                    volume_layout.addWidget(QLabel("RAID Type:"), vol_row, 0)
                                    volume_layout.addWidget(QLabel(volume_data['RAIDType']), vol_row, 1)
                                    vol_row += 1

                                if 'CapacityBytes' in volume_data:
                                    capacity_gb = volume_data['CapacityBytes'] / (1024 * 1024 * 1024)
                                    volume_layout.addWidget(QLabel("Capacity:"), vol_row, 0)
                                    volume_layout.addWidget(QLabel(f"{capacity_gb:.1f} GB"), vol_row, 1)
                                    vol_row += 1

                                if 'Status' in volume_data:
                                    status = volume_data['Status']
                                    health = status.get('Health', 'Unknown')
                                    state = status.get('State', 'Unknown')

                                    volume_layout.addWidget(QLabel("Health:"), vol_row, 0)
                                    health_label = QLabel(health)

                                    # Set color based on health
                                    if health == 'OK':
                                        health_label.setStyleSheet("color: green;")
                                    elif health == 'Warning':
                                        health_label.setStyleSheet("color: orange;")
                                    elif health == 'Critical':
                                        health_label.setStyleSheet("color: red;")

                                    volume_layout.addWidget(health_label, vol_row, 1)
                                    vol_row += 1

                                    volume_layout.addWidget(QLabel("State:"), vol_row, 0)
                                    volume_layout.addWidget(QLabel(state), vol_row, 1)
                                    vol_row += 1

                                # Add the volume widget to the volumes section
                                volumes_layout.addWidget(volume_widget)

                                # Add separator if not the last item
                                if j < len(volumes_data['Members']) - 1:
                                    separator = QWidget()
                                    separator.setFixedHeight(1)
                                    separator.setStyleSheet("background-color: #cccccc;")
                                    volumes_layout.addWidget(separator)

                        section_layout.addWidget(volumes_widget)

                except Exception as e:
                    Logger.error(f"Failed to get volume data: {str(e)}")

            self.content_layout.insertWidget(i, controller_section)

            # Add separator between controllers
            if i < len(self.data) - 1:
                separator = QWidget()
                separator.setFixedHeight(2)
                separator.setStyleSheet("background-color: #aaaaaa;")
                self.content_layout.insertWidget(i + 1, separator)

from PyQt6.QtWidgets import QVBoxLayout
