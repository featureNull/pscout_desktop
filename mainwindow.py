'''main window
'''
from PyQt5.QtWidgets import QMainWindow, QApplication, QShortcut, QFileDialog
from PyQt5.QtGui import QPixmap, QKeySequence
from PyQt5.QtCore import Qt
from PyQt5 import uic
import qtawesome as qta
from photowidget import Mode


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

        self.updateToolbaricons(Mode.IDLE)
        self.photoWidget.modeChanged.connect(self.updateToolbaricons)

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
        pass

    def loadPhoto(self, pixmap):
        w = self.photoWidget
        w.photo = pixmap
        w.enterMode(Mode.IDLE)
        w.machmalSession(pixmap)

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
            self.photoWidget.enterMode(Mode.IDLE)

    def enterMeasure(self):
        self.photoWidget.enterMode(Mode.MEASURE)

    def enterSelectRoi(self):
        self.photoWidget.enterMode(Mode.SELECT_ROI)

    def enterSelectFg(self):
        self.photoWidget.enterMode(Mode.SELECT_FG)

    def updateToolbaricons(self, mode):
        ctx = {
            Mode.MEASURE: [self.btnMeasure, 'fa5s.ruler'],
            Mode.SELECT_ROI: [self.btnRegion, 'fa5s.vector-square'],
            Mode.SELECT_FG: [self.btnCutForeground, 'fa5s.draw-polygon']
        }
        for key in ctx.keys():
            color = 'white' if key == mode else 'gray'
            icon = qta.icon(ctx[key][1], color=color)
            ctx[key][0].setIcon(icon)
