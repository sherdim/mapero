from core.module import Module
from core.port import OutputPort, InputPort
from enthought.traits.api import Range, Int
from enthought.traits.ui.api import View, Group

import types

module_info = {'name': 'otra.modulo1',
	       'desc': "Module with a OutputPort with test purpose"}

class modulo1(Module):
    """ modulo de prueba uno """
    p = Range(0,100)
    view = Group('p')
    def __init__(self, **traits):
	super(Module, self).__init__(**traits)
	self.name = 'modulo1'
	self.output_ports.append(OutputPort(types.IntType, 'salida1', self))
	
    def _parametro_changed(self):
	self.get_output('salida1').data = self.p


