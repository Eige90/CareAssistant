from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFrame, QHBoxLayout, QToolButton, QLabel, QMenu, QWidgetAction

from ui.profile_popup import ProfilePopupWidget
from app_info import APP_NAME


class TopBar(QFrame):
    back_requested = Signal()
    forward_requested = Signal()
    home_requested = Signal()
    calendar_requested = Signal()
    settings_requested = Signal()
    profile_requested = Signal()
    about_requested = Signal()
    exit_requested = Signal()
    logout_requested = Signal()

    def __init__(self, settings, parent=None):
        super().__init__(parent)
        self.settings = settings
        self.setObjectName("topBar")
        self.setFixedHeight(44)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 5, 8, 5)
        layout.setSpacing(2)

        self.file_btn = self._menu_button("Datei")
        file_menu = QMenu(self.file_btn)
        exit_action = file_menu.addAction("Beenden")
        exit_action.triggered.connect(self.exit_requested.emit)
        self.file_btn.setMenu(file_menu)

        self.view_btn = self._menu_button("Ansicht")
        view_menu = QMenu(self.view_btn)
        home_action = view_menu.addAction("Home")
        cal_action = view_menu.addAction("Kalender")
        home_action.triggered.connect(self.home_requested.emit)
        cal_action.triggered.connect(self.calendar_requested.emit)
        self.view_btn.setMenu(view_menu)

        self.account_btn = self._menu_button("Konto")
        account_menu = QMenu(self.account_btn)
        profile_action = account_menu.addAction("Profil bearbeiten")
        settings_action = account_menu.addAction("Einstellungen")
        profile_action.triggered.connect(self.profile_requested.emit)
        settings_action.triggered.connect(self.settings_requested.emit)
        self.account_btn.setMenu(account_menu)

        self.help_btn = self._menu_button("Hilfe")
        help_menu = QMenu(self.help_btn)
        about_action = help_menu.addAction("Über das Programm")
        about_action.triggered.connect(self.about_requested.emit)
        self.help_btn.setMenu(help_menu)

        for button in (self.file_btn, self.view_btn, self.account_btn, self.help_btn):
            layout.addWidget(button)

        layout.addSpacing(6)

        separator = QFrame()
        separator.setObjectName("topSeparator")
        separator.setFixedHeight(22)
        layout.addWidget(separator)
        layout.addSpacing(6)

        self.back_btn = self._nav_button("‹", "Zurück")
        self.forward_btn = self._nav_button("›", "Vor")
        self.home_btn = self._nav_button("⌂", "Home")

        self.back_btn.clicked.connect(self.back_requested.emit)
        self.forward_btn.clicked.connect(self.forward_requested.emit)
        self.home_btn.clicked.connect(self.home_requested.emit)

        layout.addWidget(self.back_btn)
        layout.addWidget(self.forward_btn)
        layout.addWidget(self.home_btn)

        self.title = QLabel(APP_NAME)
        self.title.setObjectName("topBarTitle")
        layout.addSpacing(5)
        layout.addWidget(self.title)

        layout.addStretch(1)

        self.profile_btn = QToolButton()
        self.profile_btn.setObjectName("profileButton")
        self.profile_btn.setPopupMode(QToolButton.InstantPopup)

        self.profile_menu = QMenu(self.profile_btn)
        self.profile_widget = ProfilePopupWidget(settings)
        action = QWidgetAction(self.profile_menu)
        action.setDefaultWidget(self.profile_widget)
        self.profile_menu.addAction(action)
        self.profile_btn.setMenu(self.profile_menu)

        self.profile_widget.edit_profile_requested.connect(self._edit_profile_from_popup)
        self.profile_widget.settings_requested.connect(self._settings_from_popup)
        self.profile_widget.about_requested.connect(self._about_from_popup)
        self.profile_widget.logout_requested.connect(self._logout_from_popup)

        layout.addWidget(self.profile_btn)
        self.refresh_profile()

    @staticmethod
    def _menu_button(text):
        btn = QToolButton()
        btn.setObjectName("menuButton")
        btn.setText(text)
        btn.setPopupMode(QToolButton.InstantPopup)
        return btn

    @staticmethod
    def _nav_button(text, tooltip):
        btn = QToolButton()
        btn.setObjectName("navButton")
        btn.setText(text)
        btn.setToolTip(tooltip)
        return btn

    def refresh_profile(self):
        name = self.settings.profile_name.strip()
        self.profile_btn.setText(name if name else "Profil")
        self.profile_widget.refresh()

    def set_navigation_state(self, can_back, can_forward):
        self.back_btn.setEnabled(can_back)
        self.forward_btn.setEnabled(can_forward)

    def _edit_profile_from_popup(self):
        self.profile_menu.hide()
        self.profile_requested.emit()

    def _settings_from_popup(self):
        self.profile_menu.hide()
        self.settings_requested.emit()

    def _about_from_popup(self):
        self.profile_menu.hide()
        self.about_requested.emit()

    def _logout_from_popup(self):
        self.profile_menu.hide()
        self.logout_requested.emit()

    def resizeEvent(self, event):
        width = event.size().width()
        self.title.setVisible(width >= 790)

        compact = width < 620
        self.file_btn.setVisible(not compact)
        self.account_btn.setVisible(not compact)
        self.help_btn.setVisible(not compact)
        # Ansicht remains visible because it contains the main page navigation.
        super().resizeEvent(event)
