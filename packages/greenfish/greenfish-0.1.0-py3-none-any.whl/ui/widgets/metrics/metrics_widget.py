from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtCore import pyqtSignal

from greenfish.ui.widgets.metrics.power_metrics import PowerMetricsPanel
from greenfish.ui.widgets.metrics.thermal_metrics import ThermalMetricsPanel
from greenfish.ui.widgets.metrics.processor_metrics import ProcessorMetricsPanel
from greenfish.ui.widgets.metrics.memory_metrics import MemoryMetricsPanel
from greenfish.ui.widgets.metrics.storage_metrics import StorageMetricsPanel
from greenfish.ui.widgets.metrics.network_metrics import NetworkMetricsPanel
from greenfish.ui.widgets.metrics.telemetry_panel import TelemetryPanel
from greenfish.utils.logger import Logger


class MetricsWidget(QWidget):
    """Widget for displaying system metrics and telemetry data"""

    refresh_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.client = None
        self.system_id = None
        self.chassis_id = None
        self.initUI()

    def initUI(self):
        """Initialize the UI components"""
        layout = QVBoxLayout()

        # Header with title and refresh button
        header_layout = QHBoxLayout()
        title_label = QLabel("System Metrics & Reporting")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        header_layout.addWidget(title_label)

        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(self.refresh_metrics)
        header_layout.addWidget(refresh_button)
        header_layout.addStretch()

        layout.addLayout(header_layout)

        # Tab widget for different metric types
        self.tabs = QTabWidget()

        # Create metric panels
        self.power_panel = PowerMetricsPanel()
        self.thermal_panel = ThermalMetricsPanel()
        self.processor_panel = ProcessorMetricsPanel()
        self.memory_panel = MemoryMetricsPanel()
        self.storage_panel = StorageMetricsPanel()
        self.network_panel = NetworkMetricsPanel()
        self.telemetry_panel = TelemetryPanel()

        # Add tabs
        self.tabs.addTab(self.power_panel, "Power")
        self.tabs.addTab(self.thermal_panel, "Thermal")
        self.tabs.addTab(self.processor_panel, "Processors")
        self.tabs.addTab(self.memory_panel, "Memory")
        self.tabs.addTab(self.storage_panel, "Storage")
        self.tabs.addTab(self.network_panel, "Network")
        self.tabs.addTab(self.telemetry_panel, "Telemetry")

        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def set_client(self, client, system_id=None, chassis_id=None):
        """Set the Redfish client and system/chassis IDs"""
        self.client = client
        self.system_id = system_id
        self.chassis_id = chassis_id

        # Set client for each panel
        self.power_panel.set_client(client, chassis_id)
        self.thermal_panel.set_client(client, chassis_id)
        self.processor_panel.set_client(client, system_id)
        self.memory_panel.set_client(client, system_id)
        self.storage_panel.set_client(client, system_id)
        self.network_panel.set_client(client, system_id)
        self.telemetry_panel.set_client(client)

        # Refresh metrics
        self.refresh_metrics()

    def refresh_metrics(self):
        """Refresh all metrics panels"""
        if not self.client:
            Logger.warning("Cannot refresh metrics: No Redfish client available")
            return

        Logger.info("Refreshing all system metrics")

        try:
            # Refresh each panel
            current_tab = self.tabs.currentIndex()

            self.power_panel.refresh()
            self.thermal_panel.refresh()
            self.processor_panel.refresh()
            self.memory_panel.refresh()
            self.storage_panel.refresh()
            self.network_panel.refresh()
            self.telemetry_panel.refresh()

            # Emit signal that refresh is complete
            self.refresh_requested.emit()
            Logger.success("System metrics refreshed successfully")

        except Exception as e:
            Logger.error(f"Failed to refresh metrics: {str(e)}")
