from connectionshape import ConnectionShape
from moduleshape import PortShape
from moduleshape import ModuleShape
import wx
_ = wx.GetTranslation

class InformationPopup(wx.PopupWindow):

    def __init__(self, parent, shape):
        text_types = {
            'p'   :wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL, False, "tahoma"),
            'h1' :wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False, "tahoma"),
            'h2' :wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False, "tahoma")
        }

        def add_text(parent, text, pos, font_type='normal'):
            txt = wx.StaticText(panel, -1, text, pos=pos)
            txt.SetFont(text_types[font_type])

            sz = txt.GetBestSize()
            x = pos[0]
            y = pos[1] + sz[1] + 5
            return ((x, y), sz)

        #TODO: avoid hard coded properties (should be in ui properies)
        wx.PopupWindow.__init__(self, parent)
        panel = wx.Panel(self, -1)
        panel.SetBackgroundColour(wx.Colour(255,255,190))

        self.parent = parent

        #icon = wx.Icon("OK.ico", wx.BITMAP_TYPE_ICO, 16, 16)
        #bmp = wx.EmptyBitmap(16,16)
        #bmp.CopyFromIcon(icon)

        title = ""

        if isinstance(shape, ModuleShape):
            title = shape.module.name

        if isinstance(shape, PortShape):
            title = shape.port.name

        if isinstance(shape, ConnectionShape):
            title = "%s to %s" % (shape.connection.output_port.name,
                            shape.connection.input_port.name)

        sx = 0
        sy = 0

        rect = add_text(panel, title, (5,5), 'h1')


        if isinstance(shape, ModuleShape):
            module = shape.module
            rect = add_text(panel,module.__doc__, rect[0], 'p')
            rect = add_text(panel, _("input ports"), rect[0], 'h2')
            rect = ((rect[0][0]+5, rect[0][1]), rect[1])
            for port in module.input_ports:
                rect = add_text(panel, port.name, rect[0], 'p')
            rect = ((rect[0][0]-5, rect[0][1]), rect[1])
            rect = add_text(panel, _("output ports"), rect[0], 'h2')
            rect = ((rect[0][0]+5, rect[0][1]), rect[1])
            for port in module.output_ports:
                rect = add_text(panel, port.name, rect[0], 'p')

#        for strs in tips:
#           txt = wx.StaticText(panel, -1, strs, pos=(30,20+sy))
#            txt.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL, False, "tahoma"))
#            sz = txt.GetBestSize()
#            #stbmp = wx.StaticBitmap(panel, -1, bmp, pos=(10, 5+sy+sz[1]))
#            sy = sy + sz[1] + 5
#            maxlen = max(maxlen, sz[0])

#        txt = wx.StaticText(panel, -1, description, pos=(10,30+sy))
#        txt.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL, False, "tahoma"))
#        sz = txt.GetBestSize()
#        sy = sy + sz[1] + 20

        panel.SetSize((260, 250))
        self.SetSize(panel.GetSize())
