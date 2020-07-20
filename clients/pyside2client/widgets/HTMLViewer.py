from typing import Optional

from PySide2 import QtWidgets, QtWebEngineWidgets


class HTMLViewer(QtWebEngineWidgets.QWebEngineView):

    def __init__(
        self,
        parent: Optional[QtWidgets.QWidget] = None
    ) -> None:
        super(HTMLViewer, self).__init__(parent)

        policy = QtWidgets.QSizePolicy.Expanding
        self.setSizePolicy(policy, policy)
