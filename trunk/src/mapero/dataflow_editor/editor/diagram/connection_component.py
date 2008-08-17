# Author: Zacarias F. Ojeda <zojeda@gmail.com>
# License: new BSD Style.

from mapero.dataflow_editor.editor.model.api import ConnectionGeometrics

from enthought.traits.api import WeakRef, Delegate, Any, on_trait_change
from enthought.enable.api import Component
from enthought.kiva import FILL_STROKE

class ConnectionComponent(Component):
    
    bgcolor = "transparent"

    connection_geometrics = WeakRef(ConnectionGeometrics)
    
    points = Delegate('connection_geometrics')
    
    vertex_size = 3
    
    output_port_component = Any
    input_port_component = Any
    resizable = "hv"
    
    def _draw_mainlayer(self, gc, view_bounds=None, mode="default"):
        self._draw_connection(gc)
        
    def _draw_connection(self, gc):
        start_point = self.output_port_component.absolute_position

        # Draw the path.
        gc.begin_path()
        gc.move_to(start_point[0], start_point[1])
        if self.points:
            offset_points = [(x - self.x, y + self.y) for x, y in self.points ]
            gc.lines(offset_points)
            
        end_point = self.input_port_component.absolute_position
        
        gc.line_to(end_point[0],end_point[1])
        gc.draw_path()
        
        #self.position = start_point

        # Draw the vertices.
        #self._draw_vertices(gc)


    def _draw_vertices(self, gc):
        "Draw the vertices of the polygon."

        #gc.set_fill_color(self.vertex_color_)
        gc.set_line_dash(None)

        offset = self.vertex_size / 2.0
        offset_points = [(x + self.x, y + self.y)
                         for x, y in self.points]

        if hasattr(gc, 'draw_path_at_points'):
            path = gc.get_empty_path()
            path.rect(-offset, -offset, self.vertex_size, self.vertex_size)
            gc.draw_path_at_points(offset_points, path, FILL_STROKE)

        else:
            for x, y in offset_points:
                gc.begin_path()
                gc.rect(x - offset, y - offset,
                        self.vertex_size, self.vertex_size)
                gc.fill_path()
        return

    @on_trait_change('input_port_component.absolute_position')
    def on_input_port_change_position(self, position):
        self._include_point_in_coord_box(position)

    @on_trait_change('output_port_component.absolute_position')
    def on_output_port_change_position(self, position):
        self._include_point_in_coord_box(position)
        
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
            
        