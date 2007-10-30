from enthought.traits import api as traits

class ModuleGeometrics(traits.HasTraits):
    x=traits.Float()
    y=traits.Float()
    w=traits.Float()
    h=traits.Float()
    module_id = traits.Int
    
    def __init__(self, **traits):
        super(ModuleGeometrics, self).__init__(**traits)