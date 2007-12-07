from mapero.core.module import Module
from mapero.core.port import OutputPort, InputPort
from mapero.dataflow_editor.decorators.thread import threaded_process
from numpy.oldnumeric.precision import Float, Int
from enthought.traits.api import Array, List, Str
from numpy import ones, zeros, dot, take, argsort

module_info = {	"name": "DataTransform.closest_point_finder",
				"desc": ""}

class closest_point_finder(Module):
	"""  """

	def __init__(self, **traits):
		super(closest_point_finder, self).__init__(**traits)
		self.name = 'Closest Point Finder'
		map_trait = Array(typecode=Int, shape=(None,2))
		self.op_map = OutputPort(
								 data_type = map_trait,
								 name = 'array_output',
								 module = self
								 )
		self.output_ports.append(self.op_map)

		point_set_trait = Array(typecode=Float, shape=(None,3))
		self.ip_from_point_set = InputPort(
										   data_type = point_set_trait,
										   name = 'point_set1',
										   module = self
										   )
		self.input_ports.append(self.ip_from_point_set)
		self.i_to_point_set = None

		self.ip_to_point_set = InputPort(
										 data_type = point_set_trait,
										 name = 'point_set2',
										 module = self
										 )
		self.input_ports.append(self.ip_to_point_set)
		self.i_from_point_set = None


	def update(self, input_port, old, new):
		if input_port == self.ip_from_point_set:
			self.i_from_point_set = input_port.data
		if input_port == self.ip_to_point_set:
			self.i_to_point_set = input_port.data
		if (self.i_from_point_set != None) and ( self.i_to_point_set != None):
			self.process()

	@threaded_process
	def process(self):
		from_point_set = self.i_from_point_set
		to_point_set = self.i_to_point_set

		swapped = (from_point_set.shape[0] > to_point_set.shape[0])  and True or False

		if swapped:
			temp_from = from_point_set
			temp_to = to_point_set
			to_point_set = temp_from
			from_point_set = temp_to

		o_map = -1 * ones((from_point_set.shape[0],2))

		def distance(from_index, to_index):
			from_point  = from_point_set[from_index]
			to_point  =to_point_set[to_index]
			diff = from_point - to_point
			dist = dot(diff, diff)
			return dist

		def sort_distances(from_index):
			distances = zeros((to_point_set.shape[0], 2))
			for index in range(to_point_set.shape[0]):
				distances[index] = [index, distance(from_index, index)]
			arg =  argsort(distances[:,1])
			distances = take(distances, arg, 0)
			return distances

		def taken_point(to_index):
			for index in range(o_map.shape[0]):
				if o_map[index,1] == to_index:
					return o_map[index,0]
			return False

		def is_taken_point(to_index):
			if (taken_point(to_index) != False):
				return True
			else:
				return False

		def map_point(from_index):
			distances = sort_distances(from_index)
			select_to = 0
			to_point_index = distances[select_to,0]
			while (is_taken_point(to_point_index)):
				other_from_point_index = taken_point(to_point_index)

				from_distance = distance(from_index, to_point_index)
				other_distance = distance(other_from_point_index, to_point_index)
				if from_distance < other_distance:
					o_map[other_from_point_index] = [-1, -1] #unset the other point
					o_map[from_index] = [from_index, to_point_index]
					map_point(other_from_point_index)
				else:
					select_to += 1
					to_point_index = distances[select_to,0]

			o_map[from_index] = [from_index, to_point_index]

		for index in range(from_point_set.shape[0]):
			map_point(index)
			self.progress = index * 100 / from_point_set.shape[0]
		if swapped:
			o_map = o_map.take((1,0), 1)

		print "o_map.shape: ", o_map.shape
		print "o_map: ", o_map
		self.progress = 100
		self.op_map.data = o_map
