from typing import Optional

from PySide2 import QtCore, QtWidgets, QtGui

from clients.pyside2client.widgets.ImageViewer import ImageViewer
from clients.pyside2client.widgets.HTMLViewer import HTMLViewer
from clients.pyside2client.widgets.NavBar import NavBar
from services.documents.all import CWork, Chapter, WorkType


class ChapterViewer(QtWidgets.QWidget):

    pageChangeSignal = QtCore.Signal(int)

    def __init__(
        self,
        parent: Optional[QtWidgets.QWidget] = None
    ) -> None:
        super(ChapterViewer, self).__init__(parent)

        self.isRendering = False
        self.catalogWork = None
        self.chapter = None
        self.pageNumber = None
        self.workType = None

        self.navBar = NavBar(self)
        self.navBar.pageComboBox.currentIndexChanged.connect(
            self.pageComboBoxOnCurrentIndexChanged
        )

        self.mainLayout = QtWidgets.QGridLayout(self)

        self.setLayout(self.mainLayout)

        self.imageViewer = ImageViewer(self)
        self.imageViewer.setVisible(False)

        self.htmlViewer = HTMLViewer(self)
        self.htmlViewer.setVisible(False)

        self.mainLayout.addWidget(self.navBar, 0, 0)
        self.mainLayout.addWidget(self.imageViewer, 1, 0)
        self.mainLayout.addWidget(self.htmlViewer, 1, 0)

    def setChapter(
        self,
        catalogWork: CWork,
        chapter: Chapter,
        isSameWork: bool
    ) -> None:
        self.isRendering = True
        self.catalogWork = catalogWork
        self.chapter = chapter
        self.workType = self.getWorkType()
        if self.workType is WorkType.COMIC:
            self.htmlViewer.setVisible(False)
            self.imageViewer.setVisible(True)
        elif self.workType is WorkType.TEXT:
            self.imageViewer.setVisible(False)
            self.htmlViewer.setVisible(True)
        self.navBar.setLabels(
            catalogWork.title,
            catalogWork.author,
            catalogWork.chapters,
            chapter,
            isSameWork,
            self.workType
        )
        self.isRendering = False

    def pageComboBoxOnCurrentIndexChanged(
        self,
        index: int
    ) -> None:
        if index >= 0:
            self.pageChangeSignal.emit(index + 1)

    def getWorkType(
        self
    ) -> Optional[WorkType]:
        if not self.chapter or not self.chapter.pages:
            return None
        elif self.chapter.pages[0].extension == "html":
            return WorkType.TEXT
        else:
            return WorkType.COMIC
