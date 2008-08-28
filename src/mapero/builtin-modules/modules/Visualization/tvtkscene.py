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
        self.progress = 0
        if isinstance(self.input1.data, list):
            input_actors = self.input1.data
        else:
            input_actors = [self.input1.data]
            
        for actor in input_actors:
            if ( actor not in self.input_actors ):
                self._add_actor(actor)
        for actor in self.input_actors:
            if ( actor not in input_actors ):
                self._remove_actor(actor)

        print "tvtk scene updating ..."
        self.progress = 100
        self.scene.render()

    def _add_actor(self, actor):
        print "adding actors"
        self.scene.add_actors(actor)
        self.input_actors.append(actor)
        
    def _remove_actor(self, actor):
        print "removing actors"
        self.scene.remove_actors(actor)
        self.input_actors.remove(actor)


    def create_control(self, parent):
        self.scene = DecoratedScene(parent)
        return self.scene.control
    
    def destroy_control(self):
        self.scene.destroy()



