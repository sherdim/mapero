
from enthought.traits.api import HasTraits, Property



class DiagramObjectModel(HasTraits):
    
    dataflow_element = Property
    
    def move(self, movement=[100,100]):
        raise NotImplementedError
    
    def is_included_in(self, rect):
        raise NotImplementedError
    
    def is_in(self, x,y):
        raise NotImplementedError

    def _get_dataflow_element(self):
        raise NotImplementedError
      
          
        