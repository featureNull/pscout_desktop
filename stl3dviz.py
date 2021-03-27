"""Stl anzeigen von 3D modellen
"""
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt, pyqtProperty, pyqtSignal
import temp
import vtk
import os


class StlDetailsView(QVTKRenderWindowInteractor):
    """grosses fenster mit maus interaktion
    """
    def __init__(self, *args, **kwargs):
        super(StlDetailsView, self).__init__(*args, **kwargs)
        self.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
        self.ren = vtk.vtkRenderer()
        self.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.GetRenderWindow().GetInteractor()

        self.reader = vtk.vtkSTLReader()
        self.mapper = vtk.vtkPolyDataMapper()

        # Create an actor
        actor = vtk.vtkActor()
        actor.SetMapper(self.mapper)
        actor.GetProperty().SetColor(0.7, 0.7, 0.7)

        self.ren.AddActor(actor)
        self.ren.SetBackground(0.098, 0.137, 0.176)
        self.iren.Initialize()

    def loadstl(self, stldata):
        try:
            tmpfn = temp.tempfile() + '.stl'
            with open(tmpfn, "wb") as fh:
                fh.write(stldata)
            self.reader.SetFileName(tmpfn)
            self.mapper.SetInputConnection(self.reader.GetOutputPort())
            self.reader.Update()
            self.ren.ResetCamera()
            self.update()
        finally:
            if os.path.exists(tmpfn):
                os.remove(tmpfn)

    def vtkShutdownPatch(self):
        # patch around vtk cleanup error https://pastebin.com/EwuHZBFG
        self.Finalize()


class StlThumbnail(QtWidgets.QStackedWidget):
    """Preview widget auf der linken seite
    TODO: das grau vom spinner passt von der farbe nicht
    """
    clicked = pyqtSignal(QtWidgets.QWidget)

    def __init__(self, *args, **kwargs):
        super(StlThumbnail, self).__init__(*args, **kwargs)
        self._selected = False
        self.vtkRenderWindow = None
        self.stldata = None
        self._updateStyleSheet()
        spinner = self._setupSpinnerUi()
        self.addWidget(spinner)
        self.movie.start()

    def loadstl(self, stldata):
        try:
            self.stldata = stldata
            tmpfn = temp.tempfile() + '.stl'
            with open(tmpfn, "wb") as fh:
                fh.write(stldata)
            vtkw = self._setupVtk(tmpfn)
            self.addWidget(vtkw)
            self.movie.stop()
            self.setCurrentWidget(vtkw)
        finally:
            if os.path.exists(tmpfn):
                os.remove(tmpfn)

    def vtkShutdownPatch(self):
        # patch around vtk cleanup error https://pastebin.com/EwuHZBFG
        if self.vtkRenderWindow is not None:
            self.vtkRenderWindow.Finalize()


    @pyqtProperty(bool)
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value):
        if self._selected == value:
            return
        self._selected = value
        self._updateStyleSheet()
        self.update()

    def _setupSpinnerUi(self):
        w = QtWidgets.QWidget(self)
        w.setStyleSheet('background: #333333')
        vbox = QtWidgets.QVBoxLayout(w)
        self.movie = QtGui.QMovie('./ui/gif/spinner.gif')
        spnr = QtWidgets.QLabel()
        spnr.setScaledContents(True)
        spnr.setFixedSize(36, 36)
        spnr.setMovie(self.movie)
        vbox.addStretch(1)
        vbox.addWidget(spnr, alignment=Qt.AlignHCenter)
        vbox.addStretch(1)
        return w

    def _setupVtk(self, filename: str):
        assert self.count() == 1  # do not use twice
        w = QVTKRenderWindowInteractor(self)
        voisuper = vtk.vtkInteractorStyle()  # _PassiveInteractorStyle()
        voisuper.AddObserver("LeftButtonReleaseEvent", self.onVtkButtonReleased)
        w.SetInteractorStyle(voisuper)
        renderer = vtk.vtkRenderer()
        w.GetRenderWindow().AddRenderer(renderer)
        reader = vtk.vtkSTLReader()
        reader.SetFileName(filename)
        reader.Update()
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(reader.GetOutputPort())
        # Create an actor
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(0.7, 0.7, 0.7)
        renderer.AddActor(actor)
        renderer.SetBackground(0.196, 0.254, 0.294)
        renderer.ResetCamera()
        iren = w.GetRenderWindow().GetInteractor()
        iren.Initialize()
        self.vtkRenderWindow = w.GetRenderWindow()
        return w

    def _updateStyleSheet(self):
        if self.stldata is None:
            return
        bwidth = 3 if self.selected else 1
        active = self.selected or self.underMouse()
        color = '#1464A0' if active else '#32414B'
        style = f'''#fab {{
            background: #32414B;
            border-width: {bwidth};
            border-radius: 3;
            border-color: {color};
        }}
        '''
        self.setObjectName('fab')
        self.setStyleSheet(style)

    def enterEvent(self, event):
        self._updateStyleSheet()
        self.update()

    def leaveEvent(self, event):
        self._updateStyleSheet()
        self.update()

    def onVtkButtonReleased(self, obj, event):
        self.clicked.emit(self)


class _PassiveInteractorStyle(vtk.vtkInteractorStyleUser):
    def __init__(self, parent=None):
        pass
