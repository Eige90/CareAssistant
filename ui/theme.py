from PySide6.QtGui import QColor, QPalette


LIGHT = {
    "text": "#1d1d1f",
    "muted": "#6e6e73",
    "accent": "#0a84ff",
    "accent_hover": "#0077ed",
    "accent_text": "#ffffff",
    "border": "rgba(255,255,255,120)",
    "glass": "rgba(255,255,255,172)",
    "glass_soft": "rgba(255,255,255,126)",
    "glass_hover": "rgba(255,255,255,205)",
    "menu": "rgba(250,250,252,248)",
    "weekend": "#e6372f",
    "input": "rgba(255,255,255,226)",
    "scroll": "rgba(80,80,86,125)",
    "error": "#d92d20",
    "calendar": "rgba(255,255,255,228)",
    "calendar_alt": "rgba(255,255,255,205)",
    "success": "#238636",
    "warning": "#9a6700",
}

DARK = {
    "text": "#f5f5f7",
    "muted": "#c7c7cc",
    "accent": "#0a84ff",
    "accent_hover": "#409cff",
    "accent_text": "#ffffff",
    "border": "rgba(255,255,255,48)",
    "glass": "rgba(28,28,32,182)",
    "glass_soft": "rgba(31,31,36,150)",
    "glass_hover": "rgba(63,63,70,210)",
    "menu": "rgba(30,30,34,250)",
    "weekend": "#ff6961",
    "input": "rgba(49,49,55,232)",
    "scroll": "rgba(220,220,225,120)",
    "error": "#ff6961",
    "calendar": "rgba(17,17,20,232)",
    "calendar_alt": "rgba(26,26,30,220)",
    "success": "#32d74b",
    "warning": "#ffd60a",
}


