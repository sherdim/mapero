from mapero.core.module import Module
from mapero.core.port import OutputPort, InputPort
from mapero.dataflow_editor.decorators.thread import invoke_later
from enthought.traits.api import Range, Int, Instance, File
from enthought.traits.ui.api import View, Group
from enthought.pyface.tvtk.decorated_scene import DecoratedScene
from enthought.tvtk.api import tvtk

import types

module_info = {'name': 'Visualization.vtkpolydatareader',
                'desc': "Module with cone source"}

class vtkpolydatareader(Module):
    """ modulo de prueba visual """
    vtk_file = File(filter=['*.vtk'])

    view = Group('vtk_file')


    def __init__(self, **traitsv):
        super(vtkpolydatareader, self).__init__(**traitsv)
        self.name = 'VTK Data Reader'
        self.out1 = OutputPort(
                                data_type = None,
                                name = 'out1',
                                module = self
                                )
        
        self.output_ports.append(self.out1)


    @invoke_later
    def process(self):
        print "processing ..."
        self.progress = 0

        self.poly = tvtk.PolyDataReader(file_name = self.vtk_file )
        print self.poly.file_name
        poly = self.poly.output

        self.progress = 100
        self.out1.data = self.poly.output

    def _vtk_file_changed(self):
        print "file changed "
        self.process()





