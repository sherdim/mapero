from mapero.core.module import Module
from mapero.core.port import OutputPort, InputPort
from numpy.oldnumeric.precision import Float
from enthought.traits.api import File, Array, List, Str
from enthought.traits.ui.api import  Group
from numpy import array, zeros, resize


module_info = {	"name": "DataIO.text_file_reader",
				"desc": "aaa"}

class text_file_reader(Module):
	"""  """
	file = File(filter=['*.txt'])

	def __init__(self, **traits):
		super(text_file_reader, self).__init__(**traits)
		self.name = 'Text File Reader'

		list_string_trait = List(Str)
		self.op_lines = OutputPort(
								   data_type =  list_string_trait,
								   name = 'lines', 
								   module = self
								   )
		self.output_ports.append(self.op_lines)



	def _file_changed(self):
		if (self.file != ''):
			self.process()
		else:
			self.op_lines.data = None


	view = Group('file')


	#TODO: verify the correctness file format and add other formats
	def _process(self):
		self.progress = 0
		f = open(self.file, "r", 0)
		lines = []
		for line in f:
			lines.append(line.strip())

		self.progress = 100
		self.op_lines.data = lines

