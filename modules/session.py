from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFrame

from app_info import APP_NAME


class SignedOutPage(QWidget):
    login_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("transparentPage")

        outer = QVBoxLayout(self)
        outer.setContentsMargins(24, 24, 24, 24)
        outer.setAlignment(Qt.AlignCenter)

        card = QFrame()
        card.setObjectName("loginCard")
        card.setMaximumWidth(420)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(28, 26, 28, 26)
        layout.setSpacing(14)

        title = QLabel(APP_NAME)
        title.setObjectName("loginTitle")
        title.setAlignment(Qt.AlignCenter)

        state = QLabel("Abgemeldet")
        state.setObjectName("mutedText")
        state.setAlignment(Qt.AlignCenter)

        login = QPushButton("Anmelden")
        login.setObjectName("primaryButton")
        login.clicked.connect(self.login_requested.emit)

        layout.addWidget(title)
        layout.addWidget(state)
        layout.addSpacing(6)
        layout.addWidget(login)

        outer.addWidget(card)
