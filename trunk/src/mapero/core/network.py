from mapero.core.connection import Connection
from mapero.core.module import Module
from enthought.traits import api as traits

class RepeatedModuleIDInNetworkError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class Network(Module):
	""" Network Class """

	modules = traits.List(Module)
	connections = traits.List(Connection)

	_max_module_id = traits.Int(0)
	_max_connection_id = traits.Int(0)
	updated = traits.Event

	def __init__(self, **traits):
		super(Network, self).__init__(**traits)
		
	def __set_pure_state__(self, state):
		self.modules = state.modules
		self.connections = state.connections
	
	def _modules_items_changed(self, event):
		module_ids = [module.id for module in self.modules]
		for module in event.added:
			traits = module.class_trait_names()
			if module.id == None:
				self._max_module_id = self._max_module_id + 1
				module.id = self._max_module_id
			else:
				other_modules = [mod for mod in self.modules if mod != module]
				id_modules_dict = dict([(mod.id, mod) for mod in other_modules])
				print other_modules
				sorted_ids = id_modules_dict.keys()
				sorted_ids.sort()
				for id in sorted_ids:
					if id >= module.id:
						id_modules_dict[id].id = id+1
				self._max_module_id = max(max(module_ids), module.id)

			for attr in ('progress', 'id'):
				traits.remove(attr)
			for trait in traits:
				module.on_trait_change(self._module_attr_changed, trait)
				
		if len(event.removed)>0 :
			i=0;
			for module in self.modules : 
				i = i+1
				module.id = i
			self._max_module_id = i
			
		self.updated = True
		
	def _connections_items_changed(self, event):
		for connection in event.added:
			self._max_connection_id = self._max_connection_id + 1
			connection.id = self._max_connection_id
			
		for connection in event.removed:
			connection.input_port.connection = None
			connection.output_port.connections.remove(connection)
			connection.data = None
	
		if len(event.removed)>0 :
			i=0;
			for connection in self.connections : 
				i = i+1
				connection.id = i
			self._max_connection_id = i
			
		self.updated = True
		
	def _module_attr_changed(self, module):
		self.updated = True
		