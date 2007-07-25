#!/usr/bin/env python
"""port.py
"""
# Author: Zacarias F. Ojeda <correo@zojeda.com.ar>
# Copyright (c) 2005, Enthought, Inc.
# License: BSD Style.

# Standard library imports.
import re

from enthought.traits.api import Str, Trait, HasTraits, Any, List, WeakRef

######################################################################
# `Port` class.
######################################################################
class PortNameError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class Port(HasTraits):
	#TODO: hacer comprobacion de los tipos cuando cambia data
	#TODO:
	data_type = Trait
	name = Str
	data =Any
	connection = Any
	#FIXME: debiera ser module = Instance(Module) pero no funciona :(

	def __init__(self, data_type, name, module):
		self.type = type
		self.data_type = data_type
		self.module = module
		self.name = name

	def __get_pure_state__(self):
		"""Method used by the state_pickler.
		"""
		d = self.__dict__.copy()
		for attr in ('data', 'module'):
			d.pop(attr, None)
		return d


	def __del__(self):
		print "   port: ", self.name, " deleted !!!"
		pass

class OutputPort(Port):
	connections = List(WeakRef)

	def __init__(self, data_type, name, module):
		super(OutputPort, self).__init__(data_type, name, module)

	def __del__(self):
		pass

	def update_data(self):
		for connection in self.connections:
			connection.update_data()


	def _data_changed (self):
		for connection in self.connections:
			connection.data = self.data   #TODO: ver si no es mejor hacer una referencia weak

class InputPort(Port):
	connection = Any

	def __init__(self, data_type, name, module):
		super(InputPort, self).__init__(data_type, name, module)

	def __del__(self):
		pass

	def update_data(self, old, new):
		print "updating module: ",self.module.name
		self.module.update_module(self, old, new)

	def _data_changed (self, old, new):
		self.module.update_module(self, old, new)

class MultiInputPort(InputPort):
	base_name = Str

	def __init__(self, data_type, name, module):
		super(InputPort, self).__init__(data_type, name, module)

	#TODO: fix the automatic naming port system
	def _set_output_port(self, output_port):
		super(MultiInputPort, self)._set_output_port(output_port)
		pattern = re.compile(r'^(\D+)(\d*)$')
		print self.name
		try:
			complete_name = pattern.search(self.name).groups()
			base_name = complete_name[0]
			port_number = str(int(complete_name[1]) + 1)
			self.module.input_ports.append(MultiInputPort(self.type, base_name + port_number, self.module))
		except AttributeError:
			raise PortNameError("port's name don't follow the naming rules")




