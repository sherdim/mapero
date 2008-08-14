# Author: Zacarias F. Ojeda <zojeda@gmail.com>
# License: new BSD Style.

from mapero.core.dataflow import Dataflow
from module_geometrics import ModuleGeometrics
from connection_geometrics import ConnectionGeometrics
from enthought.traits.api import HasTraits, List, Instance
from enthought.traits.has_traits import on_trait_change


class GraphicDataflowModel(HasTraits):
    dataflow = Instance(Dataflow, Dataflow())
    module_geometrics = List(ModuleGeometrics, [])
    connection_geometrics = List(ConnectionGeometrics, [])
    
    def __init__(self, **traits):
        super(GraphicDataflowModel, self).__init__(**traits)
    
    def add_module(self, module, x=200, y=200, w=200, h=100):
        self.dataflow.modules.append( module )
    
    @on_trait_change('dataflow:connections')
    def on_dataflow_connections_changes(self, event):
        for connection in event.added:
            self._add_connection_geom(connection)

        for connection in event.removed:
            self._remove_connection_geom(connection)

    @on_trait_change('dataflow:modules')
    def on_dataflow_modules_changes(self, event):
        for module in event.added:
            self._add_module_geom(module)
            
        for module in event.removed:
            self._remove_module_geom(module)

    def _add_module_geom(self, module, x=200, y=200, w=200, h=100):
        module_geometrics = ModuleGeometrics(x=x, y=y, w=w, h=h, module=module)
        self.module_geometrics.append( module_geometrics )

    def _add_connection_geom(self, connection, points=[]):
        connection_geometrics = ConnectionGeometrics(connection=connection, points=points)
        self.connection_geometrics.append( connection_geometrics )