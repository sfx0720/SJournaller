"""
First-run setup wizard: choose password, theme, font size.
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QComboBox, QSpinBox,
    QGroupBox, QFormLayout, QMessageBox,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon


class SetupDialog(QDialog):
    def __init__(self, icon: QIcon, parent=None):
        super().__init__(parent)
        self.password: str = ""
        self.theme: str = "dark"
        self.font_size: int = 13
        self._icon = icon
        self._build_ui()

    def _build_ui(self) -> None:
        self.setWindowTitle("SJournaller — Setup")
        self.setWindowIcon(self._icon)
        self.setFixedSize(480, 520)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)

        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(40, 32, 40, 32)

        # Icon
        icon_label = QLabel()
        icon_label.setPixmap(self._icon.pixmap(64, 64))
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon_label)

        # Title
        title = QLabel("Welcome to SJournaller")
        title.setObjectName("title_label")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        sub = QLabel("Set up your secure journal in just a few steps")
        sub.setObjectName("subtitle_label")
        sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sub.setWordWrap(True)
        layout.addWidget(sub)

        layout.addSpacing(8)

        # Password group
        pw_group = QGroupBox("Security")
        pw_form = QFormLayout(pw_group)
        pw_form.setSpacing(10)

        self.pw_input = QLineEdit()
        self.pw_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.pw_input.setPlaceholderText("Choose a strong password")
        pw_form.addRow("Password:", self.pw_input)

        self.pw_confirm = QLineEdit()
        self.pw_confirm.setEchoMode(QLineEdit.EchoMode.Password)
        self.pw_confirm.setPlaceholderText("Confirm password")
        pw_form.addRow("Confirm:", self.pw_confirm)

        hint = QLabel("This password encrypts your journal and is required each launch.\nThere is no recovery if you forget it.")
        hint.setObjectName("status_label")
        hint.setWordWrap(True)
        pw_form.addRow(hint)

        layout.addWidget(pw_group)

        # Appearance group
        ap_group = QGroupBox("Appearance")
        ap_form = QFormLayout(ap_group)
        ap_form.setSpacing(10)

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark", "Light"])
        self.theme_combo.setCurrentIndex(0)
        ap_form.addRow("Theme:", self.theme_combo)

        self.font_spin = QSpinBox()
        self.font_spin.setRange(10, 24)
        self.font_spin.setValue(13)
        ap_form.addRow("Font size:", self.font_spin)

        layout.addWidget(ap_group)
        layout.addStretch()

        # Buttons
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        cancel_btn = QPushButton("Quit")
        cancel_btn.setObjectName("secondary")
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(cancel_btn)

        create_btn = QPushButton("Create Journal")
        create_btn.clicked.connect(self._on_create)
        btn_row.addWidget(create_btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)

    def _on_create(self) -> None:
        pw = self.pw_input.text()
        confirm = self.pw_confirm.text()

        if not pw:
            QMessageBox.warning(self, "Validation", "Please enter a password.")
            self.pw_input.setFocus()
            return

        if len(pw) < 6:
            QMessageBox.warning(self, "Validation", "Password must be at least 6 characters.")
            self.pw_input.setFocus()
            return

        if pw != confirm:
            QMessageBox.warning(self, "Validation", "Passwords do not match.")
            self.pw_confirm.setFocus()
            return

        self.password = pw
        self.theme = "dark" if self.theme_combo.currentIndex() == 0 else "light"
        self.font_size = self.font_spin.value()
        self.accept()

    def showEvent(self, event) -> None:
        super().showEvent(event)
        self.pw_input.setFocus()