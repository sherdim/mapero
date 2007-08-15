from core.module import Module
from core.port import OutputPort, InputPort
from numpy.oldnumeric.precision import Float, Int
from enthought.traits import api as traits
from enthought.tvtk.api import tvtk
from numpy import ones, zeros, dot, take, argsort
import logging

log = logging.getLogger("mapero.logger.engine");

module_info = {	"name": "DataTransform.direct_mapping",
				"desc": ""}

class direct_mapping(Module):
	"""  """

	def start(self):
		self.name = 'Direct Mapping'

		polydata_trait = traits.Trait(tvtk.PolyData)
		self.ip_input_polydata = InputPort(polydata_trait, 'geometry', self)
		self.input_ports.append(self.ip_input_polydata)
		self.i_input_polydata = None

		self.ip_values_polydata = InputPort(polydata_trait, 'values', self)
		self.input_ports.append(self.ip_values_polydata)
		self.i_values_polydata = None

		self.op_polydata = OutputPort(polydata_trait, 'polydata', self)
		self.output_ports.append(self.op_polydata)


	def update(self, input_port, old, new):
		if input_port == self.ip_input_polydata:
			self.i_input_polydata = input_port.data
		if input_port == self.ip_values_polydata:
			self.i_values_polydata = input_port.data
		if (self.i_input_polydata != None) and ( self.i_values_polydata != None):
			self.process()


	def _process(self):
		self.progress = 0
		log.debug("starting process")
		input = self.i_input_polydata
		values = self.i_values_polydata
		probe_filter = tvtk.ProbeFilter(input=input, source=values)
		log.debug("starting update")
		probe_filter.update()
		log.debug("finished update")
		log.debug(probe_filter.output.point_data.scalars)
		
		self.op_polydata.data = probe_filter.output
		self.progress = 100
