'''Widget, which contains the input image.
'''
from enum import Enum

from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSignal, QPoint, QRect
from PyQt5.QtGui import QPainter, QPixmap, QBrush, QColor, QTransform, QPolygonF
from PyQt5.QtWidgets import QWidget, QToolButton, QDialog
import qtawesome as qta
from photo_widget_overlay import MeasureOverlay, RoiOverlay, ContourOverlay
import matching


class Mode(Enum):
    IDLE = 0
    MEASURE = 1
    SELECT_ROI = 2
    SELECT_FG = 3


DIM_COLOR = QColor(0, 0, 0, 40)


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


class PhotoWidget(QWidget):
    modeChanged = pyqtSignal(Mode)
    contourChanged = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(QWidget, self).__init__(*args, **kwargs)
        self.bkimage = QPixmap('./ui/png/tile.png')
        self.photo = None
        self.currentZoom = 1.0
        self.offset = QPoint(0, 0)
        self.mode = Mode.IDLE

        measureOverlay = MeasureOverlay(self)
        measureOverlay.doneCallBack = self.onMeasureDone
        roiOverlay = RoiOverlay(self)
        contourOverlay = ContourOverlay(self)
        contourOverlay.freehandDone = self.onFreeHandDone
        self.overlays = {
            Mode.IDLE: None,
            Mode.MEASURE: measureOverlay,
            Mode.SELECT_ROI: roiOverlay,
            Mode.SELECT_FG: contourOverlay,
        }
        # eingebettete button
        self.btnContPlus = QToolButton(self)
        self.btnContPlus.setIcon(qta.icon('fa5s.plus', color='white'))
        self.btnContPlus.setStyleSheet("background-color: #19232D")
        self.btnContPlus.clicked.connect(self.addCountour)
        self.btnContPlus.hide()

        self.btnContMinus = QToolButton(self)
        self.btnContMinus.setIcon(qta.icon('fa5s.minus', color='white'))
        self.btnContMinus.setStyleSheet("background-color: #19232D")
        self.btnContMinus.clicked.connect(self.removeCountour)
        self.btnContMinus.hide()

        # los gehts
        self.setMouseTracking(True)
        self.show()

    def machmalSession(self, pixmap):
        roi = matching.open_session(pixmap)
        overlay = self.overlays[Mode.SELECT_ROI]
        overlay.imageRoi = QRect(roi.x, roi.y, roi.w, roi.h)
        overlay = self.overlays[Mode.MEASURE]
        overlay.reset()
        overlay = self.overlays[Mode.SELECT_FG]
        overlay.contour = QPolygonF()

    def enterMode(self, mode):
        if mode == self.mode:
            return

        if mode == Mode.SELECT_FG:
            fgoverlay = self.overlays[Mode.SELECT_FG]
            if fgoverlay.contour.isEmpty():
                roioverlay = self.overlays[Mode.SELECT_ROI]
                fgoverlay.contour = matching.find_foreground(roioverlay.imageRoi)

        newoverlay = self.overlays[mode]
        oldoverlay = self.overlays[self.mode]
        if oldoverlay is not None:
            oldoverlay.leave()
        if newoverlay is not None:
            newoverlay.enter()

        self.btnContPlus.hide()
        self.btnContMinus.hide()

        self.mode = mode
        self.modeChanged.emit(mode)

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
            painter.fillRect(crc, QBrush(DIM_COLOR))
        if self.mode == Mode.IDLE:
            # alle duerfen zeichen
            for key in self.overlays.keys():
                overlay = self.overlays[key]
                if overlay is not None:
                    overlay.render(painter)
        else:
            self.overlays[self.mode].render(painter)
        painter.end()

    def event(self, event):
        overlay = self.overlays[self.mode]
        if overlay is not None:
            if overlay.routeEvent(event):
                return True
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

    def onMeasureDone(self):
        overlay = self.overlays[Mode.MEASURE]
        dlg = uic.loadUi('./ui/mesauredistdialog.ui')
        if dlg.exec_() == QDialog.Accepted:
            overlay.lengthText = dlg.lineEdit.text() + 'mm'
        else:
            overlay.reset()
        self.enterMode(Mode.IDLE)

    def onFreeHandDone(self, mousePos):
        offs = 10
        h = self.btnContPlus.height()
        self.btnContMinus.move(mousePos.x() + offs, mousePos.y() + offs - h)
        self.btnContPlus.move(mousePos.x() + offs, mousePos.y() + offs)
        self.btnContPlus.show()
        self.btnContMinus.show()

    def addCountour(self):
        overlay = self.overlays[Mode.SELECT_FG]
        self.btnContPlus.hide()
        self.btnContMinus.hide()
        overlay.contour = matching.add_foreground(overlay.freeHandPath)
        overlay.freeHandPath.clear()
        self.update()
        self.contourChanged.emit()
        kjkjh = matching.estimate_candidates()

    def removeCountour(self):
        overlay = self.overlays[Mode.SELECT_FG]
        self.btnContPlus.hide()
        self.btnContMinus.hide()
        overlay.contour = matching.remove_foreground(overlay.freeHandPath)
        overlay.freeHandPath.clear()
        self.update()
        self.contourChanged.emit()
        kjkjh = matching.estimate_candidates()
