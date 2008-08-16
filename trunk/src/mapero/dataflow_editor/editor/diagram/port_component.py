# Author: Zacarias F. Ojeda <zojeda@gmail.com>
# License: new BSD Style.

from enthought.traits.api import Float, WeakRef, Str, Any, Property, Enum, on_trait_change 
from enthought.enable.api import Component, str_to_font
from enthought.enable.enable_traits import coordinate_trait

from math import pi

class PortComponent(Component):
    
    type = Enum("input", "output")
    fill_color = (0.5, 0.5, 0.5, 1.0)
    text_color = (0.0, 0.0, 0.0, 1.0)
    padding = 0
    bgcolor = 'transparent'
    bounds=[10,10]
    port = Any
    angle = Float(0.0)
    port_name = Str
    
    absolute_position = Property
    _font = Any
    
    
    _absolute_position = coordinate_trait

    def __absolute_position_default(self):
        self._absolute_position = None
        
    def _draw_mainlayer(self, gc, view_bounds=None, mode="default"):
        dx, dy = self.bounds
        x, y = self.position
        gc.save_state()
        gc.translate_ctm(x+dx/2, y+dy/2)
        if (self.angle != 0.0):
            gc.rotate_ctm(self.angle)
        gc.set_fill_color(self.fill_color)
        gc.move_to(dx/2, dy/2)
        gc.line_to(dx/2, -dy/2)
        gc.line_to(dx*0.1, -dy*0.30)
        gc.line_to(-dx/2, -dy*0.30)
        gc.line_to(-dx/2, dy*0.30)
        gc.line_to(dx*0.1, dy*0.30)
        gc.line_to(dx/2, dy/2)
        gc.fill_path()

        if self.port_name:
            if not self._font:
                self._font = str_to_font(None, None, "modern 8")
            gc.set_font(self._font)
            (x,y,w,h) = gc.get_text_extent(self.port_name)
            if self.angle > pi/2:
                gc.translate_ctm((-2*dx -w), 0)
                gc.rotate_ctm(self.angle)
            gc.set_fill_color(self.text_color)
            gc.set_text_position(-dx -w, -h/2)
            gc.show_text(self.port_name)

        gc.restore_state()
        return

    @on_trait_change('container:position')
    def on_position_change(self, position):
        old_pos = self._absolute_position
        new_pos = [position[0]+self.position[0], 
                   position[1]+self.position[1] ]
        new_pos[0] += self.bounds[0]/2
        new_pos[1] += self.bounds[1]/2
        
        self._absolute_position = new_pos
        self.trait_property_changed('absolute_position', old_pos, new_pos)

        
    def normal_left_down(self, event):
        event.handled
        
    def _get_absolute_position(self):
        if self._absolute_position != [None]:
            return self._absolute_position
        else:
            pos = [self.container.position[0]+self.position[0], 
                   self.container.position[1]+self.position[1] ]
            pos[0] += self.bounds[0]/2
            pos[1] += self.bounds[1]/2
            self._absolute_position = pos
            return pos