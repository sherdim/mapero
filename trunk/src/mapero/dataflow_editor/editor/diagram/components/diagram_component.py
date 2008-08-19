# Author: Zacarias F. Ojeda <zojeda@gmail.com>
# License: new BSD Style.


from enthought.traits.api import HasTraits, Bool, Property

class DiagramComponent(HasTraits):
    
    selected = Bool(False)
    diagram_object_model = Property
    
    def draw_diagram_component(self, gc):
        raise NotImplementedError           
        
    def draw_diagram_component_border(self, gc):
        pass           

    def is_in(self, x,y):
        return self.diagram_object_model.is_in(x,y)

    def is_included_in(self, rect):
        return self.diagram_object_model.is_included_in(rect)
    
    def _get_diagram_object_model(self):
        raise NotImplementedError           
        
    def _draw_container_mainlayer(self, gc, view_bounds=None, mode="default"):
        self.draw_diagram_component(gc)
        
    def _draw_container_border(self, gc, view_bounds=None, mode="default"):
        self.draw_diagram_component_border(gc)
        
    def _draw_mainlayer(self, gc, view_bounds=None, mode="default"):
        self.draw_diagram_component(gc)