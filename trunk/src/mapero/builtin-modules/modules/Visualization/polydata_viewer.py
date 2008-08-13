from mapero.core.module import Module
from mapero.core.port import OutputPort, InputPort
from numpy.oldnumeric.precision import Float
from enthought.traits import api as traits
from enthought.enable2.traits import api as enable_traits  
from enthought.traits.ui.api import Group, Item
from enthought.traits.ui.api import ListEditor
from enthought.tvtk.api import tvtk
from enthought.tvtk.tvtk_base import vtk_color_trait

import logging
log = logging.getLogger("mapero.logger.module");

module_info = {'name': 'Visualization.polydata_viewer',
                 'desc': ""}

class polydata_viewer(Module):
    """ modulo de prueba uno """

#    lookup_color_list = traits.List(enable_traits.RGBAColor)
    color_1 = enable_traits.RGBAColor('red')
    color_2 = enable_traits.RGBAColor('white')
    color_3 = enable_traits.RGBAColor('blue')
    low_scalar = traits.Float
    high_scalar = traits.Float
    view = Group(
                             Item('color_1',
                                   style='custom'),
                              Item('color_2',
                                   style='custom'),
                              Item('color_3',
                                   style='custom'),
                  'low_scalar' ,
                  'high_scalar'
                  )
    
    def __init__(self, **traitsv):
        super(polydata_viewer, self).__init__(**traitsv)
        self.name = 'Point Set Viewer'

        polydata_trait = traits.Trait(tvtk.PolyData)
        polydata_trait = None
        self.ip_polydata = InputPort(
                                     data_types = polydata_trait,
                                     name = 'polydata_input',
                                     module = self
                                     )
        self.input_ports.append(self.ip_polydata)

        self.op_actor = OutputPort(
                                   data_types = polydata_trait,
                                   name = 'actors_output',
                                   module = self
                                   )
        self.output_ports.append(self.op_actor)
        self.actor = None
        self.lookup_table = None
        self.colors = [(1.0, 0.0, 0.0, 1.0),(0.5, 0.5, 0.5, 1.0),(0.0, 0.0, 0.1, 1.0)]
        
        self.low_scalar = 0
        self.high_scalar = 100
        self.recalc_lt()
        
    def execute(self):
        if (self.ip_polydata.data != None and self.ip_polydata.data != []):
            self.process()
        else:
            self.progress = 0
            self.op_actor.data = None

    def process(self):
        input_array = self.ip_polydata.data
        self.progress = 0    
        self.mapper = tvtk.PolyDataMapper(input=input_array)
        if self.lookup_table:
            self.mapper.lookup_table = self.lookup_table
        self.property = tvtk.Property()
        self.actor = tvtk.Actor(mapper=self.mapper, property=self.property)
        self.actor.mapper.scalar_range=(self.low_scalar, self.high_scalar)
        self.op_actor.data = self.actor
        self.progress = 100
    
    def _color_1_changed(self, value):
        print "color1: ",value
        self.colors[0] = value
        self.recalc_lt()
    def _color_2_changed(self, value):
        print "color2: ",value
        self.colors[1] = value
        self.recalc_lt()
    def _color_3_changed(self, value):
        print "color3: ",value
        self.colors[2] = value
        self.recalc_lt()
        
#    def _lookup_color_list_changed(self, value):
#        self.colors = value
#        self.recalc_lt()
#        
#    def _lookup_color_list_items_changed(self, event):
#        self.recalc_lt()
#        
    def recalc_lt(self):
        number_of_colors = 256
         
        colors_cnt = 0
        for color in self.colors:
            if  isinstance(color, tuple) and len(color)==4:
                colors_cnt += 1
            
        if colors_cnt >= 2:
            self.lookup_table = tvtk.LookupTable()
            self.lookup_table.number_of_colors = colors_cnt
        
            r_colors = number_of_colors/colors_cnt -1
            r_colors = 1
            log.debug("number of colors: %s" , colors_cnt)
            log.debug("colors: %s" , self.colors)

            i = 0
            for color in self.colors:
                if  isinstance(color, tuple) and len(color)==4:
                    self.lookup_table.set_table_value(i*r_colors, color[0] , color[1] , color[2], color[3])
                    i += 1
            
            if self.actor:
                self.actor.mapper.lookup_table = self.lookup_table
            
    def _low_scalar_changed(self, value):
        if self.actor:
            self.actor.mapper.scalar_range=(value, self.high_scalar)
            
    def _high_scalar_changed(self, value):
        if self.actor:
            self.actor.mapper.scalar_range=(self.low_scalar, value)
        
                