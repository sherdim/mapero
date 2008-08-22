# Author: Zacarias F. Ojeda <correo@zojeda.com.ar>
# License: new BSD.

from mapero.core.data_type import DataType

from enthought.traits.api import HasTraits, Str, Instance, Property, \
                                 List, WeakRef, Bool



class PortInstance(HasTraits):
    module = WeakRef( klass = 'mapero.core.module.Module' )
    name = Str
    data_type = DataType
    data = Property
    
    def __init__(self, **traits):
        super(PortInstance, self).__init__(**traits)
        self.add_trait('_data', self.data_type.type)
    
    def _get_data(self):
        return self._data
    
    def _set_data(self, data):
        old = self._data
        self._data = data
        self.trait_property_changed('data', old, data)
    
class InputPortInstance(PortInstance):
    
    connection = Instance( klass = 'mapero.core.connection.Connection')
    is_input_none = Bool(True)
    
    def _get_data(self):
        if self.is_input_none:
            return None
        return self._data
    
    def _set_data(self, data):
        old = self._data
        if data is None:
            self.is_input_none = True
        else:
            self.is_input_none = False
            self._data = data
        self.trait_property_changed('data', old, data)
    
class OutputPortInstance(PortInstance):

    connections = List( Instance( klass = 'mapero.core.connection.Connection') )
    
    