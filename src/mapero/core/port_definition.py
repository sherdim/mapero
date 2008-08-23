# Author: Zacarias F. Ojeda <correo@zojeda.com.ar>
# License: new BSD.

from mapero.core.data_type import DataType

from enthought.traits.api import HasTraits, Instance, Type, TraitType


class PortDefinition(HasTraits):
    """
        data_type : instance of DataType used to validate connections at 
                    design time (only compatible ports can be connected)
                    
        trait     : if no data_type is assigned, the trait attribute can
                    be used to construct a default data_type based on it
    """
    data_type = Instance( DataType, allow_none = True )
    trait = Type( TraitType )
    
    def __init__(self, **traits):
        super(PortDefinition, self).__init__(**traits)
        if self.data_type == None:
            self.data_type = DataType( type = self.trait )
    
    
class Port( PortDefinition ):
    pass

class OutputPort( Port ):
    pass

class InputPort( Port ):
    pass