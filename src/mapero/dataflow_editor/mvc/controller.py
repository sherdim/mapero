from mapero.core.module import Module
from mapero.core.connection import Connection
from mapero.core.module_manager import ModuleManager
from mapero.dataflow_editor.mvc.module_geometrics import ModuleGeometrics
from mapero.dataflow_editor.mvc.model import ConnectionGeometrics
from mapero.dataflow_editor.mvc.model import DataflowEditorModel
from mapero.dataflow_editor.mvc import module_geometrics
from mapero.dataflow_editor.mvc.persistence.state_setter import StateSetter


from enthought.traits import api as traits
from enthought.persistence import state_pickler

import logging
log = logging.getLogger("mapero.logger.mvc");

class DataflowEditorController(traits.HasTraits):
    module_manager = traits.Instance(ModuleManager)
    dataflow_editor_model = traits.Instance(DataflowEditorModel)
    
    module_geometrics_dict = traits.Dict(Module, ModuleGeometrics)
    connection_geometrics_dict =traits.Dict(Connection, ConnectionGeometrics)
    
    document = traits.Trait()
    
    network_updated = traits.Event
    
    def __init__(self, **traits):
        super(DataflowEditorController, self).__init__(**traits)
        self.module_manager = ModuleManager()
        
        if ( self.dataflow_editor_model == None ):
            self.dataflow_editor_model = DataflowEditorModel(
                                network = self.module_manager.network
                                 )
        network = self.module_manager.network
        network.on_trait_event(
                                self._network_updated, 'updated'
                              )
        self.connection_geometrics_dict = {}
        self.module_geometrics_dict = {}

            
        
    def set_network_state(self, state, create_elements = True):
        network = self.module_manager.set_network_state( state.network, create_elements )
        network.on_trait_event( self._network_updated, 'updated' )
        module_geometrics = []
        connection_geometrics = []

        
        for module_geometric_state in state.module_geometrics:
            module_geometric = ModuleGeometrics()
            state_pickler.set_state(module_geometric, module_geometric_state)
            module_geometrics.append(module_geometric)
            module = [ module for module in network.modules if module.id  ==  module_geometric.module_id][0] 
            self.module_geometrics_dict[ module ] =  module_geometric
        
        for connection_geometric_state in state.connection_geometrics:
            connection_geometric = ConnectionGeometrics()
            state_pickler.set_state(connection_geometric, connection_geometric_state)
            connection_geometrics.append(connection_geometric)
            connection = [ connection for connection in network.connections if connection.id  ==  connection_geometric.connection_id][0] 
            self.connection_geometrics_dict[ connection ] =  connection_geometric
            
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
            module_inst = self.module_manager.add('', module.label, module )
        else:
            log.debug("adding a module by module_id")
            module_inst = self.module_manager.add(module)
        if (module_inst != None):
            module_geometrics = ModuleGeometrics(x=x, y=y, w=w, h=h, module_id = module_inst.id)
            self.module_geometrics_dict[ module_inst ] = module_geometrics
            self.dataflow_editor_model.module_geometrics.append(module_geometrics)
            #self.document.UpdateAllViews

    def add_connection(self, module_from, output_port_name, module_to, input_port_name):
        connection = self.module_manager.connect(module_from, output_port_name, module_to, input_port_name)
        connection_geometrics = ConnectionGeometrics(connection_id=connection.id)
        self.connection_geometrics_dict[ connection ] = connection_geometrics
        self.dataflow_editor_model.connection_geometrics.append(connection_geometrics)
#        self.dataflow_editor_model.connection_geometrics.

    def move_module(self, module, mx, my):
        geometric = self.module_geometrics_dict[ module ]
        log.debug( "moving module:  %s  - pos (%d,%d ) " % (module.label, mx, my))
        geometric.x = geometric.x + mx
        geometric.y = geometric.y + my

    def remove_module(self, module_id):
        module = self.module_manager.get_module_by_id( module_id )
        log.debug( "removing module:  %s " % (module.label) )
        connections = self.module_manager.get_module_connections( module )
        for connection in connections:
            connection_geometrics = self.connection_geometrics_dict.pop( connection )
            self.dataflow_editor_model.connection_geometrics.remove( connection_geometrics )
        
        module_geometrics = self.module_geometrics_dict.pop( module )
        self.dataflow_editor_model.module_geometrics.remove( module_geometrics )
        self.module_manager.remove( module )
        self.network_updated = True
        
    def remove_connection(self, connection_id):
        connection = self.module_manager.get_connection_by_id( connection_id )
        connection_geometrics = self.connection_geometrics_dict.pop( connection )
        self.dataflow_editor_model.connection_geometrics.remove( connection_geometrics )
        self.module_manager.disconnect( connection )
        self.network_updated = True
        
    def refresh_module(self, module):
        connections = self.module_manager.get_module_connections( module )
        module_with_state = self.get_network_state(False, [module], connections)
        module = self.module_manager.reload(module)
        self.set_network_state(module_with_state, False)
        return module
        
    #TODO: eliminate this code ASAP
    def get_module_geometrics(self):
        return self.module_geometrics_dict
            

    def get_connection_geometrics(self):
        return self.connection_geometrics_dict

            
    def _network_updated(self):
        self.network_updated = True
        
    def get_network_state(self, all_network=True, modules=None, connections=None):
        #network_state = self.module_manager.get_network_state( all_network, modules, connections )
        
        s = state_pickler.dumps( self.dataflow_editor_model )
        dataflow_editor_model_state = state_pickler.loads_state( s )
        
        all_connections = dataflow_editor_model_state['network']['connections']
        all_modules = dataflow_editor_model_state['network']['modules']
        all_module_geometrics = dataflow_editor_model_state['module_geometrics']
        
        if all_network == True or connections==None:  
            connection_ids = [connection['id'] for connection in connections]
        else:
            connection_ids = [connection.id for connection in connections]
            
        connections_state = [ m_s for m_s in all_connections if  m_s['id'] in connection_ids ]
        dataflow_editor_model_state['network']['connections'] = connections_state
        
        if all_network == True or modules==None:  
            module_ids = [module['id'] for module in modules]
        else:
            module_ids = [module.id for module in modules]

        modules_state = [ m_s for m_s in all_modules if  m_s['id'] in module_ids ]

        dataflow_editor_model_state['network']['modules'] = modules_state
        
        module_geometrics = [mg_s for mg_s in all_module_geometrics if mg_s.module_id in module_ids]
        dataflow_editor_model_state['module_geometrics'] = module_geometrics
       
        return dataflow_editor_model_state
    
  
            
        
        