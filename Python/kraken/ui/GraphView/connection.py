
#
# Copyright 2010-2015
#

#pylint: disable-msg=W0613

from PySide import QtGui, QtCore

from mouse_grabber import MouseGrabber

class Connection(QtGui.QGraphicsPathItem):
    __defaultPen = QtGui.QPen(QtGui.QColor(168, 134, 3), 2.0)

    def __init__(self, graph, srcPort, dstPort):
        super(Connection, self).__init__(graph.itemGroup())

        self.__graph = graph
        self.__srcPort = srcPort
        self.__dstPort = dstPort
        self.__defaultPen = QtGui.QPen(self.__srcPort.getColor(), 2.0)
        self.__hoverPen = QtGui.QPen(QtCore.Qt.SolidLine)
        self.__hoverPen.setWidth(2.5)
        self.__hoverPen.setColor(self.__srcPort.getColor().lighter())

        self.setPen(self.__defaultPen)
        self.setZValue(-1)
        # self.setAcceptHoverEvents(True)

    def getSrcPort(self):
        return self.__srcPort

    def getDstPort(self):
        return self.__dstPort

    def setPortConnection(self, port):
        port.addConnection(self)

    def boundingRect(self):
        srcPoint = self.mapFromScene(self.__srcPort.outCircle().centerInSceneCoords())
        dstPoint = self.mapFromScene(self.__dstPort.inCircle().centerInSceneCoords())
        penWidth = self.__defaultPen.width()

        return QtCore.QRectF(
            min(srcPoint.x(), dstPoint.x()),
            min(srcPoint.y(), dstPoint.y()),
            abs(dstPoint.x() - srcPoint.x()),
            abs(dstPoint.y() - srcPoint.y()),
            ).adjusted(-penWidth/2, -penWidth/2, +penWidth/2, +penWidth/2)

    def paint(self, painter, option, widget):
        srcPoint = self.mapFromScene(self.__srcPort.outCircle().centerInSceneCoords())
        dstPoint = self.mapFromScene(self.__dstPort.inCircle().centerInSceneCoords())

        dist_between = dstPoint - srcPoint

        self.__path = QtGui.QPainterPath()
        self.__path.moveTo(srcPoint)
        self.__path.cubicTo(
            srcPoint + QtCore.QPointF(dist_between.x() * 0.4, 0),
            dstPoint - QtCore.QPointF(dist_between.x() * 0.4, 0),
            dstPoint
            )
        self.setPath(self.__path)
        self.prepareGeometryChange()
        super(Connection, self).paint(painter, option, widget)


    # def hoverEnterEvent(self, event):
    #     self.setPen(self.__hoverPen)
    #     super(Connection, self).hoverEnterEvent(event)

    # def hoverLeaveEvent(self, event):
    #     self.setPen(self.__defaultPen)
    #     super(Connection, self).hoverLeaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() is QtCore.Qt.MouseButton.LeftButton:
            self.__dragging = True
            self._lastDragPoint = self.mapToItem(self.__graph.itemGroup(), event.pos())
            event.accept()
        else:
            super(Connection, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.__dragging:
            pos = self.mapToItem(self.__graph.itemGroup(), event.pos())
            delta = pos - self._lastDragPoint
            if delta.x() < 0 or delta.x() > 0:

                sourceComponent = self.__srcPort.getNode().getComponent()
                targetComponent = self.__dstPort.getNode().getComponent()

                sourceComponentOutputPort = sourceComponent.getOutputByName(self.__srcPort.getName())
                targetComponentInputPort = targetComponent.getInputByName(self.__dstPort.getName())
                targetComponentInputPort.removeConnection()
                
                if delta.x() < 0:
                    MouseGrabber(self.__graph, pos, self.__srcPort, 'In')
                else:
                    MouseGrabber(self.__graph, pos, self.__dstPort, 'Out')

                # destory the connection as the MouseGrabber creates a new one
                self.destroy()

        else:
            super(Connection, self).mouseMoveEvent(event)


    def destroy(self):

        srcPort = self.getSrcPort()
        dstPort = self.getDstPort()

        srcPort.removeConnection(self)
        dstPort.removeConnection(self)

        self.scene().removeItem(self)
