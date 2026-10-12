"""
Template management dialog — add, edit, remove text skeletons.
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QWidget,
    QLineEdit, QPushButton, QListWidget, QListWidgetItem,
    QTextEdit, QSplitter, QMessageBox, QAbstractItemView,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon


class TemplateDialog(QDialog):
    """Full template manager with list + editor."""

    def __init__(self, db, icon: QIcon, parent=None):
        super().__init__(parent)
        self._db = db
        self._icon = icon
        self._templates: list[dict] = []
        self._current_id: int | None = None
        self._build_ui()
        self._refresh_list()

    def _build_ui(self) -> None:
        self.setWindowTitle("Template Manager")
        self.setWindowIcon(self._icon)
        self.resize(700, 500)

        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        # Header
        header = QLabel("Journal Templates")
        header.setObjectName("title_label")
        layout.addWidget(header)

        sub = QLabel(
            "Templates are plain-text skeletons you can apply "
            "when starting a new entry."
        )
        sub.setObjectName("subtitle_label")
        sub.setWordWrap(True)
        layout.addWidget(sub)

        # Splitter: list | editor
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # ── Left: template list ──
        left = QVBoxLayout()
        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )
        self.list_widget.currentRowChanged.connect(self._on_select)
        left.addWidget(self.list_widget)

        btn_row = QHBoxLayout()
        add_btn = QPushButton("+ New")
        add_btn.setObjectName("success")
        add_btn.clicked.connect(self._on_add)
        btn_row.addWidget(add_btn)

        del_btn = QPushButton("Delete")
        del_btn.setObjectName("danger")
        del_btn.clicked.connect(self._on_delete)
        btn_row.addWidget(del_btn)
        btn_row.addStretch()
        left.addLayout(btn_row)

        left_widget = QWidget()
        left_widget.setLayout(left)
        splitter.addWidget(left_widget)

        # ── Right: name + content editor ──
        right = QVBoxLayout()
        right.setSpacing(8)

        name_label = QLabel("Template Name")
        name_label.setObjectName("subtitle_label")
        right.addWidget(name_label)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g. Daily Reflection")
        right.addWidget(self.name_input)

        content_label = QLabel("Template Content")
        content_label.setObjectName("subtitle_label")
        right.addWidget(content_label)
        self.content_edit = QTextEdit()
        self.content_edit.setAcceptRichText(False)
        self.content_edit.setPlaceholderText("Write your template text here...")
        right.addWidget(self.content_edit)

        save_btn = QPushButton("Save Template")
        save_btn.setObjectName("success")
        save_btn.clicked.connect(self._on_save)
        right.addWidget(save_btn)
        right.addStretch()

        right_widget = QWidget()
        right_widget.setLayout(right)
        splitter.addWidget(right_widget)

        splitter.setSizes([220, 480])
        layout.addWidget(splitter)

        # Close
        close_row = QHBoxLayout()
        close_row.addStretch()
        close_btn = QPushButton("Close")
        close_btn.setObjectName("secondary")
        close_btn.clicked.connect(self.accept)
        close_row.addWidget(close_btn)
        layout.addLayout(close_row)

    def _refresh_list(self) -> None:
        self._templates = self._db.get_templates()
        self.list_widget.clear()
        for t in self._templates:
            item = QListWidgetItem(t["name"])
            item.setData(Qt.ItemDataRole.UserRole, t["id"])
            self.list_widget.addItem(item)
        self._current_id = None
        self.name_input.clear()
        self.content_edit.clear()

    def _on_select(self, row: int) -> None:
        if row < 0 or row >= len(self._templates):
            return
        t = self._templates[row]
        self._current_id = t["id"]
        self.name_input.setText(t["name"])
        self.content_edit.setPlainText(t["content"])

    def _on_add(self) -> None:
        self.list_widget.clearSelection()
        self._current_id = None
        self.name_input.clear()
        self.content_edit.clear()
        self.name_input.setFocus()

    def _on_save(self) -> None:
        name = self.name_input.text().strip()
        content = self.content_edit.toPlainText()

        if not name:
            QMessageBox.warning(self, "Validation", "Template name cannot be empty.")
            return

        try:
            if self._current_id is not None:
                self._db.update_template(self._current_id, name, content)
            else:
                new_id = self._db.add_template(name, content)
                self._current_id = new_id
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not save template:\n{e}")
            return

        self._refresh_list()
        # Re-select the saved template
        for i, t in enumerate(self._templates):
            if t["id"] == self._current_id:
                self.list_widget.setCurrentRow(i)
                break

    def _on_delete(self) -> None:
        if self._current_id is None:
            return
        reply = QMessageBox.question(
            self,
            "Delete Template",
            "Are you sure you want to delete this template?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self._db.delete_template(self._current_id)
            self._refresh_list()


class TemplateSelectDialog(QDialog):
    """Quick template picker shown when starting a new entry."""

    def __init__(self, date_str: str, templates: list[dict], icon: QIcon, parent=None):
        super().__init__(parent)
        self.selected_template: dict | None = None
        self.use_blank = False
        self._templates = templates
        self._icon = icon          # ← was missing
        self._build_ui(date_str)

    def _build_ui(self, date_str: str) -> None:
        self.setWindowTitle("New Entry")
        self.setWindowIcon(self._icon)
        self.setFixedSize(400, 350)

        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(24, 24, 24, 24)

        title = QLabel(f"New entry for {date_str}")
        title.setObjectName("title_label")
        layout.addWidget(title)

        prompt = QLabel("How would you like to start?")
        prompt.setObjectName("subtitle_label")
        layout.addWidget(prompt)

        layout.addSpacing(8)

        blank_btn = QPushButton("Blank Entry")
        blank_btn.clicked.connect(self._on_blank)
        layout.addWidget(blank_btn)

        if self._templates:
            layout.addSpacing(8)
            sep = QLabel("-- or choose a template --")
            sep.setObjectName("status_label")
            sep.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(sep)
            layout.addSpacing(4)

            for t in self._templates:
                btn = QPushButton(f"  {t['name']}")
                btn.setObjectName("secondary")
                btn.clicked.connect(lambda _, t=t: self._on_template(t))
                layout.addWidget(btn)

        layout.addStretch()

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setObjectName("secondary")
        cancel_btn.clicked.connect(self.reject)
        layout.addWidget(cancel_btn)

    def _on_blank(self) -> None:
        self.use_blank = True
        self.accept()

    def _on_template(self, template: dict) -> None:
        self.selected_template = template
        self.accept()