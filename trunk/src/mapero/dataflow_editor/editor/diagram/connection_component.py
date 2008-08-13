# Author: Zacarias F. Ojeda <zojeda@gmail.com>
# License: new BSD Style.

from mapero.dataflow_editor.editor.model.api import ConnectionGeometrics

from enthought.traits.api import Instance, Delegate, Any
from enthought.enable.api import Component
from enthought.kiva import EOF_FILL_STROKE, FILL_STROKE

class ConnectionComponent(Component):
    
    bg_color = "transparent"

    connection_geometrics = Instance(ConnectionGeometrics, ConnectionGeometrics())
    
    points = Delegate('connection_geometrics')
    
    vertex_size = 3
    
    from_port_component = Any
    to_port_component = Any
    
    def _draw_mainlayer(self, gc, view_bounds=None, mode="default"):
        self._draw_connection(gc)
        
    def _draw_connection(self, gc):
        start_point = self.from_port_component.position
        start_point[0] -= self.x
        start_point[1] += self.y

        # Draw the path.
        gc.begin_path()
        gc.move_to(start_point[0], start_point[1])
        if self.points:
            offset_points = [(x - self.x, y + self.y) for x, y in self.points ]
            gc.lines(offset_points)
        gc.line_to(100,100)
        gc.draw_path()

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

