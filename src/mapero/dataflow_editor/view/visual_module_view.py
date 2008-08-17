# Author: Zacarias F. Ojeda <zojeda@gmail.com>
# License: new BSD Style.

from mapero.core.module import VisualModule

from enthought.traits.api import WeakRef, on_trait_change
from enthought.pyface.workbench.api import View


class VisualModuleView(View):
    
    category = "Visual Modules"
    visual_module = WeakRef( VisualModule )
    
    position = 'right'
    
    def create_control(self, parent):
        return self.visual_module.create_control(parent)

    def destroy_control(self):
        self.visual_module.destroy_control()
    
    @on_trait_change('visual_module:label')
    def on_label_change(self, label):
        self.name = label
        
    def _name_default(self):
        return self.visual_module.label
    
    def _id_default(self):
        return "%s.%d" % ( self.visual_module.canonical_name,id(self.visual_module) )
