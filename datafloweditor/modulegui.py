from enthought.traits.api import Int, Instance, Trait, HasTraits, WeakRef
from enthought.pyface.widget import Widget
from mapero.core.module import Module
from mapero.datafloweditor.moduleshape import ModuleShape
from mapero.datafloweditor.connectionshape import ConnectionShape
import wx
import wx.lib.ogl as ogl
import weakref

class MyTransientPopup(wx.PopupWindow):
    def __init__(self, parent, style):
        wx.PopupWindow.__init__(self, parent, style)
        panel = wx.Panel(self, -1)
        panel.SetBackgroundColour(wx.Colour(255,255,190))

        self.parent = parent
        
        icon = wx.Icon("OK.ico", wx.BITMAP_TYPE_ICO, 16, 16)
        bmp = wx.EmptyBitmap(16,16)
        bmp.CopyFromIcon(icon)
        
        ontext, thehelp, moretext = self.GetStatic()

        sx = 0
        sy = 0
        
        txt = wx.StaticText(panel, -1, thehelp, pos=(5,5))
        txt.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, "tahoma"))

        sz = txt.GetBestSize()
        sx = sx + sz[0]
        sy = sy + sz[1] + 5

        maxlen = 0

        for strs in ontext:
            txt = wx.StaticText(panel, -1, strs, pos=(30,20+sy))
            txt.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL, False, "tahoma"))
            sz = txt.GetBestSize()
            stbmp = wx.StaticBitmap(panel, -1, bmp, pos=(10, 5+sy+sz[1]))
            sy = sy + sz[1] + 5
            maxlen = max(maxlen, sz[0])
        txt = wx.StaticText(panel, -1, moretext, pos=(10,30+sy))
        txt.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL, False, "tahoma"))
        sz = txt.GetBestSize()
        sy = sy + sz[1] + 20

        maxlen = max(maxlen, sz[0])
        panel.SetSize((maxlen+20, 25+sy))
        self.SetSize(panel.GetSize())

    def GetStatic(self):
	
	ontext = []
	ontext.append("AS_CENTER_ON_SCREEN")
	ontext.append("AS_NO_TIMEOUT")
	thehelp = "Example 1"
	moretext = "This Example Uses A PNG Image\nThat Already Has An Alpha\n" \
		   "Transparency, So There Is No\nNeed To Mask The Bitmap.\n" \
		   "There Is No Timeout, So Click\nOn The SplashScreen To Close."

        return ontext, thehelp, moretext



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
	
