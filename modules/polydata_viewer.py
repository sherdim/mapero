from core.module import Module
from core.port import OutputPort, InputPort
from numpy.oldnumeric.precision import Float
from enthought.traits import api as traits
from enthought.traits.ui.api import Group
from enthought.tvtk.api import tvtk
from enthought.tvtk.tvtk_base import vtk_color_trait

module_info = {'name': 'visualization.polydata_viewer',
                 'desc': ""}

class polydata_viewer(Module):
    """ modulo de prueba uno """

    color = vtk_color_trait((1.0, 1.0, 1.0))
    view = Group('color')
    
    def start(self):
        self.name = 'Point Set Viewer'

        polydata_trait = traits.Trait(tvtk.PolyData)
        self.ip_polydata = InputPort(polydata_trait, 'polydata_input', self)
        self.input_ports.append(self.ip_polydata)

        self.op_actor = OutputPort(polydata_trait, 'actors_output',self)
        self.output_ports.append(self.op_actor)

    def update(self, input_port, old, new):
        if (input_port == self.get_input('polydata_input')):
            if (input_port.data != None and input_port.data != []):
                self.process()
            else:
                self.progress = 0
                self.get_output('actors_output').data = None

    def _process(self):
        input_array = self.get_input('polydata_input').data
        self.progress = 0    
        mapper = tvtk.PolyDataMapper(input=input_array)
        self.property = tvtk.Property(color=self.color)
        actor = tvtk.Actor(mapper=mapper, property=self.property)
        self.op_actor.data = actor
        self.progress = 100

    def _color_changed(self):
        self.property.color = self.color
        self.op_actor.update_data()

