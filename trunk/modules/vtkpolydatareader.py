from mapero.core.module import Module
from mapero.core.port import OutputPort
from mapero.core.port import InputPort
from enthought.traits.api import Range, Int, Instance, File
from enthought.traits.ui.api import View, Group
from enthought.pyface.tvtk.decorated_scene import DecoratedScene
from enthought.tvtk.api import tvtk

import types

module_info = {'name': 'visual.vtkpolydatareader',
				 'desc': "Module with cone source"}

class vtkpolydatareader(Module):
	""" modulo de prueba visual """
	VTK_File = File(filter=['*.vtk'])

	view = Group('VTK_File')


	def start(self):
		self.name = 'VTK Data Reader'
		self.output_ports.append(OutputPort(types.IntType, 'salida1' ,self))


	def _process(self):
		self.progress = 0

		self.poly = tvtk.PolyDataReader(file_name = self.VTK_File )
		print self.poly.file_name
#		m = tvtk.PolyDataMapper(input=self.poly.output)
#		p = tvtk.Property()
#		self.actor = tvtk.Actor(mapper=m, property=p)
		poly = self.poly.output
		poly.update()
		print poly

		polys = poly.polys
		polys.init_traversal()

		npts = 0
		pts  = 0
		print polys.to_array()


		self.progress = 100
		self.get_output('salida1').data = self.poly.output

	def _VTK_File_changed(self):
		self.process()





