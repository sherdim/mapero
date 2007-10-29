from mapero.core.network import Network
from mapero.core.connection import Connection
from mapero.core.module import Module

from enthought.traits import api as traits



class Point2D(traits.HasTraits):
    x=traits.Int()
    y=traits.Int()
    
    def __init__(self, **traits):
        super(Point2D, self).__init__(**traits)

class ConnectionGeometrics(traits.HasTraits):
    points = traits.List(Point2D)
    
    def __init__(self, **traits):
        super(ConnectionGeometrics, self).__init__(**traits)

class ModuleGeometrics(traits.HasTraits):
    x=traits.Float()
    y=traits.Float()
    w=traits.Float()
    h=traits.Float()
    
    def __init__(self, **traits):
        super(ModuleGeometrics, self).__init__(**traits)

class DataflowEditorModel(traits.HasTraits):
    network = traits.Instance(Network)
    module_geometrics = traits.Dict(Module, ModuleGeometrics)
    connection_geometrics = traits.Dict(Connection, ConnectionGeometrics)
    
    def __init__(self, **traits):
        super(DataflowEditorModel, self).__init__(**traits)
    