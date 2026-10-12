"""
Password login dialog shown on application start.
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QFrame,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QFont


class LoginDialog(QDialog):
    def __init__(self, icon: QIcon, attempts_remaining: int = 5, parent=None):
        super().__init__(parent)
        self.password: str = ""
        self._icon = icon
        self._build_ui(attempts_remaining)

    def _build_ui(self, attempts: int) -> None:
        self.setWindowTitle("SJournaller — Login")
        self.setWindowIcon(self._icon)
        self.setFixedSize(420, 340)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)

        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(40, 40, 40, 40)

        # Icon
        icon_label = QLabel()
        icon_label.setPixmap(self._icon.pixmap(64, 64))
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon_label)

        # Title
        title = QLabel("SJournaller")
        title.setObjectName("title_label")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Subtitle
        sub = QLabel("Enter your password to unlock your journal")
        sub.setObjectName("subtitle_label")
        sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sub.setWordWrap(True)
        layout.addWidget(sub)

        layout.addSpacing(8)

        # Password field
        self.pw_input = QLineEdit()
        self.pw_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.pw_input.setPlaceholderText("Password")
        self.pw_input.returnPressed.connect(self._on_login)
        layout.addWidget(self.pw_input)

        if attempts < 5:
            hint = QLabel(f"{attempts} attempt{'s' if attempts != 1 else ''} remaining")
            hint.setObjectName("status_label")
            hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(hint)

        layout.addSpacing(12)

        # Buttons
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        cancel_btn = QPushButton("Quit")
        cancel_btn.setObjectName("secondary")
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(cancel_btn)

        login_btn = QPushButton("Unlock")
        login_btn.clicked.connect(self._on_login)
        btn_row.addWidget(login_btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)

    def _on_login(self) -> None:
        pw = self.pw_input.text().strip()
        if not pw:
            self.pw_input.setFocus()
            return
        self.password = pw
        self.accept()

    def showEvent(self, event) -> None:
        super().showEvent(event)
        self.pw_input.setFocus()