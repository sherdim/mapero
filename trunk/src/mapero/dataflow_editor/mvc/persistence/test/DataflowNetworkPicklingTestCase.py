from mapero.dataflow_editor.mvc.controller import DataflowEditorController
import unittest

from mapero.core.module_manager import ModuleManager

from mapero.dataflow_editor.mvc.model import *
 
from enthought.persistence import state_pickler as state_pickler



class DataflowNetworkPicklingTestCase(unittest.TestCase):
            
#    def test_module_pickling(self):
#        self.module_manager = ModuleManager()
#        m1 = self.module_manager.add("Visualization.pointset_viewer")
#        m1.label = "loadedModule"
#        m2 = self.module_manager.add("Visualization.pointset_viewer")
#        #network = self.module_manager.network
#        network = m1
#        s = state_pickler.dumps(network)    # Dump the state of `a`.
#        state = state_pickler.loads_state(s)     # Get the state back.
#        b = state_pickler.create_instance(state) # Create the object.
#        state_pickler.set_state(b, state)        # Set the object's state.
#        print m2.label
        
    def test_dataflow_pickling(self):
        self.module_manager = ModuleManager()
        value = 23
        m1 = self.module_manager.add("test.modulo1")
        m1.label = "loadedModule"
        m2 = self.module_manager.add("test.modulo2")
        m2.label = "module2"
        
        c1 = self.module_manager.connect(m1, 'out1', m2, 'in1')
        
        m1.param = value
        
        network = self.module_manager.network
        gm1 = ModuleGeometrics(x=10, y=10, h=40, w=90, module_id=m1.id)
        gm2 = ModuleGeometrics(x=100, y=10, h=40, w=90, module_id=m2.id)
        
        gc1 = ConnectionGeometrics()
        
        dataflow_network = DataflowEditorModel(
                                               network=network,
                                               module_geometrics=[gm1,gm2],
                                               connection_geometrics=[gc1]
                                               )
        
        s = state_pickler.dumps(dataflow_network)    # Dump the state of `a`.
        state = state_pickler.loads_state(s)     # Get the state back.
        
        controller = DataflowEditorController()
        dataflow_editor_model = controller.create_dataflow_model(state)

        
        print dataflow_editor_model.network.modules[1].progress
        
        
        
        
if __name__ == '__main__':
    unittest.main()
