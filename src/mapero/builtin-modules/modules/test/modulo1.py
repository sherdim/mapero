from mapero.core.module import Module
from mapero.core.port import OutputPort
from enthought.traits import api as traits
from enthought.traits.ui.api import Group

class modulo1(Module):
    """  """
    param = traits.Range(0,100)
    
    view = Group('param' )
    
    out1 = OutputPort(data_types = None)
    
    def __init__(self, **traits):
        super(modulo1, self).__init__(**traits)

    def _param_changed(self, value):
        self.out1.data = value
        self.progress = value

