from mapero.core.network import Network
from module_geometrics import ModuleGeometrics
from connection_geometrics import ConnectionGeometrics
from enthought.traits import api as traits


class DataflowEditorModel(traits.HasTraits):
    network = traits.Instance(Network)
    module_geometrics = traits.List(ModuleGeometrics, [])
    connection_geometrics = traits.List(ConnectionGeometrics, [])
    
    def __init__(self, **traits):
        super(DataflowEditorModel, self).__init__(**traits)
    