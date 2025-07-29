"""Virtual Media Manager Widget."""
import os
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                           QLabel, QComboBox, QTableWidget, QTableWidgetItem,
                           QHeaderView, QFileDialog, QMessageBox, QGroupBox,
                           QFormLayout, QLineEdit, QCheckBox, QProgressBar)
from PyQt5.QtCore import Qt, pyqtSignal, QThread

from greenfish.utils.logger import Logger
from greenfish.core.virtualmedia import MediaType, VirtualMedia

class VirtualMediaWorker(QThread):
    """Worker thread for virtual media operations."""

    finished = pyqtSignal(bool, str)
    progress = pyqtSignal(int)

    def __init__(self, client, operation, media=None, file_path=None):
        """Initialize worker thread.

        Args:
            client: Virtual media client
            operation: Operation to perform
            media: Virtual media object
            file_path: File path for mount operation
        """
        super().__init__()
        self.client = client
        self.operation = operation
        self.media = media
        self.file_path = file_path

    def run(self):
        """Run the operation."""
        try:
            result = False
            message = ""

            if self.operation == "mount":
                # Determine media type from file extension
                media_type = MediaType.ISO
                if self.file_path.lower().endswith('.img'):
                    media_type = MediaType.IMG
                elif self.file_path.lower().endswith('.vhd') or self.file_path.lower().endswith('.vhdx'):
                    media_type = MediaType.VHD
                elif self.file_path.lower().endswith('.elf'):
                    media_type = MediaType.ELF

                # Mount media
                result = self.client.mount_media(
                    self.media.id,
                    self.file_path,
                    media_type,
                    write_protected=True
                )

                if result:
                    message = f"Successfully mounted {os.path.basename(self.file_path)}"
                else:
                    message = f"Failed to mount {os.path.basename(self.file_path)}"

            elif self.operation == "unmount":
                # Unmount media
                result = self.client.unmount_media(self.media.id)

                if result:
                    message = "Successfully unmounted media"
                else:
                    message = "Failed to unmount media"

            elif self.operation == "eject":
                # Eject media
                result = self.client.eject_media(self.media.id)

                if result:
                    message = "Successfully ejected media"
                else:
                    message = "Failed to eject media"

            self.finished.emit(result, message)

        except Exception as e:
            Logger.error(f"Error in virtual media operation: {str(e)}")
            self.finished.emit(False, f"Error: {str(e)}")


