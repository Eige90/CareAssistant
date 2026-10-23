from datetime import datetime

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit,
    QFrame, QScrollArea, QStackedWidget, QGridLayout, QTabWidget, QDialog
)

from dialogs.client_dialog import ClientDialog


def fmt_date(value):
    if not value:
        return "–"
    try:
        return datetime.strptime(value, "%Y-%m-%d").strftime("%d.%m.%Y")
    except ValueError:
        return value


def value_or_dash(value):
    text = str(value or "").strip()
    return text if text else "–"


class ClientListButton(QPushButton):
    def __init__(self, client, parent=None):
        super().__init__(parent)
        self.client_id = client.get("id")
        self.setObjectName("clientListItem")
        self.setCheckable(True)
        self.setMinimumHeight(78)
        self.update_client(client)

    def update_client(self, client):
        name = f"{client.get('first_name', '')} {client.get('last_name', '')}".strip()
        file_number = client.get("file_number", "") or "Kein Aktenzeichen"
        status = client.get("status", "Aktiv")
        self.setText(f"{name}\n{file_number}  ·  {status}")


class InfoBlock(QFrame):
    def __init__(self, title, rows, parent=None):
        super().__init__(parent)
        self.setObjectName("infoBlock")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 12, 14, 14)
        layout.setSpacing(8)

        heading = QLabel(title)
        heading.setObjectName("infoBlockTitle")
        layout.addWidget(heading)

        grid = QGridLayout()
        grid.setHorizontalSpacing(18)
        grid.setVerticalSpacing(7)

        for row, (label, value) in enumerate(rows):
            key = QLabel(label)
            key.setObjectName("infoKey")
            val = QLabel(value_or_dash(value))
            val.setObjectName("infoValue")
            val.setWordWrap(True)
            grid.addWidget(key, row, 0, alignment=Qt.AlignTop)
            grid.addWidget(val, row, 1)

        grid.setColumnStretch(1, 1)
        layout.addLayout(grid)


