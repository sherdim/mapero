from mapero.core.module import Module
from mapero.core.port import OutputPort, InputPort
from numpy.oldnumeric.precision import Float
from enthought.traits.api import Array
from numpy import zeros, dot

module_info = {	"name": "DataTransform.transform",
				"desc": "Module with an OutputPort for visualize pointset in a vtk scene"}

class transform(Module):
	"""  """

	def start(self):
		self.name = 'Geometric Mapper'
		self.op_point_set = OutputPort(list, 'array_output',self)
		self.output_ports.append(self.op_point_set)

		matrix_trait = Array(typecode=Float, shape=(4,4))
		self.ip_matrix = InputPort(matrix_trait, 'matrix_map', self)
		self.input_ports.append(self.ip_matrix)
		self.matrix = None

		point_set_trait = Array(typecode=Float, shape=(None,3))
		self.ip_point_set = InputPort(point_set_trait, 'point_set', self)
		self.input_ports.append(self.ip_point_set)
		self.i_point_set = None

	def update(self, input_port, old, new):
		if input_port == self.ip_point_set:
			self.i_point_set = input_port.data
		if input_port == self.ip_matrix:
			self.matrix = input_port.data
		if (self.matrix != None) and ( self.i_point_set != None):
			self.process()


	#TODO: y_i = a_i*x+b_i
	def process(self):
		o_point_set = zeros(self.i_point_set.shape)
		a0 = self.matrix[0,0:3]
		a1 = self.matrix[1,0:3]
		a2 = self.matrix[2,0:3]
		b0 = self.matrix[0,3]
		b1 = self.matrix[1,3]
		b2 = self.matrix[2,3]
		for i in range(self.i_point_set.shape[0]):
			y0 = dot(a0,self.i_point_set[i]) + b0
			y1 = dot(a1,self.i_point_set[i]) + b1
			y2 = dot(a2,self.i_point_set[i]) + b2
			o_point_set[i] = [y0, y1, y2]
			self.progress = i * 100 / self.i_point_set.shape[0]

		self.progress = 100
		self.op_point_set.data = o_point_set


