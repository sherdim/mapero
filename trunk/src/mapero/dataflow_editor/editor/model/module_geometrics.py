from enthought.traits import api as traits
from mapero.core.module import Module

class ModuleGeometrics(traits.HasTraits):
    x=traits.Float()
    y=traits.Float()
    w=traits.Float()
    h=traits.Float()
    module = traits.WeakRef(Module)
    
    def __init__(self, **traits):
        super(ModuleGeometrics, self).__init__(**traits)