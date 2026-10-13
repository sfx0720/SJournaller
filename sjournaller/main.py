"""
Application entry point — config check → login → decrypt → run → encrypt on exit.
"""

import sys
import os

from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

from sjournaller import __version__ as APP_VERSION, __app_name__ as APP_NAME
from sjournaller.constants import (
    get_config_path, get_db_encrypted_path, get_db_temp_path,
)
from sjournaller.config import Config
from sjournaller.crypto import (
    derive_key, verify_password, hash_password,
    generate_salt, encrypt_file, decrypt_file,
)
from sjournaller.database import Database
from sjournaller.ui.styles import DARK_STYLESHEET, LIGHT_STYLESHEET
from sjournaller.ui.main_window import MainWindow
from sjournaller.ui.login_dialog import LoginDialog
from sjournaller.ui.setup_dialog import SetupDialog
from sjournaller.resources.icons import create_app_icon


DEFAULT_TEMPLATES = [
    (
        "Daily Reflection",
        "## Morning\n\n- How am I feeling today?\n- What are my priorities?\n\n"
        "## Evening\n\n- What went well?\n- What could I improve?\n- Grateful for:\n",
    ),
    (
        "Gratitude Log",
        "Three things I'm grateful for today:\n\n1. \n2. \n3. \n\n"
        "Why these matter to me:\n\n",
    ),
    (
        "Meeting Notes",
        "Meeting: \nDate: {date}\nAttendees: \n\n"
        "## Agenda\n\n\n## Notes\n\n\n## Action Items\n\n- [ ] \n",
    ),
]


def _cleanup(db: Database, enc_key: bytes) -> None:
    db_temp = get_db_temp_path()
    db_enc = get_db_encrypted_path()
    try:
        db.disconnect()
        if os.path.isfile(db_temp):
            encrypt_file(db_temp, db_enc, enc_key)
            os.remove(db_temp)
    except Exception as exc:
        if os.path.isfile(db_temp):
            print(f"WARNING: could not re-encrypt database: {exc}", file=sys.stderr)
            print(f"Plaintext database remains at: {db_temp}", file=sys.stderr)


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)
    app.setOrganizationName("SJournaller")
    app.setOrganizationDomain("com.sjournaller")

    icon = create_app_icon()
    app.setWindowIcon(icon)

    config = Config()
    password: str = ""

    # ── First-run ─────────────────────────────────────────
    if not config.exists:
        dlg = SetupDialog(icon)
        if dlg.exec() != SetupDialog.DialogCode.Accepted:
            return 0
        password = dlg.password

        enc_salt = generate_salt()
        pw_hash, pw_salt = hash_password(password)
        config.create(
            password_hash=pw_hash,
            password_salt=pw_salt,
            encryption_salt=enc_salt.hex(),
            theme=dlg.theme,
            font_size=dlg.font_size,
        )

        db_temp = get_db_temp_path()
        db_enc = get_db_encrypted_path()

        db = Database(db_temp)
        db.connect()
        for name, content in DEFAULT_TEMPLATES:
            try:
                db.add_template(name, content)
            except Exception:
                pass
        db.disconnect()

        key = derive_key(password, enc_salt)
        encrypt_file(db_temp, db_enc, key)
        os.remove(db_temp)

    # ── Login ─────────────────────────────────────────────
    else:
        config.load()
        max_attempts = 5
        for attempt in range(max_attempts):
            dlg = LoginDialog(icon, attempts_remaining=max_attempts - attempt)
            if dlg.exec() != LoginDialog.DialogCode.Accepted:
                return 0
            password = dlg.password
            if verify_password(password, config.password_hash, config.password_salt):
                break
            remaining = max_attempts - attempt - 1
            QMessageBox.warning(
                None, "Authentication Failed",
                f"Invalid password. {remaining} attempt{'s' if remaining != 1 else ''} remaining.",
            )
        else:
            QMessageBox.critical(None, "Access Denied", "Maximum login attempts exceeded.")
            return 1

    # ── Decrypt ───────────────────────────────────────────
    db_enc = get_db_encrypted_path()
    db_temp = get_db_temp_path()

    if os.path.isfile(db_temp):
        try:
            os.remove(db_temp)
        except OSError:
            pass

    enc_salt = bytes.fromhex(config.encryption_salt)
    key = derive_key(password, enc_salt)

    try:
        decrypt_file(db_enc, db_temp, key)
    except Exception as exc:
        QMessageBox.critical(
            None, "Database Error",
            f"Failed to decrypt database:\n{exc}\n\n"
            "The password may be incorrect or the database file may be corrupted.",
        )
        return 1

    db = Database(db_temp)
    db.connect()

    # ── Theme ─────────────────────────────────────────────
    if config.theme == "dark":
        app.setStyleSheet(DARK_STYLESHEET)
    else:
        app.setStyleSheet(LIGHT_STYLESHEET)

    # ── Run ───────────────────────────────────────────────
    window = MainWindow(config, db, key, icon)
    window.show()

    ret = app.exec()

    # ── Cleanup — use LIVE key from window ────────────────
    _cleanup(db, window._enc_key)

    return ret


if __name__ == "__main__":
    sys.exit(main())