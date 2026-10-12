"""
JSON-based configuration persisted to the APPDATA directory.

On first launch the file does not exist; the setup dialog creates it.
"""

import json
import os
from sjournaller.constants import get_config_path, APP_VERSION


class Config:
    def __init__(self):
        self.path = get_config_path()
        self._data: dict = {}

    # ── existence check ───────────────────────────────────
    @property
    def exists(self) -> bool:
        return os.path.isfile(self.path)

    # ── load / save ───────────────────────────────────────
    def load(self) -> None:
        with open(self.path, "r", encoding="utf-8") as f:
            self._data = json.load(f)

    def save(self) -> None:
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=2, ensure_ascii=False)

    # ── factory for first-run ─────────────────────────────
    def create(
        self,
        password_hash: str,
        password_salt: str,
        encryption_salt: str,
        **kw,
    ) -> None:
        self._data = {
            "version": APP_VERSION,
            "password_hash": password_hash,
            "password_salt": password_salt,
            "encryption_salt": encryption_salt,
            "theme": kw.get("theme", "dark"),
            "font_size": kw.get("font_size", 13),
            "export_dir": kw.get("export_dir", ""),
            "auto_save_interval": kw.get("auto_save_interval", 30),
            "date_format": kw.get("date_format", "%Y-%m-%d"),
            "show_word_count": kw.get("show_word_count", True),
        }
        self.save()

    # ── generic getter / setter ───────────────────────────
    def _get(self, key, default=None):
        return self._data.get(key, default)

    def _set(self, key, value):
        self._data[key] = value
        self.save()

    # ── typed properties ──────────────────────────────────
    @property
    def password_hash(self) -> str:
        return self._get("password_hash", "")

    @property
    def password_salt(self) -> str:
        return self._get("password_salt", "")

    @property
    def encryption_salt(self) -> str:
        return self._get("encryption_salt", "")

    @property
    def version(self) -> str:
        return self._get("version", "1.0.0")

    @property
    def theme(self) -> str:
        return self._get("theme", "dark")

    @theme.setter
    def theme(self, v: str):
        self._set("theme", v)

    @property
    def font_size(self) -> int:
        return self._get("font_size", 13)

    @font_size.setter
    def font_size(self, v: int):
        self._set("font_size", v)

    @property
    def export_dir(self) -> str:
        return self._get("export_dir", "")

    @export_dir.setter
    def export_dir(self, v: str):
        self._set("export_dir", v)

    @property
    def auto_save_interval(self) -> int:
        return self._get("auto_save_interval", 30)

    @auto_save_interval.setter
    def auto_save_interval(self, v: int):
        self._set("auto_save_interval", v)

    @property
    def date_format(self) -> str:
        return self._get("date_format", "%Y-%m-%d")

    @date_format.setter
    def date_format(self, v: str):
        self._set("date_format", v)

    @property
    def show_word_count(self) -> bool:
        return self._get("show_word_count", True)

    @show_word_count.setter
    def show_word_count(self, v: bool):
        self._set("show_word_count", v)