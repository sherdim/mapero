from mapero.core.api import VisualModule, InputPort
from enthought.traits.api import Instance, Any
from enthought.traits.ui.api import Group, Item
from enthought.pyface.gui import GUI
from enthought.tvtk.pyface.decorated_scene import DecoratedScene

import types



class tvtkscene(VisualModule):
    """ modulo de prueba visual """
    scene = Instance(DecoratedScene)
    view =  Item('scene', style='custom')

    label = 'TVTK Scene'
    input1 = InputPort(trait = Any)
    
    def __init__(self, **traitsv):
        super(tvtkscene, self).__init__(**traitsv)
        self.input_actors = []
        self.actors_pattern = "actors1"

    def execute(self):
        self.input_actors = self.input1.data
        if ( not self.input_actors ):
            self._remove_actors()
        else:
            self._add_actors()

    def _add_actors(self):
        self.progress = 0
        self.scene.add_actors(self.input_actors)
        self.progress = 100
        
    def _remove_actors(self):
        self.progress = 0
        self.scene.remove_actors(self.input_actors)
        self.progress = 100


    def create_control(self, parent):
        self.scene = DecoratedScene(parent)
        return self.scene.control
    
    def destroy_control(self):
        self.scene.destroy()



