from PyQt5 import QtCore, QtGui

from clients.pyqt5client.ConfigureServices import sp
from clients.pyqt5client.widgets.MainWindow import MainWindow
from services.documents.all import CWork
from services.storage.all import AbstractStorage


class BaseHandler(QtCore.QObject):

    @sp.inject("storage")
    def __init__(
        self,
        mainWindow: MainWindow,
        storage: AbstractStorage
    ) -> None:
        super(BaseHandler, self).__init__()

        self.storage = storage

        self.mainWindow = mainWindow

        self.catalogBrowser = self.mainWindow.catalogBrowser
        self.chapterViewer = self.mainWindow.chapterViewer

        self.treeView = self.catalogBrowser.treeView

        self.navBar = self.chapterViewer.navBar
        self.imageViewer = self.chapterViewer.imageViewer
        self.htmlViewer = self.chapterViewer.htmlViewer

    def showCatalog(
        self
    ) -> None:
        self.imageViewer.setImage(QtGui.QPixmap())
        self.htmlViewer.setHtml("")
        self.catalogBrowser.setVisible(True)
        self.chapterViewer.setVisible(False)

    def showChapter(
        self,
        catalogWork: CWork,
        chapterTitle: str,
        isSameWork: bool
    ) -> None:
        chapter = self.storage.get_chapter(
            catalogWork.title,
            catalogWork.author,
            chapterTitle
        )
        if chapter:
            self.chapterViewer.setChapter(catalogWork, chapter, isSameWork)
            if not isSameWork:
                self.catalogBrowser.setVisible(False)
                self.chapterViewer.setVisible(True)
