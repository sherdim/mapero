from mapero.core.network import Network
from mapero.core.connection import Connection
from mapero.core.catalog import Catalog
from enthought.traits import api as traits
from enthought.persistence import state_pickler
from enthought.persistence.state_pickler import StateSetterError
#from enthought.developer.helper.fbi import fbi
import gc
import sys

import logging
log = logging.getLogger("mapero.logger.engine");


class ModuleNotFoundInNetworkError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class MoreThanOneModuleInNetworkWithTheSameIDError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
    
class ConnectionNotFoundInNetworkError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class ModuleManager(traits.HasTraits):
    """ Module Manager Class """

    catalog = traits.Instance(Catalog, Catalog())
    network = traits.Instance(Network)
    
    def __init__(self, **traits):
        super(ModuleManager, self).__init__(**traits)
        if (self.network == None) :
            self.network = Network()
        self.catalog.refresh()

    def get_module_by_label(self, module_label):
        for module in self.network.modules:
            if module.label == module_label:
                return module
        raise ModuleNotFoundInNetworkError(module_label)
        
    def get_module_by_id(self, module_id):
        for module in self.network.modules:
            if module.id == module_id:
                return module
        raise ModuleNotFoundInNetworkError(module_id)

        
    def get_connection_by_id(self, connection_id):
        for connection in self.network.connections:
            if connection.id == connection_id:
                return connection
        raise ConnectionNotFoundInNetworkError(connection_id)
        
    def get_module(self, module):
        if isinstance(module,str):
            return self.get_module_by_label(module)
        else:
            if self.network.modules.index(module) > -1:
                return module
            else:
                raise ModuleNotFoundInNetworkError(str(module))


    def has_module(self, module_label):
        for module in self.network.modules:
            if module.label == module_label:
                return True
        return False

    def add(self, module_canonical_name, label = '', module = None):
        log.debug( 'module_canonical_name: %s - label: %s ' % ( module_canonical_name, label) )
        module_number = 1

        if not module:
            module = self.catalog.load_module(module_canonical_name)

        if module:
            ip = module.__module__.rfind('.')
            module.label = module.__module__[ip+1:]
            module.start_module()
            module_prefix_key = label and label or module.label
            module_key = module_prefix_key
            if self.has_module(module_key):
                while (self.has_module(module_key)):
                    module_number+=1
                    module_key = module_prefix_key+str(module_number)
            module.label = module_key
            self.network.modules.append(module)
            print "added module with id : ", module.id
            return module
        else:
            print "asdcasdca"
        
    def remove(self, module_label):
        module = self.get_module(module_label)
        self.disconnect_module(module_label)
        module.stop_module()
        self.network.modules.remove(module)
        quedan = sys.getrefcount(module)
        if quedan > 2:
                print( "in memory: %s  instances of %s" % ( sys.getrefcount(module), module.__class__ ))
#                log.error( "in memory: %s  instances of %s" % ( sys.getrefcount(module), module.__class__ ))
#                #referrers = gc.get_referrers(module)
#                #log.debug( "referrers: %s" , referrers )
#                #garbage = gc.garbage
#        #fbi()

    def reload(self, module): ## todavia no funciona
        module_connections = []

        module = self.get_module(module)
        if module:
            for connection in self.network.connections:
                if connection.input_port.module == module or connection.output_port.module == module:
                    module_connections.append(connection)
            
            canonical_name = module.canonical_name
            module_label = module.label
            self.remove(module)

            new_module = self.catalog.reload_module(module)

            self.add(canonical_name, module_label, new_module)
            for connection in module_connections:
                if connection.output_port.module == module:
                    new_module_from = new_module
                    new_module_to = connection.input_port.module
                    port_from = new_module_from.get_output(connection.output_port.name)
                    port_to = connection.input_port
                if connection.input_port.module == module:
                    new_module_from = connection.output_port.module
                    new_module_to = new_module
                    port_from = connection.output_port
                    port_to = new_module_to.get_input(connection.input_port.name)
                self.connect(new_module_from, port_from, new_module_to, port_to)
            return new_module

    def connect(self, module_label_from, module_port_form , module_label_to, module_port_to):
        module_from = self.get_module(module_label_from)
        module_to = self.get_module(module_label_to)
        port_from = module_from.get_output(module_port_form)
        port_to = module_to.get_input(module_port_to)

        new_connection = Connection(output_port=port_from, input_port=port_to)
        log.debug("new connection: from %s[%s] to %s[%s]" % (new_connection.output_port.module, new_connection.output_port, 
                                                             new_connection.input_port.module, new_connection.input_port)) 

