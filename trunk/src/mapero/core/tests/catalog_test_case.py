import unittest

from mapero.core.catalog import Catalog

class CatalogTestCase(unittest.TestCase):

    def setUp(self):
        self.catalog = Catalog()
    
    def test_import_module(self):
        m1 = self.catalog.import_module("modules.test.modulo1")
        m2 = self.catalog.import_module("modules.test.other.modulo1")
#        print "===================="
#        print_module(m1)
#        print "===================="
#        print_module(m2)
#        print "===================="

    def test_catalog(self):
        self.catalog.recorrer()
        
    def test_load_module(self):
        m1 = self.catalog.load_module("test.modulo1")
        m2 = self.catalog.load_module("test.other.modulo1")
        
#        module1 = self.catalog.load_module("test.modulo1")
#        module3 = self.catalog.load_module("test.other.modulo1")

def print_module(module):
        print dir(module)
        print module.__file__
        print module.__name__
        print module.__doc__
    
if __name__ == '__main__':
    unittest.main()
