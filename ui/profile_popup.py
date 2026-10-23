from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton

from ui.avatar import AvatarWidget


class ProfilePopupWidget(QWidget):
    edit_profile_requested = Signal()
    settings_requested = Signal()
    about_requested = Signal()
    logout_requested = Signal()

    def __init__(self, settings, parent=None):
        super().__init__(parent)
        self.settings = settings
        self.setMinimumWidth(330)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 10)
        layout.setSpacing(10)

        self.org = QLabel()
        self.org.setObjectName("profileOrg")
        layout.addWidget(self.org)

        row = QHBoxLayout()
        row.setSpacing(12)

        self.avatar = AvatarWidget(58)
        row.addWidget(self.avatar)

        info = QVBoxLayout()
        info.setSpacing(2)
        self.name = QLabel()
        self.name.setObjectName("profileName")
        self.email = QLabel()
        self.email.setObjectName("profileDetail")
        self.phone = QLabel()
        self.phone.setObjectName("profileDetail")
        info.addWidget(self.name)
        info.addWidget(self.email)
        info.addWidget(self.phone)
        row.addLayout(info, 1)
        layout.addLayout(row)

        self.edit_btn = self._row_button("Profil bearbeiten   ›")
        self.settings_btn = self._row_button("Einstellungen   ›")
        self.about_btn = self._row_button("Über das Programm   ›")
        self.logout_btn = self._row_button("Abmelden")
        self.logout_btn.setObjectName("logoutButton")

        self.edit_btn.clicked.connect(self.edit_profile_requested.emit)
        self.settings_btn.clicked.connect(self.settings_requested.emit)
        self.about_btn.clicked.connect(self.about_requested.emit)
        self.logout_btn.clicked.connect(self.logout_requested.emit)

        layout.addWidget(self.edit_btn)
        layout.addWidget(self.settings_btn)
        layout.addWidget(self.about_btn)
        layout.addWidget(self.logout_btn)

        self.refresh()

    @staticmethod
    def _row_button(text):
        btn = QPushButton(text)
        btn.setObjectName("profileEditButton")
        return btn

    def refresh(self):
        org = self.settings.profile_organization.strip() or "Organisation"
        name = self.settings.profile_name.strip() or "Profil"
        email = self.settings.profile_email.strip() or "Keine E-Mail hinterlegt"
        phone = self.settings.profile_phone.strip() or "Keine Telefonnummer hinterlegt"

        self.org.setText(org)
        self.name.setText(name)
        self.email.setText(email)
        self.phone.setText(phone)
        self.avatar.set_data(self.settings.profile_picture, name)
