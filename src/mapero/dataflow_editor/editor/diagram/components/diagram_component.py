# Author: Zacarias F. Ojeda <zojeda@gmail.com>
# License: new BSD Style.


from enthought.traits.api import HasTraits, Bool, Property

class DiagramComponent(HasTraits):
    
    selected = Bool(False)
    diagram_object_model = Property
    
    def draw_diagram_component(self, gc):
        raise NotImplementedError           
        
    def draw_selection(self, gc):
        raise NotImplementedError               
    
    def _draw_container_mainlayer(self, gc, view_bounds=None, mode="default"):
        self.draw_diagram_component(gc)
        
    def _draw_mainlayer(self, gc, view_bounds=None, mode="default"):
        self.draw_diagram_component(gc)
        
    def _draw_container_border(self, gc, view_bounds=None, mode="default"):
        if self.selected:
            self.draw_selection(gc)

    def _draw_border(self, gc, view_bounds=None, mode="default"):
        if self.selected:
            self.draw_selection(gc)
            
    def _get_diagram_object_model(self):
        raise NotImplementedError           