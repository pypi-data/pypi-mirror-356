from typing import Dict, Any, List

# Define themes
THEMES = {
    "light": {
        "name": "Light (Yellow)",
        "main_background": "rgb(255, 255, 220)",
        "widget_background": "rgb(255, 255, 220)",
        "menu_background": "rgb(255, 255, 220)",
        "button_background": "rgb(200, 200, 180)",
        "button_hover": "rgb(180, 180, 160)",
        "text_color": "rgb(51, 51, 51)",
        "border_color": "rgb(204, 204, 204)",
        "table_background": "rgb(255, 255, 255)",
        "header_background": "rgb(240, 240, 220)",
        "good_status": "rgb(220, 255, 220)",
        "warning_status": "rgb(255, 245, 200)",
        "error_status": "rgb(255, 220, 220)"
    },
    "dark": {
        "name": "Dark",
        "main_background": "rgb(50, 50, 50)",
        "widget_background": "rgb(60, 60, 60)",
        "menu_background": "rgb(45, 45, 45)",
        "button_background": "rgb(80, 80, 80)",
        "button_hover": "rgb(100, 100, 100)",
        "text_color": "rgb(220, 220, 220)",
        "border_color": "rgb(100, 100, 100)",
        "table_background": "rgb(70, 70, 70)",
        "header_background": "rgb(55, 55, 55)",
        "good_status": "rgb(50, 120, 50)",
        "warning_status": "rgb(120, 110, 50)",
        "error_status": "rgb(120, 50, 50)"
    },
    "blue": {
        "name": "Blue",
        "main_background": "rgb(240, 245, 255)",
        "widget_background": "rgb(240, 245, 255)",
        "menu_background": "rgb(230, 240, 255)",
        "button_background": "rgb(180, 200, 240)",
        "button_hover": "rgb(150, 180, 230)",
        "text_color": "rgb(40, 40, 80)",
        "border_color": "rgb(180, 200, 220)",
        "table_background": "rgb(255, 255, 255)",
        "header_background": "rgb(220, 235, 250)",
        "good_status": "rgb(220, 255, 220)",
        "warning_status": "rgb(255, 245, 200)",
        "error_status": "rgb(255, 220, 220)"
    }
}

class ThemeManager:
    """Theme manager for the application."""

    @staticmethod
    def get_themes() -> Dict[str, str]:
        """Get available themes."""
        return {key: theme["name"] for key, theme in THEMES.items()}

    @staticmethod
    def get_available_themes() -> List[str]:
        """Get list of available theme names."""
        return [theme["name"] for key, theme in THEMES.items()]

    @staticmethod
    def get_theme(theme_name: str = "light") -> Dict[str, str]:
        """Get a theme by name."""
        if theme_name in THEMES:
            return THEMES[theme_name].copy()
        return THEMES["light"].copy()

    @staticmethod
    def get_stylesheet(theme_name: str = "light") -> str:
        """Get stylesheet for a theme."""
        theme = ThemeManager.get_theme(theme_name)

        return f"""
            QMainWindow {{
                background-color: {theme["main_background"]};
            }}
            QWidget {{
                background-color: {theme["widget_background"]};
                color: {theme["text_color"]};
            }}
            QMenuBar {{
                background-color: {theme["menu_background"]};
                border-bottom: 1px solid {theme["border_color"]};
            }}
            QMenuBar::item {{
                background-color: transparent;
                padding: 4px 8px;
            }}
            QMenuBar::item:selected {{
                background-color: {theme["button_background"]};
            }}
            QMenu {{
                background-color: {theme["widget_background"]};
                border: 1px solid {theme["border_color"]};
            }}
            QMenu::item {{
                padding: 4px 20px;
            }}
            QMenu::item:selected {{
                background-color: {theme["button_background"]};
            }}
            QTreeWidget {{
                background-color: {theme["table_background"]};
                border: 1px solid {theme["border_color"]};
                border-radius: 3px;
            }}
            QTreeWidget::item {{
                padding: 2px;
            }}
            QStatusBar {{
                background-color: {theme["widget_background"]};
                border-top: 1px solid {theme["border_color"]};
            }}
            QTabWidget::pane {{
                border: 1px solid {theme["border_color"]};
                border-radius: 3px;
            }}
            QTabBar::tab {{
                background-color: {theme["header_background"]};
                border: 1px solid {theme["border_color"]};
                border-bottom: none;
                border-top-left-radius: 3px;
                border-top-right-radius: 3px;
                padding: 5px 10px;
                margin-right: 2px;
            }}
            QTabBar::tab:selected {{
                background-color: {theme["widget_background"]};
                border-bottom: 1px solid {theme["widget_background"]};
            }}
            QTabBar::tab:!selected {{
                margin-top: 2px;
            }}
            QGroupBox {{
                background-color: {theme["widget_background"]};
                border: 1px solid {theme["border_color"]};
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }}
            QPushButton {{
                padding: 5px 15px;
                background-color: {theme["button_background"]};
                border: 1px solid {theme["border_color"]};
                border-radius: 3px;
                color: {theme["text_color"]};
            }}
            QPushButton:hover {{
                background-color: {theme["button_hover"]};
            }}
            QLineEdit {{
                padding: 5px;
                border: 1px solid {theme["border_color"]};
                border-radius: 3px;
                background-color: {theme["table_background"]};
                color: {theme["text_color"]};
            }}
            QTableWidget {{
                background-color: {theme["table_background"]};
                border: 1px solid {theme["border_color"]};
                border-radius: 3px;
                color: {theme["text_color"]};
            }}
            QTableWidget::item {{
                padding: 4px;
            }}
            QHeaderView::section {{
                background-color: {theme["header_background"]};
                padding: 4px;
                border: 1px solid {theme["border_color"]};
                border-left: none;
                border-top: none;
            }}
            QProgressBar {{
                border: 1px solid {theme["border_color"]};
                border-radius: 3px;
                background-color: {theme["table_background"]};
                text-align: center;
            }}
            QProgressBar::chunk {{
                background-color: rgb(120, 180, 220);
            }}
        """
