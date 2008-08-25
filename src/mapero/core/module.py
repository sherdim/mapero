"""module.py
"""
# Author: Zacarias F. Ojeda <zojeda@gmail.com>
# License: new BSD Style.
from mapero.core.port_instance import InputPortInstance, OutputPortInstance

import inspect
import logging

from enthought.traits.api import Int, List, Str, Range, MetaHasTraits, HasTraits
from enthought.traits.ui.api import View, Group, Include

log = logging.getLogger("mapero.logger.module");


class MetaModule ( MetaHasTraits ):
    def __init__ ( cls, name, bases, dict):
        super(MetaModule, cls).__init__(name, bases, dict)
        cls.module_class = cls.__class__
#        canonical_name = cls.__module__.split('mapero.modules.')
#        cls.canonical_name = len(canonical_name)==2 and canonical_name[1] or cls.__module__
        cls.canonical_name = cls.__module__
        cls.source_code_file = inspect.getsourcefile(cls)
        

######################################################################
# `Module` class.
######################################################################
class Module( HasTraits ):
    """ Base class for all modules in the mapero structure """
    
    __metaclass__ = MetaModule
    
    __version__ = 1.0
    
    id = Int(None)
    label = Str('None')
    progress = Range(0,100, transient=True)
    
    input_ports = List(InputPortInstance, [], transient=True)
    output_ports = List(OutputPortInstance, [], transient=True)

    module_view = View(
                       Group(
                             Group('label', label='Module', springy=True),
                             Include('view'),
                             show_labels = True
                             )
                       )

    def get_port(self, name):
        for input_port in self.input_ports:
            if input_port.name == name:
                return input_port
        for output_port in self.output_ports:
            if output_port.name == name:
                return output_port
            
        raise NotImplementedError

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

    def __init__(self, **traits):
        super(VisualModule, self).__init__(**traits)

    def create_control(self, parent):
        "Subclasses should override this method and return an UI specific control"
        raise NotImplementedError

    def destroy_control(self):
        "Subclasses should override this method and destroy the UI specific control"
        raise NotImplementedError

