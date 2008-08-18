# Author: Zacarias F. Ojeda <correo@zojeda.com.ar>
# License: new BSD.

from mapero.core.connection import Connection

from enthought.traits.api import HasTraits, Int, List, WeakRef
from diagram_object_model import DiagramObjectModel

class Point2D(HasTraits):
    x = Int
    y = Int

class ConnectionGeometrics(DiagramObjectModel):
    
    points = List(Point2D)
    connection = WeakRef(Connection)
    
    def move(self, movement=[100,100]):
        pass
    
    def is_included_in(self, rect):
        raise NotImplementedError
    
    def _get_dataflow_element(self):
        return self.connection
