from mapero.core.connection import Connection
from mapero.core.module import Module
from enthought.traits.api import HasTraits, List, Event

class Network(HasTraits):
	""" Network Class """

	modules = List(Module)
	connections = List(Connection)

	updated = Event

	def __init__(self, **traits):
		super(Network, self).__init__(**traits)
		
	def __set_pure_state__(self, state):
		self.modules = state.modules
		self.connections = state.connections
	
	def _modules_items_changed(self, event):
		for module in event.added:
			traits = module.class_trait_names()
			for attr in ('progress', 'id'):
				traits.remove(attr)
			for trait in traits:
				module.on_trait_change(self._module_attr_changed, trait)
	
	def _connections_items_changed(self, event):
		for connection in event.removed:
			connection.input_port.connection = None
			connection.output_port.connections.remove(connection)
			connection.data = None
	
	def _module_attr_changed(self, module):
		self.updated = True
		