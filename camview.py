'''view mit kaera und live video'''
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QThread, pyqtSignal
import qtawesome as qta
import camera
from camera.idscam import IdsCam
import cv2

DEBUG = True


class CamView(QWidget):
    closeRequested = pyqtSignal()
    snapshot = pyqtSignal(QPixmap)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('./ui/camview.ui', self)
        self.sldrZoom.setDisabled(True)
        self.btnClose.clicked.connect(self.closeRequested)
        self.btnClose.setIcon(qta.icon('fa5s.times', color='gray'))
        self.btnSnapshot.setIcon(qta.icon('fa5s.image', color='gray'))
        self.btnSnapshot.clicked.connect(self.takeSnapshot)
        self.btnSnapshot.setDisabled(True)
        self.curFrame = QPixmap()
        self.cam = IdsCam()
        self._wt = _WorkerThread(self.cam)
        self._wt.newFrame.connect(self.onNewFrame)
        self._wt.camInitialized.connect(self.onCamInitialized)
        self._wt.error.connect(self.onCamError)
        self._wt.start()

    def pauseLiveVideo(self, val):
        if self._wt.isinit and val != self._wt.ispause:
            if val:
                self.cam.pause()
            else:
                self.cam.resume()
        self._wt.ispause = val

    def onCamInitialized(self):
        len = min(self.cam.imgheight, self.cam.imgwidth)
        slidermax = 1 * 1000  # sliders sind int x1000 fuer float scale
        slidermin = int(512 / len * 1000.0) 
        self.sldrZoom.setRange(slidermin, slidermax)
        self.sldrZoom.setValue(slidermax)
        self.sldrZoom.sliderMoved.connect(self.onSliderMoved)
        self.sldrZoom.setEnabled(True)
        self.btnSnapshot.setEnabled(True)

    def onCamError(self, text):
        QMessageBox.critical(self, 'Error', text)

    def onNewFrame(self, pixmap):
        self.curFrame = pixmap
        self.lblCamera.setPixmap(pixmap)

    def onSliderMoved(self, pos):
        self._wt.zoom = pos / 1000.0

    def takeSnapshot(self):
        self.snapshot.emit(self.curFrame)

    def wheelEvent(self, e):
        d = - e.angleDelta().y()/2000.0  # des is komisches zeug
        sldrval = self.sldrZoom.value()
        sldrvalnew = sldrval + sldrval * d
        self.sldrZoom.setValue(sldrvalnew)
        self._wt.zoom = self.sldrZoom.value() / 1000


class _WorkerThread(QThread):
    newFrame = pyqtSignal(QPixmap)
    camInitialized = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, cam):
        super().__init__()
        self.cam = cam
        self.isinit = False
        self.ispause = False
        self.zoom = 1.0
        self.stopped = False

    def run(self):
        if DEBUG:
            import pydevd
            pydevd.settrace(suspend=False)
        try:
            self.cam.open(camera.Resolution.A_REALLY_HIGH_RES, framerate=10)
            self.camInitialized.emit()
            if self.ispause:
                self.cam.pause()
            self.isinit = True
        except Exception as ex:
            self.error.emit(str(ex))
            return
        while(not self.stopped):
            if self.ispause:
                QThread.msleep(100)
                continue
            f = self.cam.grab()
            sl = round(min(self.cam.imgwidth, self.cam.imgheight) * self.zoom)
            sx = round((self.cam.imgwidth - sl) / 2)
            sy = round((self.cam.imgheight - sl) / 2)
            roi = f[sy:sy + sl, sx:sx + sl]
            resized = cv2.resize(roi, (512, 512))
            img = QImage(resized.data, resized.shape[1], resized.shape[0], QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(img)
            self.newFrame.emit(pixmap)
        self.cam.close()
