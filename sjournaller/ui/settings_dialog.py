"""
Settings dialog — theme, font, auto-save, export dir, change password.
"""

import os
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QComboBox, QSpinBox,
    QGroupBox, QFormLayout, QFileDialog, QMessageBox, QCheckBox,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

from sjournaller.crypto import (
    verify_password, hash_password, generate_salt,
    derive_key, encrypt_file, decrypt_file,
)
from sjournaller.constants import get_db_encrypted_path, get_db_temp_path


class SettingsDialog(QDialog):
    def __init__(self, config, db, enc_key: bytes, icon: QIcon, parent=None):
        super().__init__(parent)
        self._config = config
        self._db = db
        self._enc_key = enc_key
        self._icon = icon
        self.theme_changed = False
        self.password_changed = False          # ← NEW
        self.new_enc_key: bytes | None = None  # ← NEW
        self._build_ui()

    def _build_ui(self) -> None:
        self.setWindowTitle("Settings")
        self.setWindowIcon(self._icon)
        self.setFixedSize(500, 580)

        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(24, 24, 24, 24)

        title = QLabel("Settings")
        title.setObjectName("title_label")
        layout.addWidget(title)

        # Appearance
        ap = QGroupBox("Appearance")
        ap_form = QFormLayout(ap)
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark", "Light"])
        self.theme_combo.setCurrentIndex(0 if self._config.theme == "dark" else 1)
        ap_form.addRow("Theme:", self.theme_combo)

        self.font_spin = QSpinBox()
        self.font_spin.setRange(10, 24)
        self.font_spin.setValue(self._config.font_size)
        ap_form.addRow("Font size:", self.font_spin)

        self.wordcount_check = QCheckBox("Show word count in status bar")
        self.wordcount_check.setChecked(self._config.show_word_count)
        ap_form.addRow(self.wordcount_check)

        layout.addWidget(ap)

        # Editor
        ed = QGroupBox("Editor")
        ed_form = QFormLayout(ed)
        self.autosave_spin = QSpinBox()
        self.autosave_spin.setRange(5, 300)
        self.autosave_spin.setValue(self._config.auto_save_interval)
        self.autosave_spin.setSuffix(" sec")
        ed_form.addRow("Auto-save interval:", self.autosave_spin)
        layout.addWidget(ed)

        # Export
        ex = QGroupBox("Export")
        ex_form = QFormLayout(ex)
        self.export_dir_input = QLineEdit()
        self.export_dir_input.setText(self._config.export_dir or os.path.expanduser("~"))
        ex_form.addRow("Default directory:", self.export_dir_input)
        browse_btn = QPushButton("Browse...")
        browse_btn.setObjectName("secondary")
        browse_btn.clicked.connect(self._on_browse_export)
        ex_form.addRow("", browse_btn)
        layout.addWidget(ex)

        # Security
        sec = QGroupBox("Security")
        sec_form = QFormLayout(sec)

        self.old_pw = QLineEdit()
        self.old_pw.setEchoMode(QLineEdit.EchoMode.Password)
        self.old_pw.setPlaceholderText("Current password")
        sec_form.addRow("Current:", self.old_pw)

        self.new_pw = QLineEdit()
        self.new_pw.setEchoMode(QLineEdit.EchoMode.Password)
        self.new_pw.setPlaceholderText("New password (leave blank to keep current)")
        sec_form.addRow("New:", self.new_pw)

        self.confirm_pw = QLineEdit()
        self.confirm_pw.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_pw.setPlaceholderText("Confirm new password")
        sec_form.addRow("Confirm:", self.confirm_pw)

        layout.addWidget(sec)
        layout.addStretch()

        # Buttons
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setObjectName("secondary")
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(cancel_btn)

        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self._on_save)
        btn_row.addWidget(save_btn)
        layout.addLayout(btn_row)

    def _on_browse_export(self) -> None:
        d = QFileDialog.getExistingDirectory(self, "Choose Default Export Directory")
        if d:
            self.export_dir_input.setText(d)

    def _on_save(self) -> None:
        # Handle password change
        old_pw = self.old_pw.text()
        new_pw = self.new_pw.text()
        confirm_pw = self.confirm_pw.text()

        if new_pw or old_pw:
            if not old_pw:
                QMessageBox.warning(self, "Validation", "Enter your current password to change it.")
                return
            if not verify_password(old_pw, self._config.password_hash, self._config.password_salt):
                QMessageBox.warning(self, "Validation", "Current password is incorrect.")
                return
            if not new_pw:
                QMessageBox.warning(self, "Validation", "Enter a new password.")
                return
            if len(new_pw) < 6:
                QMessageBox.warning(self, "Validation", "New password must be at least 6 characters.")
                return
            if new_pw != confirm_pw:
                QMessageBox.warning(self, "Validation", "New passwords do not match.")
                return

            # Re-encrypt database with new key
            try:
                new_salt = generate_salt()
                new_key = derive_key(new_pw, new_salt)
                new_hash, new_pw_salt = hash_password(new_pw)

                # Encrypt the current temp DB with the new key
                db_temp = get_db_temp_path()
                db_enc = get_db_encrypted_path()
                encrypt_file(db_temp, db_enc, new_key)

                # Update config
                self._config._data["password_hash"] = new_hash
                self._config._data["password_salt"] = new_pw_salt
                self._config._data["encryption_salt"] = new_salt.hex()
                self._config.save()

                # ← NEW: expose the new key so MainWindow can pick it up
                self.new_enc_key = new_key
                self.password_changed = True

                QMessageBox.information(self, "Success", "Password changed successfully.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to change password:\n{e}")
                return

        # Save other settings
        old_theme = self._config.theme
        self._config.theme = "dark" if self.theme_combo.currentIndex() == 0 else "light"
        self.theme_changed = self._config.theme != old_theme
        self._config.font_size = self.font_spin.value()
        self._config.auto_save_interval = self.autosave_spin.value()
        self._config.export_dir = self.export_dir_input.text().strip()
        self._config.show_word_count = self.wordcount_check.isChecked()

        self.accept()