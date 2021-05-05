'''application haelt singletone programm sachen zusammen
'''
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtWidgets import QApplication, QMessageBox, QLabel
from PyQt5 import QtGui
import grpc
import metadata_pb2
import metadata_pb2_grpc
import matching_pb2
import matching_pb2_grpc
from session import SessionManager
from filter import FilterManager
import opencv_hacks
from resultwindow import ResultWindow


class Application(QApplication):
    '''singletone application object.
    beherbergt FilterManager und SessionManager
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stlloadthread = None
        self.sessionManager = None
        self.filterManager = None
        self.channel = None
        self.categories = None
        self.modelsMetaData = None
        self.searchsplash = QLabel(None, Qt.SplashScreen)
        self.searchsplash.setMovie(QtGui.QMovie('./ui/gif/search_spinner.gif'))
        QtGui.qApp = self

    def connectServer(self):
        # TODO settings hinzufuegen
        # self.channel = grpc.insecure_channel('localhost:50051')
        self.channel = grpc.insecure_channel('192.168.1.6:50051')
        self._load_categories()
        self._load_model_metadata()
        self.stlloadthread = _StlLoadThread(self.channel)
        self.sessionManager = SessionManager(self.channel)
        self.filterManager = FilterManager(self.categories, self.modelsMetaData)

    def closeConnection(self):
        self.channel.close()

    def findCategory(self, id: int):
        for cat in self.categories:
            if cat.id == id:
                return cat

    def findModelMetadata(self, id: int):
        for md in self.modelsMetaData:
            if md.id == id:
                return md

    def searchModel(self):
        '''quickhack, dass man was sieht
        '''
        modelids = QtGui.qApp.filterManager.filteredModelids

        if self.sessionManager.pixmap is not None:
            try:
                self.showSplash()
                pixmap = self.sessionManager.pixmap
                cont = self.sessionManager.cont
                image_data = opencv_hacks.build_oldstyle_png_with_alpha(pixmap, cont)
                modelids2 = modelids if QtGui.qApp.filterManager.anyfilterActive else []
                entis = self._old_style_matching(image_data, modelids2)
                modelids = [enti.modelid for enti in entis]
            finally:
                self.hidesplash()
        else:
            if (len(modelids) > 30):
                QMessageBox.critical(self.activeModalWidget(), 'Error', 'to much Models without Image')
                return
        lt = QtGui.qApp.stlloadthread
        self.resultwnd = ResultWindow(modelids)
        lt.receivedData.connect(self.resultwnd.loadStlContent)
        lt.startLoading(modelids)
        self.resultwnd.setGeometry(self.mainWindow.geometry())
        self.resultwnd.picView.photo = self.sessionManager.pixmap
        self.resultwnd.show()

    def showSplash(self):
        self.searchsplash.movie().start()
        self.searchsplash.show()
        rc = self.searchsplash.geometry()
        rc.moveCenter(self.mainWindow.geometry().center())
        self.searchsplash.setGeometry(rc)

    def hidesplash(self):
        self.searchsplash.movie().stop()
        self.searchsplash.hide()

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

    def _old_style_matching(self, image_data, modelids):
        done = False
        reply = None

        def process_response(future):
            nonlocal reply, done
            reply = future.result()
            done = True

        stub = matching_pb2_grpc.MatcherStub(self.channel)
        R = matching_pb2.OldStyleMatchingRequest
        if self.sessionManager.ppmm is not None:
            request = R(
                image_data=image_data,
                filteredmodelids=modelids,
                ppmm=self.sessionManager.ppmm,
                size_flags=self.sessionManager.sizeFlags.value)
        else:
            request = R(image_data=image_data, filteredmodelids=modelids)
        future = stub.OldStyleMatching.future(request)
        future.add_done_callback(process_response)
        while not done:
            self.processEvents()
        return reply.entities


class _StlLoadThread(QThread):
    receivedData = pyqtSignal(int, bytes)

    def __init__(self, channel):
        super().__init__()
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
