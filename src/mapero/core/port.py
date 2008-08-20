#!/usr/bin/env python
"""port.py
"""
# Author: Zacarias F. Ojeda <zojeda@gmail.com>
# Copyright (c) 2005, Enthought, Inc.
# License: new BSD Style.

# Standard library imports.
import re

from enthought.traits.api import Str, Trait, HasTraits, Any, List, WeakRef

import logging
log = logging.getLogger("mapero.logger.engine");
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
	data_type = Any
	name = Str
	data = Any
	connection = Any
	module = WeakRef(klass = 'mapero.core.module.Module')
	#FIXME: debiera ser module = Instance(Module) pero no funciona :(

	def __get_pure_state__(self):
		"""Method used by the state_pickler.
		"""
		d = self.__dict__.copy()
		for attr in ('data', 'data_type', 'type'):
			d.pop(attr, None)
		return d


	def __del__(self):
		log.debug( "   port: "+ self.name + " deleted !!!" )
		pass

class OutputPort(Port):
	connections = List(WeakRef)

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

	def __del__(self):
		pass

	def update_data(self, old, new):
		log.debug( "updating module: " + self.module.name)
		self.module.update_module(self, old, new)

	def _data_changed (self, old, new):
		self.module.update_module(self, old, new)

class MultiInputPort(InputPort):
	base_name = Str

	#TODO: fix the automatic naming port system
	def _connection_changed(self, connection):
		pattern = re.compile(r'^(\D+)(\d*)$')
		print self.name
		try:
			complete_name = pattern.search(self.name).groups()
			base_name = complete_name[0]
			port_number = str(int(complete_name[1]) + 1)
			new_port = MultiInputPort(data_type = self.data_type,
									  name = base_name + port_number,
									  module = self.module)
			self.module.input_ports.append(new_port)
		except AttributeError:
			raise PortNameError("port's name don't follow the naming rules")




