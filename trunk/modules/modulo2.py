from core.module import Module
from core.port import OutputPort, InputPort
from enthought.traits.api import Range, Int
from enthought.traits.ui.api import View, Group


import types

module_info = {
	'name': 'test.modulo2',
	'desc': "Module with a InputPort with test purpose"
}

class modulo2(Module):
	""" modulo de prueba dos """
	entrada = Int(0)
	view = Group('entrada')
	def __init__(self, **traits):
		super(modulo2, self).__init__(**traits)
		self.name = 'modulo2'
		self.input_ports.append(InputPort(types.IntType, 'entrada1', self))
		self.input_ports.append(InputPort(types.IntType, 'entrada2', self))

	def update(self, input_port, old, new):
		self.input_data = input_port.data
		print "entrada desde: ", input_port.name
		self.process()

	def _process(self):
		self.progress = self. input_data
