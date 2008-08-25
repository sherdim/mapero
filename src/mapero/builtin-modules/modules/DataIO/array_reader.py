from mapero.core.api import Module
from mapero.core.api import OutputPort
from enthought.traits.api import File, Array
from enthought.traits.ui.api import Group

from numpy import array, resize

class array_reader(Module):
	"""  """
	file = File(filter=["matrix text file [*.mat]", "*.mat", "text file [*.txt]", "*.txt"])

	label = 'Array Reader'
	array_output = OutputPort( trait = Array(dtype=float, shape=(None,None))  )
	
	view = Group('file')
	
	
	def start_module(self):
		self.a = array([[]], dtype=float)

	def _file_changed(self):
		self.process()

	def process(self):
		f = open(self.file, "r", 0)
		index = 0

		shape_known = False

		first_line = array(self.read_line(f))
		second_line =array(self.read_line(f))

		if first_line.shape == second_line.shape:
#			self.a = resize(self.a, (2,first_line.shape[1] and first_line.shape[1] or 1))
			self.a[0]=first_line
			self.a[1]=second_line
			index = 2
		else:
			shape_known = True
			self.a = resize(self.a, (first_line[0], first_line[1] and first_line[1] or 1))
			self.a[0]=second_line
			index = 1

		while(1):
			if shape_known:
				self.progress = index*100/self.a.shape[0]
			try:
				row =  self.read_line(f)
			except StopIteration:
				break
			self.a[index] = row
			index+=1

		self.progress = 100;
		self.array_output.data = self.a

	def read_line(self, file):
		string = file.next()
		if string.startswith('#'):
			if string.startswith('# rows'):
				rows = int(string.split()[2])
				self.a = resize(self.a, (rows, self.a.shape[1]))
				print "seteados los rows"
				print self.a.shape
			if string.startswith('# columns'):
				cols = int(string.split()[2])
				self.a = resize(self.a, (self.a.shape[0], cols) )
				print "seteados las cols"
				print self.a.shape
			return self.read_line(file)
		else:
			linea = [ float(n) for n in string.split() ]
			return  linea
