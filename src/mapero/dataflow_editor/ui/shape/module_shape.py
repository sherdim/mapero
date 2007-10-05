import wx
import wx.lib.ogl as ogl
from wx.lib.ogl._oglmisc import ATTACHMENT_MODE_EDGE, SHADOW_RIGHT
from connection_shape import ConnectionShape

import logging
log = logging.getLogger("mapero.logger.diagram");

class AttachmentPoint(object):
	def __init__(self, id = 0, x = 0, y = 0):
		self._id = id
		self._x = x
		self._y = y

class PortShape(ogl.PolygonShape):
	def __init__(self, port, isoutput=True, ishorizontal=True):
		ogl.PolygonShape.__init__(self)
		self.port = port
		self.tmp_connection = None
		self.flechita = False
		self.isoutput = isoutput
		self.ishorizontal = ishorizontal

		if isoutput and ishorizontal:
			points = [(-5,-2), (-5,3), (1,3), (6,6), (6,-5), (1,-2)]
		elif not isoutput and ishorizontal:
			points = [(-5,-5), (-5,6), (-1,3), (6,3), (6,-2), (-1,-2)]
		self.Create(points)
		self.CalculateBoundingBox()


	def OnDragLeft(self, draw, x, y, keys = 0, attachment = 0):
		if self.isoutput:
			if self.flechita:
				x0, y0, x1, y1 = self.tmp_connection.GetEnds()
				canvas = self.GetShape().GetCanvas()
				self.tmp_connection.SetEnds(x0,y0,x,y)
				canvas.Refresh()
			else:
				if self._previousHandler:
					self._previousHandler.OnDragLeft(draw, x, y, keys, attachment)

	def OnBeginDragLeft(self, x, y, keys = 0, attachment = 0):
		if self.isoutput:
			self.tmp_connection = ConnectionShape()
			shape = self.GetShape()
			canvas = shape.GetCanvas()
			x0=self.GetX()
			y0=self.GetY()
			self.tmp_connection.SetEnds(x0,y0,x0,y0)
			self.tmp_connection.AddToCanvas(canvas)
			self.tmp_connection.Show(True)
			self.flechita = True


	def OnEndDragLeft(self, x, y, keys = 0, attachment = 0):
		if self.isoutput:
			if self.flechita:
				self.tmp_connection.Delete()
				self.tmp_connection = None
				self.flechita = False
				self.GetCanvas().GetDiagram().new_connection(self.GetX(), self.GetY(), x, y)
			else:
				if self._previousHandler:
					self._previousHandler.OnEndDragLeft(x, y, keys, attachment)

