import calendar
from datetime import date, timedelta

from PySide6.QtCore import Qt, QDate, Signal
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton, QToolButton,
    QFrame, QStackedWidget, QScrollArea, QTableWidget,
    QHeaderView, QAbstractItemView, QTableWidgetItem
)

from ui.widgets import MiniMonthCard, GERMAN_MONTHS


class DayView(QScrollArea):
    def __init__(self, event_store, parent=None):
        super().__init__(parent)
        self.event_store = event_store
        self.setWidgetResizable(True)
        self.content = QWidget()
        self.content.setObjectName("transparentPage")
        self.setWidget(self.content)
        self.layout = QVBoxLayout(self.content)
        self.layout.setContentsMargins(16, 12, 16, 16)
        self.layout.setSpacing(0)

    def set_date(self, d):
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        weekdays = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
        title = QLabel(f"{weekdays[d.weekday()]}, {d:%d.%m.%Y}")
        title.setObjectName("sectionTitle")
        self.layout.addWidget(title)
        self.layout.addSpacing(10)

        events = self.event_store.for_date(d.isoformat())
        by_hour = {}
        all_day = []

        for event in events:
            if event.get("all_day"):
                all_day.append(event)
            else:
                try:
                    hour = int(event.get("start_time", "00:00").split(":")[0])
                except Exception:
                    hour = 0
                by_hour.setdefault(hour, []).append(event)

        for event in all_day:
            chip = QLabel(f"Ganztägig · {event.get('title', '')}")
            chip.setObjectName("eventChip")
            self.layout.addWidget(chip)

        if all_day:
            self.layout.addSpacing(8)

        for hour in range(24):
            row = QFrame()
            row.setObjectName("hourRow")
            row.setMinimumHeight(48)
            r = QHBoxLayout(row)
            r.setContentsMargins(8, 5, 8, 5)

            hour_label = QLabel(f"{hour:02d}:00")
            hour_label.setObjectName("hourLabel")
            r.addWidget(hour_label)

            event_col = QVBoxLayout()
            for event in by_hour.get(hour, []):
                text = f"{event.get('start_time', '')}–{event.get('end_time', '')}  {event.get('title', '')}"
                chip = QLabel(text)
                chip.setObjectName("eventChip")
                chip.setToolTip(self._event_tooltip(event))
                event_col.addWidget(chip)

            r.addLayout(event_col, 1)
            self.layout.addWidget(row)

        self.layout.addStretch(1)

    @staticmethod
    def _event_tooltip(event):
        parts = [event.get("title", "")]
        if event.get("person"):
            parts.append(f"Betreuter: {event['person']}")
        if event.get("location"):
            parts.append(f"Ort: {event['location']}")
        if event.get("notes"):
            parts.append(event["notes"])
        return "\n".join(parts)


class WeekView(QTableWidget):
    def __init__(self, event_store, parent=None):
        super().__init__(24, 7, parent)
        self.event_store = event_store
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.verticalHeader().setDefaultSectionSize(48)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setVerticalHeaderLabels([f"{h:02d}:00" for h in range(24)])

    def set_date(self, d):
        self.clearContents()
        monday = d - timedelta(days=d.weekday())
        short_days = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]
        labels = []

        for col in range(7):
            day = monday + timedelta(days=col)
            labels.append(f"{short_days[col]}\n{day:%d.%m.}")

            for event in self.event_store.for_date(day.isoformat()):
                if event.get("all_day"):
                    row = 0
                    prefix = "Ganztägig "
                else:
                    try:
                        row = int(event.get("start_time", "00:00").split(":")[0])
                    except Exception:
                        row = 0
                    prefix = f"{event.get('start_time', '')} "

                existing = self.item(row, col)
                old = existing.text() + "\n" if existing else ""
                item = QTableWidgetItem(old + prefix + event.get("title", ""))
                self.setItem(row, col, item)

        self.setHorizontalHeaderLabels(labels)


