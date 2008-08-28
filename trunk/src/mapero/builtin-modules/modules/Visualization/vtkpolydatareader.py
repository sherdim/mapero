from mapero.core.api import Module
from mapero.core.api import OutputPort, InputPort
from enthought.traits.api import Range, Int, Instance, File, Any
from enthought.traits.ui.api import View, Group
from enthought.tvtk.api import tvtk

import types

module_info = {'name': 'Visualization.vtkpolydatareader',
                'desc': "Module with cone source"}

class vtkpolydatareader(Module):
    """ modulo de prueba visual """

    label = 'VTK Data Reader'
    
    vtk_file = File(filter=['*.vtk'])

    view = Group('vtk_file')

    out1 = OutputPort( trait = Any )

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





