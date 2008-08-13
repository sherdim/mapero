# Author: Zacarias F. Ojeda <zojeda@gmail.com>
# License: new BSD Style.

from enthought.traits.api import HasTraits, Property, Instance
from enthought.traits.ui.api import View, Item
from enthought.envisage.ui.workbench.api import Workbench


class CurrentSelection(HasTraits):
    workbench = Instance(Workbench)
    current_selection = Property
    
    _current_selection = Instance(HasTraits)
    
    view_selection = View(Item(name='_current_selection',
                                       enabled_when='_current_selection is not None',
                                       style='custom', springy=True,
                                       show_label=False,),
                                  resizable=True,
                                  scrollable=True
                                  )
    
    def __init__(self, workbench):
        self.workbench = workbench
        self._current_selection = None
        self.workbench.on_trait_change(self.on_current_window_changed, 'active_window')
    
    def on_current_window_changed(self, window):
        window.on_trait_change(self.update_active_editor, 'active_editor')
            
    def update_active_editor(self, editor):
        editor.on_trait_change(self.update_selection, 'selection')
        
    def update_selection(self, event):
        selection = self.workbench.active_window.active_editor.selection
        old = self._current_selection
        if len(selection)>0:
            object = selection[0]
        else:
            object =  None
        self._current_selection = object 
        self.trait_property_changed('current_selection', old, object)
            
            
    def _get_current_selection(self):
        return self._current_selection
