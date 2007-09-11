from mapero.core.module import Module
from mapero.core.port import OutputPort, InputPort
from numpy.oldnumeric.precision import Int
from enthought.traits.api import File, Array, List, Str
from enthought.traits.ui.api import  Group
from numpy import array, zeros, resize


module_info = {	"name": "DataIO.electrodes_labeler",
				"desc": "aaa"}

class electrodes_labeler(Module):
	"""  """
	file = File(filter=['*.txt'])

	view = Group('file')

	def start(self):
		self.name = 'Electrodes Labeler'

		list_string_trait = List(Str)
		self.ip_labels = InputPort(list_string_trait, 'labels', self)
		self.input_ports.append(self.ip_labels)
		self.i_labels = None

		point_set_trait = Array(typecode=Int, shape=(None,2))
		self.ip_map = InputPort(point_set_trait, 'map_point_set', self)
		self.input_ports.append(self.ip_map)
		self.i_map = None

		self.op_labels = OutputPort(list_string_trait, 'labels', self)
		self.output_ports.append(self.op_labels)

	def update(self, input_port, old, new):
		if input_port == self.ip_labels:
			self.i_labels = input_port.data
		if input_port == self.ip_map:
			self.i_map = input_port.data
		if (self.i_labels != None) and (self.i_map != None) and (self.file != ''):
			self.process()

	def _file_changed(self):
		if (self.i_labels != None) and (self.i_map != None) and (self.file != ''):
			self.process()


	def _process(self):
		map = self.i_map
		i_labels = self.i_labels
		print "labels: ", i_labels
		o_labels = []
		self.progress = 0

		for i in range(map.shape[0]):
			print "map[i]: ", map[i]
			o_labels.append(i_labels[(int)(map[i,1])])
		print o_labels

		labels_file = file(self.file, 'w')
		for label in o_labels:
			labels_file.write(label + '\n')

		self.progress = 100
		labels_file.close()



