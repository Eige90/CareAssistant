from PySide6.QtCore import QSettings

from app_info import APP_NAME, ORGANIZATION_NAME


class AppSettings:
    def __init__(self):
        self._settings = QSettings(ORGANIZATION_NAME, APP_NAME)

    def _get(self, key, default="", typ=str):
        return self._settings.value(key, default, type=typ)

    def _set(self, key, value):
        self._settings.setValue(key, value)

    @property
    def theme(self):
        return self._get("appearance/theme", "dark")

    @theme.setter
    def theme(self, value):
        self._set("appearance/theme", value)

    @property
    def start_page(self):
        return self._get("general/start_page", "home")

    @start_page.setter
    def start_page(self, value):
        self._set("general/start_page", value)

    @property
    def background_id(self):
        return self._get("appearance/background_id", "starry_night")

    @background_id.setter
    def background_id(self, value):
        self._set("appearance/background_id", value)

    @property
    def custom_background(self):
        return self._get("appearance/custom_background", "")

    @custom_background.setter
    def custom_background(self, value):
        self._set("appearance/custom_background", value)

    @property
    def profile_name(self):
        return self._get("profile/name", "")

    @profile_name.setter
    def profile_name(self, value):
        self._set("profile/name", value)

    @property
    def profile_email(self):
        return self._get("profile/email", "")

    @profile_email.setter
    def profile_email(self, value):
        self._set("profile/email", value)

    @property
    def profile_phone(self):
        return self._get("profile/phone", "")

    @profile_phone.setter
    def profile_phone(self, value):
        self._set("profile/phone", value)

    @property
    def profile_organization(self):
        return self._get("profile/organization", "")

    @profile_organization.setter
    def profile_organization(self, value):
        self._set("profile/organization", value)

    @property
    def profile_picture(self):
        return self._get("profile/picture", "")

    @profile_picture.setter
    def profile_picture(self, value):
        self._set("profile/picture", value)

    def sync(self):
        self._settings.sync()