class MonthDayCell(QFrame):
    clicked = Signal(QDate)

    def __init__(self, qdate, in_current_month, event_store, selected_date=None, parent=None):
        super().__init__(parent)
        self.qdate = qdate
        self.setObjectName("monthDayCell")
        self.setProperty("otherMonth", not in_current_month)
        self.setProperty("weekend", qdate.dayOfWeek() in (6, 7))
        self.setProperty("today", qdate == QDate.currentDate())
        self.setProperty("selected", selected_date is not None and qdate == selected_date)
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(92)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(4)

        day = QLabel(str(qdate.day()))
        day.setObjectName("monthDateNumber")
        day.setProperty("otherMonth", not in_current_month)
        day.setProperty("weekend", qdate.dayOfWeek() in (6, 7))
        day.setProperty("today", qdate == QDate.currentDate())
        layout.addWidget(day, alignment=Qt.AlignLeft)

        iso = qdate.toString("yyyy-MM-dd")
        events = event_store.for_date(iso)
        for event in events[:3]:
            if event.get("all_day"):
                prefix = ""
            else:
                prefix = f"{event.get('start_time', '')} "
            title = event.get("title", "")
            visible = title if len(title) <= 26 else title[:23] + "…"
            chip = QLabel(prefix + visible)
            chip.setObjectName("monthEventChip")
            chip.setToolTip(self._tooltip(event))
            layout.addWidget(chip)

        if len(events) > 3:
            more = QLabel(f"+ {len(events) - 3} weitere")
            more.setObjectName("monthMore")
            layout.addWidget(more)

        layout.addStretch(1)

    @staticmethod
    def _tooltip(event):
        time_text = "Ganztägig" if event.get("all_day") else f"{event.get('start_time', '')}–{event.get('end_time', '')}"
        parts = [event.get("title", ""), time_text]
        if event.get("person"):
            parts.append(f"Betreuter: {event['person']}")
        if event.get("location"):
            parts.append(f"Ort: {event['location']}")
        return "\n".join(parts)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.qdate)
        super().mousePressEvent(event)


