from mapero.core.module import VisualModule
from mapero.core.port import OutputPort
from enthought.traits.api import Range, Str
from enthought.traits.ui.api import Group

class visual_modulo1(VisualModule):
    """  """
    param = Range(0,100)
    
    view = Group('param' )
    
    out1 = OutputPort( data_type = Str )
        
    def _param_changed(self, value):
        self.out1.data = value
        self.progress = value

    def create_control(self, parent):
        self.ui = self.edit_traits(parent=parent, kind="subpanel")
        return self.ui.control
    
    def destroy_control(self):
        if self.ui:
            self.ui.dispose()
