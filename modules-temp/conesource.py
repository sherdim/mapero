from mapero.core.module import Module
from mapero.core.port import OutputPort, InputPort
from enthought.traits.api import Range, Int, Instance
from enthought.traits.ui.api import View, Group, Item
from enthought.pyface.tvtk.decorated_scene import DecoratedScene
from enthought.tvtk.api import tvtk

import types

module_info = {'name': 'visual.conesources',
	       'desc': "Module with cone source"}

class conesources(Module):
    """ modulo de prueba visual """
    conesource = Instance(tvtk.ConeSource)
    mapper = Instance(tvtk.PolyDataMapper)
    property = Instance(tvtk.Property)
    view = Group('conesource', 'mapper','property')


    def start(self):
	self.name = 'ConeSources'
	self.output_ports.append(OutputPort(types.IntType, 'salida1',self))
	self.conesource = tvtk.ConeSource()
	
	self.mapper = tvtk.PolyDataMapper(input=self.conesource.output)
        self.property = tvtk.Property()
        self.actor = tvtk.Actor(mapper=self.mapper, property=self.property)

	self.get_output('salida1').data = self.actor
    



