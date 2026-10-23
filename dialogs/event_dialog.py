from datetime import date

from PySide6.QtCore import QDate, QTime
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QFormLayout, QLineEdit, QDateEdit, QTimeEdit,
    QCheckBox, QTextEdit, QDialogButtonBox, QMessageBox
)


class EventDialog(QDialog):
    def __init__(self, initial_date=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ereignis hinzufügen")
        self.setMinimumWidth(470)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 18)
        layout.setSpacing(14)

        title = QLabel("Neues Ereignis")
        title.setObjectName("dialogTitle")
        layout.addWidget(title)

        form = QFormLayout()
        form.setHorizontalSpacing(18)
        form.setVerticalSpacing(12)

        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("z. B. Hausbesuch Frau Müller")

        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        d = initial_date or date.today()
        if hasattr(d, "year") and callable(getattr(d, "year", None)):
            # QDate
            qdate = d
        else:
            qdate = QDate(d.year, d.month, d.day)
        self.date_edit.setDate(qdate)

        self.all_day = QCheckBox("Ganztägig")
        self.start_edit = QTimeEdit(QTime(9, 0))
        self.end_edit = QTimeEdit(QTime(10, 0))

        self.person_edit = QLineEdit()
        self.person_edit.setPlaceholderText("optional")

        self.location_edit = QLineEdit()
        self.location_edit.setPlaceholderText("optional")

        self.notes_edit = QTextEdit()
        self.notes_edit.setFixedHeight(90)

        self.all_day.toggled.connect(self._toggle_times)

        form.addRow("Titel:", self.title_edit)
        form.addRow("Datum:", self.date_edit)
        form.addRow("", self.all_day)
        form.addRow("Von:", self.start_edit)
        form.addRow("Bis:", self.end_edit)
        form.addRow("Betreuter:", self.person_edit)
        form.addRow("Ort:", self.location_edit)
        form.addRow("Notizen:", self.notes_edit)

        layout.addLayout(form)

        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self._validate)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _toggle_times(self, checked):
        self.start_edit.setEnabled(not checked)
        self.end_edit.setEnabled(not checked)

    def _validate(self):
        if not self.title_edit.text().strip():
            QMessageBox.warning(self, "Titel fehlt", "Bitte gib einen Titel für das Ereignis ein.")
            return

        if not self.all_day.isChecked() and self.end_edit.time() <= self.start_edit.time():
            QMessageBox.warning(self, "Uhrzeit prüfen", "Die Endzeit muss nach der Startzeit liegen.")
            return

        self.accept()

    def event_data(self):
        d = self.date_edit.date()
        all_day = self.all_day.isChecked()

        return {
            "title": self.title_edit.text().strip(),
            "date": f"{d.year():04d}-{d.month():02d}-{d.day():02d}",
            "all_day": all_day,
            "start_time": "" if all_day else self.start_edit.time().toString("HH:mm"),
            "end_time": "" if all_day else self.end_edit.time().toString("HH:mm"),
            "person": self.person_edit.text().strip(),
            "location": self.location_edit.text().strip(),
            "notes": self.notes_edit.toPlainText().strip(),
        }
