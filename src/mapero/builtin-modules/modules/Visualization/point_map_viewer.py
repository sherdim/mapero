from mapero.core.module import Module
from mapero.core.port import OutputPort, InputPort
from numpy.oldnumeric.precision import Float, Int
from enthought.traits import api as traits
from enthought.traits.ui.api import Group
from enthought.tvtk.api import tvtk
from enthought.tvtk.tvtk_base import  vtk_color_trait

module_info = {'name': 'Visualization.point_map_viewer',
								 'desc': ""}

class point_map_viewer(Module):
	""" modulo de prueba uno """
	radius = traits.Range(1.0, 10.0, 2.0)
	color = vtk_color_trait((1.0, 1.0, 1.0))

	def __init__(self, **traitsv):
		super(point_map_viewer, self).__init__(**traitsv)
		self.name = 'Point Map Viewer'

		point_set_trait = Array(typecode=Float, shape=(None,3))
		self.ip_from_point_set = InputPort(
										   data_types = point_set_trait,
										   name = 'from_point_set',
										   module = self
										   )
		self.input_ports.append(self.ip_from_point_set)
		self.i_to_point_set = None

		self.ip_to_point_set = InputPort(
										 data_types = point_set_trait,
										 name = 'to_point_set',
										 module = self
										 )
		self.input_ports.append(self.ip_to_point_set)
		self.i_from_point_set = None

		point_set_trait = Array(typecode=Int, shape=(None,2))
		self.ip_map = InputPort(
							    data_types = point_set_trait,
							    name = 'map_point_set',
							    module = self
							    )
		self.input_ports.append(self.ip_map)
		self.i_map = None

		self.op_actors = OutputPort(
								    data_types = point_set_trait,
								    name = 'actors_output',
								    module = self
								    )
		self.output_ports.append(self.op_actors)

		self.line_sources = []
		self.properties = []

	def execute(self):
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

