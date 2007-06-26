from mapero.core.connection import Connection
from enthought.traits.api import Int, Instance, Trait, HasTraits, WeakRef, Str
from mapero.core.module import Module
from mapero.core.port import InputPort, OutputPort
from mapero.datafloweditor.connectionshape import ConnectionShape
import wx
import wx.lib.ogl as ogl

class ConnectionGUI(HasTraits):

	connection = Instance(Connection)

	def __init__(self, connection, panel, diagram):
		self.connection = connection
		self.connection_shape = ConnectionShape()
		self.panel = panel
		self.diagram = diagram

		self.diagram.AddShape(self.connection_shape)
		self.connection_shape.SetCanvas(self.diagram.GetCanvas())

		module_shape_to = self.diagram.get_module_shape(connection.input_port.module)
		module_shape_from = self.diagram.get_module_shape(connection.output_port.module)

		attach_to = module_shape_to.get_port_attachment(connection.input_port)
		attach_from = module_shape_from.get_port_attachment(connection.output_port)

		module_shape_from.AddLine(self.connection_shape, module_shape_to, attach_from, attach_to)

		self.connection_shape.Show(True)
		self.diagram.GetCanvas().Refresh()


	def __del__(self):
		self.diagram.RemoveShape(self.connection_shape)
		self.connection_shape.DeleteControlPoints()
		self.connection_shape.Delete()
		self.diagram.GetCanvas().Refresh()
		print "ConnectionGUI destruido"
