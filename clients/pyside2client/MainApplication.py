from typing import List

from PySide2 import QtWidgets

from clients.pyside2client.handlers.all import (
    NavHandler, ViewerHandler
)
from clients.pyside2client.widgets.MainWindow import MainWindow


class MainApplication(QtWidgets.QApplication):

    def __init__(
        self,
        args: List[str]
    ) -> None:
        super(MainApplication, self).__init__(args)

        self.setupStyling()

        self.window = MainWindow()

        self.setupHandlers()

        self.window.resize(600, 600)
        self.window.show()

    def setupStyling(
        self
    ) -> None:
        self.setStyle("Fusion")
        self.setPalette(QtWidgets.QApplication.style().standardPalette())

    def setupHandlers(
        self
    ) -> None:
        self.navHandler = NavHandler(self.window)
        self.viewerHandler = ViewerHandler(self.window)
