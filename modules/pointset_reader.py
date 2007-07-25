from core.module import Module
from core.port import OutputPort, InputPort
from numpy.oldnumeric.precision import Float
from enthought.traits.api import File, Array
from enthought.traits.ui.api import  Group
from numpy import array, zeros, resize


module_info = {	"name": "DataIO.pointset_reader",
		"desc": "Module with an OutputPort for visualize pointset in a vtk scene"}

class pointset_reader(Module):
	"""  """
	file = File(filter=['*.pts'])

	def start(self):
		self.name = 'PointSet Reader'
		point_set_trait = Array(typecode=Float, shape=(None,3))
		self.op_point_set = OutputPort(point_set_trait, 'array_output', self)
		self.output_ports.append(self.op_point_set)

	def _file_changed(self):
		self.process()


	view = Group('file')


	#TODO: verify the correctness file format and add other formats
	def process(self):
		self.progress = 0
		read_line = lambda line: [ float(n) for n in line.split() ]
		f = open(self.file, "r", 0)
		cnt = int(f.readline())
		first_coord = f.readline()
		a = zeros((cnt,len(read_line(first_coord))))
		resize(a, (cnt,a.shape[0]))
		i=1
		a[0] = read_line(first_coord)
		for line in f:
			a[i] = read_line(line)
			i+=1

		self.op_point_set.data = a
		self.progress = 100






