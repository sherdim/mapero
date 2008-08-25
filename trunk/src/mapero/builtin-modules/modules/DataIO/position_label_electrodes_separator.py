from mapero.core.api import Module
from mapero.core.api import OutputPort, InputPort
from numpy.oldnumeric.precision import Float
from enthought.traits.api import File, Array, List, Str
from enthought.traits.ui.api import  Group
from numpy import array, zeros, resize


module_info = {	"name": "DataIO.position_label_electrodes_separator",
				"desc": "aaa"}

class position_label_electrodes_separator(Module):
	"""  """
	file = File(filter=['*.txt'])

	def __init__(self, **traits):
		super(position_label_electrodes_separator, self).__init__(**traits)
		self.name = 'Position-Label Separator'
		point_set_trait = Array(typecode=Float, shape=(None,3))
		self.op_point_set = OutputPort(
									   data_types = point_set_trait,
									   name = 'array_output',
									   module = self
									   )
		self.output_ports.append(self.op_point_set)

		list_string_trait = List(Str)
		self.op_labels = OutputPort(
								    data_types = list_string_trait,
								    name = 'labels',
								    module = self
								    )
		self.output_ports.append(self.op_labels)

		electrode_names_trait = List(Str)
		self.ip_registration_electrode_names = InputPort(
														 data_types = electrode_names_trait,
														 name = 'reg electrode names',
														 module = self
														 )
		self.input_ports.append(self.ip_registration_electrode_names)
		self.i_registration_electrode_names = None

	def execute(self):
		if (new != old):
			self.i_registration_electrode_names = input_port.data
			self.process()

	def _file_changed(self):
		if (self.file != ''):
			self.process()
		else:
			self.op_point_set.data


	view = Group('file')


	#TODO: verify the correctness file format and add other formats
	def process(self):
		self.progress = 0
		f = open(self.file, "r", 0)
		i=1
		point_set = array(())
		labels = []
		electrode_names = self.i_registration_electrode_names
		print electrode_names
		for line in f:
			l_p = line.split()
			if (electrode_names == None) or ( electrode_names != None and l_p[0] in electrode_names ) :
				point_set = resize(point_set, (i,3))
				labels.append(l_p[0])
				point_set[i-1]= [ float(n) for n in l_p[1:4] ]
				i+=1

		self.op_point_set.data = point_set
		print "point_set.shape: ", point_set.shape
		self.op_labels.data = labels
		print "len(labels) : ", len(labels)
		print "labels que quedaron: ", labels

		self.progress = 100
