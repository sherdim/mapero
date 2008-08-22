# Author: Zacarias F. Ojeda <correo@zojeda.com.ar>
# License: new BSD.

from mapero.core.api import Connection

from diagram_object_model import DiagramObjectModel

from enthought.traits.api import List, WeakRef
from enthought.enable.enable_traits import coordinate_trait
from enthought.traits.ui.api import View, Item

class ConnectionGeometrics(DiagramObjectModel):
    
    points = List(coordinate_trait)
    connection = WeakRef(Connection)
    start_point = coordinate_trait   # correspond to the port associated
    end_point = coordinate_trait
    
    def move(self, movement=[100,100]):
        pass
    
    def is_included_in(self, rect):
        x = min(self.start_point[0], self.end_point[0])
        y = min(self.start_point[1], self.end_point[1])
        x2 = max(self.start_point[0], self.end_point[0])
        y2 = max(self.start_point[1], self.end_point[1])

        return  ( x >= rect[0] and y  >= rect[1] and \
                 x2 <= rect[2] and y2 <= rect[3])

    def is_in(self, x, y):
        tol = 5
        x0, y0 = self.start_point
        x1, y1 = self.end_point
        
        if abs(x0 - x1) < tol:
            if abs(x0-x) < tol:
                return ((y0 > y) and (y1 < y)) or ((y0 < y) and (y1 > y))
            else:
                return False
        else:
            m = (y1 - y0) / (x1 - x0)
            b = y0 - m * x0
            yl = m*x + b
            if abs( yl-y ) < tol:
                return True

        return False
            
    def _get_dataflow_element(self):
        return self.connection

    view = View(
                Item( name = "connection", show_label = False, style = 'custom' )
                )    