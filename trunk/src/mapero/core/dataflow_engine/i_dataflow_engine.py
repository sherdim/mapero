# Author: Zacarias F. Ojeda <correo@zojeda.com.ar>
# License: new BSD.

from enthought.traits.api import Interface


class IDataflowEngine(Interface):
    
    def instanciate_ports(self, module):
        pass
    
    def execute(self):
        pass


