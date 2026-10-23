from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QPainter, QPen
from PySide6.QtWidgets import QComboBox, QListView, QStyledItemDelegate


class ComboItemDelegate(QStyledItemDelegate):
    def sizeHint(self, option, index):
        size = super().sizeHint(option, index)
        return QSize(size.width(), 36)


class ModernComboBox(QComboBox):
    """Combo box without the dated native square arrow control."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("modernCombo")
        view = QListView()
        view.setObjectName("comboPopup")
        view.setSpacing(0)
        self.setView(view)
        self.setItemDelegate(ComboItemDelegate(self))

    def paintEvent(self, event):
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        color = self.palette().text().color()
        pen = QPen(color)
        pen.setWidthF(1.5)
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)

        x = self.width() - 19
        y = self.height() // 2 - 1
        painter.drawLine(x - 4, y - 2, x, y + 2)
        painter.drawLine(x, y + 2, x + 4, y - 2)