class ModuleShape(ogl.RectangleShape):
	def __init__(self, module, w = 151, h = 91, x = 100, y = 50):
		ogl.RectangleShape.__init__(self, w, h)
		self.module = module
		self.SetCornerRadius(10)
		self._attachmentMode = ATTACHMENT_MODE_EDGE
		self.SetShadowMode(SHADOW_RIGHT, True)
		self._shadowOffsetX = 3
		self._shadowOffsetY = 3
		self.SetBrush(wx.Brush(wx.Colour(243,250,167), wx.SOLID))
		self.input_port_shapes = []
		self.output_port_shapes = []
		self.p_width = 11
		
		log.debug("creating module shape for module : %s" % module)

		self.SetX(x)
		self.SetY(y)

	def UpdateModule(self, module):
		for child in self._children:
			child.Delete()
		self._children = []
		self.input_port_shapes = []
		self.output_port_shapes = []
		self.ClearAttachments()
		self.module = module

		for input_port in self.module.input_ports:
				port_shape = PortShape(input_port, False)
				port_shape.AddToCanvas(self.GetCanvas())
				port_shape.Show(True)
				self.input_port_shapes.append(port_shape)
				self._children.append(port_shape)

		for output_port in self.module.output_ports:
				port_shape = PortShape(output_port, True)
				port_shape.AddToCanvas(self.GetCanvas())
				port_shape.Show(True)
				self.output_port_shapes.append(port_shape)
				self._children.append(port_shape)

		self.update_port_positions()
		self.GetCanvas().Refresh()
		log.debug( " updating module_shape " )

	def get_port_attachment(self, port):
		attach_id = 0
		for input_port_shape in self.input_port_shapes:
			if input_port_shape.port == port:
				return attach_id
			else:
				attach_id += 1
		for output_port_shape in self.output_port_shapes:
			if output_port_shape.port == port:
				return attach_id
			else:
				attach_id += 1


	def update_port_positions(self):
		self.ClearAttachments()
		self.p_width = 11;
		y1 = self.GetY() - self.GetHeight() / 2.0

		y = y1
		yinrate = self.GetHeight() / (len(self.input_port_shapes) + 1)
		attach_id = 0
		for input in self.input_port_shapes:
			y += yinrate
			self.p_width, p_height = input.GetBoundingBoxMin()
			x1 = self.GetX() - self.GetWidth() / 2.0 + self.p_width / 2.0 -1
			xport = x1
			yport = y - p_height / 2.0
			input.SetX(xport)
			input.SetY(yport)
			self._attachmentPoints.append(AttachmentPoint(attach_id, xport - self.GetX(), yport - self.GetY() ))
			attach_id += 1

		y = y1
		youtrate = self.GetHeight() / (len(self.output_port_shapes) + 1)
		for output in self.output_port_shapes:
			y += youtrate
			self.p_width, p_height = output.GetBoundingBoxMin()
			x1 = self.GetX() + self.GetWidth() / 2.0 - self.p_width / 2.0 - 1
			xport = x1
			yport = y - p_height / 2.0
			output.SetX(xport)
			output.SetY(yport)
			self._attachmentPoints.append(AttachmentPoint(attach_id, xport - self.GetX(), yport - self.GetY() ))
			attach_id += 1


	def OnMovePost(self, dc, x, y, old_x, old_y, display):
		self.GetCanvas().GetDiagram().move_module(self.module,  x - old_x, y - old_y)
		ogl.RectangleShape.OnMovePost(self, dc, x, y, old_x, old_y, display)


#	def OnLeftClick(self, x, y, keys, attachment):
#		self.GetCanvas().GetDiagram().edit_module(self.module)

	def OnDraw(self, dc):
		ogl.RectangleShape.OnDraw(self, dc)

		padding = 5
		y1 = self.GetY() - self.GetHeight() / 2.0

		y = y1

		if self.Selected():
			dc.SetBrush(wx.RED_BRUSH)
		else:
			dc.SetBrush(wx.BLACK_BRUSH)


		textw, texth = dc.GetTextExtent(self.module.label)
		dc.DrawText(self.module.label, self.GetX() + self._width / 2
			- self.p_width - padding - textw, self.GetY() - self._height / 2 + padding )
		dc.SetFont((wx.Font(6, wx.SWISS, wx.NORMAL, wx.NORMAL)))

		# Dibujado del progreso en el procesamiento
		xprogress = self.GetX() - self._width / 2 + self.p_width + padding
		progresswidth = self._width - 2*self.p_width - 2*padding
		progressText = 'Progress: '
		textw, texth = dc.GetTextExtent(progressText)
		dc.DrawText(progressText, xprogress, self.GetY() )
		y = self.GetY() + texth
		dc.SetBrush(wx.Brush(wx.LIGHT_GREY, wx.SOLID))
		dc.DrawRectangle(xprogress, y, progresswidth, texth)

		dc.SetBrush(wx.Brush(wx.Colour(16,198,140), wx.SOLID))
		dc.DrawRectangle(xprogress -1, y, (progresswidth*self.module.progress/100)-1, texth-1)

		self.update_port_positions()
		self.DrawLinks(dc)
	
	def SetGeometrics(self, geometrics):
		self.SetX(geometrics.x)
		self.SetY(geometrics.y)
		self.SetHeight(geometrics.h)
		self.SetWidth(geometrics.w)
		self.UpdateModule(self.module)

	def __del__(self):
		log.debug("removing module shape for module : %s" % self.module)
		
		self.input_port_shapes = []
		self.output_port_shapes = []
		
