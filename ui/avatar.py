from pathlib import Path

from PySide6.QtCore import Qt, QRectF, Signal
from PySide6.QtGui import QPainter, QPainterPath, QPixmap, QColor, QFont
from PySide6.QtWidgets import QWidget, QToolButton


class AvatarWidget(QWidget):
    def __init__(self, size=54, parent=None):
        super().__init__(parent)
        self.setFixedSize(size, size)
        self._picture = ""
        self._name = ""
        self._size = size

    def set_data(self, picture_path: str, name: str):
        self._picture = picture_path or ""
        self._name = name or ""
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = QRectF(0, 0, self.width(), self.height())
        path = QPainterPath()
        path.addEllipse(rect)
        painter.setClipPath(path)

        pix = QPixmap(self._picture) if self._picture and Path(self._picture).exists() else QPixmap()
        if not pix.isNull():
            scaled = pix.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            x = max(0, (scaled.width() - self.width()) // 2)
            y = max(0, (scaled.height() - self.height()) // 2)
            painter.drawPixmap(0, 0, scaled, x, y, self.width(), self.height())
        else:
            painter.fillRect(self.rect(), QColor("#0a84ff"))
            painter.setPen(Qt.white)
            font = QFont()
            font.setBold(True)
            font.setPointSize(max(9, self._size // 5))
            painter.setFont(font)
            painter.drawText(self.rect(), Qt.AlignCenter, self._initials())

    def _initials(self):
        words = [w for w in self._name.strip().split() if w]
        if not words:
            return "CA"
        if len(words) == 1:
            return words[0][:2].upper()
        return (words[0][0] + words[-1][0]).upper()


class EditableAvatar(QWidget):
    remove_requested = Signal()

    def __init__(self, size=82, parent=None):
        super().__init__(parent)
        self._size = size
        self._has_picture = False
        self.setFixedSize(size + 18, size + 18)
        self.setMouseTracking(True)

        self.avatar = AvatarWidget(size, self)
        self.avatar.move(8, 8)
        self.avatar.setMouseTracking(True)

        self.remove_btn = QToolButton(self)
        self.remove_btn.setObjectName("avatarRemoveButton")
        self.remove_btn.setText("×")
        self.remove_btn.setFixedSize(26, 26)
        self.remove_btn.move(size - 10, 1)
        self.remove_btn.clicked.connect(self.remove_requested.emit)
        self.remove_btn.hide()
        self.remove_btn.raise_()

    def set_data(self, picture_path: str, name: str):
        self._has_picture = bool(picture_path and Path(picture_path).exists())
        self.avatar.set_data(picture_path, name)
        if not self._has_picture:
            self.remove_btn.hide()

    def enterEvent(self, event):
        if self._has_picture:
            self.remove_btn.show()
            self.remove_btn.raise_()
        super().enterEvent(event)

    def leaveEvent(self, event):
        if not self.remove_btn.underMouse():
            self.remove_btn.hide()
        super().leaveEvent(event)
