# Author: Zacarias F. Ojeda <zojeda@gmail.com>
# License: new BSD Style.

from enthought.pyface.workbench.api import Editor
from enthought.traits.api import Instance, Property

from mapero.dataflow_editor.editor.diagram.diagram_window import DiagramWindow 
from mapero.core.catalog import Catalog
from mapero.core.connection import Connection

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
    
    dataflow_with_geom = Property()
    
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
                                         dataflow_with_geom = self.dataflow_with_geom,
                                         editor = self)
        return dataflow_diagram
    
    
    
    ##### DDE Interface #######################################################
    
    def add_module(self, module_canonical_name, position=[100,100], bounds=[100,60]):
        catalog = self.window.get_service(Catalog)
        module = catalog.load_module(module_canonical_name)
#        dataflow_with_geom = self.obj
        self.dataflow_with_geom.add_module(module, position[0], position[1],
                                            bounds[0], bounds[1])
        
        
    def add_connection(self, output_port, input_port, points = []):
        #print "output_port: ", output_port
        #print "input_port: ", input_port
        connection = Connection(output_port = output_port, input_port = input_port)
        self.dataflow_with_geom.add_connection(connection)
        
    def _get_dataflow_with_geom(self):
        return self.obj