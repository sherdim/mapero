# Author: Zacarias F. Ojeda <zojeda@gmail.com>
# License: new BSD Style.

from mapero.core.module import Module
from mapero.dataflow_editor.editor.model.api import GraphicDataflowModel

from mapero.dataflow_editor.editor.diagram.module_component import ModuleComponent
from mapero.dataflow_editor.editor.diagram.connection_component import ConnectionComponent


from enthought.traits.api import Instance, on_trait_change, TraitListEvent, Dict
from enthought.enable.api import Canvas, Viewport, Window, Scrolled
from enthought.enable.drawing.api import DrawingCanvas
from enthought.enable.tools.api import ViewportPanTool
from enthought.pyface.workbench.api import IEditor

CURRENT_SELECTION_VIEW = 'mapero.dataflow_editor.view.current_selection'

        

        
        
       
class MyCanvas(Canvas):
    bgcolor = (1.0, 0.95, 0.71, 1.0)
    draw_axes=True
    diagram = Window
    
    def normal_dropped_on(self, event):
        position = [event.x,event.y]
        self.diagram.editor.add_module( event.obj.module_info.clazz.canonical_name, position=position  )
        
    def normal_drag_over(self, event):
        self.diagram.set_drag_result('copy')
            
    
class DiagramWindow(Window):
    
    dataflow_with_geom = Instance(GraphicDataflowModel)
    
    canvas = Instance(Canvas)
    
    module_geom_component_map = Dict(Module, ModuleComponent)
    
    editor = Instance(IEditor)
    
    def __init__ ( self, parent, wid = -1, pos = None, size = None, **traits ):
        super(DiagramWindow, self).__init__(parent, wid, pos, size, **traits)
        
        
        self.canvas = MyCanvas(diagram=self)
#        viewport = Viewport(component=self.canvas, enable_zoom=True)
#        viewport.view_position = [0,0]
#        viewport.tools.append(ViewportPanTool(viewport))
#
#        # Uncomment the following to enforce limits on the zoom
#        viewport.min_zoom = 0.2
#        viewport.max_zoom = 1.5

        scrolled = Scrolled(self.canvas, fit_window = True,
                            inside_padding_width = 0,
                            mousewheel_scroll = False,
                            #viewport_component = viewport,
                            always_show_sb = True,
                            continuous_drag_update = True)
        
        self.component = scrolled
    
    @on_trait_change('editor.selection')
    def selection_items_changed(self, event):
        if isinstance(event, list):
            for module in self.module_geom_component_map:
                if module not in event:
                    self.module_geom_component_map[module].event_state = 'normal'
                else:
                    self.module_geom_component_map[module].event_state = 'selected'
        else:
            if event.added:
                for added in event.added:
                    self.module_geom_component_map[added].event_state = 'selected'
            if event.removed:
                for removed in event.removed:
                    self.module_geom_component_map[removed].event_state = 'normal'

            
    @on_trait_change('dataflow_with_geom:module_geometrics')
    def modules_changed(self, event):
        if isinstance(event, TraitListEvent): ## odd
            for module_geometrics in event.added:
                self.add_module_component(module_geometrics)
            
    @on_trait_change('dataflow_with_geom:connection_geometrics')
    def connections_changed(self, event):
        if isinstance(event, TraitListEvent): ## odd
            for connection_geometrics in event.added:
                self.add_connection_component(connection_geometrics)
            

    def add_module_component(self, module_geometrics):
        module_component = ModuleComponent(module_geometrics, diagram=self)
        self.canvas.add(module_component)
        self.canvas.invalidate_and_redraw()
        self.module_geom_component_map[module_geometrics.module] = module_component
        return module_component
        
    def add_connection_component(self, connection_geometrics):
        connection_component = ConnectionComponent(connection_geometrics, diagram=self)
        self.canvas.add(connection_component)
        self.canvas.invalidate_and_redraw()
        self.connection_geom_component_map[connection_geometrics.connection] = connection_component
        return connection_component
        

        