class VirtualMediaWidget(QWidget):
    """Virtual Media Manager widget."""

    def __init__(self, parent=None):
        """Initialize widget.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.client = None
        self.media_list = []
        self.worker = None

        self.init_ui()

    def init_ui(self):
        """Initialize UI components."""
        # Main layout
        main_layout = QVBoxLayout(self)

        # Media table
        self.media_table = QTableWidget()
        self.media_table.setColumnCount(6)
        self.media_table.setHorizontalHeaderLabels([
            "Name", "Type", "Image", "Connected", "Status", "Actions"
        ])
        self.media_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.media_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)
        self.media_table.verticalHeader().setVisible(False)
        self.media_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.media_table.setSelectionMode(QTableWidget.SingleSelection)
        self.media_table.setEditTriggers(QTableWidget.NoEditTriggers)

        # Controls
        controls_layout = QHBoxLayout()

        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh_media)

        self.connection_combo = QComboBox()
        self.connection_combo.addItem("Select Connection Type")
        self.connection_combo.addItem("Redfish")
        self.connection_combo.addItem("IPMI")
        self.connection_combo.currentIndexChanged.connect(self.on_connection_changed)

        controls_layout.addWidget(QLabel("Connection:"))
        controls_layout.addWidget(self.connection_combo)
        controls_layout.addStretch()
        controls_layout.addWidget(self.refresh_button)

        # Media details group
        details_group = QGroupBox("Media Details")
        details_layout = QFormLayout()

        self.media_name_label = QLabel("-")
        self.media_type_label = QLabel("-")
        self.media_status_label = QLabel("-")
        self.media_connected_label = QLabel("-")
        self.media_image_label = QLabel("-")

        details_layout.addRow("Name:", self.media_name_label)
        details_layout.addRow("Type:", self.media_type_label)
        details_layout.addRow("Status:", self.media_status_label)
        details_layout.addRow("Connected:", self.media_connected_label)
        details_layout.addRow("Image:", self.media_image_label)

        details_group.setLayout(details_layout)

        # Mount options group
        mount_group = QGroupBox("Mount Options")
        mount_layout = QFormLayout()

        self.file_path_edit = QLineEdit()
        self.file_path_edit.setReadOnly(True)

        self.browse_button = QPushButton("Browse...")
        self.browse_button.clicked.connect(self.browse_file)

        file_layout = QHBoxLayout()
        file_layout.addWidget(self.file_path_edit)
        file_layout.addWidget(self.browse_button)

        self.write_protected_check = QCheckBox("Write Protected")
        self.write_protected_check.setChecked(True)

        self.boot_on_next_check = QCheckBox("Boot on Next Reset")

        self.mount_button = QPushButton("Mount")
        self.mount_button.clicked.connect(self.mount_media)
        self.mount_button.setEnabled(False)

        self.unmount_button = QPushButton("Unmount")
        self.unmount_button.clicked.connect(self.unmount_media)
        self.unmount_button.setEnabled(False)

        self.eject_button = QPushButton("Eject")
        self.eject_button.clicked.connect(self.eject_media)
        self.eject_button.setEnabled(False)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.mount_button)
        buttons_layout.addWidget(self.unmount_button)
        buttons_layout.addWidget(self.eject_button)

        mount_layout.addRow("File:", file_layout)
        mount_layout.addRow("Options:", self.write_protected_check)
        mount_layout.addRow("", self.boot_on_next_check)
        mount_layout.addRow("Actions:", buttons_layout)

        mount_group.setLayout(mount_layout)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)

        # Status label
        self.status_label = QLabel()

        # Add widgets to main layout
        main_layout.addLayout(controls_layout)
        main_layout.addWidget(self.media_table)
        main_layout.addWidget(details_group)
        main_layout.addWidget(mount_group)
        main_layout.addWidget(self.progress_bar)
        main_layout.addWidget(self.status_label)

        # Connect signals
        self.media_table.itemSelectionChanged.connect(self.on_selection_changed)

    def set_client(self, client):
        """Set virtual media client.

        Args:
            client: Virtual media client
        """
        self.client = client
        self.refresh_media()

    def refresh_media(self):
        """Refresh virtual media list."""
        if not self.client or not self.client.is_connected():
            self.status_label.setText("Not connected to a server")
            self.media_table.setRowCount(0)
            self.media_list = []
            return

        try:
            # Get media list
            self.media_list = self.client.list_media()

            # Update table
            self.update_media_table()

            self.status_label.setText(f"Found {len(self.media_list)} virtual media devices")

        except Exception as e:
            Logger.error(f"Error refreshing virtual media: {str(e)}")
            self.status_label.setText(f"Error: {str(e)}")

    def update_media_table(self):
        """Update media table with current media list."""
        self.media_table.setRowCount(0)

        for media in self.media_list:
            row = self.media_table.rowCount()
            self.media_table.insertRow(row)

            # Name
            name_item = QTableWidgetItem(media.name)
            self.media_table.setItem(row, 0, name_item)

            # Type
            type_item = QTableWidgetItem(media.media_type.value if media.media_type else "Unknown")
            self.media_table.setItem(row, 1, type_item)

            # Image
            image_name = os.path.basename(media.image) if media.image else "None"
            image_item = QTableWidgetItem(image_name)
            self.media_table.setItem(row, 2, image_item)

            # Connected
            connected_item = QTableWidgetItem("Yes" if media.connected else "No")
            self.media_table.setItem(row, 3, connected_item)

            # Status
            status_item = QTableWidgetItem(media.status)
            self.media_table.setItem(row, 4, status_item)

            # Actions
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(2, 2, 2, 2)

            mount_button = QPushButton("Mount")
            mount_button.setProperty("media_index", row)
            mount_button.clicked.connect(lambda _, idx=row: self.select_media(idx))

            unmount_button = QPushButton("Unmount")
            unmount_button.setProperty("media_index", row)
            unmount_button.clicked.connect(lambda _, idx=row: self.select_media_and_unmount(idx))
            unmount_button.setEnabled(media.connected)

            actions_layout.addWidget(mount_button)
            actions_layout.addWidget(unmount_button)

            self.media_table.setCellWidget(row, 5, actions_widget)

    def select_media(self, index):
        """Select media by index.

        Args:
            index: Media index
        """
        self.media_table.selectRow(index)

    def select_media_and_unmount(self, index):
        """Select media and unmount.

        Args:
            index: Media index
        """
        self.media_table.selectRow(index)
        self.unmount_media()

    def on_selection_changed(self):
        """Handle selection change in media table."""
        selected_rows = self.media_table.selectionModel().selectedRows()

        if selected_rows:
            index = selected_rows[0].row()
            if 0 <= index < len(self.media_list):
                media = self.media_list[index]

                # Update details
                self.media_name_label.setText(media.name)
                self.media_type_label.setText(media.media_type.value if media.media_type else "Unknown")
                self.media_status_label.setText(media.status)
                self.media_connected_label.setText("Yes" if media.connected else "No")
                self.media_image_label.setText(media.image if media.image else "None")

                # Update button states
                self.mount_button.setEnabled(not media.connected)
                self.unmount_button.setEnabled(media.connected)
                self.eject_button.setEnabled(media.connected)

                # Clear file path if not connected
                if not media.connected:
                    self.file_path_edit.clear()
            else:
                self.clear_details()
        else:
            self.clear_details()

    def clear_details(self):
        """Clear media details."""
        self.media_name_label.setText("-")
        self.media_type_label.setText("-")
        self.media_status_label.setText("-")
        self.media_connected_label.setText("-")
        self.media_image_label.setText("-")

        self.mount_button.setEnabled(False)
        self.unmount_button.setEnabled(False)
        self.eject_button.setEnabled(False)

    def browse_file(self):
        """Browse for media file."""
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self, "Select Media File", "",
            "Media Files (*.iso *.img *.vhd *.vhdx *.elf);;All Files (*)"
        )

        if file_path:
            self.file_path_edit.setText(file_path)
            self.mount_button.setEnabled(True)

    def get_selected_media(self):
        """Get selected media.

        Returns:
            VirtualMedia: Selected media or None
        """
        selected_rows = self.media_table.selectionModel().selectedRows()

        if selected_rows:
            index = selected_rows[0].row()
            if 0 <= index < len(self.media_list):
                return self.media_list[index]

        return None

    def mount_media(self):
        """Mount media."""
        media = self.get_selected_media()
        file_path = self.file_path_edit.text()

        if not media:
            QMessageBox.warning(self, "Mount Error", "No media selected")
            return

        if not file_path:
            QMessageBox.warning(self, "Mount Error", "No file selected")
            return

        # Check if file exists
        if not os.path.exists(file_path):
            QMessageBox.warning(self, "Mount Error", f"File not found: {file_path}")
            return

        # Confirm mount
        reply = QMessageBox.question(
            self, "Mount Media",
            f"Are you sure you want to mount {os.path.basename(file_path)} to {media.name}?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            # Disable UI during operation
            self.setEnabled(False)
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(0)
            self.status_label.setText(f"Mounting {os.path.basename(file_path)}...")

            # Start worker thread
            self.worker = VirtualMediaWorker(
                self.client, "mount", media, file_path
            )
            self.worker.finished.connect(self.on_operation_finished)
            self.worker.progress.connect(self.progress_bar.setValue)
            self.worker.start()

    def unmount_media(self):
        """Unmount media."""
        media = self.get_selected_media()

        if not media:
            QMessageBox.warning(self, "Unmount Error", "No media selected")
            return

        if not media.connected:
            QMessageBox.warning(self, "Unmount Error", "Media is not connected")
            return

        # Confirm unmount
        reply = QMessageBox.question(
            self, "Unmount Media",
            f"Are you sure you want to unmount {media.name}?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            # Disable UI during operation
            self.setEnabled(False)
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(0)
            self.status_label.setText(f"Unmounting {media.name}...")

            # Start worker thread
            self.worker = VirtualMediaWorker(
                self.client, "unmount", media
            )
            self.worker.finished.connect(self.on_operation_finished)
            self.worker.progress.connect(self.progress_bar.setValue)
            self.worker.start()

    def eject_media(self):
        """Eject media."""
        media = self.get_selected_media()

        if not media:
            QMessageBox.warning(self, "Eject Error", "No media selected")
            return

        if not media.connected:
            QMessageBox.warning(self, "Eject Error", "Media is not connected")
            return

        # Confirm eject
        reply = QMessageBox.question(
            self, "Eject Media",
            f"Are you sure you want to eject {media.name}?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            # Disable UI during operation
            self.setEnabled(False)
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(0)
            self.status_label.setText(f"Ejecting {media.name}...")

            # Start worker thread
            self.worker = VirtualMediaWorker(
                self.client, "eject", media
            )
            self.worker.finished.connect(self.on_operation_finished)
            self.worker.progress.connect(self.progress_bar.setValue)
            self.worker.start()

    def on_operation_finished(self, success, message):
        """Handle operation completion.

        Args:
            success: Whether operation was successful
            message: Result message
        """
        # Re-enable UI
        self.setEnabled(True)
        self.progress_bar.setVisible(False)

        # Show result
        self.status_label.setText(message)

        if success:
            # Refresh media list
            self.refresh_media()
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
            self.media_table.setRowCount(0)
            self.media_list = []
            self.status_label.setText("No connection selected")
        elif index == 1:
            # Redfish connection
            if hasattr(self.parent(), "get_redfish_client"):
                redfish_client = self.parent().get_redfish_client()
                if redfish_client and redfish_client.is_connected():
                    from greenfish.core.virtualmedia import VirtualMediaClient
                    self.client = VirtualMediaClient()
                    self.client.connect_redfish(redfish_client)
                    self.refresh_media()
                else:
                    self.status_label.setText("Redfish client not connected")
            else:
                self.status_label.setText("Redfish client not available")
        elif index == 2:
            # IPMI connection
            if hasattr(self.parent(), "get_ipmi_client"):
                ipmi_client = self.parent().get_ipmi_client()
                if ipmi_client and ipmi_client.is_connected():
                    from greenfish.core.virtualmedia import VirtualMediaClient
                    self.client = VirtualMediaClient()
                    self.client.connect_ipmi(ipmi_client)
                    self.refresh_media()
                else:
                    self.status_label.setText("IPMI client not connected")
            else:
                self.status_label.setText("IPMI client not available")
