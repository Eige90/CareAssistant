from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame


class PlaceholderModule(QWidget):
    def __init__(self, name, parent=None):
        super().__init__(parent)
        self.setObjectName("transparentPage")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 18)

        panel = QFrame()
        panel.setObjectName("glassPanel")
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(20, 18, 20, 20)

        title = QLabel(name)
        title.setObjectName("pageTitle")

        panel_layout.addWidget(title)
        panel_layout.addStretch(1)
        layout.addWidget(panel)
