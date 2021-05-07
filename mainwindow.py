'''main window'''
from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QMessageBox
from searchview import SearchView
from camview import CamView
from PyQt5.QtGui import QPixmap


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # clipboard handling
        self.setAcceptDrops(True)
        # such view
        self.searchview = SearchView()
        self.searchview.camViewRequested.connect(self.displayCamView)
        # live video
        self.camview = CamView()
        self.camview.pauseLiveVideo(True)
        self.camview.closeRequested.connect(self.displaySearchView)
        self.camview.snapshot.connect(self.onCamSnapshot)
        # layout
        self.stackedwidget = QStackedWidget()
        self.stackedwidget.addWidget(self.searchview)
        self.stackedwidget.addWidget(self.camview)
        self.stackedwidget.setCurrentIndex(0)
        self.setCentralWidget(self.stackedwidget)
        self.resize(1300, 900)

    def displayCamView(self):
        self.camview.pauseLiveVideo(False)
        self.stackedwidget.setCurrentIndex(1)

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