class ThemeManager:
    def __init__(self, app):
        self.app = app
        self.system_is_dark = app.palette().color(QPalette.Window).lightness() < 128
        self.active_theme = "dark"

    def apply(self, preference):
        if preference == "system":
            theme_name = "dark" if self.system_is_dark else "light"
        elif preference in ("light", "dark"):
            theme_name = preference
        else:
            theme_name = "dark"

        self.active_theme = theme_name
        c = DARK if theme_name == "dark" else LIGHT

        palette = self.app.palette()
        palette.setColor(QPalette.WindowText, QColor(c["text"]))
        palette.setColor(QPalette.Text, QColor(c["text"]))
        palette.setColor(QPalette.ButtonText, QColor(c["text"]))
        palette.setColor(QPalette.Highlight, QColor(c["accent"]))
        palette.setColor(QPalette.HighlightedText, QColor(c["accent_text"]))
        self.app.setPalette(palette)

        self.app.setStyleSheet(self._stylesheet(c))

    @staticmethod
    def _stylesheet(c):
        return f"""
        * {{
            font-family: "Segoe UI", "Inter", Arial, sans-serif;
            font-size: 14px;
            color: {c["text"]};
        }}

        QWidget#backgroundRoot,
        QWidget#transparentPage,
        QStackedWidget#pageStack {{
            background: transparent;
        }}

        QToolTip {{
            background: {c["menu"]};
            color: {c["text"]};
            border: 1px solid {c["border"]};
            border-radius: 7px;
            padding: 5px 7px;
        }}

        /* ---------- top bar ---------- */

        QFrame#topBar {{
            background: {c["glass"]};
            border-bottom: 1px solid {c["border"]};
        }}

        QToolButton#menuButton {{
            background: transparent;
            border: none;
            border-radius: 8px;
            padding: 6px 9px;
        }}

        QToolButton#menuButton:hover {{
            background: {c["glass_hover"]};
        }}

        QToolButton#menuButton::menu-indicator,
        QToolButton#profileButton::menu-indicator {{
            image: none;
            width: 0px;
            height: 0px;
        }}

        QToolButton#navButton {{
            background: transparent;
            border: none;
            border-radius: 9px;
            min-width: 30px;
            max-width: 30px;
            min-height: 30px;
            max-height: 30px;
            font-size: 18px;
            font-weight: 650;
        }}

        QToolButton#navButton:hover {{
            background: {c["glass_hover"]};
        }}

        QToolButton#navButton:disabled {{
            color: {c["muted"]};
        }}

        QLabel#topBarTitle {{
            font-weight: 700;
            padding-left: 3px;
        }}

        QFrame#topSeparator {{
            background: {c["border"]};
            min-width: 1px;
            max-width: 1px;
        }}

        QToolButton#profileButton {{
            background: {c["glass_soft"]};
            border: 1px solid {c["border"]};
            border-radius: 16px;
            padding: 5px 12px;
            font-weight: 650;
        }}

        QToolButton#profileButton:hover {{
            background: {c["glass_hover"]};
        }}

        QMenu {{
            background: {c["menu"]};
            border: 1px solid {c["border"]};
            border-radius: 10px;
            padding: 5px;
        }}

        QMenu::item {{
            padding: 7px 28px 7px 10px;
            border-radius: 6px;
        }}

        QMenu::item:selected {{
            background: {c["accent"]};
            color: {c["accent_text"]};
        }}

        QMenu::separator {{
            height: 1px;
            background: {c["border"]};
            margin: 5px 8px;
        }}

        /* ---------- typography ---------- */

        QLabel#pageTitle {{
            font-size: 28px;
            font-weight: 750;
        }}

        QLabel#sectionTitle {{
            font-size: 17px;
            font-weight: 700;
        }}

        QLabel#mutedText,
        QLabel#smallMuted {{
            color: {c["muted"]};
        }}

        QLabel#smallMuted {{
            font-size: 12px;
        }}

        QLabel#validationError {{
            color: {c["error"]};
            font-size: 11px;
        }}

        /* ---------- glass ---------- */

        QFrame#glassPanel,
        QFrame#miniMonthCard,
        QFrame#calendarToolbar {{
            background: {c["glass"]};
            border: 1px solid {c["border"]};
            border-radius: 18px;
        }}

        QFrame#miniMonthCard {{
            background: {c["glass_soft"]};
            border-radius: 16px;
        }}

        QPushButton#glassTile {{
            background: {c["glass_soft"]};
            border: 1px solid {c["border"]};
            border-radius: 18px;
            padding: 17px;
            text-align: left;
            font-size: 15px;
            font-weight: 650;
        }}

        QPushButton#glassTile:hover {{
            background: {c["glass_hover"]};
        }}

        /* ---------- mini calendar ---------- */

        QLabel#miniMonthTitle {{
            font-size: 13px;
            font-weight: 700;
        }}

        QLabel#weekday {{
            color: {c["muted"]};
            font-size: 10px;
            font-weight: 650;
        }}

        QLabel#weekendHeader {{
            color: {c["weekend"]};
            font-size: 10px;
            font-weight: 700;
        }}

        QToolButton#miniDay {{
            background: transparent;
            border: none;
            border-radius: 9px;
            padding: 0;
            font-size: 10px;
        }}

        QToolButton#miniDay:hover {{
            background: {c["glass_hover"]};
        }}

        QToolButton#miniDay[weekend="true"] {{
            color: {c["weekend"]};
        }}

        QToolButton#miniDay[today="true"] {{
            background: {c["accent"]};
            color: {c["accent_text"]};
            font-weight: 700;
        }}

        QToolButton#plusButton {{
            background: {c["accent"]};
            color: {c["accent_text"]};
            border: none;
            border-radius: 13px;
            min-width: 26px;
            max-width: 26px;
            min-height: 26px;
            max-height: 26px;
            font-size: 18px;
            font-weight: 600;
        }}

        QToolButton#plusButton:hover {{
            background: {c["accent_hover"]};
        }}

        /* ---------- modern scrollbars ---------- */

        QScrollBar:vertical {{
            background: transparent;
            width: 10px;
            margin: 2px 1px 2px 1px;
        }}

        QScrollBar::handle:vertical {{
            background: {c["scroll"]};
            min-height: 42px;
            border-radius: 4px;
            margin: 1px 2px;
        }}

        QScrollBar::handle:vertical:hover {{
            background: {c["accent"]};
        }}

        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical {{
            height: 0px;
            width: 0px;
            background: transparent;
        }}

        QScrollBar::add-page:vertical,
        QScrollBar::sub-page:vertical {{
            background: transparent;
        }}

        QScrollBar:horizontal {{
            background: transparent;
            height: 10px;
            margin: 1px 2px;
        }}

        QScrollBar::handle:horizontal {{
            background: {c["scroll"]};
            min-width: 42px;
            border-radius: 4px;
            margin: 2px 1px;
        }}

        QScrollBar::add-line:horizontal,
        QScrollBar::sub-line:horizontal {{
            width: 0px;
            height: 0px;
            background: transparent;
        }}

        QScrollBar::add-page:horizontal,
        QScrollBar::sub-page:horizontal {{
            background: transparent;
        }}

        /* ---------- forms ---------- */

        QDialog {{
            background: {c["menu"]};
        }}

        QLabel#dialogTitle {{
            font-size: 22px;
            font-weight: 750;
        }}

        QLineEdit, QDateEdit, QTimeEdit, QTextEdit, QComboBox#modernCombo {{
            background: {c["input"]};
            border: 1px solid {c["border"]};
            border-radius: 10px;
            padding: 7px 10px;
            min-height: 22px;
            selection-background-color: {c["accent"]};
        }}

        QLineEdit:focus, QDateEdit:focus, QTimeEdit:focus,
        QTextEdit:focus, QComboBox#modernCombo:focus {{
            border-color: {c["accent"]};
        }}

        QLineEdit[invalid="true"] {{
            border: 1px solid {c["error"]};
        }}

        QComboBox#modernCombo::drop-down {{
            border: none;
            width: 34px;
            background: transparent;
        }}

        QComboBox#modernCombo::down-arrow {{
            image: none;
            width: 0px;
            height: 0px;
        }}

        QListView#comboPopup {{
            background: {c["menu"]};
            border: 1px solid {c["border"]};
            border-radius: 10px;
            padding: 4px;
            outline: 0;
        }}

        QListView#comboPopup::item {{
            border: none;
            border-radius: 7px;
            padding-left: 9px;
        }}

        QListView#comboPopup::item:selected {{
            background: {c["accent"]};
            color: {c["accent_text"]};
        }}

        QPushButton {{
            background: {c["glass_soft"]};
            border: 1px solid {c["border"]};
            border-radius: 9px;
            padding: 7px 12px;
        }}

        QPushButton:hover {{
            background: {c["glass_hover"]};
        }}

        QPushButton:checked {{
            background: {c["accent"]};
            color: {c["accent_text"]};
            border-color: {c["accent"]};
        }}

        QToolButton#avatarRemoveButton {{
            background: rgba(25,25,28,220);
            color: white;
            border: 1px solid rgba(255,255,255,110);
            border-radius: 12px;
            font-size: 18px;
            font-weight: 700;
            padding: 0;
        }}

        QToolButton#avatarRemoveButton:hover {{
            background: {c["error"]};
        }}

        /* ---------- calendar ---------- */

        QCalendarWidget {{
            background: {c["glass"]};
            border: 1px solid {c["border"]};
            border-radius: 14px;
        }}

        QCalendarWidget QWidget#qt_calendar_navigationbar {{
            background: transparent;
        }}

        QCalendarWidget QToolButton {{
            background: transparent;
            border: none;
            font-weight: 650;
            padding: 5px;
        }}

        QCalendarWidget QAbstractItemView {{
            background: transparent;
            selection-background-color: {c["accent"]};
            selection-color: {c["accent_text"]};
            outline: none;
        }}

        QTableWidget {{
            background: {c["calendar"]};
            alternate-background-color: {c["glass_soft"]};
            border: 1px solid {c["border"]};
            border-radius: 12px;
            gridline-color: {c["border"]};
        }}

        QHeaderView::section {{
            background: {c["glass_soft"]};
            border: none;
            border-right: 1px solid {c["border"]};
            border-bottom: 1px solid {c["border"]};
            padding: 7px;
            font-weight: 650;
        }}

        QScrollArea {{
            border: none;
            background: transparent;
        }}

        QScrollArea > QWidget > QWidget {{
            background: transparent;
        }}

        QFrame#hourRow {{
            background: {c["calendar"]};
            border-bottom: 1px solid {c["border"]};
        }}

        QLabel#hourLabel {{
            color: {c["muted"]};
            min-width: 54px;
            max-width: 54px;
        }}

        QLabel#eventChip {{
            background: {c["accent"]};
            color: {c["accent_text"]};
            border-radius: 7px;
            padding: 4px 7px;
            font-weight: 650;
        }}

        /* ---------- profile popup ---------- */

        QLabel#profileOrg,
        QLabel#profileName {{
            font-size: 15px;
            font-weight: 750;
        }}

        QLabel#profileDetail {{
            color: {c["muted"]};
            font-size: 12px;
        }}

        QPushButton#profileEditButton {{
            background: transparent;
            border: none;
            border-top: 1px solid {c["border"]};
            border-radius: 0;
            padding: 11px 4px;
            text-align: left;
            font-weight: 650;
        }}

        QPushButton#profileEditButton:hover {{
            background: {c["glass_hover"]};
        }}

        /* ---------- custom month calendar ---------- */

        QFrame#monthWeekHeader {{
            background: {c["calendar"]};
            border: 1px solid {c["border"]};
            border-radius: 14px;
        }}

        QLabel#monthWeekdayHeader {{
            padding: 8px 4px;
            font-weight: 700;
        }}

        QLabel#monthWeekdayHeader[weekend="true"] {{
            color: {c["weekend"]};
        }}

        QFrame#monthDayCell {{
            background: {c["calendar"]};
            border: 1px solid {c["border"]};
            border-radius: 12px;
        }}

        QFrame#monthDayCell:hover {{
            background: {c["calendar_alt"]};
            border-color: {c["accent"]};
        }}

        QFrame#monthDayCell[selected="true"] {{
            border: 2px solid {c["accent"]};
        }}

        QFrame#monthDayCell[otherMonth="true"] {{
            background: {c["glass"]};
        }}

        QLabel#monthDateNumber {{
            font-size: 13px;
            font-weight: 700;
            padding: 1px 4px;
            border-radius: 10px;
        }}

        QLabel#monthDateNumber[weekend="true"] {{
            color: {c["weekend"]};
        }}

        QLabel#monthDateNumber[otherMonth="true"] {{
            color: {c["muted"]};
        }}

        QLabel#monthDateNumber[today="true"] {{
            background: {c["accent"]};
            color: {c["accent_text"]};
        }}

        QLabel#monthEventChip {{
            background: {c["accent"]};
            color: {c["accent_text"]};
            border-radius: 6px;
            padding: 3px 5px;
            font-size: 11px;
            font-weight: 650;
        }}

        QLabel#monthMore {{
            color: {c["muted"]};
            font-size: 10px;
            padding-left: 3px;
        }}

        /* ---------- clients ---------- */

        QLabel#pageTitleSmall {{
            font-size: 22px;
            font-weight: 750;
        }}

        QLineEdit#clientSearch {{
            min-width: 220px;
        }}

        QPushButton#primaryButton {{
            background: {c["accent"]};
            color: {c["accent_text"]};
            border-color: {c["accent"]};
            font-weight: 700;
        }}

        QPushButton#primaryButton:hover {{
            background: {c["accent_hover"]};
        }}

        QPushButton#clientListItem {{
            background: {c["glass_soft"]};
            border: 1px solid {c["border"]};
            border-radius: 13px;
            padding: 11px 12px;
            text-align: left;
            font-weight: 650;
        }}

        QPushButton#clientListItem:hover {{
            background: {c["glass_hover"]};
        }}

        QPushButton#clientListItem:checked {{
            background: {c["calendar_alt"]};
            border: 2px solid {c["accent"]};
            color: {c["text"]};
        }}

        QFrame#clientHero {{
            background: {c["calendar"]};
            border: 1px solid {c["border"]};
            border-radius: 16px;
        }}

        QLabel#clientName {{
            font-size: 24px;
            font-weight: 760;
        }}

        QLabel#clientMeta {{
            color: {c["muted"]};
            font-size: 12px;
        }}

        QLabel#statusBadge {{
            background: {c["glass_soft"]};
            border: 1px solid {c["border"]};
            border-radius: 10px;
            padding: 5px 9px;
            font-weight: 700;
        }}

        QLabel#statusBadge[clientStatus="aktiv"] {{
            color: {c["success"]};
        }}

        QLabel#statusBadge[clientStatus="beendet"] {{
            color: {c["muted"]};
        }}

        QLabel#statusBadge[clientStatus="ruhend"] {{
            color: {c["warning"]};
        }}

        QFrame#infoBlock {{
            background: {c["calendar"]};
            border: 1px solid {c["border"]};
            border-radius: 14px;
        }}

        QLabel#infoBlockTitle {{
            font-size: 15px;
            font-weight: 750;
        }}

        QLabel#infoKey {{
            color: {c["muted"]};
            min-width: 110px;
        }}

        QLabel#infoValue {{
            font-weight: 600;
        }}

        QTabWidget#clientDetailTabs::pane,
        QTabWidget#clientTabs::pane {{
            background: {c["glass_soft"]};
            border: 1px solid {c["border"]};
            border-radius: 12px;
            top: -1px;
        }}

        QTabBar::tab {{
            background: {c["glass_soft"]};
            border: 1px solid {c["border"]};
            padding: 7px 13px;
            margin-right: 3px;
            border-top-left-radius: 9px;
            border-top-right-radius: 9px;
        }}

        QTabBar::tab:selected {{
            background: {c["calendar"]};
            border-bottom-color: {c["calendar"]};
            font-weight: 700;
        }}

        /* ---------- session ---------- */

        QFrame#loginCard {{
            background: {c["calendar"]};
            border: 1px solid {c["border"]};
            border-radius: 20px;
        }}

        QLabel#loginTitle {{
            font-size: 28px;
            font-weight: 760;
        }}

        QPushButton#logoutButton {{
            background: transparent;
            border: none;
            border-top: 1px solid {c["border"]};
            border-radius: 0;
            padding: 11px 4px;
            text-align: left;
            font-weight: 700;
            color: {c["error"]};
        }}

        QPushButton#logoutButton:hover {{
            background: {c["glass_hover"]};
        }}

        /* ---------- background picker ---------- */

        QToolButton#backgroundChoice {{
            background: {c["glass_soft"]};
            border: 2px solid transparent;
            border-radius: 12px;
            padding: 4px;
        }}

        QToolButton#backgroundChoice:hover {{
            background: {c["glass_hover"]};
        }}

        QToolButton#backgroundChoice:checked {{
            border-color: {c["accent"]};
        }}
        """
