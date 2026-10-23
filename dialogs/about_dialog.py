from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox

from app_info import APP_NAME, APP_VERSION, APP_AUTHOR


class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Über {APP_NAME}")
        self.setMinimumWidth(390)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 22, 22, 18)
        layout.setSpacing(10)

        title = QLabel(APP_NAME)
        title.setObjectName("dialogTitle")
        meta = QLabel(f"Version: {APP_VERSION}\nAutor: {APP_AUTHOR}")
        meta.setObjectName("mutedText")

        layout.addWidget(title)
        layout.addWidget(meta)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok)
        buttons.accepted.connect(self.accept)
        layout.addWidget(buttons)
