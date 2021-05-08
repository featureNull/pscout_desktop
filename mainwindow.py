'''main window'''
from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QMessageBox
from searchview import SearchView
from camview import CamView
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui
import pscout_settings


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stackedwidget = QStackedWidget()
        # clipboard handling
        self.setAcceptDrops(True)
        # such view
        self.searchview = SearchView()
        self.searchview.camViewRequested.connect(self.displayCamView)
        self.stackedwidget.addWidget(self.searchview)
        # live video
        if QtGui.qApp.settings.camera_type != pscout_settings.NO_CAMERA:
            self.camview = CamView()
            self.camview.pauseLiveVideo(True)
            self.camview.closeRequested.connect(self.displaySearchView)
            self.camview.snapshot.connect(self.onCamSnapshot)
            self.stackedwidget.addWidget(self.camview)
        # layout
        self.stackedwidget.setCurrentIndex(0)
        self.setCentralWidget(self.stackedwidget)
        self.resize(1300, 900)

    def displayCamView(self):
        camavail = QtGui.qApp.settings.camera_type != pscout_settings.NO_CAMERA
        if camavail:
            self.camview.pauseLiveVideo(False)
            self.stackedwidget.setCurrentIndex(1)
        else:
            QMessageBox.information(self, 'Camera', 'no Camera availible')

    def displaySearchView(self):
        self.camview.pauseLiveVideo(True)
        self.stackedwidget.setCurrentIndex(0)

    def onCamSnapshot(self, pixmap):
        self.displaySearchView()
        self.searchview.loadPhoto(pixmap)

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        if e.mimeData().hasUrls():
            urls = e.mimeData().urls()
            pixmap = QPixmap(urls[0].toLocalFile())
            if pixmap.isNull():
                QMessageBox.critical(self, 'Error', 'the object dropped is not an image')
            else:
                self.searchview.loadPhoto(pixmap)
            e.accept()
        else:
            e.ignore()
