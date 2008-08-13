from enthought.traits import api as traits

class Point2D(traits.HasTraits):
    x=traits.Int()
    y=traits.Int()
    
    
class ConnectionGeometrics(traits.HasTraits):
    points = traits.List(Point2D)
    connection_id = traits.Int
    
    def __init__(self, **traits):
        super(ConnectionGeometrics, self).__init__(**traits)
