'''application haelt singletone programm sachen zusammen
'''
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtGui
import metadata
import grpc
from session import SessionManager


class Application(QApplication):
    def __init__(self, *args, **kwargs):
        super(Application, self).__init__(*args, **kwargs)
        self.stlloadthread = None
        self.sessionManager = None
        QtGui.qApp = self

    def connectServer(self):
        # TODO settings hinzufuegen
        self.channel = grpc.insecure_channel('localhost:50051')
        metadata.init(self.channel)
        self.stlloadthread = _StlLoadThread(self.channel)
        self.sessionManager = SessionManager(self.channel)

    def closeConnection(self):
        self.channel.close()


class _StlLoadThread(QThread):
    receivedData = pyqtSignal(int, bytes)

    def __init__(self, channel):
        super(_StlLoadThread, self).__init__()
        self.modelids = None
        self.channel = channel

    def startLoading(self, modelids: list):
        self.modelids = modelids
        self.start()

    def run(self):
        for id in self.modelids:
            data = metadata.get_stl_data(self.channel, id)
            self.receivedData.emit(id, data)