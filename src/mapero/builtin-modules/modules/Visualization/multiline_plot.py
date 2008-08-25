# Author: Zacarias F. Ojeda <zojeda@gmail.com>
# License: new BSD Style.


# Enthought library imports
from enthought.enable.api import black_color_trait, LineStyle
from enthought.traits.api import Any, Array, false, Float, Instance, Property, List, Int
from enthought.traits.ui.api import View, Item


# Local relative imports
from enthought.chaco.api import AbstractMapper, AbstractPlotRenderer, \
    MultiArrayDataSource, ArrayDataSource, PlotAxis, reverse_map_1d,  \
    PlotGrid, PlotLabel, arg_find_runs
from numpy.core.ma import transpose, concatenate
from numpy.numarray.functions import compress, take
from numpy.core.numeric import array


import logging
log = logging.getLogger("mapero.logger.module");

class BaseMultiLinePlot(AbstractPlotRenderer):
	"""
	Base class for the simple X-vs-Y plots that consist of a single index
	data array and a single value data array.  Subclasses handle the actual
	rendering, but this base class takes care of most of the paperwork of
	making sure events are wired up between mappers and data/screen space
	changes, etc.
	"""

	#------------------------------------------------------------------------
	# Data-related traits
	#------------------------------------------------------------------------

	# The data source to use for the index coordinate
	index = Instance(ArrayDataSource)

	# The data source to use as value points
	value = Instance(MultiArrayDataSource)

	index_mapper = Instance(AbstractMapper)
	value_mappers = List(AbstractMapper)



	#------------------------------------------------------------------------
	# Convenience readonly properties for common annotations
	#------------------------------------------------------------------------

	hgrid = Property
	vgrid = Property
	x_axis = Property
	y_axis = Property
	labels = Property

	h = Int(20)

	a = Float(2.0)

	#------------------------------------------------------------------------
	# Other public traits
	#------------------------------------------------------------------------

	# Should be plot use downsampling?
	# This is not used right now.  We need to implement robust, fast downsampling
	# before flipping the switch on this.
	use_downsampling = True

	# Should the plot use a spatial subdivision structure for fast hittesting?
	# This makes data updates slower, but makes hittests extremely fast.
	use_subdivision = false

	# Override the default background color trait in PlotComponent.
	bgcolor = "transparent"

	# This just turns on a simple drawing of the X and Y axes... not a long
	# term solution, but good for testing.
	origin_axis_color = black_color_trait
	origin_axis_width = Float(1.0)
	origin_axis_visible = false

	#------------------------------------------------------------------------
	# Private traits
	#------------------------------------------------------------------------

	# Are the cache traits below valid, or do new ones need to be computed?
	_cache_valid = false

	# List of (x,y) data-space points; regardless of self.orientation, this
	# is always stored (index_pt, value_pt).
	_cached_data_pts = Array

	# List of (x,y) screen space points
	_screen_cache_valid = false
	_cached_screen_pts = Array

	# reference to a spatial subdivion acceleration structure
	_subdivision = Any

	#------------------------------------------------------------------------
	# Abstract methods that subclasses must implement
	#------------------------------------------------------------------------

	def _render(self, gc, points):
		" Renders an Nx2 array of screen space points on the GC "
		raise NotImplementedError

	def _gather_points(self):
		" Grabs the relevant data points within our range and caches them "
		raise NotImplementedError

	def _downsample(self):
		" Gives the renderer a chance to downsample in screen space "
		# By default, this just does a mapscreen and returns the result
		return self.map_screen(self._cached_data_pts)

	#------------------------------------------------------------------------
	# Concrete methods below
	#------------------------------------------------------------------------

	def __init__(self, **kwtraits):
		# Handling the setting/initialization of these traits manually because
		# they should be initialized in a certain order.
		kwargs_tmp = {"trait_change_notify": False}
		for trait_name in ("index", "value", "index_mapper", "value_mappers"):
			if trait_name in kwtraits:
					kwargs_tmp[trait_name] = kwtraits.pop(trait_name)
		self.set(**kwargs_tmp)
		AbstractPlotRenderer.__init__(self, **kwtraits)
		if self.index is not None:
			self.index.on_trait_change(self._either_data_changed, "data_changed")
		if self.index_mapper:
			self.index_mapper.on_trait_change(self._update_mappers, "updated")
		if self.value is not None:
			self.value.on_trait_change(self._either_data_changed, "data_changed")
