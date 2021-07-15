'''interactive Overlay for pictureEditor
'''
from PyQt5.QtGui import QPen, QPolygonF, QColor, QFontMetrics
from PyQt5.QtCore import QEvent, Qt, QLine, QPoint, QPointF, QRectF

from enum import Enum
import math
from abc import ABC, abstractmethod
import copy


class AbstractOverlay(ABC):
    '''used by widget to render region of intgerest, etc..
    '''
    def __init__(self, widget):
        self.widget = widget
        self.doneCallBack = None
        self.active = False

    def routeEvent(self, event):
        if self.active:
            if event.type() == QEvent.MouseButtonPress:
                if event.button() == Qt.LeftButton:
                    return self.handleEvent(event)
            elif event.type() == QEvent.MouseButtonRelease:
                if event.button() == Qt.LeftButton:
                    return self.handleEvent(event)
            elif event.type() == QEvent.MouseMove:
                return self.handleEvent(event)
        return False

    @abstractmethod
    def handleEvent(self, event) -> bool:
        '''handles mouse and keyboard event. retunrs True, if evetn should not
        be further processed
        '''
        pass

    @abstractmethod
    def render(self, painter):
        pass

    @abstractmethod
    def enter(self):
        pass

    @abstractmethod
    def leave(self):
        pass

    def transform(self):
        return self.widget.transform()

    def invertedTransform(self):
        trf, _ = self.transform().inverted()
        return trf


class MesOverlay(AbstractOverlay):
    '''Overlay for measure distances between image points
    '''
    def __init__(self, widget):
        super().__init__(widget)
        self._started = False
        self._line = None
        self.lengthText = None

    def handleEvent(self, event) -> bool:
        trfpos = self.invertedTransform().map(event.pos())
        processed = False
        if event.type() == QEvent.MouseButtonPress:
            if event.buttons() & Qt.LeftButton and not self._started:
                processed = True
                self._line = QLine(trfpos, trfpos)
        elif event.type() == QEvent.MouseMove:
            if event.buttons() & Qt.LeftButton or self._started:
                processed = True
                self._line.setP2(trfpos)
        elif event.type() == QEvent.MouseButtonRelease:
            if self._started:
                self.active = False
                if self.doneCallBack is not None:
                    self.doneCallBack()
            else:
                self._started = True
        if processed:
            self.widget.update()
        return processed

    def render(self, painter):
        if self._line is None:
            return
        line = self.transform().map(self._line)
        pen = QPen(Qt.white)
        pen.setWidth(3 if self.active else 2)
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)
        painter.drawLine(line)
        if self.lengthText is not None:
            fm = QFontMetrics(painter.font())
            rc = fm.boundingRect(self.lengthText)
            mx = line.x1() + line.dx() / 2 - rc.center().x()
            my = line.y1() + line.dy() / 2 - rc.center().y()
            rc.translate(mx, my)
            rc.adjust(-5, -5, 5, 5)
            painter.setPen(QPen(Qt.white))
            painter.fillRect(rc, Qt.black)
            painter.drawRect(rc)
            painter.drawText(rc, Qt.AlignCenter, self.lengthText)

    def enter(self):
        self.active = True
        self._started = False
        self._line = None
        self.lengthText = None
        self.widget.update()

    def leave(self):
        self.active = False
        self._started = False
        self.widget.update()

    def reset(self):
        self.active = False
        self._started = False
        self._line = None
        self.lengthText = None

    def lineLength(self):
        if self._line is None:
            return None
        return math.sqrt(
            self._line.dx()**2 + self._line.dy()**2
            )


class Hit(Enum):
    NoHit = 0
    Center = 1
    Top = 2
    TopRight = 3
    Right = 4
    BottomRight = 5
    Bottom = 6
    BottomLeft = 7
    Left = 8
    TopLeft = 9


