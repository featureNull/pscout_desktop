'''main window
'''
from PyQt5.QtWidgets import QMainWindow, QApplication, QShortcut, QFileDialog
from PyQt5.QtGui import QPixmap, QKeySequence
from PyQt5 import QtGui

from PyQt5.QtCore import Qt
from PyQt5 import uic
import qtawesome as qta
from pictureviz import EditorMode
from resultwindow import ResultWindow


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('./ui/mainwindow.ui', self)

        # load image button
        self.btnLoad.clicked.connect(self.openFileNameDialog)
        self.btnLoad.setIcon(qta.icon('fa5s.folder-open', color='gray'))
        self.actionLoad.triggered.connect(self.openFileNameDialog)

        # clipboard handling
        self.btnClipBoard.clicked.connect(self.copyFromClipboard)
        self.btnClipBoard.setIcon(qta.icon('fa5s.clipboard', color='gray'))
        QApplication.clipboard().dataChanged.connect(self.onClipboardChanged)
        copysc = QShortcut(QKeySequence('Ctrl+V'), self)
        copysc.activated.connect(self.copyFromClipboard)
        self.onClipboardChanged()
        self.setAcceptDrops(True)

        # 3 right buttons
        self.btnMeasure.clicked.connect(self.enterMeasure)
        messc = QShortcut(QKeySequence('Ctrl+M'), self)
        messc.activated.connect(self.enterMeasure)
        self.btnRegion.clicked.connect(self.enterSelectRoi)
        self.btnCutForeground.clicked.connect(self.enterSelectFg)

        # search button
        self.btnSearch.setIcon(qta.icon('fa5s.search', color='gray'))
        self.btnSearch.clicked.connect(self.searchModel)

        self.updateToolbaricons(EditorMode.IDLE)
        self.picEditor.modeChanged.connect(self.updateToolbaricons)

        self.btnSettings.setIcon(qta.icon('fa5s.cog', color='gray'))
        # self.contourChanged.connect(self.filterwidget.loadStatistics)

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

    def searchModel(self):
        modelids = [1, 2, 3, 4, 5, 6, 7]
        lt = QtGui.qApp.stlloadthread
        self.resultwnd = ResultWindow(modelids)
        lt.receivedData.connect(self.resultwnd.loadStlContent)
        lt.startLoading(modelids)
        self.resultwnd.setGeometry(self.geometry())
        self.resultwnd.show()

    def loadPhoto(self, pixmap):
        self.picEditor.photo = pixmap
        self.picEditor.enterMode(EditorMode.IDLE)
        self.picEditor.machmalSession(pixmap)

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        if e.mimeData().hasUrls():
            urls = e.mimeData().urls()
            pixmap = QPixmap(urls[0].toLocalFile())
            self.loadPhoto(pixmap)
            e.accept()
        else:
            e.ignore()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.picEditor.enterMode(EditorMode.IDLE)

    def enterMeasure(self):
        self.picEditor.enterMode(EditorMode.MEASURE)

    def enterSelectRoi(self):
        self.picEditor.enterMode(EditorMode.SELECT_ROI)

    def enterSelectFg(self):
        self.picEditor.enterMode(EditorMode.SELECT_FG)

    def updateToolbaricons(self, mode):
        ctx = {
            EditorMode.MEASURE: [self.btnMeasure, 'fa5s.ruler'],
            EditorMode.SELECT_ROI: [self.btnRegion, 'fa5s.vector-square'],
            EditorMode.SELECT_FG: [self.btnCutForeground, 'fa5s.draw-polygon']
        }
        for key in ctx.keys():
            color = 'white' if key == mode else 'gray'
            icon = qta.icon(ctx[key][1], color=color)
            ctx[key][0].setIcon(icon)
