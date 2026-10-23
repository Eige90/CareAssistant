from datetime import date, datetime

from PySide6.QtCore import Signal, QDate, Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QLabel, QFrame, QScrollArea,
    QHBoxLayout, QToolButton, QSizePolicy
)

from ui.widgets import MiniMonthCard, ModuleTile, ResponsiveTileGrid


def shift_month(year, month, offset):
    idx = year * 12 + month - 1 + offset
    return idx // 12, idx % 12 + 1


class CalendarGlassPanel(QFrame):
    date_selected = Signal(QDate)
    add_event_requested = Signal()

    def __init__(self, event_store, parent=None):
        super().__init__(parent)
        self.event_store = event_store
        self.setObjectName("glassPanel")
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(13, 12, 13, 12)
        layout.setSpacing(7)

        title_row = QHBoxLayout()
        title = QLabel("Kalender")
        title.setObjectName("sectionTitle")

        plus = QToolButton()
        plus.setObjectName("plusButton")
        plus.setText("+")
        plus.setToolTip("Ereignis hinzufügen")
        plus.clicked.connect(self.add_event_requested.emit)

        title_row.addWidget(title)
        title_row.addStretch(1)
        title_row.addWidget(plus)
        layout.addLayout(title_row)

        self.card_grid = QGridLayout()
        self.card_grid.setContentsMargins(0, 0, 0, 0)
        self.card_grid.setSpacing(7)
        layout.addLayout(self.card_grid)

        today = date.today()
        months = [
            shift_month(today.year, today.month, -1),
            (today.year, today.month),
            shift_month(today.year, today.month, 1),
        ]

        self.cards = []
        for year, month in months:
            card = MiniMonthCard(year, month)
            card.date_selected.connect(self.date_selected.emit)
            self.cards.append(card)

        # On the normal desktop layout the three months remain vertically stacked.
        self._relayout(1)

        upcoming_title = QLabel("Nächste Termine")
        upcoming_title.setObjectName("sectionTitle")
        layout.addWidget(upcoming_title)

        self.upcoming_box = QVBoxLayout()
        self.upcoming_box.setSpacing(3)
        layout.addLayout(self.upcoming_box)

        self.refresh_events()

    def refresh_events(self):
        while self.upcoming_box.count():
            item = self.upcoming_box.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        events = self.event_store.upcoming(3)
        if not events:
            lbl = QLabel("Keine Termine")
            lbl.setObjectName("smallMuted")
            self.upcoming_box.addWidget(lbl)
            return

        for event in events:
            dt = datetime.strptime(event["date"], "%Y-%m-%d")
            time_text = "ganztägig" if event.get("all_day") else event.get("start_time", "")
            lbl = QLabel(f"{dt:%d.%m.}  {time_text} · {event.get('title', '')}")
            lbl.setWordWrap(True)
            self.upcoming_box.addWidget(lbl)

    def _relayout(self, cols):
        while self.card_grid.count():
            self.card_grid.takeAt(0)
        for i, card in enumerate(self.cards):
            self.card_grid.addWidget(
                card, i // cols, i % cols, alignment=Qt.AlignTop | Qt.AlignLeft
            )


class HomePage(QWidget):
    open_calendar = Signal(QDate)
    open_module = Signal(str)
    add_event_requested = Signal()

    def __init__(self, event_store, parent=None):
        super().__init__(parent)
        self.setObjectName("transparentPage")

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        outer.addWidget(self.scroll)

        self.content = QWidget()
        self.content.setObjectName("transparentPage")
        self.scroll.setWidget(self.content)

        content_layout = QVBoxLayout(self.content)
        content_layout.setContentsMargins(14, 12, 14, 14)
        content_layout.setSpacing(10)

        title = QLabel("Home")
        title.setObjectName("pageTitle")
        content_layout.addWidget(title)

        self.main_grid = QGridLayout()
        self.main_grid.setSpacing(14)
        self.main_grid.setContentsMargins(0, 0, 0, 0)
        content_layout.addLayout(self.main_grid)
        content_layout.addStretch(1)

        self.calendar_panel = CalendarGlassPanel(event_store)
        self.calendar_panel.date_selected.connect(self.open_calendar.emit)
        self.calendar_panel.add_event_requested.connect(self.add_event_requested.emit)

        self.modules_panel = QFrame()
        self.modules_panel.setObjectName("glassPanel")
        modules_layout = QVBoxLayout(self.modules_panel)
        modules_layout.setContentsMargins(13, 12, 13, 12)
        modules_layout.setSpacing(10)

        mod_title = QLabel("Module")
        mod_title.setObjectName("sectionTitle")
        modules_layout.addWidget(mod_title)

        specs = [
            ("Betreute", "Stammdaten und Fälle"),
            ("Aufgaben", "To-dos und Wiedervorlagen"),
            ("Fristen", "Fristen im Blick behalten"),
            ("Dokumente", "Dokumente verwalten"),
            ("Kontakte", "Ärzte, Behörden, Einrichtungen"),
            ("Abrechnung", "Vergütung und Abrechnung"),
        ]

        tiles = []
        for name, subtitle in specs:
            tile = ModuleTile(name, subtitle)
            tile.clicked.connect(lambda checked=False, n=name: self.open_module.emit(n))
            tiles.append(tile)

        self.tile_grid = ResponsiveTileGrid(tiles)
        modules_layout.addWidget(self.tile_grid)
        modules_layout.addStretch(1)

        self._wide = None
        self._apply_layout(True)

    def refresh_events(self):
        self.calendar_panel.refresh_events()

    def resizeEvent(self, event):
        wide = event.size().width() >= 900
        if wide != self._wide:
            self._apply_layout(wide)
        super().resizeEvent(event)

    def _apply_layout(self, wide):
        self._wide = wide
        self.main_grid.removeWidget(self.calendar_panel)
        self.main_grid.removeWidget(self.modules_panel)

        if wide:
            self.main_grid.addWidget(self.calendar_panel, 0, 0, alignment=Qt.AlignTop)
            self.main_grid.addWidget(self.modules_panel, 0, 1)
            self.main_grid.setColumnStretch(0, 0)
            self.main_grid.setColumnStretch(1, 1)
        else:
            self.main_grid.addWidget(self.calendar_panel, 0, 0)
            self.main_grid.addWidget(self.modules_panel, 1, 0)
            self.main_grid.setColumnStretch(0, 1)
