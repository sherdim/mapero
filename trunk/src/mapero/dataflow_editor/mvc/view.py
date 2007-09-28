#----------------------------------------------------------------------------
# Name:         DataflowtEditor.py
# Purpose:      Dataflow Diagram Editor for pydocview
#
# Author:       Zacarias Ojeda
#
#----------------------------------------------------------------------------
import wx
import wx.lib.docview
import wx.lib.pydocview
import logging

from commands import *
from mapero.dataflow_editor.ui.shape.diagram import DataflowDiagram
from mapero.dataflow_editor.ui.interactor.keyboard import KeyboardInteractor
from mapero.dataflow_editor.ui.interactor.mouse import MouseInteractor
from mapero.dataflow_editor.ui.shape.module_shape import ModuleShape
from enthought.traits.ui.menu import Menu, Action, Separator

log = logging.getLogger("mapero.logger.mvc");

_ = wx.GetTranslation

menu_titles = [ _("Remove"),
                          _("-"),
                          _("Refresh"),
                          _("Edit Code"),
                          _("Edit Code")
                           ]

menu_title_by_id = {}
for title in menu_titles:
    menu_title_by_id[ wx.NewId() ] = title


class DataflowView(wx.lib.docview.View):

    #--- Overridden methods

    def __init__(self):
        wx.lib.docview.View.__init__(self)
        self._diagramCtrl = None
        self._wordWrap = wx.ConfigBase_Get().ReadInt("DiagramEditorWordWrap", True)
        self.selected_modules = []


    def OnCreate(self, doc, flags):
        frame = wx.GetApp().CreateDocumentFrame(self, doc, flags)
        sizer = wx.BoxSizer()
        font, color = self._GetFontAndColorFromConfig()
        self._diagramCtrl = self._BuildDiagramCtrl(frame, font, color = color)
        sizer.Add(self._diagramCtrl.GetCanvas(), 1, wx.EXPAND, 0)
        frame.SetSizer(sizer)
        frame.Layout()
        frame.Show(True)
        self.Activate()
        self.keyword_interactor = KeyboardInteractor(doc, self)
        self.mouse_interactor = MouseInteractor(doc, self)
        canvas = self._diagramCtrl.GetCanvas()
        wx.EVT_KEY_UP(canvas, self.keyword_interactor.on_event)
        wx.EVT_MOUSE_EVENTS(canvas, self.mouse_interactor.on_event)
        wx.EVT_CONTEXT_MENU(canvas, self.on_context)
        
        return True

    def remove_module(self, module):
        self.GetDocument().remove_module(module)
        
    def is_only_one_module_selected(self):
        if self.selected_modules != None and len(self.selected_modules)==1:
            return True
        else:
            return False

        
    def refresh_module(self):
        if self.selected_modules != None and len(self.selected_modules)==1:
            self.GetDocument().refresh_module(self.selected_modules[0])
    
    def edit_code(self):
        print "edit_code: "
        pass
    
    def show_module_help(self):
        print "show_module_help: "
        pass 
        
    def show_popup_menu(self, position):
        menu = Menu( 
                    Action( name = _('Copy'), enabled=False ),
                    Action( name = _('Paste'), enabled=False ),
                    Action( name = _('Delete'), enabled=False ),
                    Separator(),
                    Action( name = _('Refresh'), on_perform=self.refresh_module , enabled=self.is_only_one_module_selected() ),
                    Action( name = _('Edit Code'), on_perform=self.edit_code, enabled=self.is_only_one_module_selected() ),
                    Separator(),
                    Action( name = _('Help'), on_perform=self.show_module_help, enabled=self.is_only_one_module_selected() )
                    )
        canvas = self._diagramCtrl.GetCanvas()
        caca = menu.create_menu(canvas)
        caca.show(position[0],position[1])
            
                
    def on_context(self, event):
        self.show_popup_menu(event.GetPosition())
        
        
    def OnModify(self, event):
        self.GetDocument().Modify(True)


    def _BuildDiagramCtrl(self, parent, font, color = wx.BLACK, value = "", selection = [0, 0]):
        module_manager = self.GetDocument().get_module_manager()
        diagramCtrl = DataflowDiagram(parent, module_manager, None, self)
        return diagramCtrl


    def _GetFontAndColorFromConfig(self):
        font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        config = wx.ConfigBase_Get()
        fontData = config.Read("DiagramEditorFont", "")
        if fontData:
            nativeFont = wx.NativeFontInfo()
            nativeFont.FromString(fontData)
            font.SetNativeFontInfo(nativeFont)
        color = wx.BLACK
        colorData = config.Read("DiagramEditorColor", "")
        if colorData:
            red = int("0x" + colorData[0:2], 16)
            green = int("0x" + colorData[2:4], 16)
            blue = int("0x" + colorData[4:6], 16)
            color = wx.Color(red, green, blue)
        return font, color


    def OnCreateCommandProcessor(self):
        # Don't create a command processor, it has its own
        pass


    def OnActivateView(self, activate, activeView, deactiveView):
        if activate and self._diagramCtrl:
            # In MDI mode just calling set focus doesn't work and in SDI mode using CallAfter causes an endless loop
            if self.GetDocumentManager().GetFlags() & wx.lib.docview.DOC_SDI:
                self._diagramCtrl.SetFocus()
            else:
                def SetFocusToDiagramCtrl():
                    if self._diagramCtrl:  # Need to make sure it is there in case we are in the closeall mode of the MDI window
                        self._diagramCtrl.GetCanvas().SetFocus()
                wx.CallAfter(SetFocusToDiagramCtrl)


    def OnUpdate(self, sender = None, hint = None):
        if wx.lib.docview.View.OnUpdate(self, sender, hint):
            return
        log.debug( "updating view" )
        doc = self.GetDocument()
        diagram = self.get_diagram()
        for module, geometrics in doc.get_module_geometrics().items():
            module_shape = diagram.get_module_shape(module)
            if module_shape:
                module_shape.SetGeometrics(geometrics)
                if module in self.selected_modules:
                    module_shape.Select(True)
                else:
                    module_shape.Select(False)
                    
            else:
                log.debug( "adding module shape for : %s", module.name )
                diagram.add_module_shape(module, geometrics)

        for connection_shape in diagram.connection_shapes:
            if (connection_shape.connection not in doc.get_connection_geometrics().keys()):
                log.debug("removing connection shape for : %s", connection_shape )
                connection_shape.Select(False)
                diagram.remove_connection_shape(connection_shape.connection)
                
        for module_shape in diagram.module_shapes:
            if (module_shape.module not in doc.get_module_geometrics().keys()):
                log.debug("removing module shape for : %s", module_shape.module.name )
                module_shape.Select(False)
                diagram.remove_module_shape(module_shape.module)
                

        for connection, geometrics in doc.get_connection_geometrics().items():
            connection_shape = diagram.get_connection_shape(connection)
            if connection_shape:
                connection_shape.SetGeometrics(geometrics)
                module_from = connection.output_port.module
                module_to = connection.input_port.module
                module_from_shape = diagram.get_module_shape(module_from)
                module_to_shape = diagram.get_module_shape(module_to)
                module_from_geometrics = doc.get_module_geometrics()[module_from]
                module_to_geometrics = doc.get_module_geometrics()[module_to]
                module_from_shape.SetGeometrics(module_from_geometrics)
                module_to_shape.SetGeometrics(module_to_geometrics)

            else:
                print "adding connection shape"
                diagram.add_connection_shape(connection)
                    
        for module in self.selected_modules:
            if module not in doc.get_module_geometrics().keys():
                self.selected_modules.remove(module)
                
        diagram.GetCanvas().Refresh()



    def OnClose(self, deleteWindow = True):
        if not wx.lib.docview.View.OnClose(self, deleteWindow):
            return False
        self.Activate(False)
        if deleteWindow and self.GetFrame():
            self.GetFrame().Destroy()
        return True


    # Since ProcessEvent is not virtual, we have to trap the relevant events using this pseudo-ProcessEvent instead of EVT_MENU
    def ProcessEvent(self, event):
        id = event.GetId()
        doc = self.GetDocument()
        if id == wx.ID_UNDO:
            if not self._diagramCtrl:
                return False
            doc.GetCommandProcessor().Undo()
            self.get_diagram().GetCanvas().Refresh()
            return True
        elif id == wx.ID_REDO:
            if not self._diagramCtrl:
                return False
            doc.GetCommandProcessor().Redo()
            self.get_diagram().GetCanvas().Refresh()
            return True
        elif id == wx.ID_CUT:
            if not self._diagramCtrl:
                return False
            self._diagramCtrl.Cut()
            return True
        elif id == wx.ID_COPY:
            if not self._diagramCtrl:
                return False
            self._diagramCtrl.Copy()
            return True
        elif id == wx.ID_PASTE:
            if not self._diagramCtrl:
                return False
            self._diagramCtrl.Paste()
            return True
        elif id == wx.ID_CLEAR:
            if not self._diagramCtrl:
                return False
            self._diagramCtrl.Replace(self._diagramCtrl.GetSelection()[0], self._diagramCtrl.GetSelection()[1], '')
            return True
        elif id == wx.ID_SELECTALL:
            if not self._diagramCtrl:
                return False
            self._diagramCtrl.SetSelection(-1, -1)
            return True
        else:
            return wx.lib.docview.View.ProcessEvent(self, event)


    def ProcessUpdateUIEvent(self, event):
        if not self._diagramCtrl:
            return False

        return wx.lib.docview.View.ProcessUpdateUIEvent(self, event)


    #--- Methods for DiagramDocument to call

    def get_diagram(self):
        return self._diagramCtrl
            
    def move_module(self, module, mx, my):
        doc = self.GetDocument()
        move_command = MoveCommand(doc, module, mx, my)
        doc.GetCommandProcessor().Submit(move_command)

    def add_module(self, module_name, x, y):
        doc = self.GetDocument()
        add_module_command = AddModuleCommand(doc, module_name, x, y)
        doc.GetCommandProcessor().Submit(add_module_command)
        
    def get_module(self, x, y):
        diagram = self.get_diagram()
        module_shape = diagram.GetCanvas().FindShape(x, y)[0]
        module = None
        if isinstance(module_shape, ModuleShape):
            module = module_shape.module
        return module

    def new_connection(self, module_from, port_from, module_to, port_to):
        doc = self.GetDocument()
        new_connection_command = NewConnectionCommand(doc, module_from, port_from, module_to, port_to)
        doc.GetCommandProcessor().Submit(new_connection_command)
        
    def toggle_module_selection(self, module):
        doc = self.GetDocument()
        if module in self.selected_modules:
            self.selected_modules.remove(module)
        else:
            self.selected_modules.append(module)
        doc.UpdateAllViews()
    
    def select_module(self, module):
        doc = self.GetDocument()
        self.selected_modules = [module]
        doc.UpdateAllViews()
        
        
    def callback(self):
        print "llamada !!!"
        
    def display_context_menu(self, x=None, y=None):
        print "displaying context menu"
        menu = Menu( Action( name = 'Add', action = 'self.callback( object )' ) )
        diagram = self.get_diagram()
        menu.create_menu(diagram)
        print dir(menu)

        #self.context_menu = self.__create_context_menu()
        


