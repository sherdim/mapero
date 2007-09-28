
from base import BaseInteractor
import mapero.dataflow_editor.mvc.commands as commands

import wx
import logging
log = logging.getLogger("mapero.logger.mvc");

class MouseInteractor(BaseInteractor):
    def __init__(self, document, view):
        super(MouseInteractor, self).__init__(document, view, 'mouse_interactor')
        
        
    def on_event(self, event):
        x = event.GetX()
        y = event.GetY()
        
        if event.LeftDown():
            module = self.view.get_module(x, y)
            if module != None:
                if (event.CmdDown()):
                    self.view.toggle_module_selection(module)
                else:
                    self.view.select_module(module)
                
        if event.LeftDClick():
            module = self.view.get_module(x, y)
            if module != None:
                self.edit_module(module)
        
        if event.RightDown():
            self.view.show_popup_menu((x,y))
        event.Skip()
        
        
    def edit_module(self, module):
        ui_selected = module.edit_traits(parent=None, kind='subpanel')
        box = wx.BoxSizer( wx.VERTICAL )
        box.Add( ui_selected.control, 0, wx.ALL | wx.EXPAND )