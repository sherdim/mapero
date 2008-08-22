# Author: Zacarias F. Ojeda <correo@zojeda.com.ar>
# License: new BSD.


from enthought.traits.api import HasTraits, Instance, Any, Int, Bool 
from enthought.traits.ui.api import View, Item, Group
from mapero.core.port_instance import InputPortInstance, OutputPortInstance


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
	input_port = Instance(InputPortInstance)
	output_port = Instance(OutputPortInstance)
	data = Any( trancient = True)
	enabled = Bool
	

	def __init__(self, **traits):
		super(Connection, self).__init__(**traits)
		if self.input_port.data_type.is_compatible_with(self.output_port.data_type):
			self.output_port.connections.append(self)
			self.input_port.connection = self
		else:
			raise ModuleConnectionError(" incompatible types ")

	def _input_port_changed(self, value):
		if (value.connection != None):
			raise ModuleConnectionError("the input port only accept one connection")
		else:
			self.enabled = True

	def __get_pure_state__(self):
		"""Method used by the state_pickler.
		"""
		d = self.__dict__.copy()
		for attr in ('data',):
			d.pop(attr, None)
		return d

		
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