#        if self.value_mappers:                                                            TODO: arreglar
#            self.value_mappers.on_trait_change(self._update_mappers, "updated")
			return

	def hittest(self, screen_pt, threshold=7.0):
		"""
		Returns if the given screen point is within threshold of any data points
		on the line.  If so, then returns the (x,y) value of a datapoint near
		the screen point.  If not, then returns None.

		Note: This only checks data points and *not* the actual line segments
					connecting them.
		"""
		# TODO: implement point-line distance computation so this method isn't
		#       quite so limited!
		ndx = self.map_index(screen_pt, threshold)
		if ndx is not None:
			return (self.index.get_data()[ndx], self.value.get_data()[ndx])
		else:
			return None


	#------------------------------------------------------------------------
	# AbstractPlotRenderer interface
	#------------------------------------------------------------------------

	def map_screen(self, data_array):
		# data_array is Nx2 array
		# data_array is NxNumSignals array
		if len(data_array) == 0:
			return []
		elif len(data_array) == 1:
			xtmp, ytmp = transpose(data_array)
			x_ary = xtmp
			y_ary = ytmp                         ##TODO: Arreglar
		else:
			x_ary = data_array[:,0]
			sx = self.index_mapper.map_screen(x_ary)
			sx = sx.reshape(len(sx),1)

			y_arys = data_array[:,1:]
			sys = y_arys
			for i in range(y_arys.shape[1]):
				sys[:,i] = self.value_mappers[i].map_screen(y_arys[:,i])
			caca = (concatenate((sx,sys),1))
		return caca

	def map_data(self, screen_pt):
		screen_coord = screen_pt[0]
		return self.index_mapper.map_data(screen_coord)

	def map_index(self, screen_pt, threshold=2.0, outside_returns_none=True, \
								index_only=False):

		data_pt = self.map_data(screen_pt)
		if ((data_pt < self.index_mapper.range.low) or \
			(data_pt > self.index_mapper.range.high)) and outside_returns_none:
			return None
		half = threshold / 2.0
		index_data = self.index.get_data()
		value_data = self.value.get_data()

		if len(value_data) == 0 or len(index_data) == 0:
			return None

		ndx = reverse_map_1d(index_data, data_pt, self.index.sort_order)
		x = index_data[ndx]
		y = value_data[ndx]
		sx, sy = self.map_screen([x,y])
		if index_only and ((screen_pt[0]-sx) < threshold):
			return ndx
		elif ((screen_pt[0]-sx)**2 + (screen_pt[1]-sy)**2 < threshold*threshold):
			return ndx
		else:
			return None

	#------------------------------------------------------------------------
	# PlotComponent interface
	#------------------------------------------------------------------------

	def _draw_plot(self, gc, view_bounds=None, mode="normal"):
		self._draw_component(gc, view_bounds, mode)
		return

	def _draw_component(self, gc, view_bounds=None, mode="normal"):
		# Normal rendering
		self._gather_points()
		if self.use_downsampling:
			pts = self._downsample()
		else:
			# The BaseMultiLinePlot implementation of _downsample doesn't actually
			# do any downsampling.
			pts = self._downsample()
		self._render(gc, pts)
		return

	def _draw_default_axes(self, gc):
		if not self.origin_axis_visible:
				return
		gc.save_state()
		gc.set_stroke_color(self.origin_axis_color_)
		gc.set_line_width(self.origin_axis_width)
		gc.set_line_dash(None)

		for range in (self.index_mapper.range, self.value_mappers[0].range):
			if (range.low < 0) and (range.high > 0):
				if range == self.index_mapper.range:
					dual = self.value_mappers[0].range
					data_pts = array([[0.0,dual.low], [0.0, dual.high]])
				else:
					dual = self.index_mapper.range
					data_pts = array([[dual.low,0.0], [dual.high,0.0]])
				start,end = self.map_screen(data_pts)
				start = around(start)
				end = around(end)
				gc.move_to(int(start[0]), int(start[1]))
				gc.line_to(int(end[0]), int(end[1]))
				gc.stroke_path()
		gc.restore_state()
		return

	def _post_load(self):
		super(BaseMultiLinePlot, self)._post_load()
		self._update_mappers()
		self.invalidate_draw()
		self._cache_valid = False
		self._screen_cache_valid = False
		return

	def _update_subdivision(self):

		return

	#------------------------------------------------------------------------
	# Properties
	#------------------------------------------------------------------------

	def _get_index_range(self):
		return self.index_mapper.range

	def _set_index_range(self, val):
		self.index_mapper.range = val

	def _get_hgrid(self):
		for obj in self.underlays+self.overlays:
			if isinstance(obj, PlotGrid):
				return obj
			else:
				return None

	def _get_vgrid(self):
		for obj in self.underlays+self.overlays:
			if isinstance(obj, PlotGrid):
				return obj
			else:
				return None

	def _get_x_axis(self):
		for obj in self.underlays+self.overlays:
			if isinstance(obj, PlotAxis):
				return obj
			else:
				return None

	def _get_y_axis(self):
		for obj in self.underlays+self.overlays:
			if isinstance(obj, PlotAxis):
				return obj
			else:
				return None

	def _get_labels(self):
		labels = []
		for obj in self.underlays+self.overlays:
			if isinstance(obj, PlotLabel):
				labels.append(obj)
		return labels

	#------------------------------------------------------------------------
	# Event handlers
	#------------------------------------------------------------------------

	def _update_mappers(self):
		x_mapper = self.index_mapper

		x = self.x
		x2 = self.x2
		y = self.y
		y2 = self.y2

		x_mapper.low_pos = x
		x_mapper.high_pos = x2

		lmappers = len(self.value_mappers)

		numsings = min([lmappers, self.h])

		y_top =  y2
		htemp = (y - y2)/numsings

		for y_mapper in self.value_mappers:
			half = htemp * self.a / 2.0
			y_mapper.low_pos = y_top + half
			y_mapper.high_pos = y_top - half
			y_top += htemp

		self.invalidate_draw()
		self._cache_valid = False
		self._screen_cache_valid = False
		return

	def _bounds_changed(self):
		self._update_mappers()
		return

	def _bounds_items_changed(self):
		self._update_mappers()
		return

	def _orientation_changed(self):
		self._update_mappers()
		return

	def _index_changed(self, old, new):
		if old is not None:
			old.on_trait_change(self._either_data_changed, "data_changed", remove=True)
		if new is not None:
			new.on_trait_change(self._either_data_changed, "data_changed")
		self._either_data_changed()
		return

	def _either_data_changed(self):
		self.invalidate_draw()
		self._cache_valid = False
		self._screen_cache_valid = False
		self.request_redraw()
		return

	def _value_changed(self, old, new):
		if old is not None:
			old.on_trait_change(self._either_data_changed, "data_changed", remove=True)
		if new is not None:
				new.on_trait_change(self._either_data_changed, "data_changed")
		self._either_data_changed()
		return

	def _index_mapper_changed(self, old, new):
		self._either_mapper_changed(self, "index_mapper", old, new)
		self.trait_property_changed("x_mapper", old, new)
		return

	def _value_mappers_changed(self, old, new):
		self._either_mapper_changed(self, "value_mappers", old, new)
		self.trait_property_changed("y_mapper", old, new)
		return

	def _either_mapper_changed(self, obj, name, old, new):
		if old is not None:
			old.on_trait_change(self._mapper_updated_handler, "updated", remove=True)
		if new is not None:
			new.on_trait_change(self._mapper_updated_handler, "updated")
		self.invalidate_draw()
		self._screen_cache_valid = False
		return

	def _mapper_updated_handler(self):
		self._cache_valid = False
		self._screen_cache_valid = False
		self.invalidate_draw()
		self.request_redraw()
		return

	def update(self):
		self._update_mappers()
		self._cache_valid = False
		self._screen_cache_valid = False
		self.invalidate_draw()
		self.request_redraw()
		return

	def _bgcolor_changed(self):
		self.invalidate_draw()

	def _use_subdivision_changed(self, old, new):
		if new:
			self._set_up_subdivision()
		return

	#------------------------------------------------------------------------
	# Persistence
	#------------------------------------------------------------------------

	def __getstate__(self):
		state = super(BaseMultiLinePlot,self).__getstate__()
		for key in ['_cache_valid', '_cached_data_pts', '_screen_cache_valid',
								'_cached_screen_pts']:
			if state.has_key(key):
				del state[key]

		return state

	def __setstate__(self, state):
		super(BaseMultiLinePlot, self).__setstate__(state)
		if self.index is not None:
			self.index.on_trait_change(self._either_data_changed, "data_changed")
		if self.value is not None:
			self.value.on_trait_change(self._either_data_changed, "data_changed")

		self.invalidate_draw()
		self._cache_valid = False
		self._screen_cache_valid = False
		self._update_mappers()
		return




