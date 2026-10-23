import shutil
from pathlib import Path

from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QDialogButtonBox, QFormLayout,
    QGridLayout, QToolButton, QPushButton, QFileDialog, QButtonGroup, QWidget
)

from core.paths import BACKGROUND_DIR
from ui.controls import ModernComboBox


class SettingsDialog(QDialog):
    def __init__(self, settings, preset_paths, parent=None):
        super().__init__(parent)
        self.settings = settings
        self.preset_paths = preset_paths
        self.selected_background = settings.background_id
        self.selected_custom_path = settings.custom_background

        self.setWindowTitle("Einstellungen")
        self.setMinimumWidth(620)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 18)
        layout.setSpacing(13)

        title = QLabel("Einstellungen")
        title.setObjectName("dialogTitle")
        layout.addWidget(title)

        form = QFormLayout()
        form.setHorizontalSpacing(18)
        form.setVerticalSpacing(10)

        self.theme_combo = ModernComboBox()
        self.theme_combo.addItem("System", "system")
        self.theme_combo.addItem("Hell", "light")
        self.theme_combo.addItem("Dunkel", "dark")

        self.start_combo = ModernComboBox()
        self.start_combo.addItem("Home", "home")
        self.start_combo.addItem("Kalender", "calendar")

        self._set_combo_data(self.theme_combo, settings.theme)
        self._set_combo_data(self.start_combo, settings.start_page)

        form.addRow("Darstellung:", self.theme_combo)
        form.addRow("Startseite:", self.start_combo)
        layout.addLayout(form)

        background_title = QLabel("Hintergrund")
        background_title.setObjectName("sectionTitle")
        layout.addWidget(background_title)

        self.group = QButtonGroup(self)
        self.group.setExclusive(True)

        names = {
            "starry_night": "Van Gogh – Sternennacht",
            "preset_2": "Ozean",
            "preset_3": "Violett",
            "preset_4": "Nebel",
            "preset_5": "Abend",
        }

        grid = QGridLayout()
        grid.setSpacing(10)

        for i, (bg_id, path) in enumerate(self.preset_paths.items()):
            wrapper = QWidget()
            wlayout = QVBoxLayout(wrapper)
            wlayout.setContentsMargins(0, 0, 0, 0)
            wlayout.setSpacing(4)

            btn = QToolButton()
            btn.setObjectName("backgroundChoice")
            btn.setCheckable(True)
            btn.setIcon(QIcon(path))
            btn.setIconSize(QSize(146, 78))
            btn.setFixedSize(158, 90)
            btn.clicked.connect(
                lambda checked=False, value=bg_id: self._select_background(value)
            )
            self.group.addButton(btn)

            label = QLabel(names.get(bg_id, "Hintergrund"))
            label.setObjectName("smallMuted")
            label.setWordWrap(True)

            wlayout.addWidget(btn)
            wlayout.addWidget(label)

            grid.addWidget(wrapper, i // 3, i % 3)

            if self.selected_background == bg_id:
                btn.setChecked(True)

        layout.addLayout(grid)

        custom_btn = QPushButton("Eigenes Hintergrundbild auswählen …")
        custom_btn.clicked.connect(self.choose_custom_background)
        layout.addWidget(custom_btn)

        self.custom_label = QLabel()
        self.custom_label.setObjectName("smallMuted")
        self._refresh_custom_label()
        layout.addWidget(self.custom_label)

        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    @staticmethod
    def _set_combo_data(combo, value):
        for i in range(combo.count()):
            if combo.itemData(i) == value:
                combo.setCurrentIndex(i)
                return

    def _select_background(self, value):
        self.selected_background = value
        self.selected_custom_path = ""
        self._refresh_custom_label()

    def choose_custom_background(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Hintergrundbild auswählen",
            "",
            "Bilder (*.png *.jpg *.jpeg *.webp *.bmp)"
        )
        if not path:
            return

        self.selected_background = "custom"
        self.selected_custom_path = path

        for button in self.group.buttons():
            button.setChecked(False)

        self._refresh_custom_label()

    def _refresh_custom_label(self):
        if self.selected_background == "custom" and self.selected_custom_path:
            self.custom_label.setText(
                f"Eigenes Bild: {Path(self.selected_custom_path).name}"
            )
        else:
            self.custom_label.setText("")

    def save_to_settings(self):
        custom_stored = ""

        if self.selected_background == "custom" and self.selected_custom_path:
            source = Path(self.selected_custom_path)
            if source.exists():
                suffix = source.suffix.lower() if source.suffix else ".jpg"
                target = BACKGROUND_DIR / f"custom_background{suffix}"
                if source.resolve() != target.resolve():
                    shutil.copy2(source, target)
                custom_stored = str(target)

        self.settings.theme = self.theme_combo.currentData()
        self.settings.start_page = self.start_combo.currentData()
        self.settings.background_id = self.selected_background
        self.settings.custom_background = custom_stored
        self.settings.sync()
