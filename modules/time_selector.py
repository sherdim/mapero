from core.module import VisualModule
from core.port import OutputPort, InputPort
from enthought.util import numerix
from numpy.oldnumeric.precision import Float
from enthought.traits.api import Range, Array, Int
from enthought.traits.ui.api import Group
from enthought.chaco2.api import   add_default_axes, add_default_grids, LinearMapper,  ArrayDataSource, MultiArrayDataSource, DataRange1D
from enthought.chaco2.tools.api import RangeSelection, RangeSelectionOverlay
from enthought.chaco2.plot_containers import OverlayPlotContainer
from enthought.util.numerix import array, ArrayType, transpose, cos, sin, matrix
from scipy.special import *

from enthought.enable2.wx_backend.api import Window

from multiline_plot import MultiLinePlot

from enthought.util.numerix import linspace

import wx
import enthought

module_info = {'name': 'visualization.time_selector',
                'desc': ""}

class time_selector(VisualModule):
    """ modulo de prueba uno """

    h = Range(2,100)
    a = enthought.traits.api.Float(2.0)
    column = Range(0,12600)

    view = Group('h','a','column')

    def __init__(self, **traits):
        super(time_selector, self).__init__(**traits)
        self.name = 'Time Selector'

    def start(self):

        values_trait = Array(typecode=Float, shape=(None,None))
        self.ip_values = InputPort(values_trait, 'values', self)
        self.input_ports.append(self.ip_values)
        self.i_values = None

        selected_values_trait = Array(typecode=Float, shape=(None,1))
        self.op_selected_values = OutputPort(selected_values_trait, 'selected values', self)
        self.output_ports.append(self.op_selected_values)
        self.o_selected_values = None
        self.range_selection = None

        self.plot = None

    def _column_changed(self, value):
        if self.range_selection != None:
            self.range_selection.selection = (value,value)

    def update(self, input_port, old, new):
        if input_port == self.ip_values:
            self.i_values = input_port.data
        if (self.i_values != None) :
            self.process()

    def _process(self):
        i_values = self.i_values
        self.progress = 0

        low = 0.0
        high = i_values.shape[1]
        t = linspace(low, high, i_values.shape[1])
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

    def _selection_handler(self, value):
        print "value: ", value

    def _create_window(self):
        self.container = OverlayPlotContainer(padding=40, bgcolor="lightgray",
                use_backbuffer = True,
                border_visible = True,
                fill_padding = True)

        #FIXME: el tiempo esta en duro, tiene que utilizarse la metadata de la senal
        self.window = Window(self.parent, -1, component=self.container)
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


