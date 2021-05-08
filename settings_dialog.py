'''main window'''
from PyQt5.QtWidgets import QDialog, QListWidgetItem, QFileDialog
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import Qt
from PyQt5 import uic
import pscout_settings as ps


class SettingsDialog(QDialog):
    def __init__(self, settings):
        super().__init__()
        uic.loadUi('./ui/settings.ui', self)
        # search tab
        self._fillDefaultFilters()
        cfg = settings.max_result_count
        self.sldrWithImage.setValue(cfg.with_image)
        self.sldrWithoutImage.setValue(cfg.without_image)
        # connection tab
        cfg = settings.connection
        self.editIpAdress.setText(cfg.ip)
        self.editPort.setText(str(cfg.port))
        self.editPort.setValidator(QIntValidator(0, 99999999))
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
            default_disabled_categroies=[],
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

    def _fillDefaultFilters(self):
        itemLabels = ['1..', '2..', '3..']
        for title in itemLabels:
            item = QListWidgetItem(title)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            self.listWidget.addItem(item)

    def _loadCertificate(self):
        fileName, _ = QFileDialog.getOpenFileName(self, 'Certificate', '.', '(*.pem)')
        if len(fileName) > 0:
            self.editCertificate.setText(fileName)

    def _loadKey(self):
        fileName, _ = QFileDialog.getOpenFileName(self, 'Key', '.', '(*.pem)')
        if len(fileName) > 0:
            self.editKey.setText(fileName)
