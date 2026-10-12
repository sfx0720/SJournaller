"""
Export journal entries to a delimited text file.

Format:
    -----------[2027-01-15]----
    Entry content here...
    -----------[2027-01-12]----
    Another entry...
"""

import os
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QFileDialog, QGroupBox,
    QFormLayout, QCheckBox, QMessageBox, QProgressBar,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon


class ExportDialog(QDialog):
    def __init__(self, db, config, icon: QIcon, parent=None):
        super().__init__(parent)
        self._db = db
        self._config = config
        self._icon = icon
        self._build_ui()

    def _build_ui(self) -> None:
        self.setWindowTitle("Export Journal")
        self.setWindowIcon(self._icon)
        self.setFixedSize(500, 380)

        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(24, 24, 24, 24)

        title = QLabel("Export Journal")
        title.setObjectName("title_label")
        layout.addWidget(title)

        # Export directory
        dir_group = QGroupBox("Export Location")
        dir_form = QFormLayout(dir_group)

        self.dir_input = QLineEdit()
        self.dir_input.setText(self._config.export_dir or os.path.expanduser("~"))
        dir_form.addRow("Directory:", self.dir_input)

        browse_btn = QPushButton("Browse…")
        browse_btn.setObjectName("secondary")
        browse_btn.clicked.connect(self._on_browse)
        dir_form.addRow("", browse_btn)

        self.filename_input = QLineEdit("journal_export.txt")
        dir_form.addRow("Filename:", self.filename_input)

        layout.addWidget(dir_group)

        # Options
        opt_group = QGroupBox("Options")
        opt_form = QFormLayout(opt_group)

        self.date_check = QCheckBox("Include date separators")
        self.date_check.setChecked(True)
        opt_form.addRow(self.date_check)

        self.reverse_check = QCheckBox("Reverse order (oldest first)")
        self.reverse_check.setChecked(True)
        opt_form.addRow(self.reverse_check)

        layout.addWidget(opt_group)

        layout.addStretch()

        # Buttons
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setObjectName("secondary")
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(cancel_btn)

        export_btn = QPushButton("Export")
        export_btn.clicked.connect(self._on_export)
        btn_row.addWidget(export_btn)
        layout.addLayout(btn_row)

    def _on_browse(self) -> None:
        d = QFileDialog.getExistingDirectory(self, "Choose Export Directory")
        if d:
            self.dir_input.setText(d)

    def _on_export(self) -> None:
        out_dir = self.dir_input.text().strip()
        filename = self.filename_input.text().strip()

        if not out_dir or not filename:
            QMessageBox.warning(self, "Validation", "Please specify a directory and filename.")
            return

        if not os.path.isdir(out_dir):
            try:
                os.makedirs(out_dir, exist_ok=True)
            except OSError:
                QMessageBox.warning(self, "Error", f"Cannot create directory:\n{out_dir}")
                return

        out_path = os.path.join(out_dir, filename)
        entries = self._db.get_all_entries()

        if not entries:
            QMessageBox.information(self, "Export", "No journal entries to export.")
            return

        if self.reverse_check.isChecked():
            entries = list(reversed(entries))

        try:
            with open(out_path, "w", encoding="utf-8") as f:
                for date_str, content in entries:
                    if self.date_check.isChecked():
                        f.write(f"-----------[{date_str}]----\n")
                    f.write(content)
                    f.write("\n\n")

            self._config.export_dir = out_dir
            QMessageBox.information(
                self, "Export Complete",
                f"Exported {len(entries)} entries to:\n{out_path}",
            )
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Failed to export:\n{e}")


class ImportDialog(QDialog):
    """Import entries from the delimited text format."""

    def __init__(self, db, icon: QIcon, parent=None):
        super().__init__(parent)
        self._db = db
        self._icon = icon
        self._build_ui()

    def _build_ui(self) -> None:
        self.setWindowTitle("Import Journal")
        self.setWindowIcon(self._icon)
        self.setFixedSize(500, 250)

        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(24, 24, 24, 24)

        title = QLabel("Import Journal")
        title.setObjectName("title_label")
        layout.addWidget(title)

        sub = QLabel("Import entries from a text file with date separators:\n-----------[YYYY-MM-DD]----")
        sub.setObjectName("subtitle_label")
        sub.setWordWrap(True)
        layout.addWidget(sub)

        self.file_input = QLineEdit()
        self.file_input.setPlaceholderText("Select file to import…")
        layout.addWidget(self.file_input)

        browse_btn = QPushButton("Browse…")
        browse_btn.setObjectName("secondary")
        browse_btn.clicked.connect(self._on_browse)
        layout.addWidget(browse_btn)

        self.overwrite_check = QCheckBox("Overwrite existing entries on same date")
        layout.addWidget(self.overwrite_check)

        layout.addStretch()

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setObjectName("secondary")
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(cancel_btn)
        import_btn = QPushButton("Import")
        import_btn.clicked.connect(self._on_import)
        btn_row.addWidget(import_btn)
        layout.addLayout(btn_row)

    def _on_browse(self) -> None:
        f, _ = QFileDialog.getOpenFileName(
            self, "Select Import File", "",
            "Text Files (*.txt);;All Files (*)",
        )
        if f:
            self.file_input.setText(f)

    def _on_import(self) -> None:
        path = self.file_input.text().strip()
        if not path or not os.path.isfile(path):
            QMessageBox.warning(self, "Validation", "Please select a valid file.")
            return

        overwrite = self.overwrite_check.isChecked()
        imported = 0
        skipped = 0

        try:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()

            import re
            pattern = r"-----------\[(\d{4}-\d{2}-\d{2})\]----\n"
            parts = re.split(pattern, text)

            # parts: [preamble, date1, content1, date2, content2, ...]
            i = 1
            while i + 1 < len(parts):
                date_str = parts[i].strip()
                content = parts[i + 1].strip()
                i += 2

                exists = self._db.entry_exists(date_str)
                if exists and not overwrite:
                    skipped += 1
                    continue
                self._db.save_entry(date_str, content)
                imported += 1

            QMessageBox.information(
                self, "Import Complete",
                f"Imported {imported} entries.\nSkipped {skipped} existing entries.",
            )
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Import Error", f"Failed to import:\n{e}")