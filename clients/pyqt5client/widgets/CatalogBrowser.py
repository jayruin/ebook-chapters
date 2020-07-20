from typing import Optional

from PyQt5 import QtWidgets

from clients.pyqt5client.models.CatalogModel import CatalogModel
from services.documents.all import Catalog


class CatalogBrowser(QtWidgets.QWidget):

    def __init__(
        self,
        parent: Optional[QtWidgets.QWidget] = None
    ) -> None:
        super(CatalogBrowser, self).__init__(parent)

        self.catalog = None
        self.model = None

        self.layout = QtWidgets.QHBoxLayout(self)

        self.setLayout(self.layout)

        self.treeView = QtWidgets.QTreeView(self)
        self.treeView.header().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeToContents
        )
        self.treeView.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers
        )

        self.layout.addWidget(self.treeView, 1)

    def setCatalog(
        self,
        catalog: Catalog
    ) -> None:
        self.catalog = catalog
        self.model = CatalogModel(catalog, self)
        self.model.setHorizontalHeaderLabels(["Title", "Author", "Page Count"])
        self.treeView.setModel(self.model)
