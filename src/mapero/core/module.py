"""module.py
"""
# Author: Zacarias F. Ojeda <zojeda@gmail.com>
# License: new BSD Style.
from mapero.core.port_instance import InputPortInstance, OutputPortInstance

import inspect
import logging

from enthought.traits import api as traits
from enthought.traits.ui.api import View, Group, Include

log = logging.getLogger("mapero.logger.module");


class MetaModule ( traits.MetaHasTraits ):
    def __init__ ( cls, name, bases, dict):
        super(MetaModule, cls).__init__(name, bases, dict)
        cls.module_class = cls.__class__
#        canonical_name = cls.__module__.split('mapero.modules.')
#        cls.canonical_name = len(canonical_name)==2 and canonical_name[1] or cls.__module__
        cls.canonical_name = cls.__module__
        cls.source_code_file = inspect.getsourcefile(cls)
        
#        
#    def __call__(cls, *args):
#        inst = super(MetaModule, cls).__call__( *args )
#        MetaModule.init_ports(inst)
#        return inst
#    
    @staticmethod
    def init_ports(module):
        for attr_name in module.__class__.__dict__:
            attr = getattr(module, attr_name)
            if isinstance(attr, (InputPort, OutputPort)):
                port = type(attr)(name = attr_name, module=module)
                port.data_type = attr.data_type
                module.__dict__[attr_name] = port
                
                if isinstance(attr, InputPort):
                    module.input_ports.append(port)
                if isinstance(attr, OutputPort):
                    module.output_ports.append(port)
        

######################################################################
# `Module` class.
######################################################################
class Module(traits.HasTraits):
    """ Base class for all modules in the mapero structure """
    
    __metaclass__ = MetaModule
    
    __version__ = 1.0
    
    id = traits.Int(None)
    label = traits.Str('None')
    progress = traits.Range(0,100)
    
    input_ports = traits.List(InputPortInstance, [])
    output_ports = traits.List(OutputPortInstance, [])

    module_view = View(
                       Group(
                             Group('label', label='Module', springy=True),
                             Include('view')
                             )
                       )


    def __init__(self, **traits):
        super(Module, self).__init__(**traits)
        log.debug( "creating module" )

    def __del__(self):
        log.debug( "Module %s deleted" % self.__class__.__name__)
        print "MODULO ELIMINADO"

    def start_module(self):
        log.debug( "Module %s started" % self.__class__.__name__)

    def stop_module(self):
        log.debug( "Module %s stoped" % self.__class__.__name__)

    def pre_execute(self):
        return True

    def execute(self):
        raise NotImplementedError

    def post_execute(self):
        return True

    

class VisualModule(Module):
    win = traits.Any

    def __init__(self, **traits):
        super(VisualModule, self).__init__(**traits)

    def create_control(self, parent):
        "Subclasses should override this method and return an UI specific control"
        raise NotImplementedError

    def destroy_control(self):
        "Subclasses should override this method and destroy the UI specific control"
        raise NotImplementedError

