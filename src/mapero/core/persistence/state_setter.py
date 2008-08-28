from enthought.persistence import state_pickler
import logging
log = logging.getLogger("mapero.logger.mvc");

class StateSetter(state_pickler.StateSetter):
    def _do_instance(self, obj, state):
        if obj == None:
            obj = state_pickler.create_instance(state)
        try:
            state_pickler.StateSetter._do_instance(self, obj, state)
        except Exception, e:
            log.warning("Failed to set the state due to errors to object: %s \n %s" % (obj, e))
            
    def _do(self, obj, key, value):
        try:
            state_pickler.StateSetter._do(self, obj, key, value)
        except Exception, e:
            log.warning("Failed to set the state due to errors to object: \n obj: %s - key: %s \n exception: %s" % (obj, key, e))

def set_state(object, state):
    StateSetter().set(object, state)