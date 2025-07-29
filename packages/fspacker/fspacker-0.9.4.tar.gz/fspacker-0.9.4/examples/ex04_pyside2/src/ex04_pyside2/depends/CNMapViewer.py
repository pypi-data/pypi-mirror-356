from depends.ui_CNMapViewer import Ui_MainWindow
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QMainWindow
from PySide2.QtWidgets import QMessageBox


class CNMapViewer(QMainWindow, Ui_MainWindow):
    """主窗口."""

    def __init__(self) -> None:
        super().__init__()

        self.setupUi(self)
        self.setWindowTitle("CNMap Ver1.0")
        self.resize(800, 600)
        self.setFont(QFont("Microsoft YaHei", 10, QFont.Bold))

        self.actionaboutQt.triggered.connect(self.on_about)

    def on_about(self) -> None:
        QMessageBox.aboutQt(self, title="example for qt")
