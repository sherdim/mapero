from mapero.core.api import Module, OutputPort

from enthought.traits.api import Instance, Any
from enthought.traits.ui.api import Group
from enthought.tvtk.api import tvtk


class cone_source(Module):
    """ modulo de prueba visual """
    
    conesource = Instance(tvtk.ConeSource)
    mapper = Instance(tvtk.PolyDataMapper)
    property = Instance(tvtk.Property)
    view = Group('conesource', 'mapper','property')

    label = "Cone Source"
    
    cone_out = OutputPort( trait = Any )

    def start_module(self):
        self.conesource = tvtk.ConeSource()
	
        self.mapper = tvtk.PolyDataMapper(input=self.conesource.output)
        self.property = tvtk.Property()
        self.actor = tvtk.Actor(mapper=self.mapper, property=self.property)

        self.cone_out.data = self.actor
        
        print self.cone_out.data
    



