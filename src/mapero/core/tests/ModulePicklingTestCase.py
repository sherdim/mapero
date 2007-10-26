import unittest

from mapero.core.catalog import Catalog
from mapero.core.module_manager import ModuleManager
from mapero.core.connection import Connection
from mapero.core.module import Module 
from enthought.persistence import state_pickler as state_pickler



class ModulePicklingTestCase(unittest.TestCase):
            
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
        
    def test_network_pickling(self):
        self.module_manager = ModuleManager()
        value = 23
        m1 = self.module_manager.add("test.modulo1")
        m1.label = "loadedModule"
        m2 = self.module_manager.add("test.modulo2")
        
        self.module_manager.connect(m1, 'salida1', m2, 'entrada1')
        
        m1.param = value
        
        network = self.module_manager.network
        s = state_pickler.dumps(network)    # Dump the state of `a`.
        state = state_pickler.loads_state(s)     # Get the state back.
        b = self.module_manager.create_network_instance(state) # Create the object.
#        for connection in state.connections:
#            b.connections.append(Connection())
#        for module in state.modules:
#            b.modules.append(Module())
#        state_pickler.set_state(b, state)        # Set the object's state.
        
        print b.modules[1].progress
        
        
        
        
if __name__ == '__main__':
    unittest.main()
