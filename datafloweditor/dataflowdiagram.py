from mapero.datafloweditor.connectionshape import ConnectionShape
import wx
import wx.lib.ogl as ogl

from mapero.datafloweditor.moduleshape import PortShape, ModuleShape
from mapero.datafloweditor.modulegui import ModuleGUI
from mapero.datafloweditor.connectiongui import ConnectionGUI
from xml.dom.minidom import Document, parse

class ModuleNameDropTarget(wx.TextDropTarget):
	def __init__(self, parent):
		wx.TextDropTarget.__init__(self)
		self.parent = parent

	def OnDropText(self, x, y, data):
		print data
		self.parent.add_module(x, y, data.strip())

class DataflowDiagram(ogl.Diagram):
	def __init__(self, parent, module_manager=None, prop_editor=None, view=None):
		ogl.Diagram.__init__(self)
		canvas = ogl.ShapeCanvas(parent)
		self.SetCanvas(canvas)
		canvas.SetDiagram(self)
		canvas.SetBackgroundColour(wx.Colour(233,221,175))
		canvas.SetDropTarget(ModuleNameDropTarget(self))
		self.view = view


		canvas.SetScrollbars(20,20,2000,1000,0,0,True)
		self.ui_selected = None

		self.prop_editor = prop_editor

		self.module_shapes= []
		self.connection_shapes = []
		self.from_here = False
		self.module_selected = None

	def move_module(self, module, mx, my):
		self.view.move_module(module, mx, my)

	def get_port_shape(self, port):
		for module_gui in self.modules_gui:
			for input_port_shape in module_gui.module_shape.input_port_shapes:
				if port == input_port_shape.port:
					return input_port_shape
		for output_port_shape in module_gui.module_shape.output_port_shapes:
				if port == output_port_shape.port:
					return output_port_shape

	def get_module_shape(self, module):
		for module_shape in self.module_shapes:
			if module_shape.module == module:
				return module_shape
		return None

	def get_connection_shape(self, connection):
		for connection_shape in self.connection_shapes:
			if connection_shape.connection == connection:
				return connection_shape
		return None



	def add_module(self, x, y, module_name):
		self.view.add_module(module_name, x, y)

	def add_module_shape(self, module, geometrics):
		module_shape = ModuleShape(module)
		module_shape.SetCanvas(self.GetCanvas())
		module_shape.Show(True)
		self.AddShape(module_shape)
		self.module_shapes.append(module_shape)
		module_shape.SetGeometrics(geometrics)

	def add_connection_shape(self, connection):
		connection_shape = ConnectionShape(connection)
		connection_shape.SetCanvas(self.GetCanvas())

		module_shape_to = self.get_module_shape(connection.input_port.module)
		module_shape_from = self.get_module_shape(connection.output_port.module)

		attach_to = module_shape_to.get_port_attachment(connection.input_port)
		attach_from = module_shape_from.get_port_attachment(connection.output_port)

		module_shape_from.AddLine(connection_shape, module_shape_to, attach_from, attach_to)

		self.connection_shapes.append(connection_shape)
		self.AddShape(connection_shape)
		connection_shape.Show(True)

		self.GetCanvas().Refresh()

	def remove_module(self, module):
		module_gui = self.get_module_gui(module)
		module_gui.module_shape.Delete()
		self.modules_gui.remove(module_gui)
		self.Refresh()

	def new_connection(self, x0, y0, x1, y1):
		port_shape_from = self.GetCanvas().FindShape(x0, y0)[0]
		port_shape_to = self.GetCanvas().FindShape(x1, y1)[0]
		if isinstance(port_shape_from, PortShape) and isinstance(port_shape_to, PortShape) \
			and (port_shape_from.isoutput) and not(port_shape_to.isoutput):
			    self.view.new_connection( \
						    port_shape_from.port.module, port_shape_from.port,
			    port_shape_to.port.module, port_shape_to.port)

	def disconnect(self, module_from, port_name_from, module_to, port_name_to):
		self.Refresh()

	def edit_module(self, module):
		self.select_module(module)

	def select_module(self, module):
#		if self.ui_selected:
#			self.ui_selected.dispose()
		self.module_selected = module
		for module_shape in self.module_shapes:
			if module_shape.module == module:
				module_shape.Select(True)
			else:
				module_shape.Select(False)

		if self.module_selected:
			self.ui_selected = module.edit_traits(parent=self.prop_editor, kind='subpanel')
			box = wx.BoxSizer( wx.VERTICAL )
			box.Add( self.ui_selected.control, 0, wx.ALL | wx.EXPAND )

#			self.prop_editor.SetSizer( box )
#			self.prop_editor.SetScrollRate(10,10)
#			self.prop_editor.CenterOnParent( wx.BOTH )


			self.GetCanvas().Refresh()
