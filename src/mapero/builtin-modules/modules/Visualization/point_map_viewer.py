from mapero.core.module import Module
from mapero.core.port import OutputPort, InputPort
from numpy.oldnumeric.precision import Float, Int
from enthought.traits.api import Range, Array
from enthought.traits.ui.api import Group
from enthought.tvtk.api import tvtk
from enthought.tvtk.tvtk_base import  vtk_color_trait

module_info = {'name': 'Visualization.point_map_viewer',
								 'desc': ""}

class point_map_viewer(Module):
	""" modulo de prueba uno """
	radius = Range(1.0, 10.0, 2.0)
	color = vtk_color_trait((1.0, 1.0, 1.0))

	def start(self):
		self.name = 'Point Map Viewer'

		point_set_trait = Array(typecode=Float, shape=(None,3))
		self.ip_from_point_set = InputPort(point_set_trait, 'from_point_set', self)
		self.input_ports.append(self.ip_from_point_set)
		self.i_to_point_set = None

		self.ip_to_point_set = InputPort(point_set_trait, 'to_point_set', self)
		self.input_ports.append(self.ip_to_point_set)
		self.i_from_point_set = None

		point_set_trait = Array(typecode=Int, shape=(None,2))
		self.ip_map = InputPort(point_set_trait, 'map_point_set', self)
		self.input_ports.append(self.ip_map)
		self.i_map = None

		self.op_actors = OutputPort(point_set_trait, 'actors_output', self)
		self.output_ports.append(self.op_actors)

		self.line_sources = []
		self.properties = []

	def update(self, input_port, old, new):
		if input_port == self.ip_from_point_set:
			self.i_from_point_set = input_port.data
		if input_port == self.ip_to_point_set:
			self.i_to_point_set = input_port.data
		if input_port == self.ip_map:
			self.i_map = input_port.data
		if (self.i_from_point_set != None) and ( self.i_to_point_set != None) \
										and (self.i_map != None):
			self.process()

	def process(self):
		from_point_set = self.i_from_point_set
		to_point_set = self.i_to_point_set
		map = self.i_map
		self.progress = 0
		progress_step = 100/from_point_set.shape[0]
		actors = []
		self.line_sources = []
		self.properties = []
		for i in range(map.shape[0]):
			from_point = tuple(from_point_set[map[i,0]])
			to_point = tuple(to_point_set[map[i,1]])
			print from_point, "  --> ", to_point
			line_source = tvtk.LineSource(point1=from_point, point2=to_point)
			mapper = tvtk.PolyDataMapper(input=line_source.output)
			property = tvtk.Property(color=self.color)
			actor = tvtk.Actor(mapper=mapper, property=property)
			actors.append(actor)
			self.progress += progress_step
			self.properties.append(property)
			self.line_sources.append(line_source)
		self.op_actors.data = actors
		self.progress = 100

	def _color_changed(self):
		for property in self.properties:
			property.color = self.color
		self.get_output('actors_output').update_data()

	def _radius_changed(self):
		for line_source in self.line_sources:
			line_source.radius=self.radius
		self.get_output('actors_output').update_data()

			#view = Group('parametro', 'caca')
	view = Group('radius', 'color')

