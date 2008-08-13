from mapero.core.module import VisualModule
from mapero.core.port import OutputPort, InputPort
from numpy.oldnumeric.precision import Float
from enthought.traits import api as traits
from enthought.traits.ui.api import Group
from enthought.chaco.api import   add_default_axes, add_default_grids, LinearMapper,  ArrayDataSource, MultiArrayDataSource, DataRange1D
from enthought.chaco.tools.api import RangeSelection, RangeSelectionOverlay
from enthought.chaco.plot_containers import OverlayPlotContainer
from scipy.special import *

#from enthought.enable2.wx_backend.api import Window

#from mapero.multiline_plot import MultiLinePlot

#from enthought.util.numerix import linspace
import threading

import wx
import enthought
import thread
import time

import logging
log = logging.getLogger("mapero.logger.module");

module_info = {'name': 'Visualization.time_selector',
                'desc': ""}

class Timer:

    # Create Timer Object
    def __init__(self, interval, function, *args, **kwargs):
        self.__lock = thread.allocate_lock()
        self.__interval = interval
        self.__function = function
        self.__args = args
        self.__kwargs = kwargs
        self.__loop = False
        self.__alive = False

    # Start Timer Object
    def start(self):
        self.__lock.acquire()
        if not self.__alive:
            self.__loop = True
            self.__alive = True
            thread.start_new_thread(self.__run, ())
        self.__lock.release()

    # Stop Timer Object
    def stop(self):
        self.__lock.acquire()
        self.__loop = False
        self.__lock.release()

    # Private Thread Function
    def __run(self):
        while self.__loop:
            self.__function(*self.__args, **self.__kwargs)
            time.sleep(self.__interval)
        self.__alive = False
        
class time_selector(VisualModule):
    """ modulo de prueba uno a"""

    h = traits.Range(2,100)
    a = traits.Float(2.0)

    fm = traits.Float(1)
    time_factor = traits.Float(10.0)
    play = traits.Button(label='play')
    
    
    view = Group('h','a','fm', 'time_factor', 'play')

    def __init__(self, **traitsv):
        super(time_selector, self).__init__(**traitsv)
        self.name = 'Time Selector'

        values_trait = traits.Array(typecode=Float, shape=(None,None))
        self.ip_values = InputPort(
                                   data_types = values_trait,
                                   name = 'values',
                                   module = self
                                   )
        self.input_ports.append(self.ip_values)
        self.i_values = None

        self.ip_metadata = InputPort(
                                     data_types = traits.Str,
                                     name = 'metadata',
                                     module = self
                                     )
        self.input_ports.append(self.ip_metadata)
        self.i_metadata = None

        selected_values_trait =  traits.Array(typecode=Float, shape=(None,1))
        self.op_selected_values = OutputPort(
                                             data_types = selected_values_trait,
                                             name = 'selected values',
                                             module = self
                                             )
        self.output_ports.append(self.op_selected_values)
        self.o_selected_values = None
        self.range_selection = None

        self.plot = None
        self.timer = None
        
        
    def _play_fired(self):
        if self.timer == None:
            self.timer = Timer(self.time_factor/self.fm, self.update_ranges)
            self.timer.start()
        else:
            self.timer.stop()
            self.timer = None

    def update_ranges(self):
        log.debug(" fm: %s   time_factor: %s" % (self.fm, self.time_factor))
        selection = self.range_selection.selection
        self.range_selection.selection = (selection[0] +1, selection[1] +1)
        print " selection:  ", selection
        
    def _column_changed(self, value):
        if self.range_selection != None:
            self.range_selection.selection = (value,value)

    def execute(self):
        self.i_values = self.ip_values.data
        if (self.i_values != None) :
            self.process()

    def process(self):
        i_values = self.i_values
        self.progress = 0

        low = 0.0
        high = i_values.shape[1]
        t = linspace(low, high, i_values.shape[1])
        if ( self.plot != None ):
            self.container.remove(self.plot)
            
        self.plot = create_multi_line_plot((t,i_values),width=0.5)
        #plot = create_multi_line_plot((t,i_values),width=0.5)

        self.plot.bgcolor = "white"
        self.container.add(self.plot)

        selection_overlay = RangeSelectionOverlay(component = self.plot)
        self.range_selection = RangeSelection(self.plot)

        self.range_selection.on_trait_change(self._selection_handler, "selection")
        self.plot.tools.append(self.range_selection)
        #zoom = SimpleZoom(plot, tool_mode="box", always_on=False)
        self.plot.overlays.append(selection_overlay)

        self.progress = 100


    def _create_window(self):
        self.container = OverlayPlotContainer(padding=40, bgcolor="lightgray",
                use_backbuffer = True,
                border_visible = True,
                fill_padding = True)

        #FIXME: el tiempo esta en duro, tiene que utilizarse la metadata de la senal
        #self.window = Window(self.parent, -1, component=self.container)
        return self.window.control


    def _h_changed(self):
        if self.plot != None:
            self.plot.h = self.h
            self.plot.update()

    def _a_changed(self):
        if self.plot != None:
            self.plot.a = self.a
            self.plot.update()

    def _selection_handler(self, value):
        if self.plot != None:
            col_selected = (int)(value[0])
            print "col_selected: ", col_selected
            output = matrix(self.plot.value.get_data( axes = col_selected ))
            self.op_selected_values.data = output.T
            self.op_selected_values.update_data()



def _create_data_sources(data):
    """
    Returns datasources for index and value based on the inputs.
    """
    if (type(data) == ArrayType) or (len(data) == 2):
        index, value = data
        if type(index) in (list, tuple, ArrayType):
            index = ArrayDataSource(array(index), sort_order='ascending')
        elif not isinstance(index, AbstractDataSource):
            raise RuntimeError, "Need an array or list of values or a DataSource, got %s instead." % type(index)

        if type(value) == ArrayType:
            value = MultiArrayDataSource(array(value))
        elif not isinstance(value, AbstractDataSource):
            raise RuntimeError, "Need an array or list of values or a DataSource, got %s instead." % type(index)

        return index, value
    else:
        raise RuntimeError, "Unable to create datasources."




def create_multi_line_plot(data=[], index_bounds=None, value_bounds=None,
                                        orientation="h", color="red", width=1.0,
                                        dash="solid", value_mapper_class=LinearMapper,
                                        bgcolor="transparent", border_visible=False,
                                        add_grid=False, add_axis=False):

    index, value = _create_data_sources(data)

    if index_bounds is not None:
        index_range = DataRange1D(low=index_bounds[0], high=index_bounds[1])
    else:
        index_range = DataRange1D()
    index_range.add(index)
    index_mapper = LinearMapper(range=index_range)

    if value_bounds is not None:
        value_range = DataRange1D(low=value_bounds[0], high=value_bounds[1])
    else:
        value_range = DataRange1D()
    value_range.add(value)
    value_mappers = []
    for _ in range(value.get_data().shape[0]):
        value_mapper = value_mapper_class(range=value_range)
        value_mappers.append(value_mapper)

    plot = MultiLinePlot(index=index, value=value,
                    index_mapper = index_mapper,
                    value_mappers = value_mappers,
                    orientation = orientation,
                    color = color,
                    bgcolor = bgcolor,
                    line_width = width,
                    line_style = dash,
                    border_visible=border_visible)


    if add_grid:
        add_default_grids(plot, orientation)
    if add_axis:
        add_default_axes(plot, orientation)
    return plot


