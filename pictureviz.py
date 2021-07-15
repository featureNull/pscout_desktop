'''Widget, which contains the input image.
'''
from enum import Enum
from PyQt5 import QtGui, uic
from PyQt5.QtCore import Qt, pyqtSignal, QPoint, pyqtSlot, QRect
from PyQt5.QtGui import QPainter, QPixmap, QBrush, QColor, QTransform, QPolygonF
from PyQt5.QtWidgets import QWidget, QToolButton, QDialog, QPushButton
import qtawesome as qta
from searchview.pictureoverlays import MesOverlay, RoiOverlay, ContOverlay
import session


class EditMode(Enum):
    IDLE = 0
    MEASURE = 1
    ROI = 2
    FG = 3


class PictureEditor(QWidget):
    modeChanged = pyqtSignal(EditMode)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bkimage = QPixmap('./ui/png/tile.png')
        self.photo = None
        self.currentZoom = 1.0
        self.offset = QPoint(0, 0)
        self.mode = EditMode.IDLE
        # overlays
        self.mesOverlay = MesOverlay(self)
        self.mesOverlay.doneCallBack = self._onMeasureDone
        self.roiOverlay = RoiOverlay(self)
        self.contOverlay = ContOverlay(self)
        self.contOverlay.freehandDone = self._onFreeHandDone
        self.overlays = [self.mesOverlay, self.roiOverlay, self.contOverlay]
        # eingebettete button
        self.btnContPlus = QToolButton(self)
        self.btnContPlus.setIcon(qta.icon('fa5s.plus', color='white'))
        self.btnContPlus.setStyleSheet("background-color: #19232D")
        self.btnContPlus.clicked.connect(self._onAddCountClicked)
        self.btnContPlus.hide()
        self.btnContMinus = QToolButton(self)
        self.btnContMinus.setIcon(qta.icon('fa5s.minus', color='white'))
        self.btnContMinus.setStyleSheet("background-color: #19232D")
        self.btnContMinus.clicked.connect(self._onRemoveCountClicked)
        self.btnContMinus.hide()
        self.btnFindCont = QPushButton('Find Contours', self)
        self.btnFindCont.clicked.connect(self._onFindContClicked)
        self.btnFindCont.hide()

        mngr = QtGui.qApp.sessionManager
        mngr.contourChanged.connect(self.updateContour)
        self.setMouseTracking(True)
        self.show()

    def setPhoto(self, photo, roi=None):
        self.mesOverlay.reset()
        self.photo = photo
        if roi is not None:
            if roi.isValid():
                self.roiOverlay.imageRoi = roi
            else:
                w = photo.width()
                h = photo.height()
                self.roiOverlay.imageRoi = QRect(w/4, h/4, w/2, h/2)
            self.setMode(EditMode.ROI)
        else:
            self.update()

    def setMode(self, mode):
        if mode == self.mode:
            return
        newoverlay = self.getOverlay(mode)
        oldoverlay = self.getOverlay(self.mode)
        if oldoverlay is not None:
            oldoverlay.leave()
        if newoverlay is not None:
            newoverlay.enter()
        self.btnContPlus.hide()
        self.btnContMinus.hide()
        self.btnFindCont.setVisible(mode == EditMode.ROI)
        self.mode = mode
        self.modeChanged.emit(mode)
        self.update()

    @pyqtSlot(QPolygonF)
    def updateContour(self, cont):
        self.contOverlay.contour = cont
        self.update()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        crc = self.rect()
        painter.fillRect(crc, QBrush(self.bkimage))
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.HighQualityAntialiasing)
        if self.photo is not None:
            srcrect = self.photo.rect()
            destrect = self.transform().mapRect(srcrect)
            painter.drawPixmap(destrect, self.photo, srcrect)
            painter.fillRect(crc, QBrush(QColor(0, 0, 0, 40)))
        if self.mode == EditMode.IDLE:
            # alle duerfen zeichen
            for overlay in self.overlays:
                overlay.render(painter)
        else:
            self.getOverlay(self.mode).render(painter)
        painter.end()

    def event(self, event):
        proc = False
        overlay = self.getOverlay(self.mode)
        if overlay is not None:
            if overlay.routeEvent(event):
                proc = True
        if self.mode == EditMode.ROI:
            # update pos von fund contour button
            imroi = self.roiOverlay.imageRoi.normalized()
            br = self.transform().map(imroi.bottomRight())
            self.btnFindCont.move(br.x() - self.btnFindCont.width(), br.y() + 8)
        if proc is True:
            return True
        else:
            return super().event(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self._mousePressedPos = event.pos() - self.offset

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MiddleButton:
            self.offset = event.pos() - self._mousePressedPos
            self.update()

    def wheelEvent(self, event):
        if (event.angleDelta().y() > 0) and self.currentZoom < 3.0:
            fct = 1.10
        elif self.currentZoom > 1.0:
            fct = 1 / 1.10
        else:
            fct = 1.0
        self.currentZoom = self.currentZoom * fct
        self.update()

    def transform(self) -> QTransform:
        if self.photo is not None:
            srcrc = self.photo.rect()
            destrc = self.rect()
            trfshift = _translate(srcrc, destrc, self.offset)
            trfscale = _scale(srcrc, destrc, self.currentZoom)
            return trfscale * trfshift
        else:
            return QTransform()

    def _onMeasureDone(self):
        overlay = self.mesOverlay
        mngr = QtGui.qApp.sessionManager
        dlg = uic.loadUi('./ui/mesauredistdialog.ui')
        dlg.lineEdit.setValidator(QtGui.QIntValidator(0, 10000))
        res = dlg.exec_()
        if res == QDialog.Accepted and len(dlg.lineEdit.text()) > 0:
            overlay.lengthText = dlg.lineEdit.text() + 'mm'
            mngr.ppmm = overlay.lineLength() / float(dlg.lineEdit.text())
            if dlg.btnAcc.isChecked():
                mngr.sizeFlags = session.SizeFlags.ACCURATELY
            elif dlg.btnLessAcc.isChecked():
                mngr.sizeFlags = session.SizeFlags.LESS_ACCURATE
            elif dlg.btnInAcc.isChecked():
                mngr.sizeFlags = session.SizeFlags.INACCURATE
            else:
                mngr.sizeFlags = session.SizeFlags.UNKNOWN
        else:
            mngr.ppmm = None
            mngr.sizeFlags = session.SizeFlags.UNKNOWN
            overlay.reset()

        self.setMode(EditMode.IDLE)

    def _onFreeHandDone(self, mousePos):
        offs = 10
        h = self.btnContPlus.height()
        self.btnContMinus.move(mousePos.x() + offs, mousePos.y() + offs - h)
        self.btnContPlus.move(mousePos.x() + offs, mousePos.y() + offs)
        self.btnContPlus.show()
        self.btnContMinus.show()

    def _onAddCountClicked(self):
        sm = QtGui.qApp.sessionManager
        sm.addForeground(self.contOverlay.freeHandPath)
        self.contOverlay.freeHandPath.clear()
        self.btnContPlus.hide()
        self.btnContMinus.hide()
        self.update()

    def _onRemoveCountClicked(self):
        sm = QtGui.qApp.sessionManager
        sm.removeForeground(self.contOverlay.freeHandPath)
        self.contOverlay.freeHandPath.clear()
        self.btnContPlus.hide()
        self.btnContMinus.hide()
        self.update()

    def _onFindContClicked(self):
        self.setMode(EditMode.FG)
        sm = QtGui.qApp.sessionManager
        sm.findForeground(self.roiOverlay.imageRoi)

    def getOverlay(self, mode):
        o = {
            EditMode.IDLE: None,
            EditMode.MEASURE: self.mesOverlay,
            EditMode.ROI: self.roiOverlay,
            EditMode.FG: self.contOverlay
        }
        return o[mode]


class PictureView(QWidget):
    '''Passives Fenster in Results Fenster
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bkimage = QPixmap('./ui/png/tile.png')
        self.photo = None

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        crc = self.rect()
        painter.fillRect(crc, QBrush(self.bkimage))
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.HighQualityAntialiasing)
        if self.photo is not None:
            srcrect = self.photo.rect()
            destrect = self.transform().mapRect(srcrect)
            painter.drawPixmap(destrect, self.photo, srcrect)
        painter.end()

    def transform(self) -> QTransform:
        if self.photo is not None:
            srcrc = self.photo.rect()
            destrc = self.rect()
            trfshift = _translate(srcrc, destrc, QPoint(0, 0))
            trfscale = _scale(srcrc, destrc, 1.0)
            return trfscale * trfshift
        else:
            return QTransform()


def _scale(rectsrc, rectdest, zoom) -> QTransform:
    heightfct = rectdest.height() / rectsrc.height()
    widthfct = rectdest.width() / rectsrc.width()
    scale = min(heightfct, widthfct) * zoom
    return QTransform.fromScale(scale, scale)


def _translate(rectsrc, rectdest, offset: QPoint) -> QTransform:
    srcfct = rectsrc.width() / rectsrc.height()
    destfct = rectdest.width() / rectdest.height()
    shiftx = rectdest.width() * max((1 - srcfct / destfct) / 2, 0)
    shifty = rectdest.height() * max((1 - destfct / srcfct) / 2, 0)
    return QTransform.fromTranslate(offset.x() + shiftx, offset.y() + shifty)
