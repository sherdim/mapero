from mapero.core.module import VisualModule
from mapero.core.port import MultiInputPort
from enthought.traits.api import Instance
from enthought.traits.ui.api import Group, Item
from enthought.pyface.gui import GUI
from enthought.pyface.tvtk.decorated_scene import DecoratedScene

import types

module_info = {    'name': 'Visualization.tvtkscene',
                'desc': "Module with a InputPort with test purpose"}

class tvtkscene(VisualModule):
    """ modulo de prueba visual """
    scene = Instance(DecoratedScene)
    view = Group(
                     Item('scene', label='', style='custom'),
                label='Scene', show_labels=False
                )

    def __init__(self, **traitsv):
        super(tvtkscene, self).__init__(**traitsv)
        self.name = 'TVTK Scene'
        self.actors_pattern = "actors1"
        self.input1 = MultiInputPort(
                                     data_type = types.IntType,
                                     name = self.actors_pattern,
                                     module = self
                                     )
        self.input_ports.append(self.input1)
        self.input_actors = None

    def update(self, input_port, old, new):
        if (new == None and old != None):
            self.input_actors = old
            GUI.invoke_later( self._remove_actors )
        if (old != new) :
            self.input_actors = input_port.data
            GUI.invoke_later( self._add_actors )


    def _add_actors(self):
        self.progress = 0
        self.scene.add_actors(self.input_actors)
        self.progress = 100

    def _remove_actors(self):
        self.progress = 0
        self.scene.remove_actors(self.input_actors)
        self.progress = 100


    def _create_window(self):
        self.scene = DecoratedScene(self.parent)
        return self.scene.control



