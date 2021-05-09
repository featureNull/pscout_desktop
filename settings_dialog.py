'''main window'''
from PyQt5.QtWidgets import QDialog, QListWidgetItem, QFileDialog
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5 import uic
import pscout_settings as ps
from collections import namedtuple

Cat = namedtuple('Cat', ['shortname', 'item'])

class SettingsDialog(QDialog):
    def __init__(self, settings):
        super().__init__()
        uic.loadUi('./ui/settings.ui', self)
        # search tab
        self._fillDefaultFilters(settings.default_disabled_categroies)
        cfg = settings.max_result_count
        self.sldrWithImage.setValue(cfg.with_image)
        self.sldrWithoutImage.setValue(cfg.without_image)
        # connection tab
        cfg = settings.connection
        self.editIpAdress.setText(cfg.ip)
        self.editPort.setText(str(cfg.port))
        self.editPort.setValidator(QtGui.QIntValidator(0, 99999999))
        self.btnEnableSsl.setChecked(cfg.use_ssl)
        self.editCertificate.setText(cfg.certificate)
        self.editKey.setText(cfg.key)
        self.btnLoadCertificate.clicked.connect(self._loadCertificate)
        self.btnLoadKey.clicked.connect(self._loadKey)
        # camera
        self.comboCamera.setCurrentIndex(settings.camera_type)

    def getData(self):
        max_result_count = ps.MaxResultCount(
            with_image=self.sldrWithImage.value(),
            without_image=self.sldrWithoutImage.value()
        )
        connection = ps.Connection(
            ip=self.editIpAdress.text(),
            port=int(self.editPort.text()),
            use_ssl=self.btnEnableSsl.isChecked(),
            certificate=self.editCertificate.text(),
            key=self.editKey.text()
        )
        settings = ps.Settings(
            max_result_count=max_result_count,
            default_disabled_categroies=self._getDisabledCats(),
            connection=connection,
            camera_type=self.comboCamera.currentIndex()
        )
        return settings

    def setConnectionEnabled(self, enabled):
        '''connection enalbed disablen, weiss nicht ob es gut ist wenn die
        leute das einstellen koennen'''
        entities = [
            self.editIpAdress, self.editPort, self.btnEnableSsl,
            self.editCertificate, self.editKey,
            self.btnLoadCertificate, self.btnLoadKey
        ]
        for e in entities:
            e.setEnabled(enabled)

    def _fillDefaultFilters(self, disabledcats):
        manager = QtGui.qApp.filterManager
        self.cats = {}
        if manager is None:
            # das ist der fall, wenn wir uns nicht connecten koennen
            return
        for id, cat in manager.categories.items():
            if len(cat.shortname) > 0:
                disptext = f'({cat.shortname})  {cat.longname}'
            else:
                disptext = f'{cat.longname}'
            item = QListWidgetItem(disptext)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            if cat.shortname in disabledcats:
                item.setCheckState(Qt.Unchecked)
            else:
                item.setCheckState(Qt.Checked)
            self.listWidget.addItem(item)
            self.cats[id] = Cat(cat.shortname, item)

    def _loadCertificate(self):
        fileName, _ = QFileDialog.getOpenFileName(self, 'Certificate', '.', '(*.pem)')
        if len(fileName) > 0:
            self.editCertificate.setText(fileName)

    def _loadKey(self):
        fileName, _ = QFileDialog.getOpenFileName(self, 'Key', '.', '(*.pem)')
        if len(fileName) > 0:
            self.editKey.setText(fileName)

    def _getDisabledCats(self):
        res = []
        for cat in self.cats.values():
            if cat.item.checkState() == Qt.Unchecked:
                res.append(cat.shortname)
        return res
