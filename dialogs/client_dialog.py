from datetime import date

from PySide6.QtCore import QDate
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QFormLayout, QLineEdit, QDialogButtonBox,
    QTabWidget, QWidget, QTextEdit, QDateEdit
)

from core.validation import PHONE_ALLOWED_RE, email_is_valid, phone_is_valid
from ui.controls import ModernComboBox


class ClientDialog(QDialog):
    def __init__(self, client=None, parent=None):
        super().__init__(parent)
        self.client = client or {}
        self.setWindowTitle("Betreuten bearbeiten" if client else "Betreuten anlegen")
        self.setMinimumSize(660, 620)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(20, 20, 20, 18)
        outer.setSpacing(12)

        title = QLabel("Betreuten bearbeiten" if client else "Betreuten anlegen")
        title.setObjectName("dialogTitle")
        outer.addWidget(title)

        self.tabs = QTabWidget()
        self.tabs.setObjectName("clientTabs")
        outer.addWidget(self.tabs, 1)

        self._build_personal_tab()
        self._build_case_tab()
        self._build_care_tab()

        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self._attempt_save)
        buttons.rejected.connect(self.reject)
        outer.addWidget(buttons)

        self._load()

    def _build_personal_tab(self):
        page = QWidget()
        form = QFormLayout(page)
        form.setContentsMargins(16, 16, 16, 16)
        form.setHorizontalSpacing(20)
        form.setVerticalSpacing(10)

        self.first_name = QLineEdit()
        self.last_name = QLineEdit()
        self.birth_date = QDateEdit()
        self.birth_date.setCalendarPopup(True)
        self.birth_date.setDisplayFormat("dd.MM.yyyy")
        self.birth_date.setDate(QDate(1980, 1, 1))
        self.street = QLineEdit()
        self.postal_code = QLineEdit()
        self.city = QLineEdit()
        self.phone = QLineEdit()
        self.phone.setValidator(QRegularExpressionValidator(PHONE_ALLOWED_RE, self))
        self.email = QLineEdit()

        self.email_error = QLabel("Bitte eine vollständige E-Mail-Adresse eingeben.")
        self.email_error.setObjectName("validationError")
        self.email_error.hide()
        self.phone_error = QLabel("Telefonnummer muss 5–15 Ziffern enthalten.")
        self.phone_error.setObjectName("validationError")
        self.phone_error.hide()

        self.email.textChanged.connect(self._validate_email_live)
        self.phone.textChanged.connect(self._validate_phone_live)

        form.addRow("Vorname*:", self.first_name)
        form.addRow("Nachname*:", self.last_name)
        form.addRow("Geburtsdatum:", self.birth_date)
        form.addRow("Straße / Nr.:", self.street)
        form.addRow("PLZ:", self.postal_code)
        form.addRow("Ort:", self.city)
        form.addRow("Telefon:", self.phone)
        form.addRow("", self.phone_error)
        form.addRow("E-Mail:", self.email)
        form.addRow("", self.email_error)

        self.tabs.addTab(page, "Stammdaten")

    def _build_case_tab(self):
        page = QWidget()
        form = QFormLayout(page)
        form.setContentsMargins(16, 16, 16, 16)
        form.setHorizontalSpacing(20)
        form.setVerticalSpacing(10)

        self.court = QLineEdit()
        self.file_number = QLineEdit()
        self.appointment_date = QDateEdit()
        self.appointment_date.setCalendarPopup(True)
        self.appointment_date.setDisplayFormat("dd.MM.yyyy")
        self.appointment_date.setDate(QDate.currentDate())

        self.status = ModernComboBox()
        self.status.addItems(["Aktiv", "Ruhend", "Beendet"])

        self.task_areas = QTextEdit()
        self.task_areas.setPlaceholderText("Ein Aufgabenbereich pro Zeile")
        self.task_areas.setMinimumHeight(150)

        form.addRow("Betreuungsgericht:", self.court)
        form.addRow("Aktenzeichen:", self.file_number)
        form.addRow("Bestellung seit:", self.appointment_date)
        form.addRow("Status:", self.status)
        form.addRow("Aufgabenbereiche:", self.task_areas)

        self.tabs.addTab(page, "Betreuung")

    def _build_care_tab(self):
        page = QWidget()
        form = QFormLayout(page)
        form.setContentsMargins(16, 16, 16, 16)
        form.setHorizontalSpacing(20)
        form.setVerticalSpacing(10)

        self.health_insurance = QLineEdit()
        self.care_level = ModernComboBox()
        self.care_level.addItems(["", "1", "2", "3", "4", "5"])
        self.gdb = QLineEdit()
        self.notes = QTextEdit()
        self.notes.setMinimumHeight(160)

        form.addRow("Krankenkasse:", self.health_insurance)
        form.addRow("Pflegegrad:", self.care_level)
        form.addRow("GdB:", self.gdb)
        form.addRow("Interne Notizen:", self.notes)

        self.tabs.addTab(page, "Versorgung")

    @staticmethod
    def _date_from_iso(value, fallback):
        if not value:
            return fallback
        parsed = QDate.fromString(value, "yyyy-MM-dd")
        return parsed if parsed.isValid() else fallback

    def _load(self):
        c = self.client
        self.first_name.setText(c.get("first_name", ""))
        self.last_name.setText(c.get("last_name", ""))
        self.birth_date.setDate(self._date_from_iso(c.get("birth_date"), QDate(1980, 1, 1)))
        self.street.setText(c.get("street", ""))
        self.postal_code.setText(c.get("postal_code", ""))
        self.city.setText(c.get("city", ""))
        self.phone.setText(c.get("phone", ""))
        self.email.setText(c.get("email", ""))
        self.court.setText(c.get("court", ""))
        self.file_number.setText(c.get("file_number", ""))
        self.appointment_date.setDate(
            self._date_from_iso(c.get("appointment_date"), QDate.currentDate())
        )
        status = c.get("status", "Aktiv")
        idx = self.status.findText(status)
        self.status.setCurrentIndex(idx if idx >= 0 else 0)
        self.task_areas.setPlainText("\n".join(c.get("task_areas", [])))
        self.health_insurance.setText(c.get("health_insurance", ""))
        care_level = str(c.get("care_level", "") or "")
        idx = self.care_level.findText(care_level)
        self.care_level.setCurrentIndex(idx if idx >= 0 else 0)
        self.gdb.setText(str(c.get("gdb", "") or ""))
        self.notes.setPlainText(c.get("notes", ""))
        self._validate_email_live(self.email.text())
        self._validate_phone_live(self.phone.text())

    def _set_validity(self, widget, valid, error):
        widget.setProperty("invalid", not valid)
        widget.style().unpolish(widget)
        widget.style().polish(widget)
        error.setVisible(not valid)

    def _validate_email_live(self, text):
        self._set_validity(self.email, email_is_valid(text), self.email_error)

    def _validate_phone_live(self, text):
        self._set_validity(self.phone, phone_is_valid(text), self.phone_error)

    def _attempt_save(self):
        if not self.first_name.text().strip():
            self.first_name.setFocus()
            return
        if not self.last_name.text().strip():
            self.last_name.setFocus()
            return
        if not email_is_valid(self.email.text()):
            self.tabs.setCurrentIndex(0)
            self._validate_email_live(self.email.text())
            self.email.setFocus()
            return
        if not phone_is_valid(self.phone.text()):
            self.tabs.setCurrentIndex(0)
            self._validate_phone_live(self.phone.text())
            self.phone.setFocus()
            return
        self.accept()

    def data(self):
        birth = self.birth_date.date()
        appointment = self.appointment_date.date()
        task_areas = [
            line.strip()
            for line in self.task_areas.toPlainText().splitlines()
            if line.strip()
        ]
        return {
            "first_name": self.first_name.text().strip(),
            "last_name": self.last_name.text().strip(),
            "birth_date": birth.toString("yyyy-MM-dd"),
            "street": self.street.text().strip(),
            "postal_code": self.postal_code.text().strip(),
            "city": self.city.text().strip(),
            "phone": self.phone.text().strip(),
            "email": self.email.text().strip(),
            "court": self.court.text().strip(),
            "file_number": self.file_number.text().strip(),
            "appointment_date": appointment.toString("yyyy-MM-dd"),
            "status": self.status.currentText(),
            "task_areas": task_areas,
            "health_insurance": self.health_insurance.text().strip(),
            "care_level": self.care_level.currentText(),
            "gdb": self.gdb.text().strip(),
            "notes": self.notes.toPlainText().strip(),
        }
