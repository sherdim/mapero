# Author: Zacarias F. Ojeda <zojeda@gmail.com>
# License: new BSD Style.

from mapero.core.dataflow import Dataflow
from module_geometrics import ModuleGeometrics
from connection_geometrics import ConnectionGeometrics

from enthought.traits.api import HasTraits, List, Instance
from enthought.traits.has_traits import on_trait_change

import logging
logger = logging.getLogger()

class GraphicDataflowModel(HasTraits):
    
    dataflow = Instance(Dataflow, Dataflow())
    module_geometrics = List(ModuleGeometrics, [])
    connection_geometrics = List(ConnectionGeometrics, [])

    from_here = False
    def __init__(self, **traits):
        super(GraphicDataflowModel, self).__init__(**traits)
        self.dataflow.on_trait_change(self.on_dataflow_connections_changes, 'connections')
        self.dataflow.on_trait_change(self.on_dataflow_modules_changes, 'modules')
    
    def add_module(self, module, x=200, y=200, w=200, h=100):
        self.from_here = True
        self.dataflow.modules.append( module )
        self._add_module_geom(module, x, y, w, h)
        self.from_here = False
    
    def remove_module(self, module_geometrics):
        self.dataflow.modules.remove( module_geometrics.module )

    def remove_connection(self, connection_geometrics):
        self.dataflow.connections.remove( connection_geometrics.connection )

    def add_connection(self, connection, points=[]):
        self.from_here = True
        self.dataflow.connections.append( connection )
        self._add_connection_geom(connection, points)
        self.from_here = False
        
    @on_trait_change('dataflow:connections')
    def on_dataflow_connections_changes(self, event):
        if not self.from_here:
            for connection in event.added:
                self._add_connection_geom(connection)

            for connection in event.removed:
                self._remove_connection_geom(connection)

    @on_trait_change('dataflow:modules')
    def on_dataflow_modules_changes(self, event):
        if not self.from_here:
            for module in event.added:
                self._add_module_geom(module)
            
            for module in event.removed:
                self._remove_module_geom(module)

    def _add_module_geom(self, module, x=200, y=200, w=200, h=100):
        module_geometrics = ModuleGeometrics(position=[x,y], bounds=[w,h], module=module)
        self.module_geometrics.append( module_geometrics )

    def _add_connection_geom(self, connection, points=[]):
        connection_geometrics = ConnectionGeometrics(connection=connection, points=points)
        self.connection_geometrics.append( connection_geometrics )
        
    def _remove_module_geom(self, module):
        module_geometrics = None
        for module_geom in self.module_geometrics:
            if module_geom.module == module:
                module_geometrics = module_geom
                break
        if module_geometrics:    
            self.module_geometrics.remove(module_geometrics)
        else:
            logger.error("not module_geomtrics found for module: %s" % (module))

    def _remove_connection_geom(self, connection):
        connection_geometrics = None
        for connection_geom in self.connection_geometrics:
            if connection_geom.connection == connection:
                connection_geometrics = connection_geom
                break
        if connection_geometrics:    
            self.connection_geometrics.remove(connection_geometrics)
        else:
            logger.error("not connection_geomtrics found for connection: %s" % (connection))
                        