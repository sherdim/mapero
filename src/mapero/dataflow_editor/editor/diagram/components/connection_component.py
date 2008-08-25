# Author: Zacarias F. Ojeda <zojeda@gmail.com>
# License: new BSD Style.

from mapero.dataflow_editor.editor.model.api import ConnectionGeometrics
from mapero.dataflow_editor.editor.diagram.components.diagram_component import DiagramComponent

from enthought.traits.api import Instance, Delegate, Any, on_trait_change
from enthought.enable.api import Component

class ConnectionComponent(DiagramComponent, Component):
    
    bgcolor = "transparent"

    connection_geometrics = Instance(ConnectionGeometrics)
    
    points = Delegate('connection_geometrics')
    
    vertex_size = 3
    
    output_port_component = Any
    input_port_component = Any
    resizable = "hv"
    
    
    def _get_diagram_object_model(self):
        return self.connection_geometrics
    
    def draw_diagram_component(self, gc):
        start_point = self.connection_geometrics.start_point
        end_point = self.connection_geometrics.end_point
        
        gc.save_state()
        # Draw the path.
        gc.begin_path()
        if self.selected:
            gc.set_line_dash( (4.0, 2.0) )
        gc.move_to( *start_point )
        
        if self.points:
            offset_points = [(x - self.x, y + self.y) for x, y in self.points ]
            gc.lines(offset_points)
            
        gc.line_to( *end_point )
        gc.draw_path()
        
        #self.position = start_point

        # Draw the vertices.
        #self._draw_vertices(gc)

        gc.restore_state()
        return

    def _draw_vertices(self, gc):
        "Draw the vertices of the polygon."

        #gc.set_fill_color(self.vertex_color_)
        gc.set_line_dash([4.0,2.0])

        offset = self.vertex_size / 2.0
        #offset_points = [(x + self.x, y + self.y)
        #                 for x, y in self.points]

        if hasattr(gc, 'draw_path_at_points'):
            path = gc.get_empty_path()
            path.rect(-offset, -offset, self.vertex_size, self.vertex_size)
            #gc.draw_path_at_points(offset_points, path, FILL_STROKE)

#        else:
#            for x, y in offset_points:
#                gc.begin_path()
#                gc.rect(x - offset, y - offset,
#                        self.vertex_size, self.vertex_size)
#                gc.fill_path()
        return

    @on_trait_change('input_port_component.absolute_position')
    def on_input_port_change_position(self, position):
        if self.connection_geometrics:
            self._include_point_in_coord_box(position)
            self.connection_geometrics.end_point = position
            self.invalidate_and_redraw()

    @on_trait_change('output_port_component.absolute_position')
    def on_output_port_change_position(self, position):
        if self.connection_geometrics:
            self._include_point_in_coord_box(position)
            self.connection_geometrics.start_point = position
            self.invalidate_and_redraw()

    #utility function used to change the position and bounds
    #in order to allow the draw in the container canvas (make it visible)
    def _include_point_in_coord_box(self, point):
        if self.bounds[0] == 0:
            self.position[0] = point[0]
            self.bounds[0] = 5
        if self.bounds[1] == 0:
            self.position[1] = point[1]
            self.bounds[1] = 5

        if point[0] < self.position[0]:
            self.position[0] = point[0]
        if point[1] < self.position[1]:
            self.position[1] = point[1]
        if point[0] > self.x2:
            self.bounds[0] = point[0] - self.position[0]
        if point[1] > self.y2:
            self.bounds[1] = point[1] - self.position[1]
