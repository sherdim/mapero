"""module.py
"""
# Author: Zacarias F. Ojeda <zojeda@gmail.com>
# License: new BSD Style.
from mapero.core.data_type import DefaultDataType
from mapero.core.data_type import DataType

import inspect
import logging

from enthought.traits import api as traits
from enthought.traits.ui.api import View, Group, Include

from mapero.core.port import InputPort
from mapero.core.port import OutputPort

module_registry = []

log = logging.getLogger("mapero.logger.module");


class PortNotFoundError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class InputPortNotFoundError(PortNotFoundError):
    pass

class OutputPortNotFoundError(PortNotFoundError):
    pass


class MetaModule ( traits.MetaHasTraits ):
    def __init__ ( cls, name, bases, dict):
        super(MetaModule, cls).__init__(name, bases, dict)
        cls.module_class = cls.__class__
#        canonical_name = cls.__module__.split('mapero.modules.')
#        cls.canonical_name = len(canonical_name)==2 and canonical_name[1] or cls.__module__
        cls.canonical_name = cls.__module__
        cls.source_code_file = inspect.getsourcefile(cls)
        
        
    def __call__(cls, *args):
        inst = super(MetaModule, cls).__call__( *args )
        MetaModule.init_ports(inst)
        return inst
    
    @staticmethod
    def init_ports(module):
        for attr_name in module.__class__.__dict__:
            attr = getattr(module, attr_name)
            if isinstance(attr, (InputPort, OutputPort)):
                port = type(attr)(name = attr_name, module=module)
                if not isinstance(attr.data_type, DataType):
                    data_type = DefaultDataType(type = attr.data_type)
                else:
                    data_type = attr.data_type
                    
                port.data_type = data_type
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
    
    input_ports = traits.List(InputPort, [])
    output_ports = traits.List(OutputPort, [])

    #logs = Dict(Str, Str)

    module_view = View(
                       Group(
                             Group('label', label='Module', springy=True),
                             Include('view')
                             )
                       )

#    class ProcessThread(Thread):
#        def __init__(self, module):
#             Thread.__init__(self, name=module.__class__.__name__+'-process')
#             self.module = module
#        def run(self):
#             self.module._process()

    def __init__(self, **traits):
        super(Module, self).__init__(**traits)
        log.debug( "creating module" )
        self.module_info = {}

        #self.logs = {'error': '', 'warning': '', 'info': '', 'debug': ''}
        #self.log('info', "Module %s created", self.__class__.__name__)

    def __del__(self):
        log.debug( "Module %s deleted" % self.__class__.__name__)
        print "MODULO ELIMINADO"

    def start_module(self):
        self.start()
        log.debug( "Module %s started" % self.__class__.__name__)

    def start(self):
        pass

    def stop_module(self):
        self.stop()
        log.debug( "Module %s stoped" % self.__class__.__name__)

    def stop(self):
        pass

    def update_module(self, input_port, old=None, new=None):
        log.debug( "Updating module  %s  from  %s" % (self.__class__.__name__, input_port.name))
        self.execute()
        #print 'module %s updated from input port: %s' % (self.name, input_port)

    def execute(self):
        raise NotImplementedError

    def get_input(self, port):
        for input in self.input_ports:
            if isinstance(port,str):
                if (input.name == port):
                    return input
            else:
                if input == port:
                    return input
        raise InputPortNotFoundError(port)

    def get_output(self, port):
        for output in self.output_ports:
            if isinstance(port,str):
                if output.name == port:
                    return output
            else:
                if output == port:
                    return output
        raise OutputPortNotFoundError(port)
        
    def __get_pure_state__(self):
        traits_names = self.class_trait_names()
        avoided_traits = ['input_ports', 'output_ports', 'trait_added',
                           'trait_modified', 'progress', 'window_manager','parent','win', 'source_code' ]
        traits = [ trait for trait in traits_names if trait not in avoided_traits ]
        log.debug("returning state : %s for module [%s]" % (traits,self.__class__.__name__ ))
        result = self.get(traits)
        return result

    

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

