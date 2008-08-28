from mapero.core.api import VisualModule
from mapero.core.api import OutputPort, InputPort

from enthought.traits.api import Array, Str, Range, Float, Button
from enthought.traits.ui.api import Group
from enthought.enable.api import Window
from enthought.chaco.api import add_default_axes, add_default_grids, LinearMapper,\
      ArrayDataSource, MultiArrayDataSource, DataRange1D, AbstractDataSource, \
      OverlayPlotContainer
from enthought.chaco.tools.api import RangeSelection, RangeSelectionOverlay

from numpy.lib.function_base import linspace
import numpy.core.multiarray as mu
from numpy.core.numeric import array
from numpy.core.defmatrix import matrix

from multiline_plot import MultiLinePlot
import time
import thread

import logging
log = logging.getLogger("mapero.logger.module");


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
    """ """
    h = Range(2,100)
    a = Float(2.0)

    fm = Float(1)
    time_factor = Float(10.0)
    play = Button(label='play')
    
    
    view = Group('h','a','fm', 'time_factor', 'play')

    label = 'Time Selector'

    ### Input Ports
    ip_values = InputPort( trait = Array(dtype=float, shape=(None,None)) )
    ip_metadata = InputPort( trait = Str )

    ### Output Ports
    op_selected_values = OutputPort( trait = Array(typecode=float, shape=(None,1) ) )
    
    def start_module(self):
        self.i_values = None
        self.i_metadata = None

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
        
    def _column_changed(self, value):
        if self.range_selection != None:
            self.range_selection.selection = (value,value)

    def execute(self):
        self.i_values = self.ip_values.data
        if self.i_values != None :
            self.process()
        else:
            if self.container and self.plot :
                try:
                    self.container.remove(self.plot)
                except:
                    log.error("unable to remove plot componet")
            self.op_selected_values.data = None
        self.container.request_redraw()

    def process(self):
        i_values = self.i_values
        self.progress = 0

        low = 0.0
        high = i_values.shape[1]
        t = linspace(low, high, i_values.shape[1])
        try:
            self.container.remove(self.plot)
        except:
            log.error("unable to remove plot componet")
            
        self.plot = create_multi_line_plot((t,i_values),width=0.5)

        self.plot.bgcolor = "white"
        self.container.add(self.plot)

        self.range_selection = RangeSelection(self.plot, left_button_selects = True )

        self.range_selection.on_trait_change(self._selection_handler, "selection")
        self.plot.active_tool = self.range_selection
        self.plot.overlays.append(RangeSelectionOverlay(component = self.plot))

        self.progress = 100


    def create_control(self, parent):
        self.container = OverlayPlotContainer(padding=40, bgcolor="lightgray",
                use_backbuffer = True,
                border_visible = True,
                fill_padding = True)

        window = Window(parent, component=self.container)
        return window.control
    
    def destroy_control(self):
        #self.container.cleanup(window)
        pass


    def _h_changed(self):
        if self.plot != None:
            self.plot.h = self.h
            self.plot.update()

    def _a_changed(self):
        if self.plot != None:
            self.plot.a = self.a
            self.plot.update()

    def _selection_handler(self, value):
        if self.plot and value:
            col_selected = (int)(value[0])
            output = matrix(self.plot.value.get_data( axes = col_selected ))
            self.op_selected_values.data = output.T
        else:
            self.op_selected_values.data = None



def _create_data_sources(data):
    """
    Returns datasources for index and value based on the inputs.
    """
    if (type(data) == mu.ndarray) or (len(data) == 2):
        index, value = data
        if type(index) in (list, tuple, mu.ndarray):
            index = ArrayDataSource(array(index), sort_order='ascending')
        elif not isinstance(index, AbstractDataSource):
            raise RuntimeError, "Need an array or list of values or a DataSource, got %s instead." % type(index)

        if type(value) == mu.ndarray:
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


