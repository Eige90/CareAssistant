import sys
from pathlib import Path

from PySide6.QtCore import QDate
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QStackedWidget, QDialog

from app_info import APP_NAME
from core.settings import AppSettings
from core.event_store import EventStore
from core.client_store import ClientStore
from core.artwork import ensure_starry_night
from ui.background import BackgroundWidget
from ui.theme import ThemeManager
from ui.top_bar import TopBar
from modules.home import HomePage
from modules.calendar_module import CalendarModule
from modules.clients_module import ClientsModule
from modules.placeholder_module import PlaceholderModule
from modules.session import SignedOutPage
from dialogs.settings_dialog import SettingsDialog
from dialogs.profile_dialog import ProfileDialog
from dialogs.about_dialog import AboutDialog
from dialogs.event_dialog import EventDialog


class MainWindow(QMainWindow):
    def __init__(self, app, theme_manager, settings):
        super().__init__()
        self.app = app
        self.theme_manager = theme_manager
        self.settings = settings
        self.event_store = EventStore()
        self.client_store = ClientStore()
        self.logged_out = False

        self.setWindowTitle(APP_NAME)
        self.resize(1440, 900)
        self.setMinimumSize(760, 560)

        self.pages = {}
        self.history = []
        self.history_index = -1

        self.background = BackgroundWidget()
        self.setCentralWidget(self.background)

        layout = QVBoxLayout(self.background)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.top_bar = TopBar(settings)
        self.stack = QStackedWidget()
        self.stack.setObjectName("pageStack")

        layout.addWidget(self.top_bar)
        layout.addWidget(self.stack, 1)

        self._connect_top_bar()
        self._create_pages()
        self._create_shortcuts()
        self.apply_background()

        start = self.settings.start_page if self.settings.start_page in self.pages else "home"
        self.navigate(start)

    def _preset_paths(self):
        base = Path(__file__).resolve().parent / "assets" / "backgrounds"
        fallback = str(base / "preset_1.jpg")
        starry = ensure_starry_night(fallback)
        return {
            "starry_night": starry,
            "preset_2": str(base / "preset_2.jpg"),
            "preset_3": str(base / "preset_3.jpg"),
            "preset_4": str(base / "preset_4.jpg"),
            "preset_5": str(base / "preset_5.jpg"),
        }

    def apply_background(self):
        bg_id = self.settings.background_id
        if bg_id == "custom" and self.settings.custom_background:
            path = self.settings.custom_background
        else:
            presets = self._preset_paths()
            path = presets.get(bg_id, presets["starry_night"])
        self.background.set_background_path(path)

    def _connect_top_bar(self):
        self.top_bar.back_requested.connect(self.go_back)
        self.top_bar.forward_requested.connect(self.go_forward)
        self.top_bar.home_requested.connect(lambda: self.navigate("home"))
        self.top_bar.calendar_requested.connect(lambda: self.navigate("calendar"))
        self.top_bar.profile_requested.connect(self.open_profile)
        self.top_bar.settings_requested.connect(self.open_settings)
        self.top_bar.about_requested.connect(self.open_about)
        self.top_bar.exit_requested.connect(self.close)
        self.top_bar.logout_requested.connect(self.logout)

    def _create_pages(self):
        self.home_page = HomePage(self.event_store)
        self.calendar_page = CalendarModule(self.event_store)
        self.clients_page = ClientsModule(self.client_store)
        self.signed_out_page = SignedOutPage()

        self.home_page.open_calendar.connect(self.open_calendar_on_date)
        self.home_page.open_module.connect(self.open_module)
        self.home_page.add_event_requested.connect(self.open_new_event)
        self.calendar_page.add_event_requested.connect(self.open_new_event)
        self.signed_out_page.login_requested.connect(self.login)

        self.register_page("home", self.home_page)
        self.register_page("calendar", self.calendar_page)
        self.register_page("clients", self.clients_page)
        self.register_page("signed_out", self.signed_out_page)

    def _create_shortcuts(self):
        back_shortcut = QShortcut(QKeySequence("Alt+Left"), self)
        forward_shortcut = QShortcut(QKeySequence("Alt+Right"), self)
        home_shortcut = QShortcut(QKeySequence("Ctrl+Home"), self)

        back_shortcut.activated.connect(self.go_back)
        forward_shortcut.activated.connect(self.go_forward)
        home_shortcut.activated.connect(lambda: self.navigate("home"))

        self._shortcuts = [back_shortcut, forward_shortcut, home_shortcut]

    def register_page(self, key, widget):
        self.pages[key] = widget
        self.stack.addWidget(widget)

    def navigate(self, key, add_history=True):
        if self.logged_out and key != "signed_out":
            return
        if key not in self.pages:
            return

        if add_history and key != "signed_out":
            if self.history_index < len(self.history) - 1:
                self.history = self.history[:self.history_index + 1]
            if not self.history or self.history[-1] != key:
                self.history.append(key)
                self.history_index = len(self.history) - 1

        self.stack.setCurrentWidget(self.pages[key])
        self._update_navigation_buttons()

    def go_back(self):
        if self.logged_out or self.history_index <= 0:
            return
        self.history_index -= 1
        self.navigate(self.history[self.history_index], add_history=False)

    def go_forward(self):
        if self.logged_out or self.history_index >= len(self.history) - 1:
            return
        self.history_index += 1
        self.navigate(self.history[self.history_index], add_history=False)

    def _update_navigation_buttons(self):
        self.top_bar.set_navigation_state(
            not self.logged_out and self.history_index > 0,
            not self.logged_out and self.history_index < len(self.history) - 1,
        )

    def open_calendar_on_date(self, qdate):
        self.calendar_page.set_selected_date(qdate)
        self.navigate("calendar")

    def open_module(self, name):
        if name == "Betreute":
            self.navigate("clients")
            return

        key = f"module:{name}"
        if key not in self.pages:
            self.register_page(key, PlaceholderModule(name))
        self.navigate(key)

    def open_profile(self):
        dialog = ProfileDialog(self.settings, self)
        if dialog.exec() == QDialog.Accepted:
            dialog.save_to_settings()
            self.top_bar.refresh_profile()

    def open_settings(self):
        dialog = SettingsDialog(self.settings, self._preset_paths(), self)
        if dialog.exec() == QDialog.Accepted:
            dialog.save_to_settings()
            self.theme_manager.apply(self.settings.theme)
            self.apply_background()
            self.top_bar.refresh_profile()

    def open_about(self):
        AboutDialog(self).exec()

    def open_new_event(self, initial_date=None):
        if initial_date is None or not isinstance(initial_date, QDate):
            initial_date = QDate.currentDate()

        dialog = EventDialog(initial_date, self)
        if dialog.exec() == QDialog.Accepted:
            self.event_store.add(dialog.event_data())
            self.home_page.refresh_events()
            self.calendar_page.refresh()

    def logout(self):
        self.logged_out = True
        self.top_bar.hide()
        self.stack.setCurrentWidget(self.signed_out_page)
        self._update_navigation_buttons()

    def login(self):
        self.logged_out = False
        self.top_bar.show()
        self.top_bar.refresh_profile()
        self.navigate("home", add_history=False)


def main():
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setOrganizationName(APP_NAME)
    app.setStyle("Fusion")

    settings = AppSettings()
    theme_manager = ThemeManager(app)
    theme_manager.apply(settings.theme)

    window = MainWindow(app, theme_manager, settings)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
