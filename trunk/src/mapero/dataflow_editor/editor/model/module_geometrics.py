# Author: Zacarias F. Ojeda <zojeda@gmail.com>
# License: new BSD Style.

from mapero.core.api import Module

from diagram_object_model import DiagramObjectModel

from enthought.traits.api import Instance, Property
from enthought.enable.enable_traits import coordinate_trait, bounds_trait
from enthought.traits.ui.api import View, Item

class ModuleGeometrics(DiagramObjectModel):
 
    position = coordinate_trait
    bounds = bounds_trait
    
    module = Instance(Module)
    
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
        x = self.x
        y = self.y
        x2 = self.x2
        y2 = self.y2
        return  ( x >= rect[0] and y  >= rect[1] and \
                 x2 <= rect[2] and y2 <= rect[3])
        
    def is_in(self, x,y):
        pos = self.position
        bounds = self.bounds
        return (x >= pos[0]) and (x < pos[0] + bounds[0]) and \
               (y >= pos[1]) and (y < pos[1] + bounds[1])
        
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