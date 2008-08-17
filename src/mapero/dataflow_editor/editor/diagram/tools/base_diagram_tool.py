# Author: Zacarias F. Ojeda <zojeda@gmail.com>
# License: new BSD Style.

from enthought.traits.api import Delegate, Enum
from enthought.enable.api import Component


class BaseDiagramTool(Component):
    
    editor = Delegate('container')
    
    draw_mode = Enum('normal', 'exclusive')
    
    #used the same technique in DrawingTool but in overlay layer 
    def _draw_overlay(self, gc, view_bounds, mode="default"):
        draw_func = getattr(self, self.event_state + "_draw", None)
        if draw_func:
            draw_func(gc, view_bounds)
        return   
    
    def reset(self):
        pass     

    