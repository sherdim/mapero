from core.module import Module
from core.port import OutputPort, InputPort
from numpy.oldnumeric.precision import Float, Int
from enthought.traits.api import Array, Enum
from enthought.traits.ui.api import Group

from numpy import matrix, array
from scipy.linalg import pinv
from scipy import square, diag, identity

module_info = {'name': 'InverseSolution.binary_operator',
					 'desc': ""}

class binary_operator (Module):
	""" inverse solution """

	operator = Enum("x", "+", "-")

	view = Group('operator')

	def start(self):
		self.name = 'Binary Operator'

		matrix_trait = Array(typecode=Float, shape=(None,None))
		self.ip_first_matrix = InputPort(matrix_trait, 'first matrix', self)
		self.input_ports.append(self.ip_first_matrix)
		self.i_first_matrix = None

		self.ip_second_matrix = InputPort(matrix_trait, 'second matrix', self)
		self.input_ports.append(self.ip_second_matrix)
		self.i_second_matrix = None


		self.op_output_matrix = OutputPort(matrix_trait, 'output matrix', self)
		self.output_ports.append(self.op_output_matrix)


	def update(self, input_port, old, new):
		if input_port == self.ip_first_matrix:
			self.i_first_matrix = input_port.data
		if input_port == self.ip_second_matrix:
			self.i_second_matrix = input_port.data
		if (self.i_first_matrix != None)  \
			and ( self.i_second_matrix != None) :
			self.process()

	def _process(self):
		self.progress = 0
		op1 = matrix(self.i_first_matrix)
		op2 = matrix(self.i_second_matrix)
		result = None

		print "op1.shape: ", op1.shape
		print "op2.shape: ", op2.shape

		if self.operator == "x":
			result = op1 * op2
		if self.operator == "+":
			result = op1 + op2
		if self.operator == "-":
			result = op1 - op2

		self.progress = 100
		print "max: ", result.max()
		print "min: ", result.min()
		self.op_output_matrix.data = result


	def _operator_changed(self):
		self.process()
