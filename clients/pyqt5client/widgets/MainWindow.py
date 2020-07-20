from typing import Optional

from PyQt5 import QtCore, QtWidgets

from clients.pyqt5client.widgets.CatalogBrowser import CatalogBrowser
from clients.pyqt5client.ChapterViewer import ChapterViewer


class MainWindow(QtWidgets.QMainWindow):

    def __init__(
        self,
        parent: Optional[QtWidgets.QWidget] = None
    ) -> None:
        super(MainWindow, self).__init__(parent)

        self.setWindowTitle("Client")

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.centralWidget = QtWidgets.QWidget(self)
        self.mainLayout = QtWidgets.QGridLayout(self.centralWidget)
        self.centralWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.centralWidget)

        self.catalogBrowser = CatalogBrowser(self.centralWidget)
        self.mainLayout.addWidget(self.catalogBrowser, 0, 0)

        self.chapterViewer = ChapterViewer(self.centralWidget)
        self.mainLayout.addWidget(self.chapterViewer, 1, 0)
        self.chapterViewer.setVisible(False)
