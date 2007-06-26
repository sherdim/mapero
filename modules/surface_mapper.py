from mapero.core.module import Module
from numpy.oldnumeric.precision import Float, Int
from mapero.core.port import OutputPort
from mapero.core.port import InputPort
from enthought.traits.api import Array, Trait, Instance
from enthought.traits.ui.api import Group
from enthought.tvtk.api import tvtk

from numpy import matrix, array, zeros
from scipy.linalg import pinv
from scipy import square, diag, identity

module_info = {'name': 'InverseSolution.surface_mapper',
					 'desc': ""}

class surface_mapper (Module):
	""" surface mapper """

 	mapper = Instance(tvtk.PolyDataMapper)
 	property = Instance(tvtk.Property)

 	view = Group('mapper','property')

	def start(self):
		self.name = 'Surface Mapper'

		dipole_sources_trait = Array(typecode=Float, shape=(None,None))
		self.ip_dipole_sources = InputPort(dipole_sources_trait, 'dipole source', self)
		self.input_ports.append(self.ip_dipole_sources)
		self.i_dipole_sources = None

		cortex_trait = Trait
		self.ip_cortex = InputPort(cortex_trait, 'cortex', self)
		self.input_ports.append(self.ip_cortex)
		self.i_cortex = None

		actor_trait = Trait
		self.op_actor = OutputPort(actor_trait, 'actor', self)
		self.output_ports.append(self.op_actor)

		self.mapper = tvtk.PolyDataMapper()
		self.actor = tvtk.Actor()
		self.property = tvtk.Property()
		self.actor.property = self.property


	def update(self, input_port, old, new):
		if input_port == self.ip_dipole_sources:
			self.i_dipole_sources = input_port.data
			print "nuevo dipole sources"
		if input_port == self.ip_cortex:
			self.i_cortex = input_port.data
		if (self.i_dipole_sources != None)  \
			and ( self.i_cortex != None) :
			self.process()

	def process(self):
		self.progress = 0
		cortex = self.i_cortex
		dipoles = array(self.i_dipole_sources)
#		dipoles = zeros(12670)
#		dipoles[8197] = 1
		print "surface mapper: process ..."

		cortex.point_data.scalars = dipoles[0:dipoles.shape[0],0]
		print "dipoles.shape: ", dipoles.shape
		self.mapper.input = cortex
		self.actor.mapper = self.mapper

		self.progress = 100
		self.op_actor.data = self.actor
		self.op_actor.update_data()


