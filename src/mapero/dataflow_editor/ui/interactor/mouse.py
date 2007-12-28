
from base import BaseInteractor
import mapero.dataflow_editor.mvc.commands as commands

import wx
import logging
log = logging.getLogger("mapero.logger.mvc");

class MouseInteractor(BaseInteractor):
    def __init__(self, document, view):
        super(MouseInteractor, self).__init__(document, view, 'mouse_interactor')
        
        
    def on_event(self, event):

        if (event.LeftDown() or event.LeftDClick() or event.RightDown()) :
            self.view.Activate()
            canvas = self.view.get_diagram().GetCanvas()
            canvas.SetFocus()

            dc = wx.ClientDC(canvas)
            canvas.PrepareDC(dc)
            x, y = event.GetLogicalPosition(dc)  # this takes into account scrollbar offset
            self.select_object(x, y, event)
            
            if event.LeftDClick():
                module = self.view.get_module(x, y)
                if module != None:
                    self.edit_module(module)
            
            if event.RightDown():
                self.view.show_popup_menu((x,y))
        event.Skip()
        

    def select_object(self,x,y,event):
        module = self.view.get_module(x, y)
        connection = self.view.get_connection(x,y)
        if module != None:
            if (event.CmdDown()):
                self.view.toggle_module_selection(module)
            else:
                self.view.select_module(module)
        if connection != None:
            if (event.CmdDown()):
                self.view.toggle_connection_selection(connection)
            else:
                self.view.select_connection(connection)
            
                

    def edit_module(self, module):
        module.edit_traits(parent=self.view.frame, kind='livemodal')
