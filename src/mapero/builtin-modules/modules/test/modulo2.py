from mapero.core.module import Module
from mapero.core.port import InputPort
from enthought.traits import api as traits

import logging
log = logging.getLogger("mapero.logger.module");

class modulo2(Module):
    """ """
    def __init__(self, **traits):
        super(modulo2, self).__init__(**traits)
        self.in1 = InputPort(
                                   data_type = None,
                                   name = 'in1',
                                   module = self 
                               )
        self.input_ports.append(self.in1)

    def update(self, input_port, old=None, new=None):
        self.process()
        
    def _process(self):
        log.debug("processing")
        if (self.in1.data):
            self.progress = self.in1.data
        else:
            self.progress = 0
        print "modulo2: ", self.progress
