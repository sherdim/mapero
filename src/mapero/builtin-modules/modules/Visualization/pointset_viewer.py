from mapero.core.module import Module
from mapero.core.port import OutputPort, InputPort
from mapero.dataflow_editor.decorators.thread import threaded_process
from numpy.oldnumeric.precision import Float
from enthought.traits import api as traits
from enthought.traits.ui.api import Group
from enthought.tvtk.api import tvtk
from enthought.tvtk.tvtk_base import vtk_color_trait

module_info = {'name': 'Visualization.pointset_viewer',
				 'desc': "read an array of points in its array_input port and generate sphere actors in its actors_output"}

class pointset_viewer(Module):
	""" modulo de prueba uno """
	radius = traits.Range(1.0, 10.0, 2.0)
	color = vtk_color_trait((1.0, 1.0, 1.0))

	def __init__(self, **traits):
		super(pointset_viewer, self).__init__(**traits)
		self.name = 'Point Set Viewer'

		point_set_trait = traits.Array(typecode=Float, shape=(None,3))
		self.ip_point_set = InputPort(
									  data_types = point_set_trait,
									  name = 'array_input',
									  module = self
									  )
		self.input_ports.append(self.ip_point_set)

		self.op_actors = OutputPort(
								    data_types = point_set_trait,
								    name = 'actors_output',
								    module = self
								    )
		self.output_ports.append(self.op_actors)
		self.sphere_sources = []
		self.properties = []

	def execute(self):
		if (input_port == self.get_input('array_input')):
			if (input_port.data != None and input_port.data != []):
				self.process()
			else:
				self.progress = 0
				self.get_output('actors_output').data = None

	def process(self):
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



