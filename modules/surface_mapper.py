from core.module import Module
from core.port import OutputPort, InputPort
from numpy.oldnumeric.precision import Float, Int
from enthought.traits import api as traits
from enthought.traits.ui.api import Group
from enthought.tvtk.api import tvtk

from numpy import matrix, array, zeros
from scipy.linalg import pinv
from scipy import square, diag, identity

module_info = {'name': 'InverseSolution.surface_mapper',
                    'desc': ""}

class surface_mapper (Module):
    """ surface mapper """

    def start(self):
        self.name = 'Surface Mapper'

        dipole_sources_trait = traits.Array(typecode=Float, shape=(None,None))
        self.ip_dipole_sources = InputPort(dipole_sources_trait, 'dipole source', self)
        self.input_ports.append(self.ip_dipole_sources)
        self.i_dipole_sources = None
        
        polydata_trait = traits.Trait(tvtk.PolyData)
        self.ip_cortex = InputPort(polydata_trait, 'cortex', self)
        self.input_ports.append(self.ip_cortex)
        self.i_cortex = None

        self.op_polydata = OutputPort(polydata_trait, 'mapped cortex', self)
        self.output_ports.append(self.op_polydata)


    def update(self, input_port, old, new):
        if input_port == self.ip_dipole_sources:
            self.i_dipole_sources = input_port.data
        if input_port == self.ip_cortex:
            self.i_cortex = input_port.data
        if ( self.i_cortex != None) :
            self.process()

    def _process(self):
        self.progress = 0
        ocortex = self.i_cortex
        if (self.i_dipole_sources != None):
            dipoles = array(self.i_dipole_sources)
#        dipoles = zeros(12670)
#        dipoles[8197] = 1
            print "surface mapper: process ..."

            ocortex.point_data.scalars = dipoles[0:dipoles.shape[0],0]
            print "dipoles.shape: ", dipoles.shape

        self.progress = 100
        self.op_polydata.data = ocortex
        self.op_polydata.update_data()


