from typing import Optional

from PySide2 import QtCore, QtWidgets, QtGui


class ImageViewer(QtWidgets.QGraphicsView):

    keyReleaseSignal = QtCore.Signal(int)
    resizeSignal = QtCore.Signal()
    showSignal = QtCore.Signal()
    wheelSignal = QtCore.Signal(int)

    def __init__(
        self,
        parent: Optional[QtWidgets.QWidget] = None
    ) -> None:
        super(ImageViewer, self).__init__(parent)

        self.zoom = 0
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setBackgroundBrush(QtGui.QBrush(QtCore.Qt.black))
        self.setFrameShape(QtWidgets.QFrame.NoFrame)

    def fitToScreen(
        self
    ) -> None:
        self.fitInView(self.scene().sceneRect(), QtCore.Qt.KeepAspectRatio)

    def setImage(
        self,
        pixmap: QtGui.QPixmap
    ) -> None:
        if not pixmap.isNull():
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
        else:
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)

        scene = QtWidgets.QGraphicsScene(parent=self)
        mode = QtCore.Qt.TransformationMode.SmoothTransformation
        scene.addPixmap(pixmap).setTransformationMode(mode)
        self.setScene(scene)
        self.zoom = 0
        self.fitToScreen()

    def keyReleaseEvent(
        self,
        event: QtGui.QKeyEvent
    ) -> None:
        super(ImageViewer, self).keyReleaseEvent(event)
        self.keyReleaseSignal.emit(event.key())

    def resizeEvent(
        self,
        event: QtGui.QResizeEvent
    ) -> None:
        super(ImageViewer, self).resizeEvent(event)
        self.resizeSignal.emit()

    def showEvent(
        self,
        event: QtGui.QShowEvent
    ) -> None:
        super(ImageViewer, self).showEvent(event)
        self.showSignal.emit()

    def wheelEvent(
        self,
        event: QtGui.QWheelEvent
    ) -> None:
        super(ImageViewer, self).wheelEvent(event)
        self.wheelSignal.emit(event.angleDelta().y())
