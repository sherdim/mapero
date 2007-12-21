
from base import BaseInteractor
import mapero.dataflow_editor.mvc.commands as commands

import logging

log = logging.getLogger("mapero.logger.mvc");

class KeyboardInteractor(BaseInteractor):
    keyboard_maps = {'DELETE SELECTION':'CTRL+D'}
    action_ids = ['remove', 'add']
    def __init__(self, document, view):
        super(KeyboardInteractor, self).__init__(document, view, 'keyword_interactor')
        self.map = {(False,False,False,False,'\x7f'):'delete',
                             (False,False,False,False,'C'):'context_menu'}
        
    def on_event(self, event):
        alt = event.AltDown()
        meta = event.MetaDown()
        shift = event.ShiftDown()
        ctrl = event.ControlDown()
        key = event.GetKeyCode()
        try:
            combination = (alt, meta, shift, ctrl, chr(key).upper())
            print combination
            command = self.map[combination] 
        except:
            command = None
        if (command!=None):
            log.debug(command)
            if command=='delete':
                for module in self.view.selected_modules:
                    module_shape = self.view.get_diagram().get_module_shape(module)
                    x = module_shape.GetX()
                    y = module_shape.GetY()
                    del_command = commands.RemoveModuleCommand(self.document, module, x, y)
                    self.document.GetCommandProcessor().Submit(del_command)
            if command=='context_menu':
                self.view.display_context_menu()
                
