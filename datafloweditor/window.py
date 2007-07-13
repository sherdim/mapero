#!/usr/bin/python
# Standard library imports.
import os
import os.path
import random
import sys
import logging

import wx

import wx.lib.ogl as ogl

# Enthought library imports.
from enthought.pyface import GUI
from enthought.pyface import PythonShell
from enthought.pyface import SplitApplicationWindow , SplitPanel
from enthought.pyface.action import Action, Group, MenuBarManager, MenuManager,\
																		Separator

from enthought.traits import Float, Str, Instance
from enthought.traits.ui import View, Item
from mapero.core.module import Module
from mapero.core.modulemanager import ModuleManager
from mapero.datafloweditor.diagram import DataflowDiagram

from mapero.core.catalog import Catalog
from mapero.core.ui.catalog_tree import CatalogTree

# Standard library imports.
import os, sys, copy

# Put the Enthought library on the Python path.
sys.path.append(os.path.abspath(r'..\..\..'))




class ExitAction(Action):
	""" Exits the application. """
	def __init__(self, window):
			""" Creates a new action. """
			self._window = window
			self.name = "E&xit"

	def perform(self):
			""" Performs the action. """
			self._window.close()

class AddModuleAction(Action):
	""" Add a module to the diagram """
	def __init__(self, window):
			""" Creates a new action. """
			self._window = window
			self.name = "&Add Module"

	def perform(self):
			""" Performs the action. """
			self._window._add_module()

class SaveNetworkAction(Action):
	""" Saves the network to a file """
	def __init__(self, window):
		""" Creates a new action"""
		self._window = window
		self.name = "&Save Network"
	def perform(self):
		""" Performs the action"""
		self._window._save_network()

class LoadNetworkAction(Action):
	""" Loads the network from a file """
	def __init__(self, window):
		""" Creates a new action"""
		self._window = window
		self.name = "&Load Network"
	def perform(self):
		""" Performs the action"""
		self._window._load_network()

class DataflowWindow(SplitApplicationWindow):
	""" An example application window. """

	# The ratio of the size of the left/top pane to the right/bottom pane.
	ratio = Float(0.75)

	# The direction in which the panel is split.
	direction = Str('horizontal')


	module_manager = Instance(ModuleManager)
	diagram = Instance(DataflowDiagram)

	# The `PythonShell` instance.
	python_shell = Instance(PythonShell)


	###########################################################################
	# 'object' interface.
	###########################################################################
	def __init__(self, **traits):
		""" Creates a new window. """

		# Base class constructor.
		super(DataflowWindow, self).__init__(**traits)

		# Create the window's menu bar.
		self._create_my_menu_bar()
		self.module_manager = ModuleManager()

	def _add_module(self):
		for item in self._catalog_tree.selection:
			if isinstance(item,str):
				self.add_module(item)

	def add_module(self, module_name):
		module = self.module_manager.add(module_name)

	def _remove_module(self):
		pass

	def remove_module(self, module_name):
		if self.module_manager.modules.has_key(module_name):
			self.python_shell.control.locals[module_name]
			self.diagram.remove_module(module)

	def _save_network(self):
		fileWriter = open ( '/home/zaca/Desktop/network.mpr', 'w' )
		self.diagram.save_diagram(fileWriter)
		fileWriter.close()

	def _load_network(self):
		fileReader = open ( '/home/zaca/Desktop/network.mpr', 'r' )
		self.diagram.load_diagram(fileReader)
		fileReader.close()

	###########################################################################
	# Protected 'SplitApplicationWindow' interface.
	###########################################################################

	def _create_lhs(self, parent):
			""" Creates the left hand side or top depending on the style. """

			self._rhs = SplitPanel(
					parent    = parent,
					rhs       = self._create_diagram,
					lhs       = self._create_left_panel,
					direction = 'vertical'
			)

			return self._rhs.control


	def _create_diagram(self, parent):
		self.diagram = DataflowDiagram(parent, self.module_manager, self._prop_editor)
		canvas = self.diagram.GetCanvas()
		return canvas

	def _create_left_panel(self, parent):
			self._izq = SplitPanel(
					parent    = parent,
					rhs       = self._create_prop_editor,
					lhs       = self._create_catalog_tree,
					direction = 'horizontal'
			)
			return self._izq.control


	def _create_prop_editor(self, parent):
		panel = wx.Panel( parent, -1 )
		sizer = wx.BoxSizer(wx.VERTICAL)
		panel.SetSizer(sizer)
		panel.SetAutoLayout(True)
		self._prop_editor = wx.ScrolledWindow(panel, -1, style=wx.CLIP_CHILDREN)
		sizer.Add(self._prop_editor, 1, wx.ALL | wx.EXPAND)
		sizer.Fit(panel)
		sizer.Layout()
		return panel

	def _create_catalog_tree(self, parent):
		self._catalog_tree = CatalogTree(parent, root=self.module_manager.catalog._catalog.items()[0], )
		wx.EVT_MOTION(self._catalog_tree.control, self._on_catalog_tree_anytrait_changed)
		return self._catalog_tree.control

	def _create_rhs(self, parent):
		""" Creates the right hand side or bottom depending on the style. """
		self.python_shell = PythonShell(parent)
		self.python_shell.bind('mm', self.module_manager)
		self.python_shell.bind('panel', self._prop_editor)
		self.python_shell.bind('de', self)
		return self.python_shell.control


	###########################################################################
	# Private interface.
	###########################################################################
	def _on_catalog_tree_anytrait_changed(self, evt):
		""" On Dragging in Catalog Tree """
		if evt.Dragging():
			for selection in self._catalog_tree.selection:
				if isinstance(selection,str):
					data = wx.TextDataObject()
					#text = selection + ' '  ##esta cagada me llevo una manana entera
					text = selection
					data.SetText(text)
					ds = wx.DropSource(self.control)
					ds.SetData(data)
					result = ds.DoDragDrop(wx.Drag_AllowMove)
					if result == wx.DragCopy:
						"copy"
					elif result == wx.DragMove:
						"moved"
					else:
						"failed"

			return

	def _create_my_menu_bar(self):
		""" Creates the window's menu bar. """
		self.menu_bar_manager = MenuBarManager(
			MenuManager(
				Separator(),
					ExitAction(self),
					LoadNetworkAction(self),
					SaveNetworkAction(self),
					name = '&File',
			),
			MenuManager(
					name = '&Edit',
			),
			MenuManager(
				Separator(),
				AddModuleAction(self),
				name = '&Module',
			),
		)



# Application entry point.
if __name__ == '__main__':
		# Create the GUI.
		ogl.OGLInitialize()
		gui = GUI()

		# Create and open an application window.
		window = DataflowWindow(size=(800,600))
		window.title = 'Pruebas Dataflow Editor'
		window.open()

		# Start the GUI event loop!
		gui.start_event_loop()

##### EOF #####################################################################


