from typing import Optional, List

from PySide2 import QtCore, QtWidgets

from services.documents.all import CChapter, Chapter, WorkType


class NavBar(QtWidgets.QWidget):

    def __init__(
        self,
        parent: Optional[QtWidgets.QWidget] = None
    ) -> None:
        super(NavBar, self).__init__(parent)

        self.mainLayout = QtWidgets.QHBoxLayout(self)

        self.setLayout(self.mainLayout)

        self.backButton = QtWidgets.QPushButton("Back", self)

        self.workTitleLabel = QtWidgets.QLabel(self)
        self.workTitleLabel.setFrameStyle(QtWidgets.QFrame.StyledPanel)
        self.workTitleLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.workAuthorLabel = QtWidgets.QLabel(self)
        self.workAuthorLabel.setFrameStyle(QtWidgets.QFrame.StyledPanel)
        self.workAuthorLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.chapterTitleComboBox = QtWidgets.QComboBox(self)

        self.pageComboBox = QtWidgets.QComboBox(self)

        self.totalPageCountLabel = QtWidgets.QLabel(self)
        self.totalPageCountLabel.setFrameStyle(QtWidgets.QFrame.StyledPanel)
        self.totalPageCountLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.mainLayout.addWidget(self.backButton, 1)
        self.mainLayout.addWidget(self.workTitleLabel, 3)
        self.mainLayout.addWidget(self.workAuthorLabel, 3)
        self.mainLayout.addWidget(self.chapterTitleComboBox, 3)
        self.mainLayout.addWidget(self.pageComboBox, 1)
        self.mainLayout.addWidget(self.totalPageCountLabel, 1)

    def setLabels(
        self,
        workTitle: str,
        workAuthor: str,
        catalogChapters: List[CChapter],
        currentChapter: Chapter,
        isSameWork: bool,
        workType: WorkType
    ) -> None:
        if not isSameWork:
            self.workTitleLabel.setText(workTitle)
            self.workAuthorLabel.setText(workAuthor)
            self.chapterTitleComboBox.clear()
            self.chapterTitleComboBox.addItems([
                catalogChapter.chapter_title
                for catalogChapter in catalogChapters
            ])
        self.chapterTitleComboBox.setCurrentText(currentChapter.chapter_title)
        self.pageComboBox.clear()
        if workType is WorkType.COMIC:
            self.pageComboBox.addItems([
                str(i + 1)
                for i in range(len(currentChapter.pages))
            ])
            self.totalPageCountLabel.setText(str(len(currentChapter.pages)))
        elif workType is WorkType.TEXT:
            self.pageComboBox.addItems(["1"])
            self.totalPageCountLabel.setText("1")

    def setPageNumber(
        self,
        pageNumber: int
    ) -> None:
        self.pageComboBox.setCurrentIndex(pageNumber - 1)
