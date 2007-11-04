from mapero.core.module import Module
from mapero.core.port import OutputPort
from enthought.traits import api as traits
from enthought.traits.ui.api import Group
from enthought.tvtk.api import tvtk

import types

module_info = {'name': 'Visualization.cone_source',
	       'desc': "Module with cone source"}

class cone_source(Module):
    """ modulo de prueba visual """
    conesource = traits.Instance(tvtk.ConeSource)
    mapper = traits.Instance(tvtk.PolyDataMapper)
    property = traits.Instance(tvtk.Property)
    view = Group('conesource', 'mapper','property')


    def __init__(self, **traitsv):
        super(cone_source, self).__init__(**traitsv)
        self.name = 'ConeSources'
        self.out1 = OutputPort(
							   data_type = types.IntType,
							   name = 'salida1',
							   module = self
							   )
        self.output_ports.append(self.out1)
        self.conesource = tvtk.ConeSource()
	
        self.mapper = tvtk.PolyDataMapper(input=self.conesource.output)
        self.property = tvtk.Property()
        self.actor = tvtk.Actor(mapper=self.mapper, property=self.property)

        self.out1.data = self.actor
    



