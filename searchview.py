'''search view mit filter und image content'''
from PyQt5.QtWidgets import QWidget, QApplication, QShortcut, QFileDialog
from PyQt5.QtGui import QPixmap, QKeySequence
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtGui

from PyQt5.QtCore import Qt
from PyQt5 import uic
import qtawesome as qta
from pictureviz import EditMode
import opencv_hacks


class SearchView(QWidget):
    camViewRequested = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('./ui/searchview.ui', self)
        self.picEditor.modeChanged.connect(self.updateToolbaricons)
        # setup load image button
        self.btnLoad.clicked.connect(self.openFileNameDialog)
        self.btnLoad.setIcon(qta.icon('fa5s.folder-open', color='gray'))
        # clipboard handling
        self.btnClipBoard.clicked.connect(self.copyFromClipboard)
        self.btnClipBoard.setIcon(qta.icon('fa5s.clipboard', color='gray'))
        QApplication.clipboard().dataChanged.connect(self.onClipboardChanged)
        copysc = QShortcut(QKeySequence('Ctrl+V'), self)
        copysc.activated.connect(self.copyFromClipboard)
        self.onClipboardChanged()
        # close image
        self.btnCloseImage.setIcon(qta.icon('fa5s.trash-alt', color='gray'))
        self.btnCloseImage.setEnabled(False)
        self.btnCloseImage.clicked.connect(self.closePhoto)
        QtGui.qApp.sessionManager.stateChanged.connect(self.btnCloseImage.setEnabled)
        # camera
        self.btnCamera.clicked.connect(self.camViewRequested)
        self.btnCamera.setIcon(qta.icon('fa5s.video', color='gray'))
        # 3 right buttons
        self.btnMeasure.clicked.connect(self.enterMeasure)
        messc = QShortcut(QKeySequence('Ctrl+M'), self)
        messc.activated.connect(self.enterMeasure)
        self.btnRegion.clicked.connect(self.enterSelectRoi)
        self.btnCutForeground.clicked.connect(self.enterSelectFg)
        # search button
        self.btnSearch.setIcon(qta.icon('fa5s.search', color='gray'))
        self.btnSearch.clicked.connect(QtGui.qApp.searchModel)
        self.updateToolbaricons(EditMode.IDLE)
        # settings
        self.btnSettings.setIcon(qta.icon('fa5s.cog', color='gray'))

    def openFileNameDialog(self):
        filter = 'Image files (*.jpg *.png)'
        fileName, _ = QFileDialog.getOpenFileName(self, 'Open Image file', filter=filter)
        if fileName:
            self.loadPhoto(QPixmap(fileName))

    def onClipboardChanged(self):
        hlp = QApplication.clipboard().mimeData().hasImage()
        self.btnClipBoard.setEnabled(hlp)

    def copyFromClipboard(self):
        pixmap = QApplication.clipboard().pixmap()
        self.loadPhoto(pixmap)

    def loadPhoto(self, pixmap):
        pixmap512x512 = opencv_hacks.qpixmap_to_border_512x512(pixmap)
        rect = QtGui.qApp.sessionManager.open(pixmap512x512)
        self.picEditor.setPhoto(pixmap512x512, rect)

    def closePhoto(self):
        self.picEditor.setMode(EditMode.IDLE)
        QtGui.qApp.sessionManager.close()
        self.picEditor.setPhoto(None)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.picEditor.setMode(EditMode.IDLE)

    def enterMeasure(self):
        self.picEditor.setMode(EditMode.MEASURE)

    def enterSelectRoi(self):
        self.picEditor.setMode(EditMode.ROI)

    def enterSelectFg(self):
        self.picEditor.setMode(EditMode.FG)

    def updateToolbaricons(self, mode):
        ctx = {
            EditMode.MEASURE: [self.btnMeasure, 'fa5s.ruler'],
            EditMode.ROI: [self.btnRegion, 'fa5s.vector-square'],
            EditMode.FG: [self.btnCutForeground, 'fa5s.draw-polygon']
        }
        for key in ctx.keys():
            color = 'white' if key == mode else 'gray'
            icon = qta.icon(ctx[key][1], color=color)
            ctx[key][0].setIcon(icon)
