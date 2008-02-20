
from base import BaseInteractor
import mapero.dataflow_editor.mvc.commands as commands

import logging

log = logging.getLogger("mapero.logger.mvc");

class KeyboardInteractor(BaseInteractor):
    keyboard_maps = {'DELETE SELECTION':'CTRL+D'}
    action_ids = ['remove', 'add']
    def __init__(self, document, view):
        super(KeyboardInteractor, self).__init__(document, view, 'keyword_interactor')
        self.map = {(False,True,False,False,'\x7f'):'delete',
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
            print command 
        except:
            command = None
        if (command!=None):
            log.debug(command)
            if command=='delete' and ( self.view.selected_modules != None or self.view.selected_connections != None ) :
                del_command = commands.DeleteSelectionCommand(self.document, self.view.selected_modules, self.view.selected_connections)
                self.document.GetCommandProcessor().Submit(del_command)
            if command=='context_menu':
                self.view.display_context_menu()
                
