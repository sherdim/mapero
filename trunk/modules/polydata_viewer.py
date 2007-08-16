from core.module import Module
from core.port import OutputPort, InputPort
from numpy.oldnumeric.precision import Float
from enthought.traits import api as traits
from enthought.traits.ui.api import Group, Item
from enthought.traits.ui.api import ListEditor
from enthought.tvtk.api import tvtk
from enthought.tvtk.tvtk_base import vtk_color_trait

module_info = {'name': 'visualization.polydata_viewer',
                 'desc': ""}

class polydata_viewer(Module):
    """ modulo de prueba uno """

    color = vtk_color_trait((1.0, 1.0, 1.0))
    lookup_color_list = traits.List(traits.Color)
    low_scalar = traits.Float
    high_scalar = traits.Float
    view = Group(Item('lookup_color_list', resizable=True, height=300), 'low_scalar' ,'high_scalar')
    
    def start(self):
        self.name = 'Point Set Viewer'

        polydata_trait = traits.Trait(tvtk.PolyData)
        self.ip_polydata = InputPort(polydata_trait, 'polydata_input', self)
        self.input_ports.append(self.ip_polydata)

        self.op_actor = OutputPort(polydata_trait, 'actors_output',self)
        self.output_ports.append(self.op_actor)
        self.actor = None
        self.lookup_table = None
        self.colors = []

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
        self.mapper = tvtk.PolyDataMapper(input=input_array)
        if self.lookup_table:
            self.mapper.lookup_table = self.lookup_table
        self.property = tvtk.Property(color=self.color)
        self.actor = tvtk.Actor(mapper=self.mapper, property=self.property)
        self.op_actor.data = self.actor
        self.progress = 100

    def _lookup_color_list_changed(self, value):
        self.colors = value
        self.recalc_lt()
        
    def _lookup_color_list_items_changed(self, event):
        self.recalc_lt()
        
    def recalc_lt(self):
        number_of_colors = 256
#        print event.added
#        if event.added:
#            for color in event.added:
#                self.colors.insert(event.index, color )
#        if event.removed:
#            self.colors.remove(event.removed )
#            
        colors_cnt = len(self.colors)
        if colors_cnt >= 2:
            self.lookup_table = tvtk.LookupTable()
            self.lookup_table.number_of_colors = colors_cnt
        
            r_colors = number_of_colors/colors_cnt -1
            r_colors = 1
            for i in range(colors_cnt):
                red = self.colors[i].Red()/255
                green = self.colors[i].Green()/255
                blue = self.colors[i].Blue()/255
                self.lookup_table.set_table_value(i*r_colors, red , green , blue, 1)
            
            if self.actor:
                self.actor.mapper.lookup_table = self.lookup_table
            
    def _low_scalar_changed(self, value):
        if self.actor:
            self.actor.mapper.scalar_range=(value, self.high_scalar)
            
    def _high_scalar_changed(self, value):
        if self.actor:
            self.actor.mapper.scalar_range=(self.low_scalar, value)
        
                