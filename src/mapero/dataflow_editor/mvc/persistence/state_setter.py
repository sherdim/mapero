from enthought.persistence import state_pickler
import logging
log = logging.getLogger("mapero.logger.mvc");

class StateSetter(state_pickler.StateSetter):
    def _do_instance(self, obj, state):
        if obj == None:
            print "obj == NONE"
            obj = state_pickler.create_instance(state)
        try:
            state_pickler.StateSetter._do_instance(self, obj, state)
        except:
            log.warning("Failed to set the state due to errors: " % state)
            
#        try 
#            super(StateSetter, self)._do_instance(obj, state)
#        except StateSetterError:
#            instance = state_pickler.create_instance(state)
#            