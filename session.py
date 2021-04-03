from PyQt5.QtCore import QObject, pyqtSignal
import matching_pb2 as pb2
import matching_pb2_grpc as pb2_grpc
from PyQt5.QtCore import QByteArray, QBuffer, QIODevice, QPointF, QRectF, QRect
from PyQt5.QtGui import QPolygonF, QPixmap

Stup = pb2_grpc.MatcherStub


class SessionManager(QObject):
    # session wurde aufgetan, oder geschlossen
    closed = pyqtSignal()
    opened = pyqtSignal(QPixmap)
    contourChanged = pyqtSignal(QPolygonF)
    roiChanged = pyqtSignal(QRectF)
    stateChanged = pyqtSignal(bool)

    def __init__(self, channel):
        super().__init__()
        self.roi = None
        self.cont = None
        self._channel = channel
        self._uuid = None
        self.pixmap = None

    def open(self, pixmap):
        '''opens new image session'''
        if self._uuid is not None:
            self.close()
        self.pixmap = pixmap
        stub = Stup(self._channel)
        request = pb2.OpenSessionRequest(image_data=_decode(pixmap))
        reply = stub.OpenSession(request)
        self._uuid = reply.object_fg.uuid
        self.stateChanged.emit(True)
        return roi_to_rect(reply.object_fg.roi)

    def close(self):
        stub = Stup(self._channel)
        stub.CloseSession(pb2.SessionRequest(uuid=self._uuid))
        self.pixmap = self.roi = self._uuid = None
        self.stateChanged.emit(False)

    def findForeground(self, rect):
        def process_response(future):
            res = future.result()
            cont = _contour_to_qpolygonf(res.contour)
            self.cont = cont
            self.contourChanged.emit(cont)
        stub = Stup(self._channel)
        request = pb2.FindForeGroundRequest(uuid=self._uuid, roi=_rect_to_roi(rect))
        future = stub.FindForeGround.future(request)
        future.add_done_callback(process_response)

    def addForeground(self, polyline, linewidth=11):
        type = pb2.CorrectForeGroundRequest.Type.ADD
        self._correctForeground(polyline, linewidth, type)

    def removeForeground(self, polyline, linewidth=11):
        type = pb2.CorrectForeGroundRequest.Type.REMOVE
        self._correctForeground(polyline, linewidth, type)

    def _correctForeground(self, polyline, linewidth, type):
        def process_response(future):
            res = future.result()
            cont = _contour_to_qpolygonf(res.contour)
            self.cont = cont
            self.contourChanged.emit(cont)
        stub = Stup(self._channel)
        corline = _qpolyline_to_point2d_array(polyline)
        R = pb2.CorrectForeGroundRequest
        request = R(uuid=self._uuid, type=type, corline=corline, lineWidth=linewidth)
        future = stub.CorrectForeGround.future(request)
        future.add_done_callback(process_response)

    '''
    def estimate_candidates():
        assert _uuid is not None
        stub = pb2_grpc.MatcherStub(_channel)
        request = pb2.SessionRequest(uuid=_uuid)
        reply = stub.EstimateCandidates(request)
        return reply.modelids
    '''


def _decode(pixmap, format='jpg'):
    ba = QByteArray()
    buff = QBuffer(ba)
    buff.open(QIODevice.WriteOnly)
    ok = pixmap.save(buff, format)
    assert ok
    return ba.data()


def _rect_to_roi(r):
    box = pb2.Box2D(x=r.x(), y=r.y(), w=r.width(), h=r.height())
    return box


def roi_to_rect(box):
    return QRect(box.x, box.y, box.w, box.h)


def _contour_to_qpolygonf(contour):
    polygon = QPolygonF()
    for p in contour:
        polygon.append(QPointF(p.x, p.y))
    return polygon


def _qpolyline_to_point2d_array(polyline):
    return [pb2.Point2D(x=round(p.x()), y=round(p.y())) for p in polyline]
