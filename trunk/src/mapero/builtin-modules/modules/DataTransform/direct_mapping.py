from mapero.core.api import Module
from mapero.core.api import OutputPort, InputPort
from numpy.oldnumeric.precision import Float, Int
from enthought.traits.api import Any
from enthought.tvtk.api import tvtk
from numpy import ones, zeros, dot, take, argsort
import logging

log = logging.getLogger("mapero.logger.engine");

class direct_mapping(Module):
	""" direct_mapping module """

	label = 'Direct Mapping'
	
	ip_values_polydata = InputPort( trait = Any )
	ip_input_polydata = InputPort( trait = Any )
			
	op_polydata = OutputPort( trait = Any)
	def start_module(self):
		self.i_values_polydata = None
		self.i_input_polydata = None

	def execute(self):
		self.i_input_polydata = self.ip_input_polydata.data
		self.i_values_polydata = self.ip_values_polydata.data
		if (self.i_input_polydata != None) and ( self.i_values_polydata != None):
			self.procesar()

	def procesar(self):
		self.progress = 0
		log.debug("starting process")
		print "starting process"
		input = self.i_input_polydata
		values = self.i_values_polydata
		probe_filter = tvtk.ProbeFilter(input=input, source=values)
		log.debug("starting update")
		probe_filter.update()
		log.debug("finished update")
		print "finished process"
		
		self.op_polydata.data = probe_filter.output
		self.progress = 100
