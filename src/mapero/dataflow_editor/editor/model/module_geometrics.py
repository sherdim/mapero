# Author: Zacarias F. Ojeda <zojeda@gmail.com>
# License: new BSD Style.

from mapero.core.module import Module

from diagram_object_model import DiagramObjectModel

from enthought.traits.api import WeakRef, Property
from enthought.enable.enable_traits import coordinate_trait, bounds_trait
from enthought.traits.ui.api import View, Item, Group

class ModuleGeometrics(DiagramObjectModel):
 
    position = coordinate_trait
    bounds = bounds_trait
    
    module = WeakRef(Module)
    
    x = Property
    x2 = Property
    y = Property
    y2 = Property
    height = Property
    width = Property
    
    def move(self, movement=[100,100]):
        new_pos = [self.x + movement[0], self.y + movement[1]]
        self.position = new_pos

    def is_included_in(self, rect):
        if self.x >= rect[0] and self.y>= rect[1] \
            and self.x2 <= rect[2] and self.y2 <= rect[3]:
            return True
        else:
            return False
    
    def _get_dataflow_element(self):
        return self.module

    def _get_x(self):
        return self.position[0]

    def _get_y(self):
        return self.position[1]

    def _get_x2(self):
        return self.position[0] + self.bounds[0]

    def _get_y2(self):
        return self.position[1] + self.bounds[1]
    
    def _get_width(self):
        return self.bounds[0]
    
    def _get_height(self):
        return self.bounds[1]

    view = View(
                Item( name = "module", show_label = False, style = 'custom' )
                )