"""
Programmatically generated application icons using Qt painting.
No external image files required at runtime.
"""

from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor, QPen, QFont
from PyQt6.QtCore import Qt, QRectF


def create_app_icon(size: int = 64) -> QIcon:
    """Create the SJournaller notebook icon."""
    pixmap = QPixmap(size, size)
    pixmap.fill(QColor(0, 0, 0, 0))
    p = QPainter(pixmap)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    s = size / 64.0

    # Left page
    p.setBrush(QColor("#89b4fa"))
    p.setPen(Qt.PenStyle.NoPen)
    p.drawRoundedRect(QRectF(4*s, 8*s, 26*s, 48*s), 3*s, 3*s)
    # Right page
    p.setBrush(QColor("#cba6f7"))
    p.drawRoundedRect(QRectF(34*s, 8*s, 26*s, 48*s), 3*s, 3*s)
    # Spine
    p.setBrush(QColor("#45475a"))
    p.drawRect(QRectF(28*s, 6*s, 8*s, 52*s))
    # Lines
    pen = QPen(QColor("#1e1e2e"), max(1, int(0.8*s)))
    p.setPen(pen)
    for i in range(6):
        y = 16*s + i * 7*s
        p.drawLine(int(8*s), int(y), int(25*s), int(y))
        p.drawLine(int(38*s), int(y), int(55*s), int(y))
    p.end()
    return QIcon(pixmap)