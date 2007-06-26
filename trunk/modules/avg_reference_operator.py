from mapero.core.module import Module
from numpy.oldnumeric.precision import Float, Int
from mapero.core.port import OutputPort
from mapero.core.port import InputPort
from enthought.traits.api import Array, List, Str

from numpy import array, resize

module_info = {'name': 'InverseSolution.average_reference_operator',
				'desc': ""}

class average_reference_operator(Module):
	""" average reference operator """

	def start(self):
		self.name = 'Avg Ref Op'

		registration_values_trait = Array(typecode=Float, shape=(None,None))
		self.ip_registration_values = InputPort(registration_values_trait, 'registration values', self)
		self.input_ports.append(self.ip_registration_values)
		self.i_registration_values = None

		electrode_names_trait = List(Str)
		self.ip_registration_electrode_names = InputPort(electrode_names_trait, 'reg electrode names', self)
		self.input_ports.append(self.ip_registration_electrode_names)
		self.i_registration_electrode_names = None

		lead_field_trait = Array(typecode=Float, shape=(None,None))
		self.ip_lead_field = InputPort(lead_field_trait, 'lead field', self)
		self.input_ports.append(self.ip_lead_field)
		self.i_lead_field = None

		self.ip_lead_field_electrode_names = InputPort(electrode_names_trait, 'lead field electrode names', self)
		self.input_ports.append(self.ip_lead_field_electrode_names)
		self.i_lead_field_electrode_names = None

		self.op_registration_values_avg = OutputPort(registration_values_trait, 'registration values avg', self)
		self.output_ports.append(self.op_registration_values_avg)

		self.op_lead_field_avg = OutputPort(lead_field_trait, 'lead field avg', self)
		self.output_ports.append(self.op_lead_field_avg)

	def update(self, input_port, old, new):
		if input_port == self.ip_registration_values:
			self.i_registration_values = input_port.data
		if input_port == self.ip_lead_field:
			self.i_lead_field = input_port.data
		if input_port == self.ip_registration_electrode_names:
			self.i_registration_electrode_names = input_port.data
		if input_port == self.ip_lead_field_electrode_names:
			self.i_lead_field_electrode_names = input_port.data
		if (self.i_registration_values != None)  \
			and ( self.i_lead_field != None) \
			and (self.i_registration_electrode_names != None) \
			and (self.i_lead_field_electrode_names != None):
			self.process()

	def _process(self):
		self.progress = 0
		i_registration_values = self.i_registration_values
		i_lead_field = self.i_lead_field
		i_registration_electrode_names = self.i_registration_electrode_names
		i_lead_field_electrode_names = self.i_lead_field_electrode_names

		i_reg_cols = i_registration_values.shape[1]
		i_lead_cols = i_lead_field.shape[1]
		o_registration_values_avg = array(())
		o_lead_field_avg = array(())

		row_counter = 0
		reg_row_counter = 0
		for reg_name in i_registration_electrode_names:
			lead_row_counter = 0
			for lead_name in i_lead_field_electrode_names:
				if reg_name == lead_name:
					o_registration_values_avg = resize(o_registration_values_avg, (row_counter+1, i_reg_cols))
					o_lead_field_avg = resize(o_lead_field_avg, (row_counter+1, i_lead_cols))
					print "electrode name: ", reg_name
					print "o_registration_values_avg.shape: " , o_registration_values_avg.shape
					print "o_lead_field_avg.shape: ", o_lead_field_avg.shape
					print "row_counter: ", row_counter
					print "reg_row_counter: ", reg_row_counter
					print "lead_row_counter: ", lead_row_counter
					o_registration_values_avg[row_counter] = i_registration_values[reg_row_counter]
					o_lead_field_avg[row_counter] = i_lead_field[lead_row_counter]
					row_counter += 1
				lead_row_counter += 1
			reg_row_counter += 1


		o_registration_values_avg = \
			o_registration_values_avg - o_registration_values_avg.mean(0)

		o_lead_field_avg = \
			o_lead_field_avg - o_lead_field_avg.mean(0)


		print "o_registration_values_avg: ", o_registration_values_avg
		print "o_lead_field_avg", o_lead_field_avg
		self.op_registration_values_avg.data = o_registration_values_avg
		self.op_lead_field_avg.data = o_lead_field_avg
		self.progress = 100










