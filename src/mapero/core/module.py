#!/usr/bin/env python
"""module.py
"""

# Author: Zacarias F. Ojeda <correo@zojeda.com.ar>
# Copyright (c) 2005, Enthought, Inc.
# License: BSD Style.

# Standard library imports.
import wx
import logging
from threading import Thread
from enthought.traits.api import HasTraits, Range, Any, List, Str

from mapero.core.port import InputPort
from mapero.core.port import OutputPort

from enthought.traits.ui.api import View, Group, Include

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
class Module(HasTraits):
    """ Base class for all modules in the mapero structure """
    label = Str
    progress = Range(0,100)

    input_ports = List(InputPort)
    output_ports = List(OutputPort)

    #logs = Dict(Str, Str)

    module_view = View(    Group(
                        Group('label', label='General'),
                        Include('view')))

    class ProcessThread(Thread):
        def __init__(self, module):
             Thread.__init__(self)
             self.module = module
        def run(self):
             self.module._process()

    def __init__(self, **traits):
        super(Module, self).__init__(**traits)
        logging.debug( "creating module" )
        self.module_info = {}

        #self.logs = {'error': '', 'warning': '', 'info': '', 'debug': ''}
        #self.log('info', "Module %s created", self.__class__.__name__)

    def __del__(self):
        logging.debug( "Module %s deleted" % self.__class__.__name__)

    def start_module(self):
        self.start()
        logging.debug( "Module %s started" % self.__class__.__name__)

    def start(self):
        pass

    def stop_module(self):
        self.stop()
        logging.debug( "Module %s stoped" % self.__class__.__name__)

    def stop(self):
        pass

    def update_module(self, input_port, old=None, new=None):
        self.update(input_port, old, new)
        #print 'module %s updated from input port: %s' % (self.name, input_port)

    def update(self, input_port, old=None, new=None):
        print 'datos actualizados'


    def process(self):
#        process_thread = self.ProcessThread(self)
#        logging.debug("starting module processing thread : " +  self.__class__.__name__ )
#        process_thread.start()
#        logging.debug("started module processing thread : " + self.__class__.__name__ )
        self._process()

    def _process(self):
        pass

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
        """Method used by the state_pickler.
        """
        d = self.__dict__.copy()
        for attr in d.keys():
            if attr not in self.trait_names():
                d.pop(attr, None)
        return d




class VisualModule(Module):
    parent = Any

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


