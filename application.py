'''application haelt singletone programm sachen zusammen
'''
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtGui
import grpc
import metadata_pb2
import metadata_pb2_grpc
from session import SessionManager
from filter import FilterManager


class Application(QApplication):
    def __init__(self, *args, **kwargs):
        super(Application, self).__init__(*args, **kwargs)
        self.stlloadthread = None
        self.sessionManager = None
        self.filterManager = None
        self.channel = None
        self.categories = None
        self.modelsMetaData = None
        QtGui.qApp = self

    def connectServer(self):
        # TODO settings hinzufuegen
        self.channel = grpc.insecure_channel('localhost:50051')
        # metadata.init(self.channel)
        self._load_categories()
        self._load_model_metadata()
        self.stlloadthread = _StlLoadThread(self.channel)
        self.sessionManager = SessionManager(self.channel)
        self.filterManager = FilterManager(self.categories, self.modelsMetaData)

    def closeConnection(self):
        self.channel.close()

    def _load_categories(self):
        stub = metadata_pb2_grpc.DatabaseStub(self.channel)
        language = metadata_pb2.Language.EN
        request = metadata_pb2.GetCategoriesRequest(language=language)
        response = stub.GetCategories(request)
        self.categories = response.entities

    def _load_model_metadata(self):
        stub = metadata_pb2_grpc.DatabaseStub(self.channel)
        request = metadata_pb2.GetModelsMetadataRequest()
        response = stub.GetModelsMetadata(request)
        self.modelsMetaData = response.entities


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
        for modelid in self.modelids:
            # TODO fehlerbehandlung, was wenn der server wegkippt
            stub = metadata_pb2_grpc.DatabaseStub(self.channel)
            request = metadata_pb2.GetStlDataRequest(modelid=modelid)
            reply = stub.GetStlData(request)
            self.receivedData.emit(modelid, reply.data)