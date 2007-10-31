from mapero.core.module import Module
from mapero.core.port import OutputPort
from enthought.traits import api as traits
from enthought.traits.ui.api import Group

class modulo1(Module):
    """ """
    param = traits.Range(100)
    
    view = Group('param')
    
    def __init__(self, **traits):
        super(modulo1, self).__init__(**traits)
        self.out1 = OutputPort(
                                   data_type = None,
                                   name = 'out1',
                                   module = self 
                               )
        self.output_ports.append(self.out1)
        
    def _param_changed(self, value):
        self.out1.data = value

