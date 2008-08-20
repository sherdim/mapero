# Author: Zacarias F. Ojeda <correo@zojeda.com.ar>
# License: new BSD.

from enthought.traits.api import HasTraits, Instance, Property, Any, Int, Bool 
from enthought.traits.ui.api import View, Item, Group

from mapero.core.port import OutputPort, InputPort




# Standard library imports.

class ModuleConnectionError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)


######################################################################
# `Conection` class.
######################################################################
class Connection(HasTraits):
	id = Int
	input_port = Instance(InputPort)
	output_port = Instance(OutputPort)
	data = Any
	enabled = Property(Bool)
	
	_enabled = True

	def __init__(self, **traits):
		super(Connection, self).__init__(**traits)
		if self.input_port.data_type.is_compatible_with(self.output_port.data_type):
			self.output_port.connections.append(self)
			self.input_port.connection = self
			self.enabled = True
		else:
			raise ModuleConnectionError(" incompatible types ")

	def update_data(self):
		self.input_port.update_data(self.data, self.data)

	def _input_port_changed(self, value):
		if (value.connection != None):
			raise ModuleConnectionError("the input port only accept one connection")
		else:
			self.enabled = True

	def _data_changed(self, old, new):
		self.input_port.data = self.data

	def _set_enabled(self, value):
		if (value != self.enabled):
			if (value == True):
				if (self.input_port != None) and (self.output_port != None):
					self.data = self.output_port.data
			else:
				self.data = None
			self._enabled = value

	def _get_enabled(self):
		return self._enabled
	
	def __get_pure_state__(self):
		"""Method used by the state_pickler.
		"""
		d = self.__dict__.copy()
		for attr in ('data',):
			d.pop(attr, None)
		return d

	def __del__(self):
		self.enabled = False
		self.input_port.connection = None
		self.output_port.connections.remove(self)
		
	view = View(
			    Group(
					  Item( name = "enabled"),
					  Group(
						    Item( name = "data", style = 'readonly', enabled_when='enabled', show_label=False),
						    label = 'Data'
						    ),
					  label='Connection', springy=True,
					  )
			    )    	


