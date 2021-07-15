'''resultwindow nach erfolgreichen suche
'''
from PyQt5.QtWidgets import QMainWindow, QMenu
from PyQt5 import uic
import qtawesome as qta
from dimension_filter_dialog import DimensionFilterDialog


class ResultWindowNeu(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('./ui/resultwindow_neu.ui', self)
        self.btnBackward.setIcon(qta.icon('fa5s.arrow-left', color='gray'))
        self.btnBackward.clicked.connect(self.goBackward)

        self.btnForward.setIcon(qta.icon('fa5s.arrow-right', color='gray'))
        self.btnCopyPartNum.setIcon(qta.icon('fa5s.copy', color='gray'))
        self.btnDownloadDoc.setIcon(qta.icon('fa5s.file-download', color='gray'))
        self.btnBom.setIcon(qta.icon('fa5s.sort-amount-down-alt', color='gray'))
        self.btnMatUseage.setIcon(qta.icon('fa5s.sort-amount-up-alt', color='gray'))

        menu = QMenu()
        menu.addAction("Step File")
        menu.addAction("Stl File")
        menu.addSeparator()
        menu.addAction("blablabl.txt")
        self.btnDownloadDoc.setMenu(menu)

    def goBackward(self):
        dlg = DimensionFilterDialog()
        dlg.exec()
