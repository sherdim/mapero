#!/usr/bin/env python
"""module.py
"""

# Author: Zacarias F. Ojeda <correo@zojeda.com.ar>
# Copyright (c) 2005, Enthought, Inc.
# License: BSD Style.

# Standard library imports.
import wx

from enthought.traits import api as traits

from mapero.core.port import InputPort
from mapero.core.port import OutputPort
from mapero.dataflow_editor.decorators.thread import threaded_process, invoke_later

from enthought.traits.ui.api import View, Group, Include

import logging
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

######################################################################
# `Module` class.
######################################################################
class Module(traits.HasTraits):
    """ Base class for all modules in the mapero structure """
    id = traits.Int
    label = traits.Str
    progress = traits.Range(0,100)

    input_ports = traits.List(InputPort)
    output_ports = traits.List(OutputPort)

    #logs = Dict(Str, Str)

    module_view = View(Group(
                        Group('label', label='General'),
                        Include('view')))

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
        self.update(input_port, old, new)
        #print 'module %s updated from input port: %s' % (self.name, input_port)

    def update(self, input_port, old=None, new=None):
        print 'datos actualizados'

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
                           'trait_modified', 'progress', 'parent' ]
        traits = [ trait for trait in traits_names if trait not in avoided_traits ]
        log.debug("returning state : %s for module [%s]" % (traits,self.__class__.__name__ ))
        result = self.get(traits)
        return result

    

class VisualModule(Module):
    parent = traits.Any

    def __init__(self, **traits):
        super(VisualModule, self).__init__(**traits)


    def start_module(self):
        if not self.parent:
            self.parent = wx.Frame(None, -1, self.name)
            self.win = self._create_window()

            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(self.win, 1, wx.EXPAND)
            self.parent.SetSizer(sizer)
            super(VisualModule, self).start_module()
            self.parent.Show( True )

    def stop_module(self):
        if self.parent:
            self.parent.Destroy()
            super(VisualModule, self).stop_module()

    def _create_window(self):
        "Subclasses should override this method and return an enable.wx.Window"
        raise NotImplementedError


