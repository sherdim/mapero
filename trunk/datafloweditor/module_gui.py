from enthought.traits.api import Int, Instance, Trait, HasTraits, WeakRef
from enthought.pyface.widget import Widget
from mapero.core.module import Module
from mapero.datafloweditor.moduleshape import ModuleShape
from mapero.datafloweditor.connectionshape import ConnectionShape
import wx
import wx.lib.ogl as ogl
import weakref


class ModuleGUI(HasTraits):
    module = Instance(Module)
    module_shape = Instance(ModuleShape)

    def __init__(self, module, panel = None, diagram = None, x = 101, y = 101):
	self.module = module
	self.panel = panel
	self.diagram = diagram
	self.module_shape = ModuleShape(module, 151, 91, x, y)

	self.diagram.AddShape(self.module_shape)
	self.module_shape.SetCanvas(self.diagram.GetCanvas())
	self.module_shape.Show(True)
	self.diagram.GetCanvas().Refresh()
	self.module.on_trait_change(self.update_shape)
	self.update_shape()

    def __del__(self):
	self.diagram.RemoveShape(self.module_shape)
	self.module_shape.Delete()
	self.diagram.GetCanvas().Refresh()
	print "ModuleGUI destruido"

    def update_shape(self):
	self.module_shape.UpdateModule(self.module)
	
    def edit_module(self):
	    self.module.edit_traits(kind = 'live')
	
