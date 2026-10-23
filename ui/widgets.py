import calendar
from datetime import date

from PySide6.QtCore import Qt, QDate, Signal
from PySide6.QtWidgets import (
    QFrame, QLabel, QToolButton, QVBoxLayout, QGridLayout, QPushButton, QWidget
)


GERMAN_MONTHS = [
    "", "Januar", "Februar", "März", "April", "Mai", "Juni",
    "Juli", "August", "September", "Oktober", "November", "Dezember"
]
WEEKDAYS = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]


class MiniMonthCard(QFrame):
    date_selected = Signal(QDate)

    def __init__(self, year: int, month: int, parent=None):
        super().__init__(parent)
        self.setObjectName("miniMonthCard")
        self.setMinimumWidth(205)
        self.setMaximumWidth(250)
        self.setFixedHeight(158)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(10, 8, 10, 8)
        outer.setSpacing(3)

        title = QLabel(f"{GERMAN_MONTHS[month]} {year}")
        title.setObjectName("miniMonthTitle")
        outer.addWidget(title)

        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(1)
        grid.setVerticalSpacing(0)

        for col, name in enumerate(WEEKDAYS):
            lbl = QLabel(name)
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setObjectName("weekendHeader" if col >= 5 else "weekday")
            grid.addWidget(lbl, 0, col)

        today = date.today()
        weeks = calendar.Calendar(firstweekday=0).monthdayscalendar(year, month)

        for row, week in enumerate(weeks, start=1):
            for col, day_num in enumerate(week):
                if not day_num:
                    spacer = QLabel("")
                    spacer.setFixedSize(21, 19)
                    grid.addWidget(spacer, row, col, alignment=Qt.AlignCenter)
                    continue

                btn = QToolButton()
                btn.setObjectName("miniDay")
                btn.setText(str(day_num))
                btn.setProperty("weekend", col >= 5)
                btn.setProperty(
                    "today",
                    today.year == year
                    and today.month == month
                    and today.day == day_num
                )
                btn.setFixedSize(21, 19)
                qdate = QDate(year, month, day_num)
                btn.clicked.connect(
                    lambda checked=False, d=qdate: self.date_selected.emit(d)
                )
                grid.addWidget(btn, row, col, alignment=Qt.AlignCenter)

        outer.addLayout(grid)


class ModuleTile(QPushButton):
    def __init__(self, title: str, subtitle: str, parent=None):
        super().__init__(parent)
        self.setObjectName("glassTile")
        self.setMinimumWidth(190)
        self.setMinimumHeight(102)
        self.setMaximumHeight(118)
        self.setText(f"{title}\n\n{subtitle}")


class ResponsiveTileGrid(QWidget):
    def __init__(self, tiles, parent=None):
        super().__init__(parent)
        self.tiles = list(tiles)
        self.grid = QGridLayout(self)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(11)
        self._columns = 0
        self._relayout(2)

    def resizeEvent(self, event):
        width = event.size().width()
        cols = 3 if width >= 920 else 2 if width >= 560 else 1
        if cols != self._columns:
            self._relayout(cols)
        super().resizeEvent(event)

    def _relayout(self, columns):
        self._columns = columns
        while self.grid.count():
            self.grid.takeAt(0)

        for i, tile in enumerate(self.tiles):
            self.grid.addWidget(tile, i // columns, i % columns)

        for col in range(columns):
            self.grid.setColumnStretch(col, 1)
