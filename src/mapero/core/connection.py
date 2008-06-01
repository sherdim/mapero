#!/usr/bin/env python
# Author: Zacarias F. Ojeda <correo@zojeda.com.ar>
# License: new BSD.

from enthought.traits import api as traits

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
class Connection(traits.HasTraits):
	id = traits.Int
	input_port = traits.Instance(InputPort())
	output_port = traits.Instance(OutputPort())
	data = traits.Any
	enable = traits.Property(traits.Bool)

	def __init__(self, **traits):
		super(Connection, self).__init__(**traits)
		self.output_port.connections.append(self)
		self.input_port.connection = self
		self.enable = True

	def update_data(self):
		self.input_port.update_data(self.data, self.data)

	def _input_port_changed(self, value):
		if (value.connection != None):
			raise ModuleConnectionError("the input port only accept one connection")
		else:
			self.enable = True

	def _data_changed(self, old, new):
		self.input_port.data = self.data

	def _set_enable(self, value):
		if (value != self.enable):
			if (value == True):
				if (self.input_port != None) and (self.output_port != None):
					self.data = self.output_port.data
			else:
				self.data = None

	def _get_enable(self):
		pass
	
	def __get_pure_state__(self):
		"""Method used by the state_pickler.
		"""
		d = self.__dict__.copy()
		for attr in ('data',):
			d.pop(attr, None)
		return d

	def __del__(self):
		self.enable = False
		self.input_port.connection = None
		self.output_port.connections.remove(self)


