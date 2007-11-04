from module_shape import ModuleShape
from module_shape import PortShape
from connection_shape import ConnectionShape
from mapero.dataflow_editor.information_popup import InformationPopup

import wx
import wx.lib.ogl as ogl
import logging

log = logging.getLogger('mapero.logger.diagram')

ID_MOUSE_MOVE = 101


class ModuleNameDropTarget(wx.TextDropTarget):
    def __init__(self, parent):
        wx.TextDropTarget.__init__(self)
        self.parent = parent

    def OnDropText(self, x, y, data):
        print data
        self.parent.add_module(x, y, data.strip())


class DataflowDiagram(ogl.Diagram):
    def __init__(self, parent, module_manager=None, prop_editor=None, view=None):
        ogl.Diagram.__init__(self)
        canvas = ogl.ShapeCanvas(parent)
        self.SetCanvas(canvas)
        canvas.SetDiagram(self)
        canvas.SetBackgroundColour(wx.Colour(233,221,175))
        canvas.SetDropTarget(ModuleNameDropTarget(self))
        wx.EVT_MOUSE_EVENTS(canvas, self.OnMouseEvent)
        self.view = view


        canvas.SetScrollbars(20,20,2000,1000,0,0,True)
        self.ui_selected = None

        self.prop_editor = prop_editor

        self.module_shapes= []
        self.connection_shapes = []
        self.from_here = False
        self.module_selected = None
        log.debug( "starting diagram !!!" )
        
    def OnMouseEvent(self, evt):
        canvas = self.GetCanvas()
        dc = wx.ClientDC(canvas)
        canvas.PrepareDC(dc)
        x, y = evt.GetLogicalPosition(dc)
        (winx, winy) = evt.GetPositionTuple()
        shape = canvas.FindShape(x, y)[0]

#        if shape != None:
#            if not hasattr(self, "popup"):
#                popup = InformationPopup(canvas, shape)
#                self.popup = popup
#                pos = canvas.ClientToScreen((winx,winy))
#                print pos
#                popup.Position(pos, (0,-10))
#                popup.Show()
#        else:
#            if hasattr(self, "popup"):
#                self.popup.Destroy()
#                del self.popup

        canvas.OnMouseEvent(evt)

    def move_module(self, module, mx, my):
        self.view.move_module(module, mx, my)

    def get_port_shape(self, port):
        for module_gui in self.modules_gui:
            for input_port_shape in module_gui.module_shape.input_port_shapes:
                if port == input_port_shape.port:
                    return input_port_shape
        for output_port_shape in module_gui.module_shape.output_port_shapes:
                if port == output_port_shape.port:
                    return output_port_shape

    def get_module_shape(self, module):
        for module_shape in self.module_shapes:
            if module_shape.module == module:
                return module_shape
        return None

    def get_connection_shape(self, connection):
        for connection_shape in self.connection_shapes:
            if connection_shape.connection == connection:
                return connection_shape
        return None



    def add_module(self, x, y, module_name):
        cx, cy = self.GetCanvas().CalcUnscrolledPosition(x,y)
        self.view.add_module(module_name, cx, cy)

    def add_module_shape(self, module, geometrics):
        module_shape = ModuleShape(module)
        module_shape.SetCanvas(self.GetCanvas())
        module_shape.Show(True)
        self.AddShape(module_shape)
        self.module_shapes.append(module_shape)
        module_shape.SetGeometrics(geometrics)
        
    def remove_module_shape(self, module):
        log.debug("removing module_shape for module : %s " % (module))
        module_shape = self.get_module_shape(module)
        for input_port_shape in module_shape.input_port_shapes:
            self.RemoveShape(input_port_shape)
        for output_port_shape in module_shape.output_port_shapes:
            self.RemoveShape(output_port_shape)

        self.RemoveShape(module_shape)
        self.module_shapes.remove(module_shape)
        
    def remove_connection_shape(self, connection):
        log.debug("removing connection_shape for connection : %s " % (connection))
        connection_shape = self.get_connection_shape(connection)
        module_shape_from = self.get_module_shape(connection.output_port.module)
        module_shape_from.RemoveLine(connection_shape)
        
        log.debug("connection_shape founded : %s " % (connection_shape) )
 
        self.RemoveShape(connection_shape)
        self.connection_shapes.remove(connection_shape)

    def add_connection_shape(self, connection):
        connection_shape = ConnectionShape(connection)
        connection_shape.SetCanvas(self.GetCanvas())

        module_shape_to = self.get_module_shape(connection.input_port.module)
        module_shape_from = self.get_module_shape(connection.output_port.module)

        attach_to = module_shape_to.get_port_attachment(connection.input_port)
        attach_from = module_shape_from.get_port_attachment(connection.output_port)

        module_shape_from.AddLine(connection_shape, module_shape_to, attach_from, attach_to)

        self.connection_shapes.append(connection_shape)
        self.AddShape(connection_shape)
        connection_shape.Show(True)

        self.GetCanvas().Refresh()

    def new_connection(self, x0, y0, x1, y1):
        port_shape_from = self.GetCanvas().FindShape(x0, y0)[0]
        port_shape_to = self.GetCanvas().FindShape(x1, y1)[0]
        if isinstance(port_shape_from, PortShape) and isinstance(port_shape_to, PortShape) \
            and (port_shape_from.isoutput) and not(port_shape_to.isoutput):
                self.view.new_connection( \
                            port_shape_from.port.module, port_shape_from.port,
                port_shape_to.port.module, port_shape_to.port)

    def disconnect(self, module_from, port_name_from, module_to, port_name_to):
        self.Refresh()

    def edit_module(self, module):
        self.select_module(module)

    def select_module(self, module):
#        if self.ui_selected:
#            self.ui_selected.dispose()
        self.module_selected = module
        for module_shape in self.module_shapes:
            if module_shape.module == module:
                module_shape.Select(True)
            else:
                module_shape.Select(False)


            self.GetCanvas().Refresh()
