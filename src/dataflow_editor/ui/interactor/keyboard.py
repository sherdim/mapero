
from base import BaseInteractor

import logging

log = logging.getLogger("mapero.logger.mvc");

class KeyboardInteractor(BaseInteractor):
    keyboard_maps = {'DELETE SELECTION':'CTRL+D'}
    def __init__(self, document, view):
        super(KeyboardInteractor, self).__init__(document, view, 'keyword_interactor')
    	self.map = {(False,False,False,True,'D'):'delete'}
        
    def on_event(self, event):
	alt = event.AltDown()
	meta = event.MetaDown()
	shift = event.ShiftDown()
	ctrl = event.ControlDown()
	key = event.GetKeyCode()
	try:
	    combination = (alt, meta, shift, ctrl, chr(key).upper())
	    command = self.map[combination] 
	except:
	    command = None
	if (command!=None):
		print command