class MultiLinePlot(BaseMultiLinePlot):

	# The color of the line
	color = black_color_trait

	# The thickness of the line
	line_width = Float(1.0)

	# The line dash style
	line_style = LineStyle

	# Traits UI View
	traits_view = View(Item("color", style="custom"), "line_width", "line_style",
										 buttons=["OK", "Cancel"])

	def hittest(self, screen_pt, threshold=7.0):
		"""
		Returns if the given screen point is within threshold of any data points
		on the line.  If so, then returns the (x,y) value of a datapoint near
		the screen point.  If not, then returns None.

		Note: This only checks data points and *not* the actual line segments
					connecting them.
		"""
		# TODO: implement point-line distance computation so this method isn't
		#       quite so limited!
		ndx = self.map_index(screen_pt, threshold)
		if ndx is not None:
			return (self.index.get_data()[ndx], self.value.get_data()[ndx])
		else:
			return None

	def interpolate(self, index_value):
		"""
		Returns the value of the plot at the given index value in screen
		space.
		Raises IndexError when index_value exeeds the bounds of indexes on value.
		"""

		if self.index is None or self.value is None:
			raise IndexError, "cannot index when data source index or value is None"

		index_data = self.index.get_data()
		value_data = self.value.get_data()

		from base import reverse_map_1d
		ndx = reverse_map_1d(index_data, index_value, self.index.sort_order)

		# quick test to see if this value is already in the index array
		if index_value == index_data[ndx]:
			return value_data[ndx]

		# get x and y values to interpolate between
		if index_value < index_data[ndx]:
			x0 = index_data[ndx - 1]
			y0 = value_data[ndx - 1]
			x1 = index_data[ndx]
			y1 = value_data[ndx]
		else:
			x0 = index_data[ndx]
			y0 = value_data[ndx]
			x1 = index_data[ndx + 1]
			y1 = value_data[ndx + 1]

		if x1 != x0:
			slope = float(y1 - y0)/float(x1 - x0)

		dx = index_value - x0
		yp = y0 + slope * dx

		return yp

	#------------------------------------------------------------------------
	# Private methods; implements the BaseMultiLinePlot stub methods
	#------------------------------------------------------------------------

	def _gather_points(self):
		"""
		Gathers up the data points that are within our bounds and stores them
		"""
		if not self._cache_valid:
			if not self.index or not self.value:
					return

			index = self.index.get_data()
			values = self.value.get_data()

			lindex = len(index)            ##
			lvalues = values.shape[1]      ## eliminar
			if lindex == 0 or lvalues == 0 or lindex != lvalues:
				log.warn("Chaco2: using empty dataset; index_len=%d, value_len=%d." \
														% (lindex, lvalues))
				self._cached_data_pts = []
				self._cache_valid = True
