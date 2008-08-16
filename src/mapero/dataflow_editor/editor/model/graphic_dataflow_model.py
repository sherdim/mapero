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
        self.dataflow.on_trait_change(self.on_dataflow_connections_changes, 'connections')
        self.dataflow.on_trait_change(self.on_dataflow_modules_changes, 'modules')
    
    def add_module(self, module, x=200, y=200, w=200, h=100):
        self.dataflow.on_trait_change(self.on_dataflow_modules_changes, 'modules', remove=True)
        self.dataflow.modules.append( module )
        self._add_module_geom(module, x, y, w, h)
        self.dataflow.on_trait_change(self.on_dataflow_modules_changes, 'modules')

    def add_connection(self, connection, points=[]):
        self.dataflow.on_trait_change(self.on_dataflow_connections_changes, 'connections', remove=True)
        self.dataflow.connections.append( connection )
        self._add_connection_geom(connection, points)
        self.dataflow.on_trait_change(self.on_dataflow_connections_changes, 'connections')
        
    def on_dataflow_connections_changes(self, event):
        for connection in event.added:
            self._add_connection_geom(connection)

        for connection in event.removed:
            self._remove_connection_geom(connection)

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