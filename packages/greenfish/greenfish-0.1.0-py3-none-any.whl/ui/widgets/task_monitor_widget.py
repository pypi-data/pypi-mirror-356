from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QTableWidget, QTableWidgetItem, QHeaderView, QPushButton,
                             QProgressBar)
from PyQt6.QtCore import Qt, QTimer
from typing import Dict, Any, List

class TaskMonitorWidget(QWidget):
    """Widget for monitoring and managing Redfish tasks."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.tasks = {}
        self.setup_ui()

    def setup_ui(self):
        """Setup the user interface."""
        layout = QVBoxLayout(self)

        # Header
        header = QLabel("Task Monitor")
        header.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(header)

        # Task table
        self.task_table = QTableWidget()
        self.task_table.setColumnCount(5)
        self.task_table.setHorizontalHeaderLabels(["ID", "Name", "State", "Progress", "Actions"])
        self.task_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.task_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.task_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.task_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        layout.addWidget(self.task_table)

        # Buttons row
        button_layout = QHBoxLayout()

        self.refresh_button = QPushButton("Refresh Tasks")
        self.refresh_button.clicked.connect(self.refresh_tasks)
        button_layout.addWidget(self.refresh_button)

        self.clear_button = QPushButton("Clear Completed")
        self.clear_button.clicked.connect(self.clear_completed_tasks)
        button_layout.addWidget(self.clear_button)

        layout.addLayout(button_layout)

        # Set styling
        self.setStyleSheet("""
            QTableWidget {
                background-color: rgb(255, 255, 255);
                border: 1px solid #CCCCCC;
                border-radius: 3px;
            }
            QTableWidget::item {
                padding: 4px;
            }
            QHeaderView::section {
                background-color: rgb(240, 240, 220);
                padding: 4px;
                border: 1px solid #CCCCCC;
                border-left: none;
                border-top: none;
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

        # Timer for polling tasks
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_tasks)
        self.timer.start(5000)  # Poll every 5 seconds

    def add_task(self, task: Dict[str, Any]):
        """Add a new task to the monitor."""
        task_id = task.get("Id", "Unknown")
        if task_id in self.tasks:
            # Update existing task
            self.tasks[task_id].update(task)
        else:
            # Add new task
            self.tasks[task_id] = task

        # Update the table
        self.update_task_table()

    def update_tasks(self):
        """Poll and update active tasks."""
        # This method would be called periodically to update task status
        # It requires a redfish client with active connection
        # Implementation would call the redfish client to get task updates
        pass

    def refresh_tasks(self):
        """Manually refresh all tasks."""
        # Trigger immediate task update
        self.update_tasks()

    def clear_completed_tasks(self):
        """Remove completed tasks from the monitor."""
        completed_tasks = []
        for task_id, task in self.tasks.items():
            if task.get("TaskState") in ["Completed", "Cancelled", "Exception"]:
                completed_tasks.append(task_id)

        for task_id in completed_tasks:
            del self.tasks[task_id]

        self.update_task_table()

    def update_task_table(self):
        """Update the task table with current task data."""
        self.task_table.setRowCount(len(self.tasks))

        row = 0
        for task_id, task in self.tasks.items():
            # Task ID
            id_item = QTableWidgetItem(task_id)
            id_item.setFlags(id_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.task_table.setItem(row, 0, id_item)

            # Task Name
            name = task.get("Name", "Unknown Task")
            name_item = QTableWidgetItem(name)
            name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.task_table.setItem(row, 1, name_item)

            # Task State
            state = task.get("TaskState", "Unknown")
            state_item = QTableWidgetItem(state)
            state_item.setFlags(state_item.flags() & ~Qt.ItemFlag.ItemIsEditable)

            # Set color based on state
            if state == "Completed":
                state_item.setBackground(QTableWidgetItem().setBackground(Qt.green))
            elif state == "Running":
                state_item.setBackground(QTableWidgetItem().setBackground(Qt.blue))
            elif state == "Exception":
                state_item.setBackground(QTableWidgetItem().setBackground(Qt.red))

            self.task_table.setItem(row, 2, state_item)

            # Progress bar
            progress_widget = QWidget()
            progress_layout = QHBoxLayout(progress_widget)
            progress_layout.setContentsMargins(4, 4, 4, 4)

            progress_bar = QProgressBar()
            progress_bar.setTextVisible(True)
            progress_value = task.get("PercentComplete", 0)
            progress_bar.setValue(progress_value)

            progress_layout.addWidget(progress_bar)
            self.task_table.setCellWidget(row, 3, progress_widget)

            # Actions button
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(4, 4, 4, 4)

            view_button = QPushButton("View")
            actions_layout.addWidget(view_button)

            self.task_table.setCellWidget(row, 4, actions_widget)

            row += 1
