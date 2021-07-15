from PyQt5.QtWidgets import QDialog, QMessageBox, QAbstractSpinBox
from PyQt5.QtGui import QPixmap
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
    def __init__(self):
        super().__init__()
        uic.loadUi('./ui/dimension_filter_dialog.ui', self)
        self.rundPixmap = QPixmap('./ui/png/rund.png')
        self.laengePixmap = QPixmap('./ui/png/laenge.png')
        self.cbxShape.currentIndexChanged.connect(self.updateUiState)
        self.btnGreaterThan.clicked.connect(self.updateUiState)
        self.btnOk.clicked.connect(self.onOkClicked)
        self.spnbxTolerance.setStepType(QAbstractSpinBox.AdaptiveDecimalStepType)
        self.lineEdit.returnPressed.connect(self._computeTolerance)
        self.updateUiState()

    def updateUiState(self):
        ix = self.cbxShape.currentIndex()
        pxmap = self.laengePixmap if ix == 0 else self.rundPixmap
        self.lblImage.setPixmap(pxmap)
        enabled = not self.btnGreaterThan.isChecked()
        self.spnbxTolerance.setEnabled(enabled)

    def myResult(self) -> Result:
        txt = self.lineEdit.text()
        value = float(txt.replace(',', '.'))  # deutsche tastatur
        shape = Shape.LENGTH if self.cbxShape.currentIndex() else Shape.DIAMETER
        r = Result(value, shape)
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
        self.spnbxTolerance.setFocus()

    def onOkClicked(self):
        try:
            self.myResult()
        except ValueError:
            QMessageBox.critical(self, 'Dimension Filter', 'No Value given')
        else:
            self.accept()
