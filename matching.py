import matching_pb2
import matching_pb2_grpc
from PyQt5.QtCore import QByteArray, QBuffer, QIODevice, QPointF
from PyQt5.QtGui import QPolygonF

_channel = None
_request_uuid = None


def init(channel):
    global _channel
    _channel = channel


def open_session(pixmap):
    global _request_uuid
    imgdata = _compress_bixmap(pixmap, format='jpg')
    if _request_uuid is not None:
        close_session()
    stub = matching_pb2_grpc.MatcherStub(_channel)
    request = matching_pb2.OpenSessionRequest()
    request.image_data = imgdata
    reply = stub.OpenSession(request)
    _request_uuid = reply.object_fg.uuid
    return reply.object_fg.roi


def close_session():
    global _request_uuid
    assert _request_uuid is not None
    stub = matching_pb2_grpc.MatcherStub(_channel)
    stub.CloseSession(matching_pb2.SessionRequest(uuid=_request_uuid))
    _request_uuid = None


def find_foreground(rect):
    assert _request_uuid is not None
    roi = _rect_to_roi(rect)
    stub = matching_pb2_grpc.MatcherStub(_channel)
    request = matching_pb2.FindForeGroundRequest(uuid=_request_uuid, roi=roi)
    reply = stub.FindForeGround(request)
    return _contour_to_qpolygonf(reply.contour)


def add_foreground(polyline, linewidth=11):
    assert _request_uuid is not None
    stub = matching_pb2_grpc.MatcherStub(_channel)
    Request = matching_pb2.CorrectForeGroundRequest
    corline = _qpolyline_to_point2d_array(polyline)
    request = Request(uuid=_request_uuid, corline=corline, lineWidth=linewidth, type=Request.Type.ADD)
    reply = stub.CorrectForeGround(request)
    return _contour_to_qpolygonf(reply.contour)


def estimate_candidates():
    assert _request_uuid is not None
    stub = matching_pb2_grpc.MatcherStub(_channel)
    request = matching_pb2.SessionRequest(uuid=_request_uuid)
    reply = stub.EstimateCandidates(request)
    return reply.modelids


def remove_foreground(polyline, linewidth=11):
    assert _request_uuid is not None
    stub = matching_pb2_grpc.MatcherStub(_channel)
    Request = matching_pb2.CorrectForeGroundRequest
    corline = _qpolyline_to_point2d_array(polyline)
    request = Request(uuid=_request_uuid, corline=corline, lineWidth=linewidth, type=Request.Type.REMOVE)
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


def _contour_to_qpolygonf(contour):
    polygon = QPolygonF()
    for p in contour:
        polygon.append(QPointF(p.x, p.y))
    return polygon


def _qpolyline_to_point2d_array(polyline):
    P2D = matching_pb2.Point2D
    return [P2D(x=round(p.x()), y=round(p.y())) for p in polyline]