class ClientDetail(QWidget):
    edit_requested = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.client = None

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(12)

        header = QFrame()
        header.setObjectName("clientHero")
        h = QHBoxLayout(header)
        h.setContentsMargins(18, 16, 18, 16)

        name_col = QVBoxLayout()
        self.name = QLabel()
        self.name.setObjectName("clientName")
        self.meta = QLabel()
        self.meta.setObjectName("clientMeta")
        name_col.addWidget(self.name)
        name_col.addWidget(self.meta)
        h.addLayout(name_col, 1)

        self.status = QLabel()
        self.status.setObjectName("statusBadge")
        h.addWidget(self.status)

        self.edit_btn = QPushButton("Bearbeiten")
        self.edit_btn.clicked.connect(self._edit)
        h.addWidget(self.edit_btn)

        outer.addWidget(header)

        self.tabs = QTabWidget()
        self.tabs.setObjectName("clientDetailTabs")
        outer.addWidget(self.tabs, 1)

        self.overview_scroll = QScrollArea()
        self.overview_scroll.setWidgetResizable(True)
        self.overview_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.overview_content = QWidget()
        self.overview_content.setObjectName("transparentPage")
        self.overview_scroll.setWidget(self.overview_content)
        self.overview_layout = QGridLayout(self.overview_content)
        self.overview_layout.setContentsMargins(12, 12, 12, 12)
        self.overview_layout.setSpacing(12)
        self.tabs.addTab(self.overview_scroll, "Übersicht")

        self.notes_page = QWidget()
        notes_layout = QVBoxLayout(self.notes_page)
        notes_layout.setContentsMargins(16, 16, 16, 16)
        self.notes = QLabel()
        self.notes.setWordWrap(True)
        self.notes.setTextInteractionFlags(Qt.TextSelectableByMouse)
        notes_layout.addWidget(self.notes)
        notes_layout.addStretch(1)
        self.tabs.addTab(self.notes_page, "Notizen")

    def _edit(self):
        if self.client:
            self.edit_requested.emit(self.client.get("id", ""))

    def set_client(self, client):
        self.client = client
        full_name = f"{client.get('first_name', '')} {client.get('last_name', '')}".strip()
        self.name.setText(full_name)

        meta_parts = []
        if client.get("birth_date"):
            meta_parts.append(f"geb. {fmt_date(client.get('birth_date'))}")
        if client.get("file_number"):
            meta_parts.append(client.get("file_number"))
        self.meta.setText("  ·  ".join(meta_parts) if meta_parts else "")

        status = client.get("status", "Aktiv")
        self.status.setText(status)
        self.status.setProperty("clientStatus", status.lower())
        self.status.style().unpolish(self.status)
        self.status.style().polish(self.status)

        while self.overview_layout.count():
            item = self.overview_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        address = " ".join(x for x in [client.get("street", "")] if x).strip()
        city_line = " ".join(x for x in [client.get("postal_code", ""), client.get("city", "")] if x).strip()
        if address and city_line:
            address = f"{address}\n{city_line}"
        elif city_line:
            address = city_line

        stammdaten = InfoBlock("Stammdaten", [
            ("Geburtsdatum", fmt_date(client.get("birth_date"))),
            ("Adresse", address),
            ("Telefon", client.get("phone")),
            ("E-Mail", client.get("email")),
        ])

        betreuung = InfoBlock("Betreuungsfall", [
            ("Gericht", client.get("court")),
            ("Aktenzeichen", client.get("file_number")),
            ("Bestellung seit", fmt_date(client.get("appointment_date"))),
            ("Status", status),
        ])

        areas = client.get("task_areas", [])
        areas_text = "\n".join(f"• {x}" for x in areas) if areas else "–"
        aufgaben = InfoBlock("Aufgabenbereiche", [
            ("Bestellt für", areas_text),
        ])

        versorgung = InfoBlock("Versorgung", [
            ("Krankenkasse", client.get("health_insurance")),
            ("Pflegegrad", client.get("care_level")),
            ("GdB", client.get("gdb")),
        ])

        self.overview_layout.addWidget(stammdaten, 0, 0)
        self.overview_layout.addWidget(betreuung, 0, 1)
        self.overview_layout.addWidget(aufgaben, 1, 0)
        self.overview_layout.addWidget(versorgung, 1, 1)
        self.overview_layout.setColumnStretch(0, 1)
        self.overview_layout.setColumnStretch(1, 1)
        self.overview_layout.setRowStretch(2, 1)

        self.notes.setText(value_or_dash(client.get("notes")))


