"""module.py
"""
# Author: Zacarias F. Ojeda <zojeda@gmail.com>
# License: new BSD Style.
from mapero.core.port_instance import InputPortInstance, OutputPortInstance
from enthought.traits.has_traits import HasStrictTraits

import inspect
import logging

from enthought.traits.api import Int, List, Str, Range, HasTraits, MetaHasTraits
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
class Module( HasStrictTraits ):
    """ Base class for all modules in the mapero structure """
    
    __metaclass__ = MetaModule
    
    __version__ = 1.0
    
    id = Int(None)
    label = Str('None')
    progress = Range(0,100)
    
    input_ports = List(InputPortInstance, [])
    output_ports = List(OutputPortInstance, [])

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

    def __get_pure_state__(self):
        traits_names = self.class_trait_names()
        avoided_traits = ['input_ports', 'output_ports', 'trait_added',
                           'trait_modified', 'progress' ]
        traits = [ trait for trait in traits_names if trait not in avoided_traits ]
        log.debug("returning state : %s for module [%s]" % (traits,self.__class__.__name__ ))
        result = self.get(traits)
        return result
    
class VisualModule(Module):

    def __init__(self, **traits):
        super(VisualModule, self).__init__(**traits)

    def create_control(self, parent):
        "Subclasses should override this method and return an UI specific control"
        raise NotImplementedError

    def destroy_control(self):
        "Subclasses should override this method and destroy the UI specific control"
        raise NotImplementedError

