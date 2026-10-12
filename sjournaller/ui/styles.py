"""
Qt stylesheets — Catppuccin-inspired dark & light themes.
"""

DARK_STYLESHEET = """
QMainWindow { background-color: #1e1e2e; }

QWidget {
    color: #cdd6f4;
    font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
    font-size: 13px;
}

QMenuBar {
    background-color: #181825;
    border-bottom: 1px solid #313244; padding: 2px;
}
QMenuBar::item { padding: 4px 12px; background: transparent; }
QMenuBar::item:selected { background-color: #313244; border-radius: 4px; }

QMenu {
    background-color: #1e1e2e; border: 1px solid #313244;
    border-radius: 6px; padding: 4px;
}
QMenu::item { padding: 6px 24px; border-radius: 4px; }
QMenu::item:selected { background-color: #45475a; }
QMenu::separator { height: 1px; background: #313244; margin: 4px 8px; }

QToolBar {
    background-color: #181825; border-bottom: 1px solid #313244;
    spacing: 4px; padding: 4px 8px;
}
QToolButton {
    background-color: transparent; border: 1px solid transparent;
    border-radius: 6px; padding: 5px 10px; color: #cdd6f4; font-size: 12px;
}
QToolButton:hover { background-color: #313244; border: 1px solid #45475a; }
QToolButton:pressed { background-color: #45475a; }
QToolButton:checked { background-color: #313244; border: 1px solid #89b4fa; color: #89b4fa; }

QFrame#sidebar {
    background-color: #181825; border-right: 1px solid #313244;
}

QCalendarWidget { background-color: #181825; border: none; }
QCalendarWidget QWidget { background-color: #181825; color: #cdd6f4; }
QCalendarWidget QToolButton {
    background-color: #313244; color: #cdd6f4;
    border-radius: 4px; padding: 4px; font-weight: bold;
}
QCalendarWidget QToolButton:hover { background-color: #45475a; }
QCalendarWidget QMenu { background-color: #1e1e2e; color: #cdd6f4; }
QCalendarWidget QAbstractItemView {
    background-color: #1e1e2e; color: #cdd6f4;
    selection-background-color: #89b4fa; selection-color: #1e1e2e; border: none;
}

QTextEdit {
    background-color: #1e1e2e; color: #cdd6f4;
    border: 1px solid #313244; border-radius: 6px;
    padding: 12px; font-size: 14px; selection-background-color: #45475a;
}
QTextEdit:focus { border: 1px solid #89b4fa; }

QPlainTextEdit {
    background-color: #1e1e2e; color: #cdd6f4;
    border: 1px solid #313244; border-radius: 6px;
    padding: 12px; font-size: 14px; selection-background-color: #45475a;
}
QPlainTextEdit:focus { border: 1px solid #89b4fa; }

QLabel#date_label { font-size: 18px; font-weight: bold; color: #89b4fa; padding: 8px; }
QLabel#status_label { color: #a6adc8; font-size: 11px; }
QLabel#title_label { font-size: 22px; font-weight: bold; color: #cba6f7; }
QLabel#subtitle_label { font-size: 14px; color: #a6adc8; }
QLabel#prompt_label { font-size: 16px; color: #a6adc8; padding: 20px; }

QLineEdit {
    background-color: #313244; color: #cdd6f4;
    border: 1px solid #45475a; border-radius: 6px;
    padding: 8px 12px; font-size: 13px;
    selection-background-color: #89b4fa; selection-color: #1e1e2e;
}
QLineEdit:focus { border: 1px solid #89b4fa; }

QPushButton {
    background-color: #89b4fa; color: #1e1e2e; border: none;
    border-radius: 6px; padding: 8px 20px; font-size: 13px;
    font-weight: bold; min-height: 20px;
}
QPushButton:hover { background-color: #b4d0fb; }
QPushButton:pressed { background-color: #74a8f8; }
QPushButton#secondary { background-color: #313244; color: #cdd6f4; }
QPushButton#secondary:hover { background-color: #45475a; }
QPushButton#danger { background-color: #f38ba8; color: #1e1e2e; }
QPushButton#danger:hover { background-color: #f5a0b8; }
QPushButton#success { background-color: #a6e3a1; color: #1e1e2e; }
QPushButton#success:hover { background-color: #bce8b8; }

QDialog { background-color: #1e1e2e; }

QListWidget {
    background-color: #181825; color: #cdd6f4;
    border: 1px solid #313244; border-radius: 6px; padding: 4px;
}
QListWidget::item { padding: 8px; border-radius: 4px; }
QListWidget::item:selected { background-color: #45475a; color: #cdd6f4; }
QListWidget::item:hover { background-color: #313244; }

QScrollBar:vertical {
    background-color: #181825; width: 10px; border-radius: 5px;
}
QScrollBar::handle:vertical {
    background-color: #45475a; min-height: 20px; border-radius: 5px;
}
QScrollBar::handle:vertical:hover { background-color: #585b70; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
QScrollBar:horizontal {
    background-color: #181825; height: 10px; border-radius: 5px;
}
QScrollBar::handle:horizontal {
    background-color: #45475a; min-width: 20px; border-radius: 5px;
}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0px; }

QStatusBar {
    background-color: #181825; color: #a6adc8;
    border-top: 1px solid #313244; font-size: 11px;
}

QComboBox {
    background-color: #313244; color: #cdd6f4;
    border: 1px solid #45475a; border-radius: 6px;
    padding: 6px 12px; min-height: 20px;
}
QComboBox:hover { border: 1px solid #89b4fa; }
QComboBox::drop-down { border: none; width: 24px; }
QComboBox QAbstractItemView {
    background-color: #1e1e2e; color: #cdd6f4;
    selection-background-color: #45475a; border: 1px solid #313244;
}

QSpinBox {
    background-color: #313244; color: #cdd6f4;
    border: 1px solid #45475a; border-radius: 6px;
    padding: 6px 12px; min-height: 20px;
}

QGroupBox {
    border: 1px solid #313244; border-radius: 6px;
    margin-top: 12px; padding-top: 16px;
    font-weight: bold; color: #cba6f7;
}
QGroupBox::title { subcontrol-origin: margin; left: 12px; padding: 0 6px; }

QCheckBox { color: #cdd6f4; spacing: 8px; }
QCheckBox::indicator { width: 18px; height: 18px; border-radius: 4px; }
QCheckBox::indicator:unchecked { background-color: #313244; border: 1px solid #45475a; }
QCheckBox::indicator:checked { background-color: #89b4fa; border: 1px solid #89b4fa; }

QMessageBox { background-color: #1e1e2e; }

QToolTip {
    background-color: #313244; color: #cdd6f4;
    border: 1px solid #45475a; border-radius: 4px; padding: 4px;
}

QSplitter::handle { background-color: #313244; width: 2px; }
"""