class ClientsModule(QWidget):
    def __init__(self, client_store, parent=None):
        super().__init__(parent)
        self.setObjectName("transparentPage")
        self.store = client_store
        self.selected_id = None
        self.list_buttons = {}

        outer = QVBoxLayout(self)
        outer.setContentsMargins(18, 16, 18, 18)
        outer.setSpacing(12)

        header = QFrame()
        header.setObjectName("glassPanel")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(14, 11, 14, 11)

        title = QLabel("Betreute")
        title.setObjectName("pageTitleSmall")
        header_layout.addWidget(title)
        header_layout.addStretch(1)

        self.search = QLineEdit()
        self.search.setObjectName("clientSearch")
        self.search.setPlaceholderText("Name oder Aktenzeichen suchen")
        self.search.setClearButtonEnabled(True)
        self.search.setMaximumWidth(360)
        self.search.textChanged.connect(self.refresh_list)
        header_layout.addWidget(self.search)

        add_btn = QPushButton("+  Betreuten anlegen")
        add_btn.setObjectName("primaryButton")
        add_btn.clicked.connect(self.add_client)
        header_layout.addWidget(add_btn)

        outer.addWidget(header)

        body = QHBoxLayout()
        body.setSpacing(12)
        outer.addLayout(body, 1)

        left = QFrame()
        left.setObjectName("glassPanel")
        left.setMinimumWidth(280)
        left.setMaximumWidth(340)
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(10, 10, 10, 10)
        left_layout.setSpacing(8)

        self.count_label = QLabel()
        self.count_label.setObjectName("smallMuted")
        left_layout.addWidget(self.count_label)

        self.list_scroll = QScrollArea()
        self.list_scroll.setWidgetResizable(True)
        self.list_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.list_container = QWidget()
        self.list_container.setObjectName("transparentPage")
        self.list_layout = QVBoxLayout(self.list_container)
        self.list_layout.setContentsMargins(0, 0, 0, 0)
        self.list_layout.setSpacing(6)
        self.list_layout.addStretch(1)
        self.list_scroll.setWidget(self.list_container)
        left_layout.addWidget(self.list_scroll, 1)

        body.addWidget(left)

        right = QFrame()
        right.setObjectName("glassPanel")
        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(12, 12, 12, 12)

        self.detail_stack = QStackedWidget()
        self.detail_stack.setObjectName("transparentStack")

        empty = QWidget()
        empty_layout = QVBoxLayout(empty)
        empty_layout.setAlignment(Qt.AlignCenter)
        empty_title = QLabel("Betreuten auswählen")
        empty_title.setObjectName("sectionTitle")
        empty_layout.addWidget(empty_title, alignment=Qt.AlignCenter)

        self.detail = ClientDetail()
        self.detail.edit_requested.connect(self.edit_client)

        self.detail_stack.addWidget(empty)
        self.detail_stack.addWidget(self.detail)
        right_layout.addWidget(self.detail_stack)
        body.addWidget(right, 1)

        self.refresh_list()

    def refresh_list(self):
        query = self.search.text().strip().lower()
        clients = self.store.all()
        if query:
            clients = [
                c for c in clients
                if query in f"{c.get('first_name', '')} {c.get('last_name', '')}".lower()
                or query in c.get("file_number", "").lower()
            ]

        while self.list_layout.count():
            item = self.list_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        self.list_buttons = {}
        active_count = sum(1 for c in self.store.all() if c.get("status", "Aktiv") != "Beendet")
        self.count_label.setText(f"{active_count} aktiv · {len(self.store.all())} gesamt")

        if not clients:
            label = QLabel("Keine Betreuten gefunden" if query else "Noch keine Betreuten angelegt")
            label.setObjectName("smallMuted")
            label.setWordWrap(True)
            self.list_layout.addWidget(label)
            self.list_layout.addStretch(1)
            self.detail_stack.setCurrentIndex(0)
            return

        for client in clients:
            btn = ClientListButton(client)
            btn.clicked.connect(lambda checked=False, cid=client.get("id"): self.select_client(cid))
            self.list_buttons[client.get("id")] = btn
            self.list_layout.addWidget(btn)

        self.list_layout.addStretch(1)

        if self.selected_id and self.store.get(self.selected_id):
            self.select_client(self.selected_id)
        else:
            self.select_client(clients[0].get("id"))

    def select_client(self, client_id):
        client = self.store.get(client_id)
        if not client:
            self.detail_stack.setCurrentIndex(0)
            return

        self.selected_id = client_id
        for cid, button in self.list_buttons.items():
            button.setChecked(cid == client_id)

        self.detail.set_client(client)
        self.detail_stack.setCurrentIndex(1)

    def add_client(self):
        dialog = ClientDialog(parent=self)
        if dialog.exec() == QDialog.Accepted:
            client = self.store.add(dialog.data())
            self.selected_id = client.get("id")
            self.refresh_list()

    def edit_client(self, client_id):
        client = self.store.get(client_id)
        if not client:
            return
        dialog = ClientDialog(client=client, parent=self)
        if dialog.exec() == QDialog.Accepted:
            self.store.update(client_id, dialog.data())
            self.selected_id = client_id
            self.refresh_list()

