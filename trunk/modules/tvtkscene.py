from mapero.core.module import VisualModule
from mapero.core.port import OutputPort
from mapero.core.port import InputPort , MultiInputPort
from enthought.traits.api import Range, Int, Instance
from enthought.traits.ui.api import View, Group, Item
from enthought.pyface.tvtk.decorated_scene import DecoratedScene
from enthought.pyface.tvtk.picker import Picker
from enthought.tvtk.api import tvtk
from enthought.enable2.wx_backend.api import Window
from enthought.enable2.api import Container
import wx

import re

import types

module_info = {	'name': 'visual.tvtkscene',
				'desc': "Module with a InputPort with test purpose"}

class tvtkscene(VisualModule):
	""" modulo de prueba visual """
	scene = Instance(DecoratedScene)
	view = Group(
			 Item('scene', label='', style='custom'),
					 label='Scene', show_labels=False)

	def __init__(self, **traits):
		super(tvtkscene, self).__init__(**traits)
		self.name = 'TVTK Scene'
		self.actors_pattern = "actors1"
		self.input_ports.append(MultiInputPort(types.IntType, self.actors_pattern, self))


	def update(self, input_port, old, new):
		self.progress = 0
		if (old == new) :
			pass
		else:
			if isinstance(input_port.data, list):
				print len(input_port.data)
				self.scene.add_actors(input_port.data)
			else:
				self.scene.add_actors([input_port.data])
		self.scene.render()
		self.progress = 100
		print "rerendered scene"


	def _create_window(self):
		self.scene = DecoratedScene(self.parent)
		return self.scene.control



