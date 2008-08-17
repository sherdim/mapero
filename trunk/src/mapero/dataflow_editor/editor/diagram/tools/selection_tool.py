# Author: Zacarias F. Ojeda <zojeda@gmail.com>
# License: new BSD Style.


from mapero.dataflow_editor.editor.diagram.tools.base_diagram_tool import BaseDiagramTool
from mapero.dataflow_editor.editor.diagram.module_component import ModuleComponent
from mapero.dataflow_editor.editor.diagram.connection_component import ConnectionComponent


class SelectionTool(BaseDiagramTool):

    start = [0,0]
    end = [0,0]
    
    bg_color = (0.6,0.6,1.0,0.4)
    bgcolor = "transparent"
    selection = []

    def reset(self):
        self.start = [0,0]
        self.end = [0,0]
        self.event_state = 'normal'
        self.selection = []
    
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
            self.event_state = 'moving'
            comp = components[0]
            if isinstance(comp, ModuleComponent):
                self.editor.selection = [comp.module_geom.module]
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
        for comp in self.container.components:
            if isinstance(comp, (ModuleComponent, ConnectionComponent)):
                if comp.position[0] >= min_c[0]    \
                    and comp.position[1]>=min_c[1] \
                    and comp.x2 <= max_c[0]  \
                    and comp.y2 <= max_c[1]:
                    if isinstance(comp, ModuleComponent):
                        module = comp.module_geom.module
                        if (module not in self.editor.selection):
                            self.editor.selection.append( module )
                else:
                    if isinstance(comp, ModuleComponent):
                        module = comp.module_geom.module
                        if (module in self.editor.selection):
                            self.editor.selection.remove( module )
                    
        
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
            self.event_state = 'moving'
        else:
            self.reset()
            self.editor.selection = []
        self.request_redraw()
            
    def moving_mouse_move(self, event):
        print "moving_mouse_move"
        
    def moving_left_up(self, event):
        "move to here"
        self.reset()
                
        