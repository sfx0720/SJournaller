"""
SQLite wrapper for journal entries and templates.

The database file lives decrypted in a temp location only while
the app is running.  On close it is re-encrypted and deleted.
"""

import sqlite3
from datetime import datetime
from typing import Optional


class Database:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn: Optional[sqlite3.Connection] = None

    # ── connect / disconnect ───────────────────────────────
    def connect(self) -> None:
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.execute("PRAGMA foreign_keys=ON")
        self._create_tables()

    def disconnect(self) -> None:
        if self.conn:
            self.conn.close()
            self.conn = None

    def _create_tables(self) -> None:
        c = self.conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS entries (
                date       TEXT PRIMARY KEY,
                content    TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS templates (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                name       TEXT NOT NULL UNIQUE,
                content    TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        self.conn.commit()

    # ── entries ───────────────────────────────────────────
    def get_entry(self, date: str) -> Optional[str]:
        row = self.conn.execute(
            "SELECT content FROM entries WHERE date=?", (date,)
        ).fetchone()
        return row["content"] if row else None

    def entry_exists(self, date: str) -> bool:
        return (
            self.conn.execute(
                "SELECT 1 FROM entries WHERE date=?", (date,)
            ).fetchone()
            is not None
        )

    def save_entry(self, date: str, content: str) -> None:
        now = datetime.now().isoformat()
        if self.entry_exists(date):
            self.conn.execute(
                "UPDATE entries SET content=?, updated_at=? WHERE date=?",
                (content, now, date),
            )
        else:
            self.conn.execute(
                "INSERT INTO entries (date,content,created_at,updated_at) VALUES (?,?,?,?)",
                (date, content, now, now),
            )
        self.conn.commit()

    def delete_entry(self, date: str) -> None:
        self.conn.execute("DELETE FROM entries WHERE date=?", (date,))
        self.conn.commit()

    def get_all_entries(self) -> list[tuple[str, str]]:
        rows = self.conn.execute(
            "SELECT date, content FROM entries ORDER BY date DESC"
        ).fetchall()
        return [(r["date"], r["content"]) for r in rows]

    def get_entry_dates(self) -> list[str]:
        rows = self.conn.execute(
            "SELECT date FROM entries ORDER BY date DESC"
        ).fetchall()
        return [r["date"] for r in rows]

    def search_entries(self, query: str) -> list[tuple[str, str]]:
        rows = self.conn.execute(
            "SELECT date, content FROM entries WHERE content LIKE ? ORDER BY date DESC",
            (f"%{query}%",),
        ).fetchall()
        return [(r["date"], r["content"]) for r in rows]

    def get_entry_count(self) -> int:
        row = self.conn.execute("SELECT COUNT(*) AS c FROM entries").fetchone()
        return row["c"]

    # ── templates ─────────────────────────────────────────
    def get_templates(self) -> list[dict]:
        rows = self.conn.execute(
            "SELECT id, name, content FROM templates ORDER BY name"
        ).fetchall()
        return [{"id": r["id"], "name": r["name"], "content": r["content"]} for r in rows]

    def get_template(self, tid: int) -> Optional[dict]:
        r = self.conn.execute(
            "SELECT id, name, content FROM templates WHERE id=?", (tid,)
        ).fetchone()
        return {"id": r["id"], "name": r["name"], "content": r["content"]} if r else None

    def add_template(self, name: str, content: str) -> int:
        now = datetime.now().isoformat()
        c = self.conn.execute(
            "INSERT INTO templates (name,content,created_at,updated_at) VALUES (?,?,?,?)",
            (name, content, now, now),
        )
        self.conn.commit()
        return c.lastrowid

    def update_template(self, tid: int, name: str, content: str) -> None:
        now = datetime.now().isoformat()
        self.conn.execute(
            "UPDATE templates SET name=?, content=?, updated_at=? WHERE id=?",
            (name, content, now, tid),
        )
        self.conn.commit()

    def delete_template(self, tid: int) -> None:
        self.conn.execute("DELETE FROM templates WHERE id=?", (tid,))
        self.conn.commit()