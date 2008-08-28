# Author: Zacarias F. Ojeda <correo@zojeda.com.ar>
# License: new BSD.

from mapero.core.data_type import DataType

from enthought.traits.api import HasPrivateTraits, Str, Instance, Property, \
                                 List, WeakRef, Bool



class PortInstance(HasPrivateTraits):
    module = WeakRef( klass = 'mapero.core.module.Module' )
    name = Str
    data_type = Instance(DataType)
    data = Property
    
    is_data_none = Bool(True)

    def __init__(self, **traits):
        super(PortInstance, self).__init__(**traits)
        self.add_trait('_data', self.data_type.type)

    def _get_data(self):
        if self.is_data_none:
            return None
        return self._data
    
    def _set_data(self, data):
        old = self._data
        if data is None:
            self.is_data_none = True
        else:
            self.is_data_none = False
            self._data = data
    
class InputPortInstance(PortInstance):
    
    connection = Instance( klass = 'mapero.core.connection.Connection')
    
    def _set_data(self, data):
        super(InputPortInstance, self)._set_data(data)
        self.module.execute()
    
class OutputPortInstance(PortInstance):

    connections = List( Instance( klass = 'mapero.core.connection.Connection') )

    def update_data(self):
        print "updating data"
        for connection in self.connections:
            if connection.enabled:
                connection.input_port.module.execute()

    def _set_data(self, data):
        super(OutputPortInstance, self)._set_data(data)
        for connection in self.connections:
            if connection.enabled:
                connection.data = data
    
