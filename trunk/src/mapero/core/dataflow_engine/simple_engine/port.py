"""port.py
"""
# Author: Zacarias F. Ojeda <zojeda@gmail.com>
# License: new BSD Style.

from enthought.traits.api import on_trait_change
from mapero.core.port_instance import InputPortInstance, OutputPortInstance

class SimpleOutputPort(OutputPortInstance):
	
	@on_trait_change('data')
	def on_data_change(self, data):
		for connection in self.connections:
			if connection.enabled:
				connection.data = data

class SimpleInputPort(InputPortInstance):
	
	@on_trait_change('data')
	def on_data_in_connection_change(self, data):
		self.module.execute()

#class MultiInputPort(SimpleInputPort):
#	base_name = Str
#
#	#TODO: fix the automatic naming port system
#	def _connection_changed(self, connection):
#		pattern = re.compile(r'^(\D+)(\d*)$')
#		print self.name
#		try:
#			complete_name = pattern.search(self.name).groups()
#			base_name = complete_name[0]
#			port_number = str(int(complete_name[1]) + 1)
#			new_port = MultiInputPort(data_type = self.data_type,
#									  name = base_name + port_number,
#									  module = self.module)
#			self.module.input_ports.append(new_port)
#		except AttributeError:
#			raise PortNameError("port's name don't follow the naming rules")