LIGHT_STYLESHEET = """
QMainWindow { background-color: #eff1f5; }

QWidget {
    color: #4c4f69;
    font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
    font-size: 13px;
}

QMenuBar {
    background-color: #e6e9ef; border-bottom: 1px solid #ccd0da; padding: 2px;
}
QMenuBar::item { padding: 4px 12px; background: transparent; }
QMenuBar::item:selected { background-color: #ccd0da; border-radius: 4px; }

QMenu {
    background-color: #eff1f5; border: 1px solid #ccd0da;
    border-radius: 6px; padding: 4px;
}
QMenu::item { padding: 6px 24px; border-radius: 4px; }
QMenu::item:selected { background-color: #ccd0da; }
QMenu::separator { height: 1px; background: #ccd0da; margin: 4px 8px; }

QToolBar {
    background-color: #e6e9ef; border-bottom: 1px solid #ccd0da;
    spacing: 4px; padding: 4px 8px;
}
QToolButton {
    background-color: transparent; border: 1px solid transparent;
    border-radius: 6px; padding: 5px 10px; color: #4c4f69; font-size: 12px;
}
QToolButton:hover { background-color: #ccd0da; border: 1px solid #bcc0cc; }
QToolButton:pressed { background-color: #bcc0cc; }
QToolButton:checked { background-color: #ccd0da; border: 1px solid #1e66f5; color: #1e66f5; }

QFrame#sidebar { background-color: #e6e9ef; border-right: 1px solid #ccd0da; }

QCalendarWidget QWidget { background-color: #e6e9ef; color: #4c4f69; }
QCalendarWidget QToolButton {
    background-color: #ccd0da; color: #4c4f69;
    border-radius: 4px; padding: 4px; font-weight: bold;
}
QCalendarWidget QAbstractItemView {
    background-color: #eff1f5; color: #4c4f69;
    selection-background-color: #1e66f5; selection-color: #eff1f5; border: none;
}

QTextEdit {
    background-color: #eff1f5; color: #4c4f69;
    border: 1px solid #ccd0da; border-radius: 6px;
    padding: 12px; font-size: 14px; selection-background-color: #ccd0da;
}
QTextEdit:focus { border: 1px solid #1e66f5; }

QPlainTextEdit {
    background-color: #eff1f5; color: #4c4f69;
    border: 1px solid #ccd0da; border-radius: 6px;
    padding: 12px; font-size: 14px; selection-background-color: #ccd0da;
}
QPlainTextEdit:focus { border: 1px solid #1e66f5; }

QLabel#date_label { font-size: 18px; font-weight: bold; color: #1e66f5; padding: 8px; }
QLabel#status_label { color: #7c7f93; font-size: 11px; }
QLabel#title_label { font-size: 22px; font-weight: bold; color: #7287fd; }
QLabel#subtitle_label { font-size: 14px; color: #7c7f93; }
QLabel#prompt_label { font-size: 16px; color: #7c7f93; padding: 20px; }

QLineEdit {
    background-color: #ccd0da; color: #4c4f69;
    border: 1px solid #bcc0cc; border-radius: 6px;
    padding: 8px 12px; font-size: 13px;
}
QLineEdit:focus { border: 1px solid #1e66f5; }

QPushButton {
    background-color: #1e66f5; color: #eff1f5; border: none;
    border-radius: 6px; padding: 8px 20px; font-size: 13px;
    font-weight: bold; min-height: 20px;
}
QPushButton:hover { background-color: #3a7af6; }
QPushButton:pressed { background-color: #0b56e4; }
QPushButton#secondary { background-color: #ccd0da; color: #4c4f69; }
QPushButton#secondary:hover { background-color: #bcc0cc; }
QPushButton#danger { background-color: #d20f39; color: #eff1f5; }
QPushButton#danger:hover { background-color: #e03058; }
QPushButton#success { background-color: #40a02b; color: #eff1f5; }
QPushButton#success:hover { background-color: #52b63c; }

QDialog { background-color: #eff1f5; }

QListWidget {
    background-color: #e6e9ef; color: #4c4f69;
    border: 1px solid #ccd0da; border-radius: 6px; padding: 4px;
}
QListWidget::item { padding: 8px; border-radius: 4px; }
QListWidget::item:selected { background-color: #ccd0da; color: #4c4f69; }
QListWidget::item:hover { background-color: #bcc0cc; }

QScrollBar:vertical { background-color: #e6e9ef; width: 10px; border-radius: 5px; }
QScrollBar::handle:vertical { background-color: #bcc0cc; min-height: 20px; border-radius: 5px; }
QScrollBar::handle:vertical:hover { background-color: #9ca0b0; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
QScrollBar:horizontal { background-color: #e6e9ef; height: 10px; border-radius: 5px; }
QScrollBar::handle:horizontal { background-color: #bcc0cc; min-width: 20px; border-radius: 5px; }
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0px; }

QStatusBar { background-color: #e6e9ef; color: #7c7f93; border-top: 1px solid #ccd0da; font-size: 11px; }

QComboBox {
    background-color: #ccd0da; color: #4c4f69;
    border: 1px solid #bcc0cc; border-radius: 6px;
    padding: 6px 12px; min-height: 20px;
}
QComboBox::drop-down { border: none; width: 24px; }
QComboBox QAbstractItemView {
    background-color: #eff1f5; color: #4c4f69;
    selection-background-color: #ccd0da; border: 1px solid #ccd0da;
}

QSpinBox {
    background-color: #ccd0da; color: #4c4f69;
    border: 1px solid #bcc0cc; border-radius: 6px;
    padding: 6px 12px; min-height: 20px;
}

QGroupBox {
    border: 1px solid #ccd0da; border-radius: 6px;
    margin-top: 12px; padding-top: 16px;
    font-weight: bold; color: #7287fd;
}
QGroupBox::title { subcontrol-origin: margin; left: 12px; padding: 0 6px; }

QCheckBox { color: #4c4f69; spacing: 8px; }
QCheckBox::indicator { width: 18px; height: 18px; border-radius: 4px; }
QCheckBox::indicator:unchecked { background-color: #ccd0da; border: 1px solid #bcc0cc; }
QCheckBox::indicator:checked { background-color: #1e66f5; border: 1px solid #1e66f5; }

QMessageBox { background-color: #eff1f5; }

QToolTip {
    background-color: #ccd0da; color: #4c4f69;
    border: 1px solid #bcc0cc; border-radius: 4px; padding: 4px;
}

QSplitter::handle { background-color: #ccd0da; width: 2px; }
"""