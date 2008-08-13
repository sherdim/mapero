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
    
    def add_module(self, module, x=200, y=200, w=200, h=100):
        self.network.modules.append( module )
        module_geometrics = ModuleGeometrics(x=x, y=y, w=w, h=h, module_id=module.id)
        self.module_geometrics.append( module_geometrics )