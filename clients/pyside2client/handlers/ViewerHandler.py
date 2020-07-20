import math

from PySide2 import QtCore, QtWidgets, QtGui

from clients.pyside2client.ConfigureServices import sp
from clients.pyside2client.handlers.all import BaseHandler
from clients.pyside2client.widgets.MainWindow import MainWindow
from services.documents.all import Chapter, WorkType
from services.htmlparsers.all import ParserBase64


class ViewerHandler(BaseHandler):

    @sp.inject("html_parser")
    def __init__(
        self,
        mainWindow: MainWindow,
        html_parser: ParserBase64
    ) -> None:
        super(ViewerHandler, self).__init__(mainWindow)

        self.htmlParser = html_parser

        self.chapterViewer.pageChangeSignal.connect(
            self.onPageChange
        )
        self.imageViewer.keyReleaseSignal.connect(
            self.imageViewerOnKeyReleaseSignal
        )
        self.imageViewer.resizeSignal.connect(
            self.imageViewerOnResizeSignal
        )
        self.imageViewer.showSignal.connect(
            self.imageViewerOnShowSignal
        )
        self.imageViewer.wheelSignal.connect(
            self.imageViewerOnWheelSignal
        )
        self.navBar.backButton.clicked.connect(
            self.backButtonOnClick
        )
        self.navBar.chapterTitleComboBox.currentIndexChanged.connect(
            self.chapterTitleComboBoxOnCurrentIndexChanged
        )

    @QtCore.Slot(int)
    def onPageChange(
        self,
        pageNumber: int
    ) -> None:
        chapter = self.chapterViewer.chapter
        workType = self.chapterViewer.workType
        if pageNumber > len(chapter.pages) or pageNumber <= 0:
            return
        self.chapterViewer.pageNumber = pageNumber
        self.navBar.setPageNumber(pageNumber)
        if workType is WorkType.COMIC:
            pm = QtGui.QPixmap()
            pm.loadFromData(
                chapter.pages[pageNumber - 1].raw_data
            )
            self.imageViewer.setFocus()
            self.imageViewer.setImage(pm)
        elif workType is WorkType.TEXT:
            self.loadParser(self.chapterViewer.chapter)
            self.htmlParser.feed(
                chapter.pages[0].raw_data.decode("utf-8")
            )
            self.htmlViewer.setHtml(self.htmlParser.get_buffer())

    @QtCore.Slot(int)
    def imageViewerOnKeyReleaseSignal(
        self,
        key: int
    ) -> None:
        if key == QtCore.Qt.Key_Left or key == QtCore.Qt.Key_Up:
            self.chapterViewer.pageChangeSignal.emit(
                self.chapterViewer.pageNumber - 1
            )
        elif key == QtCore.Qt.Key_Right or key == QtCore.Qt.Key_Down:
            self.chapterViewer.pageChangeSignal.emit(
                self.chapterViewer.pageNumber + 1
            )

    @QtCore.Slot()
    def imageViewerOnResizeSignal(
        self
    ) -> None:
        self.imageViewer.fitToScreen()

    @QtCore.Slot()
    def imageViewerOnShowSignal(
        self
    ) -> None:
        self.imageViewer.fitToScreen()

    @QtCore.Slot(int)
    def imageViewerOnWheelSignal(
        self,
        rotation: int
    ) -> None:
        if rotation > 0:
            factor = 1.25
            self.imageViewer.zoom += 1
        elif rotation < 0:
            factor = 0.8
            self.imageViewer.zoom -= 1

        if self.imageViewer.zoom > 0:
            self.imageViewer.scale(factor, factor)
        elif self.imageViewer.zoom == 0:
            self.imageViewer.fitToScreen()
        else:
            self.imageViewer.zoom = 0

    @QtCore.Slot()
    def backButtonOnClick(
        self
    ) -> None:
        self.showCatalog()

    @QtCore.Slot(int)
    def chapterTitleComboBoxOnCurrentIndexChanged(
        self,
        index: int
    ) -> None:
        if index >= 0 and not self.chapterViewer.isRendering:
            chapterTitle = self.navBar.chapterTitleComboBox.currentText()
            cWork = self.chapterViewer.catalogWork
            self.showChapter(cWork, chapterTitle, True)

    def loadParser(
        self,
        chapter: Chapter
    ) -> None:
        digits = int(math.log10(len(chapter.pages))) + 1
        for index, page in enumerate(chapter.pages[1:], start=2):
            self.htmlParser.add_file_mapping(
                f"{str(index).zfill(digits)}.{page.extension}",
                page.raw_data
            )
