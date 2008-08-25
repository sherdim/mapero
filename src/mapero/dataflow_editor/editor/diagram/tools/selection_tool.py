# Author: Zacarias F. Ojeda <zojeda@gmail.com>
# License: new BSD Style.

from mapero.dataflow_editor.editor.model.diagram_object_model import DiagramObjectModel

from mapero.dataflow_editor.editor.diagram.tools.base_diagram_tool import BaseDiagramTool
from mapero.dataflow_editor.editor.diagram.components.diagram_component import DiagramComponent

class SelectionTool(BaseDiagramTool):

    start = [0,0]
    end = [0,0]
    
    bg_color = (0.6,0.6,1.0,0.4)
    bgcolor = "transparent"
    selection = []
    start_moving = [0,0]
    movement = [0,0]

    def reset(self):
        self.start = [0,0]
        self.end = [0,0]
        self.event_state = 'normal'
        self.start_moving = [0,0]
        self.movement = [0,0]
        self.container.request_redraw()
    
    def selecting_draw(self, gc, view_bounds):
        gc.save_state()
        gc.set_fill_color(self.bg_color)
        x,y = self.start
        w,h = self.end[0]-x, self.end[1]-y
        gc.begin_path()
        gc.rect(x,y,w,h)
        gc.draw_path()
        gc.restore_state()
            
    def normal_left_down(self, event):
        components = self.container.components_at(event.x, event.y)
        if len( components )>0:
            self.start_moving = [event.x, event.y]
            self.movement = [0,0]
            
            self.event_state = 'moving'
            for comp in components:
                self.editor.selection = [comp.diagram_object_model]
        else:
            self.start = [event.x, event.y]
            self.end = [event.x, event.y]
            self.editor.selection = []
            self.event_state = 'selecting'
        self.request_redraw()

    def selecting_mouse_move(self, event):
        self.end[0] = event.x
        self.end[1] = event.y
        
        min_c = [min(self.start[0], self.end[0]), min(self.start[1], self.end[1])]
        max_c = [max(self.start[0], self.end[0]), max(self.start[1], self.end[1])]
        rect = min_c + max_c
        
        for comp in self.container.components:
            if isinstance(comp, DiagramComponent):
                diagram_object_model = comp.diagram_object_model
                if diagram_object_model.is_included_in( rect ):
                    if (diagram_object_model not in self.editor.selection):
                        self.editor.selection.append( diagram_object_model )
                else:
                    if (diagram_object_model in self.editor.selection):
                        self.editor.selection.remove( diagram_object_model )
                    
        
        self.request_redraw()
        
    def selecting_key_pressed(self, event):
        if event.character == 'Esc':
            self.reset()
            self.request_redraw()
            
    def selecting_left_up(self, event):
        self.reset()
        if len(self.editor.selection)>0:
            self.event_state = 'selected'
        else:
            self.reset()
            
        self.request_redraw()
        
    def selected_left_down(self, event):
        components = self.container.components_at(event.x, event.y)
        if len( components )>0:
            self.start_moving = [event.x, event.y]
            self.movement = [0,0]
            self.event_state = 'moving'
        else:
            self.reset()
            self.editor.selection = []
        self.request_redraw()
            
    def moving_mouse_move(self, event):
        movement = [0,0]
        movement[0] = event.x - self.start_moving[0]
        movement[1] = event.y - self.start_moving[1]
        for diagram_object in self.editor.selection:
            if isinstance(diagram_object, DiagramObjectModel):
                comp = self.container.window.diagram_object_component_dict[diagram_object]
                comp.diagram_object_model.move(movement)
        self.container.request_redraw()
        self.start_moving = [event.x, event.y]
        
    def moving_left_up(self, event):
        self.reset()
        
        