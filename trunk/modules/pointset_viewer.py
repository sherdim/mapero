from core.module import Module
from core.port import OutputPort, InputPort
from numpy.oldnumeric.precision import Float
from enthought.traits.api import Range, Array
from enthought.traits.ui.api import Group
from enthought.tvtk.api import tvtk
from enthought.tvtk.tvtk_base import vtk_color_trait

module_info = {'name': 'visualization.pointset_viewer',
				 'desc': "read an array of points in its array_input port and generate sphere actors in its actors_output"}

class pointset_viewer(Module):
	""" modulo de prueba uno """
	radius = Range(1.0, 10.0, 2.0)
	color = vtk_color_trait((1.0, 1.0, 1.0))

	def start(self):
		self.name = 'Point Set Viewer'

		point_set_trait = Array(typecode=Float, shape=(None,3))
		self.ip_point_set = InputPort(point_set_trait, 'array_input', self)
		self.input_ports.append(self.ip_point_set)

		self.op_actors = OutputPort(point_set_trait, 'actors_output',self)
		self.output_ports.append(self.op_actors)
		self.sphere_sources = []
		self.properties = []

	def update(self, input_port, old, new):
		if (input_port == self.get_input('array_input')):
			if (input_port.data != None and input_port.data != []):
				self.process()
			else:
				self.progress = 0
				self.get_output('actors_output').data = None

	def _process(self):
		input_array = self.get_input('array_input').data
		self.progress = 0
		progress_step = 100/input_array.shape[0]
		actors = []
		self.sphere_sources = []
		self.properties = []
		for i in range(input_array.shape[0]):
			sphere_source = tvtk.SphereSource(center=tuple(input_array[i]), radius=self.radius)
			mapper = tvtk.PolyDataMapper(input=sphere_source.output)
			property = tvtk.Property(color=self.color)
			actor = tvtk.Actor(mapper=mapper, property=property)
			actors.append(actor)
			self.progress += progress_step
			self.properties.append(property)
			self.sphere_sources.append(sphere_source)
		self.op_actors.data = actors
		self.progress = 100

	def _color_changed(self):
		for property in self.properties:
			property.color = self.color
		self.op_actors.update_data()

	def _radius_changed(self):
		for sphere_source in self.sphere_sources:
			sphere_source.radius=self.radius
		self.op_actors.update_data()

	#view = Group('parametro', 'caca')
	view = Group('radius', 'color')



