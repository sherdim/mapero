from mapero.core.module import Module
from mapero.core.module_manager import ModuleManager
from mapero.dataflow_editor.mvc.module_geometrics import ModuleGeometrics
from mapero.dataflow_editor.mvc.model import ConnectionGeometrics
from mapero.dataflow_editor.mvc.model import DataflowEditorModel


from enthought.traits import api as traits
from enthought.persistence import state_pickler
from mapero.dataflow_editor.mvc import module_geometrics
from mapero.dataflow_editor.mvc.persistence.state_setter import StateSetter

import logging
log = logging.getLogger("mapero.logger.mvc");

class DataflowEditorController(traits.HasTraits):
    module_manager = traits.Instance(ModuleManager)
    dataflow_editor_model = traits.Instance(DataflowEditorModel)
    document = traits.Trait()
    
    def __init__(self, **traits):
        super(DataflowEditorController, self).__init__(**traits)
        self.module_manager = ModuleManager()
        
        if ( self.dataflow_editor_model == None ):
            self.dataflow_editor_model = DataflowEditorModel(
                                network = self.module_manager.network
                                 )
            
        
    def create_dataflow_model(self, state):
        network = self.module_manager.create_network_instance(state.network)
        state_setter = StateSetter()
        state_setter.set(network, state.network)
        module_geometrics = []
        connection_geometrics = []
        
        for module_geometric_state in state.module_geometrics:
            module_geometric = ModuleGeometrics()
            state_pickler.set_state(module_geometric, module_geometric_state)
            module_geometrics.append(module_geometric)
        
        for connection_geometric_state in state.connection_geometrics:
            connection_geometric = ConnectionGeometrics()
            state_pickler.set_state(connection_geometric, connection_geometric_state)
            connection_geometrics.append(connection_geometric)
            
        dataflow_editor_model = DataflowEditorModel(
                                             network = network,
                                             module_geometrics = module_geometrics,
                                             connection_geometrics = connection_geometrics
                                             )
        
        self.module_manager.network = network
        self.dataflow_editor_model = dataflow_editor_model
    
    def add_module(self, module, x, y, w = 151, h = 91):
        self.module_manager.set(trait_change_notify = False)
        log.debug( "module parameter type : %s"  % (type(module)) )
        log.debug( "adding module: %s - geometrics:  ( x: %d, y: %d, w: %d, h: %d )"  %  (module, x, y, w, h) )
        if isinstance(module, Module):
            log.debug("adding a module by instance")
            module_inst = self.module_manager.add('', module.name, module )
        else:
            log.debug("adding a module by module_id")
            module_inst = self.module_manager.add(module)
        if (module_inst != None):
            module_geometrics = ModuleGeometrics(x=x, y=y, w=w, h=h, module_id = module_inst.id)
            self.dataflow_editor_model.module_geometrics.append(module_geometrics)
            #self.document.UpdateAllViews

    def add_connection(self, module_from, output_port_name, module_to, input_port_name):
        connection = self.module_manager.connect(module_from, output_port_name, module_to, input_port_name)
        connection_geometrics = ConnectionGeometrics(connection_id=connection.id)
        self.dataflow_editor_model.connection_geometrics.append(connection_geometrics)
#        self.dataflow_editor_model.connection_geometrics.

    def move_module(self, module, mx, my):
        geometric = self.get_module_geometrics()[module]
        log.debug( "moving module:  %s  - pos (%d,%d ) " % (module.label, mx, my))
        geometric.x += mx
        geometric.y += my

    def remove_module(self, module):
        log.debug( "removing module:  %s " % (module.name))
        connections = self.module_manager.get_module_connections(module)
        for connection in connections:
            del self.dataflow_editor_model.connection_geometrics[connection]
        self.module_manager.remove(module)
        del self.dataflow_editor_model.module_geometrics[module]
        
    def refresh_module(self, module):
        self.module_manager.reload(module)
        
    #TODO: eliminate this code ASAP
    def get_module_geometrics(self):
        module_geometrics_dict = {}
        for module in self.dataflow_editor_model.network.modules:
            geometrics = self._get_module_geometrics(module)
            module_geometrics_dict[module] = geometrics
            
        return module_geometrics_dict

    def _get_module_geometrics(self, module):
        for geometrics in self.dataflow_editor_model.module_geometrics:
            if geometrics.module_id == module.id:
                return geometrics
            

    def get_connection_geometrics(self):
        connection_geometrics_dict = {}
        for connection in self.dataflow_editor_model.network.connections:
            geometrics = self._get_connection_geometrics(connection)
            connection_geometrics_dict[connection] = geometrics
            
        return connection_geometrics_dict

    def _get_connection_geometrics(self, connection):
        for geometrics in self.dataflow_editor_model.connection_geometrics:
            if geometrics.connection_id == connection.id:
                return geometrics
            
