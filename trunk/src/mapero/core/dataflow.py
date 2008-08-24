# Author: Zacarias F. Ojeda <zojeda@gmail.com>
# License: new BSD Style.

from mapero.core.api import Connection
from mapero.core.api import Module
from mapero.core.api import IDataflowEngine

from mapero.core.dataflow_engine.simple_engine.simple_engine import SimpleEngine

from enthought.traits.api import Instance, List, Int, Event
from enthought.traits.has_traits import on_trait_change
from enthought.persistence import state_pickler

class RepeatedModuleIDInDataflowError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)
	
class ModuleNotFoundInDataflowError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class MoreThanOneModuleInDataflowWithTheSameIDError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class ConnectionNotFoundInDataflowError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)


class Dataflow(Module):
	""" Dataflow Class """

	modules = List(Module)
	connections = List(Connection)

	_max_module_id = Int(0)
	_max_connection_id = Int(0)

	updated = Event
	
	engine = Instance(IDataflowEngine, transient = True)

	def __init__(self, **traits):
		super(Dataflow, self).__init__(**traits)
		self.engine = SimpleEngine(dataflow = self)
		
		
	def execute(self):
		self.engine.execute()
		
	def get_module_by_label(self, module_label):
		for module in self.modules:
			if module.label == module_label:
				return module
		raise ModuleNotFoundInDataflowError(module_label)

	def get_module_by_id(self, module_id):
		for module in self.modules:
			if module.id == module_id:
				return module
		raise ModuleNotFoundInDataflowError(module_id)

	def get_connection_by_id(self, connection_id):
		for connection in self.Dataflow.connections:
			if connection.id == connection_id:
				return connection
		raise ConnectionNotFoundInDataflowError(connection_id)

	def get_module(self, module):
		if isinstance(module, str):
			return self.get_module_by_label(module)
		else:
			try: 
				self.modules.index(module)
				return module
			except:
				raise ModuleNotFoundInDataflowError(str(module))


	def disconnect_module(self, module):
		connections = [connection for connection in self.connections 
					   if connection.input_port.module == module
					    or connection.output_port.module == module]
		
		for connection in connections:
			self.connections.remove(connection)

	@on_trait_change('modules_items')
	def on_modules_items_change(self, event):
		module_ids = [module.id for module in self.modules]
		for module in event.removed:
			self.disconnect_module(module)
			
		for module in event.added:
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
				
		if len(event.removed)>0 :
			i=0;
			for module in self.modules : 
				i = i+1
				module.id = i
			self._max_module_id = i
			
		self.updated = True
		
	@on_trait_change('connections_items')
	def on_connections_items_change(self, event):
		for connection in event.added:
			if connection.input_port.module not in self.modules or \
			   connection.output_port.module not in self.modules:
				self.connections.remove(connection)
				raise ModuleNotFoundInDataflowError  
			self._max_connection_id = self._max_connection_id + 1
			connection.id = self._max_connection_id
			
		for connection in event.removed:
			connection.input_port.connection = None
			connection.output_port.connections.remove(connection)
	
		if len(event.removed)>0 :
			i=0;
			for connection in self.connections : 
				i = i+1
				connection.id = i
			self._max_connection_id = i
			
		self.updated = True
	
	def __set_pure_state__(self, state):
		for module_state in state.modules:
			module = state_pickler.create_instance(module_state)
			self.modules.append(module)
			state_pickler.set_state(module, module_state)

		for connection_state in state.connections:
			out_module = self.get_module_by_id(connection_state.output_port.module.id)
			in_module = self.get_module_by_id(connection_state.input_port.module.id)
			
			out_port = out_module.get_port(connection_state.output_port.name)
			in_port = in_module.get_port(connection_state.input_port.name)
			
			connection = Connection(output_port = out_port, input_port = in_port)
			connection.enabled = connection_state.enabled
			self.connections.append(connection)
			
