from mapero.core.module import Module
from mapero.core.port import OutputPort
from mapero.core.port import InputPort
from enthought.traits.api import Range, Int
from enthought.traits.ui.api import View, Group

import types

module_info = {
	'name': 'test.modulo1',
	'desc': "Module with a OutputPort with test purpose"
}

class modulo1(Module):
	""" modulo de prueba uno """
	parametro = Range(0,100)
	caca = Range(0,100)

	def start(self):
		self.name = 'modulo1'
		self.output_ports.append(OutputPort(types.IntType, 'salida1',self))
		self.get_output('salida1').data = 0

	def _parametro_changed(self):
		self.get_output('salida1').data = self.parametro

	#view = Group('parametro', 'caca')
	view = Group('parametro')




