import unittest

from mapero.core.module_manager import ModuleManager 

class ModuleManagerTestCase(unittest.TestCase):
    
    def setUp(self):
        self.module_manager = ModuleManager()
        print "setup"
        
    def testone(self):
        print "testone"
        
if __name__ == '__main__':
    unittest.main()
