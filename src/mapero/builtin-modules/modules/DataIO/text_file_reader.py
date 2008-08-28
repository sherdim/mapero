from mapero.core.api import Module
from mapero.core.api import OutputPort, InputPort
from numpy.oldnumeric.precision import Float
from enthought.traits.api import File, Array, List, Str
from enthought.traits.ui.api import  Group
from numpy import array, zeros, resize

class text_file_reader(Module):
	""" Text File Reader """

	file = File(filter=['*.txt'])
	view = Group('file')


	label = 'Text File Reader'
	
	### Output port
	op_lines = OutputPort( trait = List(Str) )


	def _file_changed(self):
		if (self.file != ''):
			self.process()
		else:
			self.op_lines.data = None

	def process(self):
		self.progress = 0
		f = open(self.file, "r", 0)
		lines = []
		for line in f:
			lines.append(line.strip())

		self.progress = 100
		self.op_lines.data = lines

