from mapero.core.api import Module, InputPort

from enthought.traits.api import Int, Str

import logging
log = logging.getLogger("mapero.logger.module");

class modulo2(Module):
    """ aaaaaaa  """

    label = "Modulo 2"
    in1 = InputPort( trait = Int )

    def execute(self):
        if (self.in1.data):
            self.progress = self.in1.data
            pass
        else:
            self.progress = 0
        #print "# id: %s \t progress : %s" % (id(self), self.progress)
