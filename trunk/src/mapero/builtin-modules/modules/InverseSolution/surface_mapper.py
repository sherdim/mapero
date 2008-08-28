from mapero.core.api import Module
from mapero.core.api import OutputPort, InputPort
from enthought.traits.api import Any, Array
from enthought.traits.ui.api import Group
from enthought.tvtk.api import tvtk

from numpy import matrix, array, zeros
from scipy.linalg import pinv
from scipy import square, diag, identity

import logging
log = logging.getLogger("mapero.logger.module");

class surface_mapper(Module):
    """ surface mapper """

    label = 'Surface Mapper'
    ip_dipole_sources = InputPort( trait = Array(typecode=float, shape=(None,None)) )
    ip_cortex = InputPort( trait = Any)
    
    op_polydata = OutputPort( trait = Any)
    
    def start_module(self):

        self.i_dipole_sources = None
        self.i_cortex = None

    def execute(self):
        self.i_dipole_sources = self.ip_dipole_sources.data
        self.i_cortex = self.ip_cortex.data
        if ( self.i_cortex != None) :
            self.procesar()

    def procesar(self):
        self.progress = 0
        ocortex = self.i_cortex
        if (self.i_dipole_sources != None):
            dipoles = array(self.i_dipole_sources)
#        dipoles = zeros(12670)
#        dipoles[8197] = 1
            log.debug( "surface mapper: process ...")

            ocortex.point_data.scalars = dipoles[0:dipoles.shape[0],0]
            print "dipoles.shape: ", dipoles.shape
            #log.debug( "dipoles.shape: %s" % dipoles.shape )

        self.progress = 100
        self.op_polydata.data = ocortex


