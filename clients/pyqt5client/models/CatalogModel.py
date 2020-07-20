from typing import Optional

from PyQt5 import QtWidgets, QtGui

from services.documents.all import Catalog


class CatalogModel(QtGui.QStandardItemModel):
    def __init__(
        self,
        catalog: Catalog,
        parent: Optional[QtWidgets.QWidget] = None
    ) -> None:
        super(CatalogModel, self).__init__(parent)

        for catalogWork in catalog.works:
            workTitleItem = QtGui.QStandardItem(catalogWork.title)
            workAuthorItem = QtGui.QStandardItem(catalogWork.author)
            totalPageCount = 0
            self.appendRow([workTitleItem, workAuthorItem])
            for catalogChapter in catalogWork.chapters:
                chapterTitleItem = QtGui.QStandardItem(catalogChapter.chapter_title)
                pageCountItem = QtGui.QStandardItem(str(catalogChapter.number_of_pages))
                workTitleItem.appendRow([chapterTitleItem, QtGui.QStandardItem(None), pageCountItem])
                totalPageCount += catalogChapter.number_of_pages
            self.setItem(workTitleItem.row(), 2, QtGui.QStandardItem(str(totalPageCount)))
