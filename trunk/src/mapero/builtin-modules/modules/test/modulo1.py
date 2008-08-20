from mapero.core.module import Module
from mapero.core.port import OutputPort
from enthought.traits.api import Range, Int, Str
from enthought.traits.ui.api import Group

class modulo1(Module):
    """  """
    
    __version__  = 0
    __name__     = "Module1 "
    
    param = Range(0,100)
    
    view = Group('param' )
    
    out1 = OutputPort( data_type = Int )
    
    def __init__(self, **traits):
        super(modulo1, self).__init__(**traits)

    def _param_changed(self, value):
        self.out1.data = value
        self.progress = value

