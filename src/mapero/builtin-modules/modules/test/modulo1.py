from mapero.core.api import Module, OutputPort 

from enthought.traits.api import Range, Int, Str
from enthought.traits.ui.api import Group

class modulo1(Module):
    """  """
    
    __version__  = 0

    label     = "Module 1"
    
    param = Range(0,100)
    
    view = Group('param' )
    
    out1 = OutputPort( trait = Int )
    
    def __init__(self, **traits):
        super(modulo1, self).__init__(**traits)

    def _param_changed(self, value):
        self.out1.data = value
        if value == 50:
            self.out1.data = "error"
        self.progress = value

