from mapero.core.connection import Connection
from mapero.core.module import Module
from enthought.traits.api import HasTraits,  List

class Network(HasTraits):
	""" Network Class """

	modules = List(Module)
	connections = List(Connection)

	def __init__(self, **traits):
		super(Network, self).__init__(**traits)
