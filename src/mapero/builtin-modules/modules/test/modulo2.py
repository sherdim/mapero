from mapero.core.module import Module
from mapero.core.port import InputPort, MultiInputPort
from enthought.traits.api import Int

import logging
log = logging.getLogger("mapero.logger.module");

class modulo2(Module):
    """ aaaaaaa  """
    in1 = InputPort( data_type = Int )

    def execute(self):
        log.debug("processin  g")
        if (self.in1.data):
            self.progress = self.in1.data
            pass
        else:
            self.progress = 0
        print "id: %s \t progress : %s" % (id(self), self.progress)
