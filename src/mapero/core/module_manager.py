from mapero.core.network import Network
from mapero.core.connection import Connection
from mapero.core.catalog import Catalog
from enthought.traits import api as traits
from enthought.persistence import state_pickler
import gc
import sys

import logging
log = logging.getLogger("mapero.logger.engine");


class ModuleNotFoundInNetworkError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class ModuleManager(traits.HasTraits):
    """ Module Manager Class """

    catalog = traits.Trait(Catalog(),traits.Instance(Catalog()))
    network = traits.Trait(Network(), traits.Instance(Network()))
    max_module_id = traits.Int(0)
    max_connection_id = traits.Int(0)
    
    def __init__(self, **traits):
        super(ModuleManager, self).__init__(**traits)
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

    def get_module(self, module_label):
        if isinstance(module_label,str):
            return self.get_module_by_label(module_label)
        else:
            if self.network.modules.index(module_label) > -1:
                return module_label
            else:
                raise ModuleNotFoundInNetworkError(str(module_label))


    def has_module(self, module_label):
        for module in self.network.modules:
            if module.label == module_label:
                return True
        return False

    def add(self, module_id, label = '', module = None):
        log.debug( 'module_id: %s - label: %s ' % ( module_id, label) )
        module_number = 1

        if not module:
            module = self.catalog.load_module(module_id)

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
            self.max_module_id += 1
            module.id = self.max_module_id
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
                log.debug( "quedan: %s ", sys.getrefcount(module))
                referrers = gc.get_referrers(module)
                log.debug( "referrers: %s" , referrers )
                garbage = gc.garbage
        #fbi()

    def reload(self, module_label): ## todavia no funciona
        module_connections = []

        module = self.get_module(module_label)
        if module:
            for connection in self.network.connections:
                if connection.input_port.module == module or connection.output_port.module == module:
                    module_connections.append(connection)
                    class_module = module.module_info['name']
                    module_label = module.label
                    self.remove(module_label)

                    new_module = self.catalog.reload_module(class_module)

                    self.add(class_module, module_label, new_module)
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


    def connect(self, module_label_from, module_port_form , module_label_to, module_port_to):
        module_from = self.get_module(module_label_from)
        module_to = self.get_module(module_label_to)
        port_from = module_from.get_output(module_port_form)
        port_to = module_to.get_input(module_port_to)

        new_connection = Connection(output_port=port_from, input_port=port_to)
        log.debug("new connection: from %s[%s] to %s[%s]" % (new_connection.output_port.module, new_connection.output_port, 
                                                             new_connection.input_port.module, new_connection.input_port)) 

        self.max_connection_id += 1
        new_connection.id = self.max_connection_id
#        for connection in self.network.connections:
#            if connection == new_connection:
#                raise ModuleConnectionError('The connection has been established previously')
#            if connection.input_port.module == module_to and connection.input_port.name == module_port_to:
#                raise ModuleConnectionError('The target module.port has a previous connection')

        self.network.connections.append(new_connection)
        return new_connection


    def disconnect(self, module_label_from, module_port_form , module_label_to, module_port_to):
        module_from = self.get_module(module_label_from)
        module_to = self.get_module(module_label_to)
        port_from = module_from.get_output(module_port_form)
        port_to = module_to.get_input(module_port_to)
        for connection in self.network.connections:
            if (port_from == connection.output_port) and (port_to == connection.input_port):
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
    
    def create_network_instance(self, state):
        network = Network()
        self.max_module_id = 0
        self.max_connection_id = 0
        def get_module(module_label):
            for module in network.modules:
                if module.label == module_label:
                    return module

        for module_state in state.modules:
            module_id = module_state.__metadata__['module']
            module_id = module_id.split('mapero.modules.')[1]
            module = self.catalog.load_module(module_id)
            module.label = module_state['label']
            module.id = module_state['id']
            module.start_module()
            self.max_module_id = module.id > self.max_module_id and module.id or self.max_module_id
            network.modules.append(module)
        for connection_state in state.connections:
            input_port = get_module(connection_state.input_port.module.label).get_input(connection_state.input_port.name)
            output_port = get_module(connection_state.output_port.module.label).get_output(connection_state.output_port.name)
            
            connection = Connection(input_port=input_port, output_port=output_port)
            connection.id = connection_state['id']
            self.max_connection_id = connection.id > self.max_connection_id and connection.id or self.max_connection_id
            network.connections.append(connection)
            
        self.network = network
        return network
        
