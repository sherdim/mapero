import wx
import wx.aui
import wx.lib.ogl as ogl
import wx.lib.docview as docview
import wx.lib.pydocview as pydocview
from core.catalog import Catalog
from core.ui.catalog_tree import CatalogTree

class DataflowEditorFrame(pydocview.DocTabbedParentFrame):
    def __init__(self, docManager, frame, id, title, pos = wx.DefaultPosition,
                size = wx.DefaultSize, style = wx.DEFAULT_FRAME_STYLE,
                name = "DataflowEditorFrame",
                embeddedWindows = 0, minSize=20):
        super(DataflowEditorFrame, self).__init__(docManager, frame, id, title, pos,
                        size, style, name, embeddedWindows, minSize )

        catalog = Catalog()
        self._catalog_tree = CatalogTree(self, root=catalog.get_catalog().items()[0], )
        wx.EVT_MOTION(self._catalog_tree.control, self._on_catalog_tree_anytrait_changed)

        self.mgr = wx.aui.AuiManager(self)
        self.mgr.AddPane(self.networks_panel, wx.CENTER, 'Networks')
        self.mgr.AddPane(self._catalog_tree.control, wx.LEFT, 'Catalog')
        self.mgr.Update()

    def CreateNotebook(self):
        """
        Creates the notebook to use for the tabbed document interface.
        """
        self.networks_panel = wx.Panel(self)

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

