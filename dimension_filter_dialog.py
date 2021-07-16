from PyQt5.QtWidgets import QDialog, QMessageBox, QAbstractSpinBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5 import uic
from dataclasses import dataclass
from enum import Enum


class Shape(Enum):
    LENGTH = 1
    DIAMETER = 2


@dataclass
class Result:
    shape: Shape
    value: float
    tolerance: float = None
    greater_than = False


class DimensionFilterDialog(QDialog):
    def __init__(self, shape: Shape):
        super().__init__()
        uic.loadUi('./ui/dimension_filter_dialog.ui', self)
        self.shape = shape
        iconfn = 'rund.png' if shape == Shape.DIAMETER else 'laenge.png'
        self.lblImage.setPixmap(QPixmap(f'./ui/png/{iconfn}'))
        self.btnGreaterThan.clicked.connect(self.updateUiState)
        self.btnOk.clicked.connect(self.onOkClicked)
        self.spnbxTolerance.setStepType(QAbstractSpinBox.AdaptiveDecimalStepType)
        self.lineEdit.returnPressed.connect(self._computeTolerance)
        self.updateUiState()

    def updateUiState(self):
        enabled = not self.btnGreaterThan.isChecked()
        self.spnbxTolerance.setEnabled(enabled)

    def myResult(self) -> Result:
        txt = self.lineEdit.text()
        value = float(txt.replace(',', '.'))  # deutsche tastatur
        r = Result(value, self.shape)
        if self.btnGreaterThan.isChecked():
            r.greater_than = True
        else:
            r.tolerance = self.spnbxTolerance.value()

    def _computeTolerance(self):
        try:
            txt = self.lineEdit.text()
            value = float(txt.replace(',', '.'))
        except ValueError:
            return
        tol = max(value / 100 * 2, 0.1)
        self.spnbxTolerance.setValue(tol)
        decimals = 2 if tol > 100.0 else 1
        self.spnbxTolerance.setDecimals(decimals)

    def onOkClicked(self):
        try:
            self.myResult()
        except ValueError:
            QMessageBox.critical(self, 'Dimension Filter', 'No Value given')
        else:
            self.accept()

    def keyPressEvent(self, evt):
        if evt.key() in [Qt.Key_Return, Qt.Key_Enter]:
            if self.lineEdit.hasFocus():
                self.spnbxTolerance.setFocus()
                self.spnbxTolerance.selectAll()
            elif self.spnbxTolerance.hasFocus():
                self.btnOk.setFocus()
            elif self.btnOk.hasFocus():
                self.onOkClicked()
