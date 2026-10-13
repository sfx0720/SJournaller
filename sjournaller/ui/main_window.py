"""
Main application window — calendar, editor, templates, all tied together.
"""

import os
from datetime import datetime, date

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QFrame, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTextEdit, QCalendarWidget, QListWidget,
    QListWidgetItem, QSplitter, QToolBar, QStatusBar,
    QFileDialog, QMessageBox, QMenu, QLineEdit,
    QAbstractItemView, QApplication,
)
from PyQt6.QtCore import Qt, QDate, QTimer, QSize
from PyQt6.QtGui import (
    QIcon, QAction, QTextCharFormat, QColor, QFont,
    QKeySequence,
)

from sjournaller.constants import APP_NAME, APP_VERSION, APP_COPYRIGHT, APP_AUTHOR
from sjournaller.config import Config
from sjournaller.database import Database
from sjournaller.ui.template_dialog import TemplateDialog, TemplateSelectDialog
from sjournaller.ui.export_dialog import ExportDialog, ImportDialog
from sjournaller.ui.settings_dialog import SettingsDialog
from sjournaller.resources.icons import create_app_icon


class MainWindow(QMainWindow):
    def __init__(
        self,
        config: Config,
        db: Database,
        enc_key: bytes,
        icon: QIcon,
    ):
        super().__init__()
        self._config = config
        self._db = db
        self._enc_key = enc_key
        self._icon = icon

        self._current_date: str = ""
        self._is_dirty: bool = False
        self._entry_dates: list[str] = []

        self._build_ui()
        self._build_menus()
        self._build_toolbar()
        self._build_statusbar()
        self._setup_autosave()
        self._refresh_entry_dates()
        self._go_today()

    # ── UI construction ───────────────────────────────────

    def _build_ui(self) -> None:
        self.setWindowTitle(APP_NAME)
        self.setWindowIcon(self._icon)
        self.resize(1100, 720)
        self.setMinimumSize(800, 500)

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        splitter = QSplitter(Qt.Orientation.Horizontal)

        # ── Left sidebar ──
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(8, 8, 8, 8)
        sidebar_layout.setSpacing(8)

        # Search
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search entries...")
        self.search_input.textChanged.connect(self._on_search)
        sidebar_layout.addWidget(self.search_input)

        # Calendar
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.setHorizontalHeaderFormat(
            QCalendarWidget.HorizontalHeaderFormat.SingleLetterDayNames
        )
        self.calendar.clicked.connect(self._on_calendar_click)
        sidebar_layout.addWidget(self.calendar)

        # Recent entries
        recent_label = QLabel("Recent Entries")
        recent_label.setObjectName("subtitle_label")
        sidebar_layout.addWidget(recent_label)

        self.recent_list = QListWidget()
        self.recent_list.currentRowChanged.connect(self._on_recent_click)
        sidebar_layout.addWidget(self.recent_list)

        splitter.addWidget(sidebar)

        # ── Right: editor area ──
        editor_container = QWidget()
        editor_layout = QVBoxLayout(editor_container)
        editor_layout.setContentsMargins(16, 12, 16, 12)
        editor_layout.setSpacing(8)

        # Date header
        header_row = QHBoxLayout()
        self.date_label = QLabel("Select a date")
        self.date_label.setObjectName("date_label")
        header_row.addWidget(self.date_label)

        header_row.addStretch()

        self.delete_btn = QPushButton("Delete Entry")
        self.delete_btn.setObjectName("danger")
        self.delete_btn.setVisible(False)
        self.delete_btn.clicked.connect(self._on_delete_entry)
        header_row.addWidget(self.delete_btn)

        editor_layout.addLayout(header_row)

        # Editor
        self.editor = QTextEdit()
        self.editor.setAcceptRichText(False)
        self.editor.setPlaceholderText("Start writing...")
        self.editor.textChanged.connect(self._on_text_changed)
        self.editor.setFont(QFont("Segoe UI", self._config.font_size))
        editor_layout.addWidget(self.editor)

        splitter.addWidget(editor_container)
        splitter.setSizes([260, 840])

        main_layout.addWidget(splitter)

    def _build_menus(self) -> None:
        mb = self.menuBar()

        # File
        file_menu = mb.addMenu("&File")
        self._add_action(file_menu, "&Go to Today", self._go_today, "Ctrl+T")
        self._add_action(file_menu, "&Export...", self._on_export, "Ctrl+E")
        self._add_action(file_menu, "&Import...", self._on_import, "Ctrl+I")
        file_menu.addSeparator()
        self._add_action(file_menu, "&Quit", self.close, "Ctrl+Q")

        # Edit
        edit_menu = mb.addMenu("&Edit")
        self._add_action(edit_menu, "&Save Entry", self._save_current, "Ctrl+S")
        self._add_action(edit_menu, "&Delete Entry", self._on_delete_entry)
        edit_menu.addSeparator()
        self._add_action(edit_menu, "&Templates...", self._on_templates, "Ctrl+L")

        # View
        view_menu = mb.addMenu("&View")
        self._add_action(view_menu, "&Toggle Theme", self._toggle_theme, "Ctrl+Shift+T")
        self._add_action(view_menu, "&Increase Font", self._font_increase, "Ctrl++")
        self._add_action(view_menu, "&Decrease Font", self._font_decrease, "Ctrl+-")

        # Help
        help_menu = mb.addMenu("&Help")
        self._add_action(help_menu, "&About", self._on_about)
        self._add_action(help_menu, "&Settings...", self._on_settings, "Ctrl+,")

    def _add_action(self, menu, text, slot, shortcut=None) -> None:
        action = QAction(text, self)
        action.triggered.connect(slot)
        if shortcut:
            action.setShortcut(QKeySequence(shortcut))
        menu.addAction(action)

    def _build_toolbar(self) -> None:
        tb = self.addToolBar("Main")
        tb.setMovable(False)
        tb.setIconSize(QSize(20, 20))

        today_btn = QPushButton("Today")
        today_btn.clicked.connect(self._go_today)
        tb.addWidget(today_btn)

        tb.addSeparator()

        template_btn = QPushButton("Templates")
        template_btn.clicked.connect(self._on_templates)
        tb.addWidget(template_btn)

        export_btn = QPushButton("Export")
        export_btn.clicked.connect(self._on_export)
        tb.addWidget(export_btn)

        import_btn = QPushButton("Import")
        import_btn.clicked.connect(self._on_import)
        tb.addWidget(import_btn)

        tb.addSeparator()

        settings_btn = QPushButton("Settings")
        settings_btn.clicked.connect(self._on_settings)
        tb.addWidget(settings_btn)

    def _build_statusbar(self) -> None:
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status_label = QLabel("Ready")
        self.chars_label = QLabel("Chars: 0")
        self.words_label = QLabel("Words: 0")
        self.saved_label = QLabel("")
        self.status.addWidget(self.status_label, 1)
        self.status.addPermanentWidget(self.words_label)
        self.status.addPermanentWidget(self.chars_label)
        self.status.addPermanentWidget(self.saved_label)

    def _setup_autosave(self) -> None:
        self._autosave_timer = QTimer(self)
        self._autosave_timer.timeout.connect(self._autosave)
        interval = max(5, self._config.auto_save_interval) * 1000
        self._autosave_timer.start(interval)

    # ── Date / entry management ───────────────────────────

    def _date_to_str(self, qdate: QDate) -> str:
        return qdate.toString("yyyy-MM-dd")

    def _str_to_qdate(self, s: str) -> QDate:
        y, m, d = map(int, s.split("-"))
        return QDate(y, m, d)

    def _select_date(self, date_str: str) -> None:
        # Save previous entry if dirty
        if self._is_dirty and self._current_date:
            self._save_current()

        self._current_date = date_str
        self._is_dirty = False

        # Update UI
        qdate = self._str_to_qdate(date_str)
        d = date(int(date_str[:4]), int(date_str[5:7]), int(date_str[8:10]))
        display = d.strftime("%A, %B %d, %Y")
        self.date_label.setText(display)
        self.calendar.setSelectedDate(qdate)

        # Load entry or prompt for template
        content = self._db.get_entry(date_str)
        if content is not None:
            self.editor.setPlainText(content)
            self.delete_btn.setVisible(True)
        else:
            # New entry — ask about template
            templates = self._db.get_templates()
            if templates:
                dlg = TemplateSelectDialog(date_str, templates, self._icon, self)
                if dlg.exec() == TemplateSelectDialog.DialogCode.Accepted:
                    if dlg.use_blank:
                        self.editor.setPlainText("")
                    elif dlg.selected_template:
                        self.editor.setPlainText(dlg.selected_template["content"])
                    self.delete_btn.setVisible(True)
                else:
                    # User cancelled — still show empty editor
                    self.editor.setPlainText("")
                    self.delete_btn.setVisible(False)
            else:
                self.editor.setPlainText("")
                self.delete_btn.setVisible(True)

        self.editor.setFont(QFont("Segoe UI", self._config.font_size))
        self._update_status()
        self._highlight_entry_dates()

    def _refresh_entry_dates(self) -> None:
        self._entry_dates = self._db.get_entry_dates()
        self._highlight_entry_dates()
        self._refresh_recent_list(self._entry_dates)

    def _highlight_entry_dates(self) -> None:
        # Reset all
        default_fmt = QTextCharFormat()
        self.calendar.setDateTextFormat(QDate(), default_fmt)

        # Highlight dates with entries
        entry_fmt = QTextCharFormat()
        is_dark = self._config.theme == "dark"
        entry_fmt.setBackground(QColor("#45475a") if is_dark else QColor("#ccd0da"))
        entry_fmt.setFontWeight(QFont.Weight.Bold)

        for ds in self._entry_dates:
            qd = self._str_to_qdate(ds)
            self.calendar.setDateTextFormat(qd, entry_fmt)

    def _refresh_recent_list(self, dates: list[str]) -> None:
        self.recent_list.blockSignals(True)
        self.recent_list.clear()
        for ds in dates[:50]:
            d = date(int(ds[:4]), int(ds[5:7]), int(ds[8:10]))
            item = QListWidgetItem(d.strftime("%Y-%m-%d  (%a)"))
            item.setData(Qt.ItemDataRole.UserRole, ds)
            self.recent_list.addItem(item)
        self.recent_list.blockSignals(False)

    # ── Slots ─────────────────────────────────────────────

    def _on_calendar_click(self, qdate: QDate) -> None:
        self._select_date(self._date_to_str(qdate))

    def _on_recent_click(self, row: int) -> None:
        if row < 0:
            return
        item = self.recent_list.item(row)
        date_str = item.data(Qt.ItemDataRole.UserRole)
        if date_str:
            self._select_date(date_str)

    def _on_text_changed(self) -> None:
        self._is_dirty = True
        self._update_status()

    def _on_search(self) -> None:
        query = self.search_input.text().strip()
        if not query:
            self._refresh_recent_list(self._entry_dates)
            return
        results = self._db.search_entries(query)
        dates = [d for d, _ in results]
        self._refresh_recent_list(dates)

    def _go_today(self) -> None:
        today = QDate.currentDate()
        self._select_date(self._date_to_str(today))

    def _save_current(self) -> None:
        if not self._current_date:
            return
        content = self.editor.toPlainText()
        self._db.save_entry(self._current_date, content)
        self._is_dirty = False
        now = datetime.now().strftime("%H:%M:%S")
        self.saved_label.setText(f"Saved {now}")
        self._refresh_entry_dates()
        self.delete_btn.setVisible(True)

    def _autosave(self) -> None:
        if self._is_dirty and self._current_date:
            self._save_current()

    def _on_delete_entry(self) -> None:
        if not self._current_date:
            return
        reply = QMessageBox.question(
            self, "Delete Entry",
            f"Delete the entry for {self._current_date}?\nThis cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self._db.delete_entry(self._current_date)
            self.editor.setPlainText("")
            self._is_dirty = False
            self.delete_btn.setVisible(False)
            self._refresh_entry_dates()
            self.status_label.setText("Entry deleted")

    def _on_templates(self) -> None:
        dlg = TemplateDialog(self._db, self._icon, self)
        dlg.exec()

    def _on_export(self) -> None:
        dlg = ExportDialog(self._db, self._config, self._icon, self)
        dlg.exec()

    def _on_import(self) -> None:
        dlg = ImportDialog(self._db, self._icon, self)
        if dlg.exec() == ImportDialog.DialogCode.Accepted:
            self._refresh_entry_dates()

    def _on_settings(self) -> None:
        dlg = SettingsDialog(self._config, self._db, self._enc_key, self._icon, self)
        if dlg.exec() == SettingsDialog.DialogCode.Accepted:
            # ← NEW: sync the encryption key if password was changed
            if dlg.password_changed and dlg.new_enc_key is not None:
                self._enc_key = dlg.new_enc_key

            self.editor.setFont(QFont("Segoe UI", self._config.font_size))
            if dlg.theme_changed:
                self._apply_theme()
            # Update autosave interval
            interval = max(5, self._config.auto_save_interval) * 1000
            self._autosave_timer.setInterval(interval)

    def _toggle_theme(self) -> None:
        self._config.theme = "light" if self._config.theme == "dark" else "dark"
        self._apply_theme()
        self._highlight_entry_dates()

    def _apply_theme(self) -> None:
        from sjournaller.ui.styles import DARK_STYLESHEET, LIGHT_STYLESHEET
        app = QApplication.instance()
        if self._config.theme == "dark":
            app.setStyleSheet(DARK_STYLESHEET)
        else:
            app.setStyleSheet(LIGHT_STYLESHEET)

    def _font_increase(self) -> None:
        self._config.font_size = min(24, self._config.font_size + 1)
        self.editor.setFont(QFont("Segoe UI", self._config.font_size))

    def _font_decrease(self) -> None:
        self._config.font_size = max(10, self._config.font_size - 1)
        self.editor.setFont(QFont("Segoe UI", self._config.font_size))

    def _on_about(self) -> None:
        QMessageBox.about(
            self,
            f"About {APP_NAME}",
            f"<h2>{APP_NAME}</h2>"
            f"<p>Version {APP_VERSION}</p>"
            f"<p>{APP_COPYRIGHT}</p>"
            f"<p>A secure, encrypted personal journal application.</p>"
            f"<p>Entries are stored in an encrypted SQLite database<br>"
            f"protected by your password.</p>",
        )

    def _update_status(self) -> None:
        text = self.editor.toPlainText()
        chars = len(text)
        words = len(text.split()) if text.strip() else 0
        self.chars_label.setText(f"Chars: {chars}")
        if self._config.show_word_count:
            self.words_label.setText(f"Words: {words}")
        else:
            self.words_label.setText("")

    # ── Close event ───────────────────────────────────────

    def closeEvent(self, event) -> None:
        if self._is_dirty and self._current_date:
            self._save_current()
        event.accept()