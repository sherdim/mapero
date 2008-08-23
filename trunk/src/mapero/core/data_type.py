# Author: Zacarias F. Ojeda <zojeda@gmail.com>
# License: new BSD Style.


from enthought.traits.api import HasTraits, Type, TraitType, Any

class DataType(HasTraits):
    type = Any( transient=True ) #Type( TraitType, allow_none = False) persistence problems with it
    
    def is_compatible_with(self, other_type):
        return issubclass(self.type, other_type.type)
    
    
class DefaultDataType(DataType):
    pass