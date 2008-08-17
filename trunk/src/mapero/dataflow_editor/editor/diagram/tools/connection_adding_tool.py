# Author: Zacarias F. Ojeda <zojeda@gmail.com>
# License: new BSD Style.

from mapero.dataflow_editor.editor.diagram.module_component import ModuleComponent
from mapero.dataflow_editor.editor.diagram.port_component import PortComponent

from enthought.traits.api import Delegate
from mapero.dataflow_editor.editor.diagram.tools.base_diagram_tool import BaseDiagramTool


class ConnectionAddingTool(BaseDiagramTool):
    start = [0,0]
    end = [0,0]
    
    dash_line = (4.0, 2.0)
    
    editor = Delegate('container')
    
    def reset(self):
        self.start = [0,0]
        self.end = [0.0]
        self._input_port_comp = None
        self._output_port_comp = None
        self.event_state = "normal"
        self.draw_mode = 'normal'
    
    def drawing_draw(self, gc, view_bounds=None):
        gc.begin_path()
        gc.move_to(self.start[0],self.start[1])
        gc.line_to(self.end[0],self.end[1])
        gc.draw_path()

    def drawing_mouse_move(self, event):
        self.end = [event.x, event.y]
        event.handled
        self.request_redraw()
        
    def drawing_key_pressed(self, event):
        if event.character == 'Esc':
            self.reset()
            self.request_redraw()
    
    def drawing_left_down(self, event):
        input_port_comp = self._is_port_type_at(event.x, event.y, "input")
        if (input_port_comp):
            self._input_port_comp = input_port_comp
            self.editor.add_connection(self._output_port_comp.port, self._input_port_comp.port)
        self.reset()
        self.request_redraw()

    def normal_left_down(self, event):
        output_port_comp = self._is_port_type_at(event.x, event.y, "output")
        if (output_port_comp):
            self.start = output_port_comp.absolute_position
            self.end =  output_port_comp.absolute_position
            self.event_state = "drawing"
            self._output_port_comp = output_port_comp
            self.draw_mode = 'exclusive'
            event.handled = True
            self.request_redraw()
    
    def _is_port_type_at(self, x, y, type):
        components = self.container.components_at(x, y)
        module_components = [mod_comp for mod_comp in components if isinstance(mod_comp, ModuleComponent) ]
        port_components = []
        for mod_comp in module_components:
            port_components += mod_comp.components_at(x, y)
        port_comps = [port_comp for port_comp in port_components if isinstance(port_comp, PortComponent) and port_comp.type==type]
        if len(port_comps)==1:
            return port_comps[0]
        else:
            return [] 
            
