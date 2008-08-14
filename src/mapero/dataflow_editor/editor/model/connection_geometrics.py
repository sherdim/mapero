# Author: Zacarias F. Ojeda <correo@zojeda.com.ar>
# License: new BSD.

from mapero.core.connection import Connection

from enthought.traits.api import HasTraits, Int, List, WeakRef

class Point2D(HasTraits):
    x = Int
    y = Int

class ConnectionGeometrics(HasTraits):
    points = List(Point2D)
    connection = WeakRef(Connection)
    
    def __init__(self, **traits):
        super(ConnectionGeometrics, self).__init__(**traits)
