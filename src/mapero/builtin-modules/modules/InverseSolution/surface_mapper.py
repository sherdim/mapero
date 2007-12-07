from mapero.core.module import Module
from mapero.core.port import OutputPort, InputPort
from mapero.dataflow_editor.decorators.thread import invoke_later
from numpy.oldnumeric.precision import Float, Int
from enthought.traits import api as traits
from enthought.traits.ui.api import Group
from enthought.tvtk.api import tvtk

from numpy import matrix, array, zeros
from scipy.linalg import pinv
from scipy import square, diag, identity

import logging
log = logging.getLogger("mapero.logger.module");

module_info = {'name': 'InverseSolution.surface_mapper',
                    'desc': ""}

class surface_mapper(Module):
    """ surface mapper """

    def __init__(self, **traitsv):
        super(surface_mapper, self).__init__(**traitsv)
        self.name = 'Surface Mapper'

        dipole_sources_trait = traits.Array(typecode=Float, shape=(None,None))
        self.ip_dipole_sources = InputPort(
                                           data_type = dipole_sources_trait,
                                           name = 'dipole source',
                                           module = self
                                           )
        self.input_ports.append(self.ip_dipole_sources)
        self.i_dipole_sources = None
        
        polydata_trait = traits.Trait(tvtk.PolyData)
        self.ip_cortex = InputPort(
                                   data_type = polydata_trait,
                                   name = 'cortex',
                                   module = self
                                   )
        self.input_ports.append(self.ip_cortex)
        self.i_cortex = None

        self.op_polydata = OutputPort(
                                      data_type = polydata_trait,
                                      name = 'mapped cortex',
                                      module = self
                                      )
        self.output_ports.append(self.op_polydata)


    def update(self, input_port, old, new):
        if input_port == self.ip_dipole_sources:
            self.i_dipole_sources = input_port.data
        if input_port == self.ip_cortex:
            self.i_cortex = input_port.data
        if ( self.i_cortex != None) :
            self.procesar()

    @invoke_later
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
        self.op_polydata.update_data()


