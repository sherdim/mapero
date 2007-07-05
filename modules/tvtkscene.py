from mapero.core.module import VisualModule
from mapero.core.port import OutputPort
from mapero.core.port import InputPort , MultiInputPort
from enthought.traits.api import Range, Int, Instance
from enthought.traits.ui.api import View, Group, Item
from enthought.pyface.tvtk.decorated_scene import DecoratedScene
from enthought.pyface.tvtk.picker import Picker
from enthought.tvtk.api import tvtk
from enthought.enable2.wx_backend.api import Window
from enthought.enable2.api import Container
import wx

import re

import types

module_info = {    'name': 'visual.tvtkscene',
                'desc': "Module with a InputPort with test purpose"}

class tvtkscene(VisualModule):
    """ modulo de prueba visual """
    scene = Instance(DecoratedScene)
    view = Group(
            Item('scene', label='', style='custom'),
                    label='Scene', show_labels=False)

    def __init__(self, **traits):
        super(tvtkscene, self).__init__(**traits)
        self.name = 'TVTK Scene'
        self.actors_pattern = "actors1"
        self.input_ports.append(MultiInputPort(types.IntType, self.actors_pattern, self))
        self.input_actors = None

    def update(self, input_port, old, new):
        if (old == new) :
            self.input_actors = None
        else:
            if isinstance(input_port.data, list):
                self.input_actors = input_port.data
            else:
                self.input_actors = [input_port.data]
        self.process()


    def _process(self):
        self.progress = 0
        self.scene.add_actors(self.input_actors)
        self.progress = 100
        print "rerendered scene"


    def _create_window(self):
        self.scene = DecoratedScene(self.parent)
        return self.scene.control



