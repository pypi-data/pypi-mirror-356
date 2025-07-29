from PyQt6.QtWidgets import (
    QDialog, QTabWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QComboBox, QSpinBox, QCheckBox, QGroupBox, QRadioButton,
    QWidget, QMessageBox, QFileDialog
)
from PyQt6.QtCore import Qt, pyqtSignal

from greenfish.config.settings import settings
from greenfish.config.themes import ThemeManager
from greenfish.config.config_manager import config_manager
from greenfish.utils.logger import logger

class SettingsDialog(QDialog):
    """Dialog for configuring application settings."""

    settings_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setMinimumSize(500, 400)

        self.theme_manager = ThemeManager()
        self.setup_ui()
        self.load_current_settings()

    def setup_ui(self):
        """Create the UI elements."""
        layout = QVBoxLayout(self)

        # Tabs
        self.tabs = QTabWidget()

        # General settings tab
        general_tab = QWidget()
        general_layout = QVBoxLayout(general_tab)

        # Theme selection
        theme_layout = QHBoxLayout()
        theme_label = QLabel("Theme:")
        self.theme_combo = QComboBox()

        # Get available themes
        themes = self.theme_manager.get_available_themes()
        self.theme_combo.addItems(themes)

        # Set current theme
        current_theme = settings.get_theme()
        index = self.theme_combo.findText(current_theme)
        if index >= 0:
            self.theme_combo.setCurrentIndex(index)

        theme_layout.addWidget(theme_label)
        theme_layout.addWidget(self.theme_combo)
        general_layout.addLayout(theme_layout)

        # Auto-reconnect option
        reconnect_layout = QHBoxLayout()
        self.reconnect_check = QCheckBox("Auto-reconnect on application start")
        self.reconnect_check.setChecked(settings.get_auto_reconnect())
        reconnect_layout.addWidget(self.reconnect_check)
        general_layout.addLayout(reconnect_layout)

        # Refresh interval
        refresh_layout = QHBoxLayout()
        refresh_label = QLabel("Refresh interval (seconds):")
        self.refresh_spin = QSpinBox()
        self.refresh_spin.setMinimum(5)
        self.refresh_spin.setMaximum(3600)
        self.refresh_spin.setValue(settings.get_refresh_interval())
        refresh_layout.addWidget(refresh_label)
        refresh_layout.addWidget(self.refresh_spin)
        general_layout.addLayout(refresh_layout)

        # Configuration import/export
        config_layout = QHBoxLayout()
        import_button = QPushButton("Import Configuration")
        import_button.clicked.connect(self.import_config)
        export_button = QPushButton("Export Configuration")
        export_button.clicked.connect(self.export_config)
        config_layout.addWidget(import_button)
        config_layout.addWidget(export_button)
        general_layout.addLayout(config_layout)

        general_layout.addStretch()

        # Add tabs
        self.tabs.addTab(general_tab, "General")

        layout.addWidget(self.tabs)

        # Buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_settings)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

        # Apply styling
        self.setStyleSheet("""
            QDialog {
                background-color: rgb(255, 255, 220);
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

    def load_current_settings(self):
        """Load current settings from the settings object."""
        # General settings
        self.reconnect_check.setChecked(settings.get_auto_reconnect())
        self.refresh_spin.setValue(settings.get_refresh_interval())

        # Appearance settings
        current_theme = settings.get_theme()
        index = self.theme_combo.findText(current_theme)
        if index >= 0:
            self.theme_combo.setCurrentIndex(index)

    def save_settings(self):
        """Save settings and close the dialog."""
        # Save theme
        settings.set_theme(self.theme_combo.currentText())

        # Save auto-reconnect
        settings.set_auto_reconnect(self.reconnect_check.isChecked())

        # Save refresh interval
        settings.set_refresh_interval(self.refresh_spin.value())

        # Save to file
        settings.save()

        # Emit signal
        self.settings_changed.emit()

        self.accept()

    def import_config(self):
        """Import configuration from a file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Import Configuration",
            "",
            "JSON Files (*.json);;All Files (*)"
        )

        if not file_path:
            return

        if config_manager.import_config(file_path):
            QMessageBox.information(self, "Import Successful", "Configuration imported successfully.")

            # Reload settings
            settings.load_settings()

            # Update UI
            current_theme = settings.get_theme()
            index = self.theme_combo.findText(current_theme)
            if index >= 0:
                self.theme_combo.setCurrentIndex(index)

            self.reconnect_check.setChecked(settings.get_auto_reconnect())
            self.refresh_spin.setValue(settings.get_refresh_interval())
        else:
            QMessageBox.critical(self, "Import Failed", "Failed to import configuration.")

    def export_config(self):
        """Export configuration to a file."""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Configuration",
            "",
            "JSON Files (*.json);;All Files (*)"
        )

        if not file_path:
            return

        # Save current settings first
        settings.set_theme(self.theme_combo.currentText())
        settings.set_auto_reconnect(self.reconnect_check.isChecked())
        settings.set_refresh_interval(self.refresh_spin.value())

        if config_manager.export_config(file_path):
            QMessageBox.information(self, "Export Successful", "Configuration exported successfully.")
        else:
            QMessageBox.critical(self, "Export Failed", "Failed to export configuration.")