#        for connection in self.network.connections:
#            if connection == new_connection:
#                raise ModuleConnectionError('The connection has been established previously')
#            if connection.input_port.module == module_to and connection.input_port.name == module_port_to:
#                raise ModuleConnectionError('The target module.port has a previous connection')

        self.network.connections.append(new_connection)
        return new_connection


#    def disconnect(self, module_label_from, module_port_form , module_label_to, module_port_to):
#        module_from = self.get_module(module_label_from)
#        module_to = self.get_module(module_label_to)
#        port_from = module_from.get_output(module_port_form)
#        port_to = module_to.get_input(module_port_to)
#        for connection in self.network.connections:
#            if (port_from == connection.output_port) and (port_to == connection.input_port):
#                self.network.connections.remove(connection)

    def disconnect(self, connection):
        self.network.connections.remove(connection)
        
    def disconnect_module(self, module):
        connections = self.get_module_connections(module)
        for connection in connections:
            self.network.connections.remove(connection)
            
    def get_module_connections(self, module):
        module = self.get_module(module)

        def filter_connections(connection):
            if (connection.input_port.module == module            \
                        or connection.output_port.module == module):
                return True
            else:
                return False

        connections = filter(filter_connections, self.network.connections)
        return connections
    
    def set_network_state(self, state, create_elements=True):
        network = self.network
        def get_module(module_id):
            modules = [module for module in network.modules if module.id == module_id ]
            if(len(modules)>2):
                log.error("More tha One Module in the network with the same ID : " + modules)
                raise MoreThanOneModuleInNetworkWithTheSameIDError(modules)
            if (len(modules)==1): 
                return modules[0]
            else:
                return None
        def get_connection(connection_id):
            connections = [connection for connection in network.connections if connection.id == connection_id ]
            assert(len(connections)<2)
            if (len(connections)==1): 
                return connections[0]
            else:
                return None
            
        for module_state in state.modules:
            module_canonical_name = module_state.__metadata__['module']
            if(create_elements) :
                module = self.catalog.load_module(module_canonical_name)
                module.start_module()
            else:
                module = get_module(module_state['id'])
            try:   
                state_pickler.set_state(module, module_state)
                network.modules.append(module)
            except StateSetterError, e:
                log.error(e)
                
        for connection_state in state.connections:
            if(create_elements):
                input_port = get_module(connection_state.input_port.module_.id).get_input(connection_state.input_port.name)
                output_port = get_module(connection_state.output_port.module_.id).get_output(connection_state.output_port.name)
            
                connection = Connection(input_port=input_port, output_port=output_port)
                network.connections.append(connection)
            else:
                connection = get_connection(connection_state['id'])
            try:   
                state_pickler.set_state(connection, connection_state)
            except StateSetterError, e:
                log.error(e)
            
            
        self.network = network
        return network
        
    def get_network_state(self, all_network=True, modules=None, connections=None):
        network = self.network
        network_state = state_pickler.get_state(network)
        
        if (all_network == False):

            module_ids = [ module.id for module in modules ]
            connection_ids = [ connection.id for connection in connections ]

            module_states = [ module_state for module_state in network_state.modules if module_state.id in module_ids] 
            connection_states = [ connection_state for connection_state in network_state.connections if connection_state.id in connection_ids]
            
            network_state.modules = module_states
            network_state.connections = connection_states 
        
        return network_state
        
