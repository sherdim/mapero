import wx
import wx.lib.ogl as ogl
from wx.lib.ogl._oglmisc import CONTROL_POINT_ENDPOINT_TO, CONTROL_POINT_SIZE, CONTROL_POINT_LINE, CONTROL_POINT_ENDPOINT_FROM, ARROW_ARROW


DRAW_CONTROL_POINT_SIZE = 3

class ConnectionControlPoint(ogl.LineControlPoint):
	def __init__(self, theCanvas = None, object = None, size = 0.0, x = 0.0, y = 0.0, the_type = 0):
		ogl.LineControlPoint.__init__(self, theCanvas, object, size, x, y, the_type)

	def OnDraw(self, dc):
		if self._type == CONTROL_POINT_ENDPOINT_FROM or self._type == CONTROL_POINT_ENDPOINT_TO:
			pass
		else:
			dc.DrawEllipse(self._xpos - self.GetWidth() / 2.0,
		self._ypos - self.GetHeight() / 2.0,
		self.GetWidth(), self.GetHeight())


class ConnectionShape(ogl.LineShape):

	def __init__(self, connection = None):
		ogl.LineShape.__init__(self)
		self.MakeLineControlPoints(2)
		self.AddArrow(ARROW_ARROW)
		self.MakeControlPoints()
		self.connection = connection


	def OnLeftDoubleClick(self, x, y, keys = 0, attachment = 0):
		"""
		The dragging is done here.
		"""
		shape = self.GetShape()
		canvas = shape.GetCanvas()
		dc = wx.ClientDC(canvas)
		canvas.PrepareDC(dc)

		shape.InsertLineControlPoint(dc, [x, y])
		shape.DeleteControlPoints()
		shape.MakeControlPoints()
		canvas.Redraw(dc)

	def MakeControlPoints(self):
		 """Make handle control points."""
		 if self._canvas and self._lineControlPoints:
			first = self._lineControlPoints[0]
			last = self._lineControlPoints[-1]


			control = ConnectionControlPoint(self._canvas, self, 0, first[0], first[1], CONTROL_POINT_ENDPOINT_FROM)
			control._point = first
			self._canvas.AddShape(control)
	 		control.SetCanvas(self._canvas)
			self._controlPoints.append(control)

			for point in self._lineControlPoints[1:-1]:
				 control = ConnectionControlPoint(self._canvas, self, DRAW_CONTROL_POINT_SIZE, point[0], point[1], CONTROL_POINT_LINE)
				 control._point = point
				 self._canvas.AddShape(control)
				 self._controlPoints.append(control)

				 control = ConnectionControlPoint(self._canvas, self, CONTROL_POINT_SIZE, last[0], last[1], CONTROL_POINT_ENDPOINT_TO)
				 control._point = last
				 self._canvas.AddShape(control)
				 self._controlPoints.append(control)

	def InsertLineControlPoint(self, dc = None, point = None):
		"""Insert a control point at an optional given position."""
		if dc:
			self.Erase(dc)
		if point:
			x, y = point
		pos = 0
		if self.HitTest(x, y):
			for i in range(len(self._lineControlPoints) - 1):
				point1 = self._lineControlPoints[i]
				point2 = self._lineControlPoints[i + 1]

				xmin = min(point1[0], point2[0])
				xmax = max(point1[0], point2[0])
				ymin = min(point1[1], point2[1])
				ymax = max(point1[1], point2[1])

				if (x >= xmin) and (x <= xmax) and (y >= ymin) and (y <= ymax):
					pos = i
				else:
					ogl.LineShape.InsertLineControlPoint(dc, point)

					point = wx.RealPoint(x, y)
					self._lineControlPoints.insert(pos+1, point)

		else:
			ogl.LineShape.InsertLineControlPoint(dc, point)

	def SetGeometrics(self, geometrics):
	    print "geometrics: ", geometrics

