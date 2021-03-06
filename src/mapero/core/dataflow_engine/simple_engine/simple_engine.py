# Author: Zacarias F. Ojeda <correo@zojeda.com.ar>
# License: new BSD.

from enthought.traits.api import HasTraits, Any, on_trait_change, implements
from mapero.core.dataflow_engine.i_dataflow_engine import IDataflowEngine
from mapero.core.port_definition import InputPort, OutputPort
from mapero.core.port_instance import InputPortInstance, OutputPortInstance
from mapero.core.decorators.thread import threaded_process



class SimpleEngine(HasTraits):
    
    implements(IDataflowEngine)
    
    dataflow = Any

    def instanciate_ports(self, module):
        for attr_name in module.__class__.__dict__:
            attr = getattr(module, attr_name)
            if isinstance(attr, InputPort):
                port = InputPortInstance(name = attr_name, module=module, data_type = attr.data_type)
                module.__dict__[attr_name] = port
                module.input_ports.append(port)
            if isinstance(attr, OutputPort):
                port = OutputPortInstance(name = attr_name, module=module, data_type = attr.data_type )
                module.__dict__[attr_name] = port
                module.output_ports.append(port)
    
    def execute(self):
        pass
    
    @on_trait_change('dataflow')
    def on_dataflow_change(self, dataflow):
        dataflow.engine = self

    @on_trait_change('dataflow:modules_items')
    def on_modules_changes(self, event):
        for module in event.added:
            self.instanciate_ports(module)
            module.start_module()
        for module in event.removed:
            module.stop_module()
            
    def set_input_port_data(self, input_port, data):
        input_port.data = data
        
    @on_trait_change('dataflow:connections_items')
    def on_connection_changes(self, event):
        for connection in event.added:
            if connection.enabled:
                connection.data = connection.output_port.data
                self.set_input_port_data(connection.input_port, connection.data)
            
        for connection in event.removed:
            connection.enabled = False
            connection.data = None
            connection.input_port.data = None

    @on_trait_change('dataflow:connections:data')
    def on_connection_data_change(self, connection, trait_name, data):
        connection.input_port.data = data
        
    @on_trait_change('dataflow:connections:enabled')
    def on_connection_enable_change(self, connection, trait_name, enabled):
        if enabled:
            connection.data = connection.output_port.data
            connection.input_port.data = connection.data
        else:
            connection.data = None
            connection.input_port.data = None