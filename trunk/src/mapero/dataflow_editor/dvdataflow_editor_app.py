import os.path
from pkg_resources import resource_filename, resource_stream

#sys.path.append(mro_dir)
import wx
import wx.lib.ogl as ogl
import wx.lib.docview as docview
import wx.lib.pydocview as pydocview
import logging.config

from mapero.dataflow_editor.editor_frame import DataflowEditorFrame
from mapero.dataflow_editor.mvc.document import DataflowDocument
from mapero.dataflow_editor.mvc.view import DataflowView

_ = wx.GetTranslation


#----------------------------------------------------------------------------
# Classes
#----------------------------------------------------------------------------

class DataflowEditorApplication(pydocview.DocApp):

    SPLASH = resource_filename(__name__, "splash.png")
    ICON = resource_filename(__name__, "mapero_logo.png")

    def OpenMainFrame(self):
        docManager = self.GetDocumentManager()
        frame = DataflowEditorFrame(docManager, None, -1, self.GetAppName())

        frame.Show(True)



    def OnInit(self):
        # Call the super - this is important!!!
        pydocview.DocApp.OnInit(self)

        # Show the splash dialog while everything is loading up
        if os.path.exists(DataflowEditorApplication.SPLASH):
                self.ShowSplash(DataflowEditorApplication.SPLASH)

        # Set the name and the icon
        self.SetAppName(_("Mapero DataflowEditor"))
        self.SetDefaultIcon(wx.Icon(DataflowEditorApplication.ICON, wx.BITMAP_TYPE_PNG))

        # Initialize the document manager
        docManager = docview.DocManager(flags = self.GetDefaultDocManagerFlags())
        self.SetDocumentManager(docManager)

        # Create a template for text documents and associate it with the docmanager
        textTemplate = docview.DocTemplate(docManager,
                                                    _("Dataflow"),
                                                    "*.mprd",
                                                    _("Dataflow"),
                                                    _("mprd"),
                                                    _("Dataflow Document"),
                                                    _("Dataflow View"),
                                                    DataflowDocument,
                                                    DataflowView,
                                                    icon=wx.Icon(DataflowEditorApplication.ICON, wx.BITMAP_TYPE_PNG))
        docManager.AssociateTemplate(textTemplate)

        # Install services - these can install menu and toolbar items
        windowMenuService     = self.InstallService(pydocview.WindowMenuService())
        filePropertiesService = self.InstallService(pydocview.FilePropertiesService())
        if os.path.exists(DataflowEditorApplication.SPLASH):
            aboutService      = self.InstallService(pydocview.AboutService(image=wx.Image(DataflowEditorApplication.SPLASH)))
        else:
            aboutService      = self.InstallService(pydocview.AboutService())

        #optionsService        = self.InstallService(pydocview.DocOptionsService(supportedModes=docview.DOC_SDI))
        # Install the DataflowEditor's option panel into the OptionsService
        #optionsService.AddOptionsPanel(DataflowEditor.DataflowOptionsPanel)

        # If it is an MDI app open the main frame
        self.OpenMainFrame()

        # Open any files that were passed via the command line
        self.OpenCommandLineArgs()

        # If nothing was opened and it is an SDI app, open up an empty text document
        if not docManager.GetDocuments() and docManager.GetFlags() & docview.DOC_SDI:
            textTemplate.CreateDocument('', docview.DOC_NEW).OnNewDocument()

        # Close the splash dialog
        if os.path.exists(DataflowEditorApplication.SPLASH):
            self.CloseSplash()

        # Show the tips dialog
        if os.path.exists("tips.txt"):
            wx.CallAfter(self.ShowTip, wx.GetApp().GetTopWindow(), wx.CreateFileTipProvider("tips.txt", 0))

        wx.UpdateUIEvent.SetUpdateInterval(1000)  # Overhead of updating menus was too much.  Change to update every N milliseconds.

        # Tell the framework that everything is great
        return True

#----------------------------------------------------------------------------
# Main
#----------------------------------------------------------------------------

# Run the DataflowEditorApplication and do not redirect output to the wxPython error dialog
ogl.OGLInitialize()
app = DataflowEditorApplication(redirect=False)
logging_conf = resource_stream(__name__, 'logging.conf')
logging.config.fileConfig(logging_conf)
app.MainLoop()