class RoiOverlay(AbstractOverlay):
    '''Definie Rectangular region of interest
    '''
    def __init__(self, widget):
        super().__init__(widget)
        self.imageRoi = QRectF(10, 20, 30, 40)
        self._mousePressedPos = None
        self._itemRoiCache = None
        self._hit = Hit.NoHit

    @property
    def itemRoi(self):
        mat = self.transform()
        return mat.mapRect(self.imageRoi)

    def handleEvent(self, event) -> bool:
        trf = self.invertedTransform()
        processed = False

        if event.type() == QEvent.MouseButtonPress:
            self._mousePressedPos = event.pos()
            self._itemRoiCache = copy.deepcopy(self.itemRoi)

            if self._hit == Hit.Center:
                self.widget.setCursor(Qt.ClosedHandCursor)
        elif event.type() == QEvent.MouseMove and event.buttons() & Qt.LeftButton:
            rc = copy.deepcopy(self._itemRoiCache)
            shift = event.pos() - self._mousePressedPos
            processed = True

            if self._hit == Hit.Center:
                rc.translate(shift)
            elif self._hit == Hit.Top:
                rc.setTop(event.pos().y())
            elif self._hit == Hit.Bottom:
                rc.setBottom(event.pos().y())
            elif self._hit == Hit.Left:
                rc.setLeft(event.pos().x())
            elif self._hit == Hit.Right:
                rc.setRight(event.pos().x())
            elif self._hit == Hit.TopRight:
                rc.setTopRight(event.pos())
            elif self._hit == Hit.BottomRight:
                rc.setBottomRight(event.pos())
            elif self._hit == Hit.BottomLeft:
                rc.setBottomLeft(event.pos())
            elif self._hit == Hit.TopLeft:
                rc.setTopLeft(event.pos())

            self.imageRoi = trf.mapRect(rc)
            self.widget.update()
        elif event.type() == QEvent.MouseMove:
            # mouse move without button pressed
            hitnew = self._hitTest(self.itemRoi, event.pos())
            if self._hit != hitnew:
                if hitnew == Hit.Top or hitnew == Hit.Bottom:
                    cursor = Qt.SizeVerCursor
                elif hitnew == Hit.Left or hitnew == Hit.Right:
                    cursor = Qt.SizeHorCursor
                elif hitnew == Hit.TopRight or hitnew == Hit.BottomLeft:
                    cursor = Qt.SizeBDiagCursor
                elif hitnew == Hit.BottomRight or hitnew == Hit.TopLeft:
                    cursor = Qt.SizeFDiagCursor
                elif hitnew == Hit.Center:
                    cursor = Qt.OpenHandCursor
                else:
                    cursor = Qt.ArrowCursor
                self.widget.setCursor(cursor)
            self._hit = hitnew
        elif event.type() == QEvent.MouseButtonRelease:
            processed = True
            if self._hit == Hit.Center:
                self.widget.setCursor(Qt.OpenHandCursor)
        return processed

    def render(self, painter):
        if self.active:
            painter.setPen(QPen(Qt.white, 3))
            painter.drawRect(self.itemRoi)

    def enter(self):
        self.active = True

    def leave(self):
        self.active = False
        self.widget.setCursor(Qt.ArrowCursor)

    def _hitTest(self, rc: QRectF, mousePos: QPointF) -> Hit:
        maxdist = 4
        if not rc.adjusted(-maxdist, -maxdist, maxdist, maxdist).contains(mousePos):
            return Hit.NoHit

        def dist(p1, p2):
            return (p1 - p2).manhattanLength()

        if dist(rc.topLeft(), mousePos) < maxdist:
            return Hit.TopLeft
        elif dist(rc.topRight(), mousePos) < maxdist:
            return Hit.TopRight
        elif dist(rc.bottomRight(), mousePos) < maxdist:
            return Hit.BottomRight
        elif dist(rc.bottomLeft(), mousePos) < maxdist:
            return Hit.BottomLeft
        elif abs(rc.left() - mousePos.x()) < maxdist:
            return Hit.Left
        elif abs(rc.right() - mousePos.x()) < maxdist:
            return Hit.Right
        elif abs(rc.top() - mousePos.y()) < maxdist:
            return Hit.Top
        elif abs(rc.bottom() - mousePos.y()) < maxdist:
            return Hit.Bottom
        elif rc.contains(mousePos):
            return Hit.Center
        else:
            return Hit.NoHit


class ContOverlay(AbstractOverlay):
    '''Definie contour item
    '''
    def __init__(self, widget):
        super().__init__(widget)
        self.freehandDone = None
        # fill dummydata
        self.contour = QPolygonF()
        self.contour.append(QPointF(23, 24))
        self.contour.append(QPointF(50, 50))
        self.contour.append(QPointF(21, 76))
        self.freeHandPath = QPolygonF()
        self.curmouspos = QPoint()

    def handleEvent(self, event) -> bool:
        trf = self.invertedTransform()
        processed = False

        if event.type() == QEvent.MouseButtonPress:
            self.freeHandPath.clear()
            trfmpos = trf.map(event.pos())
            self.freeHandPath.append(trfmpos)
            processed = True
        elif event.type() == QEvent.MouseMove and event.buttons() & Qt.LeftButton:
            trfmpos = trf.map(event.pos())
            self.freeHandPath.append(trfmpos)
            processed = True
        elif event.type() == QEvent.MouseMove:
            # mouse move without button pressed
            self.curmouspos = event.pos()
            self.widget.update()
        elif event.type() == QEvent.MouseButtonRelease:
            processed = True
            if self.freehandDone:
                self.freehandDone(event.pos())
        if processed:
            self.widget.update()

        return processed

    def render(self, painter):
        if self.active:
            trf = self.transform()
            painter.setPen(QPen(Qt.white, 5))
            cont = trf.map(self.contour)
            painter.drawPolygon(cont)
            if len(self.freeHandPath) > 0:
                pen = QPen(QColor(255, 255, 255, 180), 22)
                pen.setCapStyle(Qt.RoundCap)
                pen.setJoinStyle(Qt.RoundJoin)
                painter.setPen(pen)
                fh = trf.map(self.freeHandPath)
                painter.drawPolyline(fh)
            else:
                # zeichnen einer kreis, zur suggestion
                painter.setPen(QPen(Qt.black, 1))
                painter.drawEllipse(self.curmouspos, 11, 11)

    def enter(self):
        self.freeHandPath.clear()
        self.active = True
        self.widget.update()

    def leave(self):
        self.freeHandPath.clear()
        self.active = False
        self.widget.update()
