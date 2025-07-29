from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea
from PyQt6.QtCore import Qt

from greenfish.utils.logger import Logger


class BaseMetricsPanel(QWidget):
    """Base class for all metrics panels"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.client = None
        self.resource_id = None
        self.data = None
        self.initUI()

    def initUI(self):
        """Initialize the UI components"""
        layout = QVBoxLayout()

        # Create a scroll area for the content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        # Content widget that will contain all the metrics
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)

        # Status label for showing loading/error messages
        self.status_label = QLabel("No data available")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.content_layout.addWidget(self.status_label)

        scroll.setWidget(self.content_widget)
        layout.addWidget(scroll)

        self.setLayout(layout)

    def set_client(self, client, resource_id=None):
        """Set the Redfish client and resource ID"""
        self.client = client
        self.resource_id = resource_id

    def refresh(self):
        """Refresh the metrics data - to be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement refresh()")

    def clear_content(self):
        """Clear all content from the panel"""
        # Remove all widgets except the status label
        while self.content_layout.count() > 1:
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def show_loading(self):
        """Show loading message"""
        self.status_label.setText("Loading data...")
        self.status_label.setVisible(True)

    def show_error(self, message):
        """Show error message"""
        self.status_label.setText(f"Error: {message}")
        self.status_label.setVisible(True)

    def hide_status(self):
        """Hide the status label"""
        self.status_label.setVisible(False)

    def create_section(self, title):
        """Create a section with a title"""
        section = QWidget()
        section_layout = QVBoxLayout(section)
        section_layout.setContentsMargins(0, 10, 0, 10)

        # Section title
        title_label = QLabel(title)
        title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        section_layout.addWidget(title_label)

        return section, section_layout
