import shutil
from pathlib import Path

from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QFormLayout, QLineEdit, QDialogButtonBox,
    QHBoxLayout, QPushButton, QFileDialog
)

from core.paths import PROFILE_DIR
from core.validation import PHONE_ALLOWED_RE, email_is_valid, phone_is_valid
from ui.avatar import EditableAvatar


class ProfileDialog(QDialog):
    def __init__(self, settings, parent=None):
        super().__init__(parent)
        self.settings = settings
        self.selected_picture = settings.profile_picture

        self.setWindowTitle("Profil bearbeiten")
        self.setMinimumWidth(500)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 18)
        layout.setSpacing(13)

        title = QLabel("Profil bearbeiten")
        title.setObjectName("dialogTitle")
        layout.addWidget(title)

        picture_row = QHBoxLayout()
        picture_row.setSpacing(12)
        self.avatar = EditableAvatar(82)
        self.avatar.set_data(self.selected_picture, settings.profile_name)
        self.avatar.remove_requested.connect(self.remove_picture)
        picture_row.addWidget(self.avatar)

        choose_btn = QPushButton("Profilbild auswählen …")
        choose_btn.clicked.connect(self.choose_picture)
        picture_row.addWidget(choose_btn)
        picture_row.addStretch(1)
        layout.addLayout(picture_row)

        form = QFormLayout()
        form.setHorizontalSpacing(18)
        form.setVerticalSpacing(7)

        self.name_edit = QLineEdit(settings.profile_name)
        self.email_edit = QLineEdit(settings.profile_email)
        self.phone_edit = QLineEdit(settings.profile_phone)
        self.organization_edit = QLineEdit(settings.profile_organization)

        self.phone_edit.setValidator(QRegularExpressionValidator(PHONE_ALLOWED_RE, self))

        self.email_error = QLabel("Bitte eine vollständige E-Mail-Adresse eingeben.")
        self.email_error.setObjectName("validationError")
        self.email_error.hide()

        self.phone_error = QLabel("Telefonnummer muss 5–15 Ziffern enthalten.")
        self.phone_error.setObjectName("validationError")
        self.phone_error.hide()

        self.name_edit.textChanged.connect(
            lambda text: self.avatar.set_data(self.selected_picture, text)
        )
        self.email_edit.textChanged.connect(self._validate_email_live)
        self.phone_edit.textChanged.connect(self._validate_phone_live)

        form.addRow("Name:", self.name_edit)
        form.addRow("E-Mail:", self.email_edit)
        form.addRow("", self.email_error)
        form.addRow("Telefon:", self.phone_edit)
        form.addRow("", self.phone_error)
        form.addRow("Organisation:", self.organization_edit)
        layout.addLayout(form)

        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self._attempt_save)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self._validate_email_live(self.email_edit.text())
        self._validate_phone_live(self.phone_edit.text())

    def choose_picture(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Profilbild auswählen",
            "",
            "Bilder (*.png *.jpg *.jpeg *.webp *.bmp)",
        )
        if not path:
            return
        self.selected_picture = path
        self.avatar.set_data(path, self.name_edit.text())

    def remove_picture(self):
        self.selected_picture = ""
        self.avatar.set_data("", self.name_edit.text())

    def _set_validity(self, widget, valid, error_label):
        widget.setProperty("invalid", not valid)
        widget.style().unpolish(widget)
        widget.style().polish(widget)
        error_label.setVisible(not valid)

    def _validate_email_live(self, text):
        self._set_validity(self.email_edit, email_is_valid(text), self.email_error)

    def _validate_phone_live(self, text):
        self._set_validity(self.phone_edit, phone_is_valid(text), self.phone_error)

    def _attempt_save(self):
        email_ok = email_is_valid(self.email_edit.text())
        phone_ok = phone_is_valid(self.phone_edit.text())
        self._validate_email_live(self.email_edit.text())
        self._validate_phone_live(self.phone_edit.text())

        if not email_ok:
            self.email_edit.setFocus()
            return
        if not phone_ok:
            self.phone_edit.setFocus()
            return
        self.accept()

    def save_to_settings(self):
        stored_path = ""
        if self.selected_picture:
            source = Path(self.selected_picture)
            if source.exists():
                suffix = source.suffix.lower() if source.suffix else ".png"
                target = PROFILE_DIR / f"avatar{suffix}"
                if source.resolve() != target.resolve():
                    shutil.copy2(source, target)
                stored_path = str(target)

        self.settings.profile_name = self.name_edit.text().strip()
        self.settings.profile_email = self.email_edit.text().strip()
        self.settings.profile_phone = self.phone_edit.text().strip()
        self.settings.profile_organization = self.organization_edit.text().strip()
        self.settings.profile_picture = stored_path
        self.settings.sync()
