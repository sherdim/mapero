from mapero.core.network import Network
from mapero.core.connection import Connection
from mapero.core.catalog import Catalog
from mapero.core.module import Module
from enthought.traits.api import HasTraits, Instance, Trait
import gc
import sys

import logging
log = logging.getLogger("mapero.logger.engine");


class ModuleNotFoundInNetworkError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class ModuleManager(HasTraits):
    """ Module Manager Class """

    catalog = Trait(Catalog(),Instance(Catalog()))
    network = Trait(Network(), Instance(Network()))

    def __init__(self, **traits):
        super(ModuleManager, self).__init__(**traits)
        self.catalog.refresh()

    def get_module_by_label(self, module_label):
        for module in self.network.modules:
            if module.label == module_label:
                return module
            raise ModuleNotFoundInNetworkError(module_label)

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
            self.network.modules.append(module)
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
        
