from mapero.core.catalog import ModuleInfo
import wx
#import wx.aui

import wx.lib.pydocview as pydocview
from mapero.core.catalog import Catalog
from mapero.dataflow_editor.ui.catalog_tree import CatalogTree

class DataflowEditorFrame(pydocview.DocTabbedParentFrame):
    def __init__(self, docManager, frame, id, title, pos = wx.DefaultPosition,
                size = wx.DefaultSize, style = wx.DEFAULT_FRAME_STYLE,
                name = "DataflowEditorFrame",
                embeddedWindows = 0, minSize=20):

        super(DataflowEditorFrame, self).__init__(docManager, frame, id, title, pos,
                        size, style, name, embeddedWindows )


#        self.mgr = wx.aui.AuiManager(self)
#        self.mgr.AddPane(self.networks_panel, wx.CENTER, 'Networks')
#        self.mgr.AddPane(self._catalog_tree.control, wx.LEFT, 'Catalog')
#        self.mgr.Update()


#    def _LayoutWindow(self):
#        """
#        Lays out the frame.
#        """
#        wx.LayoutAlgorithm().LayoutFrame(self, self.networks_panel)
        


    def OnSize(self, event):
        event.Skip()
        
    def CreateNotebook(self):
        """
        Creates the notebook to use for the tabbed document interface.
        """
        print "creating notebook"

        split = wx.SplitterWindow(self, -1, style=wx.SP_3D)
        
        #split.SetMinimumPaneSize(20)
        self.split = split

        catalog = Catalog()
        self._catalog_tree = CatalogTree(self.split, root=catalog.modules)
        wx.EVT_MOTION(self._catalog_tree.control, self._on_catalog_tree_anytrait_changed)
        
        self.networks_panel = wx.Panel(self.split, -1, style=wx.BORDER_RAISED)
        vbox_np = wx.BoxSizer()
        
        split.SplitVertically(self._catalog_tree.control, self.networks_panel, 220)
    
        if wx.Platform != "__WXMAC__":
                self._notebook = wx.Notebook(self.networks_panel, wx.NewId())
        else:
                self._notebook = wx.Listbook(self.networks_panel, wx.NewId(), style=wx.LB_LEFT)
        # self._notebook.SetSizer(wx.NotebookSizer(self._notebook))
        if wx.Platform != "__WXMAC__":
            wx.EVT_NOTEBOOK_PAGE_CHANGED(self, self._notebook.GetId(), self.OnNotebookPageChanged)
        else:
            wx.EVT_LISTBOOK_PAGE_CHANGED(self, self._notebook.GetId(), self.OnNotebookPageChanged)
        wx.EVT_RIGHT_DOWN(self._notebook, self.OnNotebookRightClick)
        wx.EVT_MIDDLE_DOWN(self._notebook, self.OnNotebookMiddleClick)
        # wxBug: wx.Listbook does not implement HitTest the same way wx.Notebook
        # does, so for now don't fire MouseOver events.
        if wx.Platform != "__WXMAC__":
                wx.EVT_MOTION(self._notebook, self.OnNotebookMouseOver)
        templates = wx.GetApp().GetDocumentManager().GetTemplates()
        iconList = wx.ImageList(16, 16, initialCount = len(templates))
        self._iconIndexLookup = []
        for template in templates:
            icon = template.GetIcon()
            if icon:
                if icon.GetHeight() != 16 or icon.GetWidth() != 16:
                    icon.SetHeight(16)
                    icon.SetWidth(16)
                    if wx.GetApp().GetDebug():
                        print "Warning: icon for '%s' isn't 16x16, not crossplatform" % template._docTypeName
                iconIndex = iconList.AddIcon(icon)
                self._iconIndexLookup.append((template, iconIndex))

        icon = pydocview.getBlankIcon()
        if icon.GetHeight() != 16 or icon.GetWidth() != 16:
            icon.SetHeight(16)
            icon.SetWidth(16)
            if wx.GetApp().GetDebug():
                print "Warning: getBlankIcon isn't 16x16, not crossplatform"
        self._blankIconIndex = iconList.AddIcon(icon)
        self._notebook.AssignImageList(iconList)
        
        
        vbox_np.Add(self._notebook, 1, wx.EXPAND, 0)
        self.networks_panel.SetSizer(vbox_np)
        
        all_sizer = wx.BoxSizer(wx.VERTICAL)
        all_sizer.Add(self.split, 1 ,wx.EXPAND, 0)
        self.SetSizer(all_sizer)
        #all_sizer.Fit(self)
        self.Layout()
        
        


    ###########################################################################
    # Private interface.
    ###########################################################################
    def _on_catalog_tree_anytrait_changed(self, evt):
        """ On Dragging in Catalog Tree """
        if evt.Dragging():
            for selection in self._catalog_tree.selection:
                if isinstance(selection,ModuleInfo):
                    data = wx.TextDataObject()
                    #text = selection + ' '  ##esta cagada me llevo una manana entera
                    text = selection.canonical_name
                    print "text: ", text
                    data.SetText(text)
                    ds = wx.DropSource(self._catalog_tree.control)
                    ds.SetData(data)
                    result = ds.DoDragDrop(wx.Drag_AllowMove)
                    if result == wx.DragCopy:
                        "copy"
                    elif result == wx.DragMove:
                        "moved"
                    else:
                        "failed"

            return
        evt.Skip()