class MonthView(QWidget):
    date_selected = Signal(QDate)

    def __init__(self, event_store, parent=None):
        super().__init__(parent)
        self.setObjectName("transparentPage")
        self.event_store = event_store
        self.current_date = QDate.currentDate()

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(6)

        header = QFrame()
        header.setObjectName("monthWeekHeader")
        header_grid = QGridLayout(header)
        header_grid.setContentsMargins(0, 0, 0, 0)
        header_grid.setSpacing(1)
        for col, name in enumerate(["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]):
            lbl = QLabel(name)
            lbl.setObjectName("monthWeekdayHeader")
            lbl.setProperty("weekend", col >= 5)
            lbl.setAlignment(Qt.AlignCenter)
            header_grid.addWidget(lbl, 0, col)
            header_grid.setColumnStretch(col, 1)
        outer.addWidget(header)

        self.grid_host = QWidget()
        self.grid_host.setObjectName("transparentPage")
        self.grid = QGridLayout(self.grid_host)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setHorizontalSpacing(1)
        self.grid.setVerticalSpacing(1)
        outer.addWidget(self.grid_host, 1)

    def set_date(self, d):
        self.current_date = QDate(d.year, d.month, d.day)
        self._rebuild()

    def _rebuild(self):
        while self.grid.count():
            item = self.grid.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        year = self.current_date.year()
        month = self.current_date.month()
        first = QDate(year, month, 1)
        start = first.addDays(-(first.dayOfWeek() - 1))

        selected = self.current_date
        for idx in range(42):
            qdate = start.addDays(idx)
            row = idx // 7
            col = idx % 7
            cell = MonthDayCell(
                qdate,
                qdate.month() == month,
                self.event_store,
                selected_date=selected,
            )
            cell.clicked.connect(self.date_selected.emit)
            self.grid.addWidget(cell, row, col)

        for col in range(7):
            self.grid.setColumnStretch(col, 1)
        for row in range(6):
            self.grid.setRowStretch(row, 1)


class YearView(QScrollArea):
    date_selected = Signal(QDate)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.content = QWidget()
        self.content.setObjectName("transparentPage")
        self.setWidget(self.content)

        self.grid = QGridLayout(self.content)
        self.grid.setContentsMargins(16, 16, 16, 16)
        self.grid.setSpacing(12)

        self.year = None
        self.cards = []
        self._columns = 0

    def set_year(self, year):
        if year == self.year:
            return

        self.year = year
        while self.grid.count():
            item = self.grid.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        self.cards = []
        for month in range(1, 13):
            card = MiniMonthCard(year, month)
            card.date_selected.connect(self.date_selected.emit)
            self.cards.append(card)

        self._relayout(self._columns or 4)

    def resizeEvent(self, event):
        width = event.size().width()
        cols = 4 if width >= 1100 else 3 if width >= 820 else 2 if width >= 560 else 1
        if cols != self._columns:
            self._relayout(cols)
        super().resizeEvent(event)

    def _relayout(self, cols):
        self._columns = cols
        while self.grid.count():
            self.grid.takeAt(0)
        for i, card in enumerate(self.cards):
            self.grid.addWidget(card, i // cols, i % cols, alignment=Qt.AlignTop | Qt.AlignLeft)
        for col in range(cols):
            self.grid.setColumnStretch(col, 1)


class CalendarToolbar(QFrame):
    previous = Signal()
    today = Signal()
    next = Signal()
    add_event = Signal()
    view_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("calendarToolbar")

        self.grid = QGridLayout(self)
        self.grid.setContentsMargins(10, 8, 10, 8)
        self.grid.setHorizontalSpacing(10)
        self.grid.setVerticalSpacing(8)

        self.nav = QWidget()
        nav_layout = QHBoxLayout(self.nav)
        nav_layout.setContentsMargins(0, 0, 0, 0)
        nav_layout.setSpacing(6)

        prev_btn = QPushButton("‹")
        today_btn = QPushButton("Heute")
        next_btn = QPushButton("›")
        plus_btn = QToolButton()
        plus_btn.setObjectName("plusButton")
        plus_btn.setText("+")
        plus_btn.setToolTip("Ereignis hinzufügen")

        self.title = QLabel()
        self.title.setObjectName("sectionTitle")

        prev_btn.clicked.connect(self.previous.emit)
        today_btn.clicked.connect(self.today.emit)
        next_btn.clicked.connect(self.next.emit)
        plus_btn.clicked.connect(self.add_event.emit)

        nav_layout.addWidget(prev_btn)
        nav_layout.addWidget(today_btn)
        nav_layout.addWidget(next_btn)
        nav_layout.addSpacing(7)
        nav_layout.addWidget(self.title)
        nav_layout.addWidget(plus_btn)
        nav_layout.addStretch(1)

        self.switcher = QWidget()
        switch_layout = QHBoxLayout(self.switcher)
        switch_layout.setContentsMargins(0, 0, 0, 0)
        switch_layout.setSpacing(5)

        self.buttons = {}
        for name in ("Tag", "Woche", "Monat", "Jahr"):
            btn = QPushButton(name)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked=False, n=name: self.view_changed.emit(n))
            self.buttons[name] = btn
            switch_layout.addWidget(btn)

        self._compact = None
        self._relayout(False)

    def set_title(self, text):
        self.title.setText(text)

    def set_active_view(self, name):
        for key, button in self.buttons.items():
            button.setChecked(key == name)

    def resizeEvent(self, event):
        compact = event.size().width() < 760
        if compact != self._compact:
            self._relayout(compact)
        super().resizeEvent(event)

    def _relayout(self, compact):
        self._compact = compact
        self.grid.removeWidget(self.nav)
        self.grid.removeWidget(self.switcher)

        if compact:
            self.grid.addWidget(self.nav, 0, 0)
            self.grid.addWidget(self.switcher, 1, 0, alignment=Qt.AlignLeft)
        else:
            self.grid.addWidget(self.nav, 0, 0)
            self.grid.addWidget(self.switcher, 0, 1, alignment=Qt.AlignRight)


class CalendarModule(QWidget):
    add_event_requested = Signal(QDate)

    def __init__(self, event_store, parent=None):
        super().__init__(parent)
        self.setObjectName("transparentPage")
        self.event_store = event_store
        self.current_date = date.today()
        self.active_view = "Monat"

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 12)
        layout.setSpacing(8)

        self.toolbar = CalendarToolbar()
        self.toolbar.previous.connect(self.go_previous)
        self.toolbar.today.connect(self.go_today)
        self.toolbar.next.connect(self.go_next)
        self.toolbar.add_event.connect(self._request_add_event)
        self.toolbar.view_changed.connect(self.set_view)
        layout.addWidget(self.toolbar)

        self.stack = QStackedWidget()
        self.stack.setObjectName("pageStack")

        self.day_view = DayView(event_store)
        self.week_view = WeekView(event_store)
        self.month_view = MonthView(event_store)
        self.month_view.date_selected.connect(self.set_selected_date)
        self.year_view = YearView()
        self.year_view.date_selected.connect(self.set_selected_date)

        self.stack.addWidget(self.day_view)
        self.stack.addWidget(self.week_view)
        self.stack.addWidget(self.month_view)
        self.stack.addWidget(self.year_view)

        layout.addWidget(self.stack, 1)

        self.set_view("Monat")
        self.refresh()

    @staticmethod
    def _shift_month(year, month, offset):
        idx = year * 12 + month - 1 + offset
        return idx // 12, idx % 12 + 1

    def _request_add_event(self):
        d = self.current_date
        self.add_event_requested.emit(QDate(d.year, d.month, d.day))

    def set_selected_date(self, qdate):
        self.current_date = date(qdate.year(), qdate.month(), qdate.day())
        self.refresh()

    def set_view(self, name):
        mapping = {"Tag": 0, "Woche": 1, "Monat": 2, "Jahr": 3}
        if name not in mapping:
            return
        self.active_view = name
        self.stack.setCurrentIndex(mapping[name])
        self.toolbar.set_active_view(name)
        self.refresh()

    def refresh(self):
        d = self.current_date

        self.day_view.set_date(d)
        self.week_view.set_date(d)
        self.month_view.set_date(d)
        self.year_view.set_year(d.year)

        if self.active_view == "Tag":
            title = d.strftime("%d.%m.%Y")
        elif self.active_view == "Woche":
            monday = d - timedelta(days=d.weekday())
            sunday = monday + timedelta(days=6)
            title = f"{monday:%d.%m.%Y} – {sunday:%d.%m.%Y}"
        elif self.active_view == "Monat":
            title = f"{GERMAN_MONTHS[d.month]} {d.year}"
        else:
            title = str(d.year)

        self.toolbar.set_title(title)

    def go_today(self):
        self.current_date = date.today()
        self.refresh()

    def go_previous(self):
        d = self.current_date
        if self.active_view == "Tag":
            d -= timedelta(days=1)
        elif self.active_view == "Woche":
            d -= timedelta(days=7)
        elif self.active_view == "Monat":
            y, m = self._shift_month(d.year, d.month, -1)
            d = date(y, m, min(d.day, calendar.monthrange(y, m)[1]))
        else:
            y = d.year - 1
            d = date(y, d.month, min(d.day, calendar.monthrange(y, d.month)[1]))
        self.current_date = d
        self.refresh()

    def go_next(self):
        d = self.current_date
        if self.active_view == "Tag":
            d += timedelta(days=1)
        elif self.active_view == "Woche":
            d += timedelta(days=7)
        elif self.active_view == "Monat":
            y, m = self._shift_month(d.year, d.month, 1)
            d = date(y, m, min(d.day, calendar.monthrange(y, m)[1]))
        else:
            y = d.year + 1
            d = date(y, d.month, min(d.day, calendar.monthrange(y, d.month)[1]))
        self.current_date = d
        self.refresh()
