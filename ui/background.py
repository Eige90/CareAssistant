from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPixmap
from PySide6.QtWidgets import QWidget


class BackgroundWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._pixmap = QPixmap()
        self.setObjectName("backgroundRoot")

    def set_background_path(self, path: str):
        pixmap = QPixmap(path) if path else QPixmap()
        self._pixmap = pixmap
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        if self._pixmap.isNull():
            painter.fillRect(self.rect(), self.palette().window())
            return

        target = self.rect()
        scaled = self._pixmap.scaled(
            target.size(),
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation
        )

        x = max(0, (scaled.width() - target.width()) // 2)
        y = max(0, (scaled.height() - target.height()) // 2)
        source = scaled.rect().adjusted(x, y, -x, -y)

        if source.width() < target.width() or source.height() < target.height():
            painter.drawPixmap(target, scaled)
        else:
            painter.drawPixmap(target, scaled, source)
