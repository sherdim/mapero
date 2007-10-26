#!/usr/bin/env python
# Author: Zacarias F. Ojeda <correo@zojeda.com.ar>
# Copyright (c) 2005, Enthought, Inc.
# License: BSD Style.
from enthought.traits.traits import Property
from enthought.traits.traits import Any
from enthought.traits.traits import WeakRef
from enthought.traits.traits import Bool

from enthought.traits.api import Instance, HasTraits

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
	input_port = Instance(InputPort())
	output_port = Instance(OutputPort())
	data = Any
	enable = Property(Bool)

	def __init__(self, **traits):
		super(Connection, self).__init__(**traits)
		self.input_port.connection = self
		self.output_port.connections.append(self)
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

	def 	_set_enable(self, value):
		if (value != self.enable):
			if (value == True):
				if (self.input_port != None) and (self.output_port != None):
					self.input_port.data = self.output_port.data
			else:
				self.input_port.data = None

	def _get_enable(self):
		pass

	def __del__(self):
		self.enable = False
		self.input_port.connection = None
		self.output_port.connections.remove(self)


