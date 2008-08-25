# Author: Zacarias F. Ojeda <zojeda@gmail.com>
# License: new BSD Style.


from enthought.traits.api import HasTraits, Type, TraitType, Any

class DataType(HasTraits):
    type = Any( transient=True ) #Type( TraitType, allow_none = False) persistence problems with it
    
    def is_compatible_with(self, other_type):
        if isinstance(self.type, type) and isinstance(other_type.type, type):
            return issubclass(self.type, other_type.type)
        elif isinstance(self.type, type) and isinstance(other_type.type, TraitType):
            return isinstance(self.type, other_type.type)
        elif isinstance(self.type, TraitType) and isinstance(other_type.type, TraitType):
            return issubclass(type(self.type), type(other_type.type))
    
    
class DefaultDataType(DataType):
    pass