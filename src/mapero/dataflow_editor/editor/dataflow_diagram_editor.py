# Author: Zacarias F. Ojeda <zojeda@gmail.com>
# License: new BSD Style.

from enthought.traits.api import Instance, Property, List, on_trait_change
from enthought.pyface.workbench.api import Editor

from mapero.core.catalog import Catalog
from mapero.core.api import VisualModule, Connection

from mapero.dataflow_editor.editor.model.module_geometrics import ModuleGeometrics
from mapero.dataflow_editor.editor.model.connection_geometrics import ConnectionGeometrics
from mapero.dataflow_editor.editor.diagram.diagram_window import DiagramWindow 
from mapero.dataflow_editor.editor.model.diagram_object_model import DiagramObjectModel
from mapero.dataflow_editor.view.visual_module_view import VisualModuleView

#### Handy functions ##########################################################

def _id_generator():
    """ Return an ever-increasing number useful for creating unique Ids. """

    n = 1
    while True:
        yield(n)
        n += 1

_id_generator = _id_generator()

class DataflowDiagramEditor(Editor):

    dataflow_diagram = Instance(DiagramWindow)
    
    ui_dataflow = Property()
    
    selection = List(DiagramObjectModel)
    
    ###########################################################################
    # 'IWorkbenchPart' interface.
    ###########################################################################

    #### Trait initializers ###################################################
    
    def _id_default(self):
        """ Trait initializer. """

        return 'de_%d' % _id_generator.next()

    def _name_default(self):
        """ Trait initializer. """

        return 'Dataflow Diagram [%s]' % (self.id)

    #### Methods ##############################################################
    
    def create_control(self, parent):
        """ Create the toolkit-specific control that represents the editor. """

        # We hold a reference to the scene itself to make sure it does not get
        # garbage collected (because we only return the scene's 'control' not
        # the scene itself). The scene is also referenced by the scene manager.
        self.dataflow_diagram = self._create_dataflow_diagram(parent)

        return self.dataflow_diagram.control

    
    def _create_dataflow_diagram(self, parent):
        dataflow_diagram = DiagramWindow(parent = parent,
                                         ui_dataflow = self.ui_dataflow,
                                         editor = self)
        print self.ui_dataflow
        return dataflow_diagram
    
    
    
    ##### DDE Interface #######################################################
    
    def add_module(self, module_canonical_name, position=[100,100], bounds=[100,60]):
        catalog = self.window.get_service(Catalog)
        module = catalog.load_module(module_canonical_name)
#        ui_dataflow = self.obj
        self.ui_dataflow.add_module(module, position[0], position[1],
                                            bounds[0], bounds[1])
        
        
    def add_connection(self, output_port, input_port, points = []):
        #print "output_port: ", output_port
        #print "input_port: ", input_port
        connection = Connection(output_port = output_port, input_port = input_port)
        self.ui_dataflow.add_connection(connection)
        
    def remove_selection(self):
        #TODO: very ugly use of isinstance
        for selection in self.selection:
            if isinstance(selection, ModuleGeometrics):
                self.ui_dataflow.remove_module(selection)
            if isinstance(selection, ConnectionGeometrics):
                self.ui_dataflow.remove_connection(selection)
        self.selection = []
        
    def _get_ui_dataflow(self):
        return self.obj
    
    @on_trait_change('obj:dataflow.modules')
    def on_modules_change(self, event):
        if not isinstance(event,list):
            for module in event.added:
                if isinstance(module, VisualModule):
                    view = VisualModuleView(visual_module = module)
                    self.window.add_view(view)
            for module in event.removed:
                if isinstance(module, VisualModule):
                    view = self.window.get_view_by_id(
                                VisualModuleView.construct_visual_module_view_id(self.window, module)
                                )
                    self.window.close_view(view)
