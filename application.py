'''application haelt singletone programm sachen zusammen
'''
from PyQt5.QtCore import QThread, QObject, pyqtSignal
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtGui
import matching_pb2
import matching_pb2_grpc
from PyQt5.QtCore import QByteArray, QBuffer, QIODevice, QPointF, QRectF, QRect
from PyQt5.QtGui import QPolygonF, QPixmap
import metadata
import grpc


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
        self.sessionManager = _SessionManager(self.channel)

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


class _SessionManager(QObject):
    # session wurde aufgetan, oder geschlossen
    closed = pyqtSignal()
    opened = pyqtSignal(QPixmap)
    contourChanged = pyqtSignal(QPolygonF)
    roiChanged = pyqtSignal(QRectF)

    def __init__(self, channel):
        super(QObject, self).__init__()
        self.roi = None
        self._channel = channel
        self._uuid = None

    def open(self, pixmap):
        '''opens new image session
        '''
        imgdata = _compress_bixmap(pixmap, format='jpg')
        if self._uuid is not None:
            self.close()
        stub = matching_pb2_grpc.MatcherStub(self._channel)
        request = matching_pb2.OpenSessionRequest()
        request.image_data = imgdata
        reply = stub.OpenSession(request)
        self._uuid = reply.object_fg.uuid
        return roi_to_rect(reply.object_fg.roi)

    def close(self):
        stub = matching_pb2_grpc.MatcherStub(self._channel)
        stub.CloseSession(matching_pb2.SessionRequest(uuid=self._uuid))
        self._uuid = None
        self.roi = None

    def findForeground(self, rect):
        roi = _rect_to_roi(rect)
        stub = matching_pb2_grpc.MatcherStub(self._channel)
        request = matching_pb2.FindForeGroundRequest(uuid=self._uuid, roi=roi)
        reply = stub.FindForeGround(request)
        return _contour_to_qpolygonf(reply.contour)

    def addForeground(self, polyline, linewidth=11):
        assert self._uuid is not None
        stub = matching_pb2_grpc.MatcherStub(self._channel)
        Request = matching_pb2.CorrectForeGroundRequest
        corline = _qpolyline_to_point2d_array(polyline)
        request = Request(uuid=self._uuid, corline=corline, lineWidth=linewidth, type=Request.Type.ADD)
        reply = stub.CorrectForeGround(request)
        return _contour_to_qpolygonf(reply.contour)

    '''
    def estimate_candidates():
        assert _uuid is not None
        stub = matching_pb2_grpc.MatcherStub(_channel)
        request = matching_pb2.SessionRequest(uuid=_uuid)
        reply = stub.EstimateCandidates(request)
        return reply.modelids
    '''

    def removeForeground(self, polyline, linewidth=11):
        assert self._uuid is not None
        stub = matching_pb2_grpc.MatcherStub(self._channel)
        Request = matching_pb2.CorrectForeGroundRequest
        corline = _qpolyline_to_point2d_array(polyline)
        request = Request(uuid=self._uuid, corline=corline, lineWidth=linewidth, type=Request.Type.REMOVE)
        reply = stub.CorrectForeGround(request)
        return _contour_to_qpolygonf(reply.contour)


def _compress_bixmap(pixmap, format='jpg'):
    ba = QByteArray()
    buff = QBuffer(ba)
    buff.open(QIODevice.WriteOnly)
    ok = pixmap.save(buff, format)
    assert ok
    return ba.data()


def _rect_to_roi(r):
    box = matching_pb2.Box2D(x=r.x(), y=r.y(), w=r.width(), h=r.height())
    return box

def roi_to_rect(box):
    return QRect(box.x, box.y, box.w, box.h)


def _contour_to_qpolygonf(contour):
    polygon = QPolygonF()
    for p in contour:
        polygon.append(QPointF(p.x, p.y))
    return polygon


def _qpolyline_to_point2d_array(polyline):
    P2D = matching_pb2.Point2D
    return [P2D(x=round(p.x()), y=round(p.y())) for p in polyline]
