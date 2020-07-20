from PyQt5 import QtCore, QtWidgets, QtGui

from clients.pyqt5client.handlers.all import BaseHandler
from clients.pyqt5client.widgets.MainWindow import MainWindow
from services.documents.all import CWork


class NavHandler(BaseHandler):

    def __init__(
        self,
        mainWindow: MainWindow
    ) -> None:
        super(NavHandler, self).__init__(mainWindow)

        self.catalogBrowser.treeView.doubleClicked.connect(
            self.treeViewOnClick
        )

        catalog = self.storage.get_catalog()
        self.catalogBrowser.setCatalog(catalog)

    @QtCore.pyqtSlot()
    def treeViewOnClick(
        self
    ) -> None:
        model = self.catalogBrowser.model
        row = [
            model.itemFromIndex(index).text()
            for index in self.treeView.selectedIndexes()
        ]
        if not row[1]:
            parentIndex = self.treeView.selectedIndexes()[0].parent()
            parentItem = model.itemFromIndex(parentIndex)
            workTitle = model.item(parentItem.row(), 0).text()
            workAuthor = model.item(parentItem.row(), 1).text()
            chapterTitle = row[0]

            cWork = self.catalogBrowser.catalog.get_work(workTitle, workAuthor)
            self.showChapter(cWork, chapterTitle, False)
