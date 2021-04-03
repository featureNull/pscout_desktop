'''resultwindow nach erfolgreichen suche
'''
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import QSize, pyqtSlot
from PyQt5 import uic
from PyQt5 import QtGui

from flowlayout import FlowLayout
from stl3dviz import StlThumbnail


class ResultWindow(QMainWindow):
    def __init__(self, modelids):
        super().__init__()
        uic.loadUi('./ui/resultwindow.ui', self)
        self._setupScrollArea()
        self.modelids = modelids
        self.thumbnails = {}

        for id in modelids:
            tn = StlThumbnail()
            tn.setMinimumSize(QSize(180, 180))
            tn.setMaximumSize(QSize(180, 180))
            tn.setToolTip(_build_tooltip_text(id))
            tn.clicked.connect(self._ontumbnailClicked)
            self.thumbnailLayout.addWidget(tn)
            self.thumbnails[id] = tn

    @pyqtSlot(int, bytes)
    def loadStlContent(self, id, stldata):
        self.thumbnails[id].loadstl(stldata)

    @pyqtSlot(QWidget)
    def _ontumbnailClicked(self, w: StlThumbnail):
        for id in self.thumbnails.keys():
            tn = self.thumbnails[id]
            tn.selected = w == tn
            if w == tn:
                curid = id
        if w.stldata is not None:
            self.stlView.loadstl(w.stldata)
            self.infoText.setText(_build_info_text(curid))

    def _setupScrollArea(self):
        container = QWidget()
        layout = FlowLayout(margin=10)
        layout.heightChanged.connect(self.contentWidget.setMinimumHeight)
        container.setLayout(layout)
        hlp = QVBoxLayout()
        hlp.addWidget(container)
        hlp.addStretch()
        self.contentWidget.setLayout(hlp)
        self.thumbnailLayout = layout

    def closeEvent(self, event):
        # workaround vtk bug see vtkShutdownPatch
        while self.thumbnailLayout.count() > 0:
            item = self.thumbnailLayout.takeAt(0)
            if item.widget() is not None:
                w = item.widget()
                if type(w) is StlThumbnail:
                    w.vtkShutdownPatch()
        self.stlView.vtkShutdownPatch()


def _build_tooltip_text(modelid) -> str:
    md = QtGui.qApp.findModelMetadata(modelid)
    cat = QtGui.qApp.findCategory(md.categoryid)
    html = f'''
    <html><head/><body><p>
        <b>{md.artikelnum} ({cat.shortname})</b>
        <br/>{md.shortdesc}
        </p></body></html>
    '''
    return html


def _build_info_text(modelid) -> str:
    md = QtGui.qApp.findModelMetadata(modelid)
    cat = QtGui.qApp.findCategory(md.categoryid)
    html = f'''
    <html><head/><body><p>
        <b>{md.artikelnum} ({cat.shortname})</b>
        <br/>{md.shortdesc}
        <p>{md.longdesc}</p>
        </p></body></html>
    '''
    return html