#
			index_mask = self.index_mapper.range.mask_data(index)
			value_mask = self.value_mappers[0].range.mask_data(values)

			size_diff = lvalues - lindex
			if size_diff > 0:
				print 'WARNING lineplot._gather_points: len(values)', len(values), '- len(index)', len(index), '=', size_diff, '\n'
				index_max = lindex
				values = values[:index_max]
				value_mask = value_mask[:index_max]
			else:
				index_max = lvalues
				index = index[:index_max]
				index_mask = index_mask[:index_max]

			point_mask = index_mask & value_mask

			# Expand the width of every group of points so we draw the lines
			# up to their next point, outside the plot area
			end = point_mask.shape[1]
			lsignals = values.shape[0]
			for i in range(values.shape[0]):
				for run in arg_find_runs(point_mask[i,:], "flat"):
					if run[0] != 0:
						point_mask[i,run[0]-1] = 1
					if run[1] != end:
						point_mask[i,run[1]] = 1

			#for i in range(lsignals):
			index = index.reshape(1,lindex)
			points = transpose(concatenate((index,values)))
			#self._cached_data_pts = zeros(lindex, lsignals)
			self._cached_data_pts = array(compress(point_mask[0], points, axis=0))
			self._cache_valid = True
		return

	def _downsample(self):
		if not self._screen_cache_valid:
			self._cached_screen_pts = array(self.map_screen(self._cached_data_pts))
			self._screen_cache_valid = True

			pts = self._cached_screen_pts

			# some boneheaded short-circuits
			m = self.index_mapper
			if (pts.shape[0] < 400) or (pts.shape[0] < m.high_pos - m.low_pos):
				return self._cached_screen_pts

			# the new point array and a counter of how many actual points we've added
			# to it
			new_pts = zeros(pts.shape, "d")
			numpoints = 1
			new_pts[0] = pts[0]

			last_x, last_y = pts[0]
			for x, y in pts[1:]:
				if (x-last_x)**2 + (y-last_y)**2 > 2:
					new_pts[numpoints] = (x,y)
					last_x = x
					last_y = y
					numpoints += 1

			self._cached_screen_pts = new_pts[:numpoints]
		return self._cached_screen_pts

	def _render(self, gc, points):
		if len(points) == 0:
				return

		gc.save_state()
		gc.set_antialias(True)
		if len(points) > 0:
			gc.clip_to_rect(self.x, self.y, self.width-1, self.height-1)
			gc.set_stroke_color(self.color_)
			gc.set_line_width(self.line_width)
			gc.set_line_dash(self.line_style_)

			gc.begin_path()
			for i in range(points.shape[1]-1):
				pts = take(points, (0,i+1), 1)
				gc.lines(pts)
				gc.stroke_path()

			# Draw the default axes, if necessary
		self._draw_default_axes(gc)

		gc.restore_state()
		return

	def _render_icon(self, gc, x, y, width, height):
		gc.save_state()
		gc.set_stroke_color(self.color_)
		gc.set_line_width(self.line_width)
		gc.set_line_dash(self.line_style_)
		gc.move_to(x, y+height/2)
		gc.line_to(x+width, y+height/2)
		gc.stroke_path()
		gc.restore_state()
		return

	def _downsample_vectorized(self):
		"""
		Does an analysis on the screen-space points stored in self._cached_data_pts
		and replaces it with a downsampled version.
		"""
		pts = self._cached_screen_pts  #.astype(int)

		# some boneheaded short-circuits
		m = self.index_mapper
		if (pts.shape[0] < 400) or (pts.shape[0] < m.high_pos - m.low_pos):
			return

		pts2 = concatenate((array([[0.0,0.0]]), pts[:-1]))
		z = abs(pts - pts2)
		d = z[:,0] + z[:,1]
		#...
		return

	def _color_changed(self):
		self.invalidate_draw()
		self.request_redraw()
		return

	def _line_style_changed(self):
		self.invalidate_draw()
		self.request_redraw()
		return

	def _line_width_changed(self):
		self.invalidate_draw()
		self.request_redraw()
		return

	def __getstate__(self):
		state = super(MultiLinePlot,self).__getstate__()
		for key in ['traits_view']:
			if state.has_key(key):
				del state[key]
		return state



