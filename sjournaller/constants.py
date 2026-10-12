"""
Application-wide constants, metadata, and path helpers.
"""

import os

# ── Metadata ──────────────────────────────────────────────
APP_NAME = "SJournaller"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Syphax@SyphaxSolutions"
APP_DESCRIPTION = "A secure personal journal application"
APP_COPYRIGHT = "© 2027 Syphax Solutions"
APP_ID = "com.syphaxsolutions.sjournaller.app"

# ── Directory / file names ────────────────────────────────
APP_DIR_NAME = "sjournaller"
CONFIG_FILENAME = "config.json"
DB_ENCRYPTED_FILENAME = "journal.enc"
DB_TEMP_FILENAME = "journal.db"

# ── Crypto constants ──────────────────────────────────────
PBKDF2_ITERATIONS = 480_000        # OWASP 2023 recommendation for SHA-256
KEY_LENGTH = 32                    # 256 bits → Fernet key after base64
SALT_LENGTH = 16

# ── Defaults ──────────────────────────────────────────────
DEFAULT_FONT_SIZE = 13
DEFAULT_THEME = "dark"
DEFAULT_EXPORT_DIR = ""
DEFAULT_AUTO_SAVE_INTERVAL = 30    # seconds
DEFAULT_DATE_FORMAT = "%Y-%m-%d"


# ── Path helpers ──────────────────────────────────────────

def get_appdata_dir() -> str:
    """Return the application data directory, creating it if needed."""
    if os.name == "nt":
        base = os.environ.get("APPDATA", os.path.expanduser("~"))
    else:
        base = os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))
    appdata = os.path.join(base, APP_DIR_NAME)
    os.makedirs(appdata, exist_ok=True)
    return appdata


def get_data_dir() -> str:
    """Return the data directory (for database files)."""
    data_dir = os.path.join(get_appdata_dir(), "data")
    os.makedirs(data_dir, exist_ok=True)
    return data_dir


def get_config_path() -> str:
    return os.path.join(get_appdata_dir(), CONFIG_FILENAME)


def get_db_encrypted_path() -> str:
    return os.path.join(get_data_dir(), DB_ENCRYPTED_FILENAME)


def get_db_temp_path() -> str:
    return os.path.join(get_data_dir(), DB_TEMP_FILENAME)