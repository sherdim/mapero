# Author: Zacarias F. Ojeda <zojeda@gmail.com>
# License: new BSD Style.

from mapero.dataflow_editor.editor.model.api import GraphicDataflowModel

from mapero.dataflow_editor.editor.diagram.components.module_component import ModuleComponent
from mapero.dataflow_editor.editor.diagram.components.connection_component import ConnectionComponent
from mapero.dataflow_editor.editor.diagram.tools.connection_adding_tool import ConnectionAddingTool
from mapero.dataflow_editor.editor.diagram.tools.selection_tool import SelectionTool


from enthought.traits.api import Instance, Any, on_trait_change, TraitListEvent, Dict, Delegate
from enthought.traits.ui.menu import Menu, Action, Separator

from enthought.enable.api import Viewport, Window, Scrolled
from enthought.enable.drawing.api import DrawingCanvas
from enthought.enable.tools.api import ViewportPanTool
from enthought.pyface.workbench.api import IEditor
from mapero.dataflow_editor.editor.diagram.components.diagram_component import DiagramComponent
from mapero.dataflow_editor.editor.model.diagram_object_model import DiagramObjectModel

class MyCanvas(DrawingCanvas):
    bgcolor = (1.0, 0.95, 0.71, 1.0)
    draw_axes=True
    window = Window
    editor = Delegate('window')
    module_geom_component_map  = Delegate('window')
    connection_geom_component_map  = Delegate('window')
    auto_size = False
    fit_window = False
    
    def __init__(self, window):
        self.window = window
        self.auto_size = False
        self.fit_window = False
        self.bounds = [3000,3000]
        self.activate(ConnectionAddingTool( container = self ))
        self.listening_tools.append( SelectionTool(container = self) )
    
    def normal_dropped_on(self, event):
        position = [int(event.x), int(event.y)]
        self.editor.add_module( event.obj.module_info.clazz.canonical_name, position=position  )
        
    def normal_drag_over(self, event):
        self.window.set_drag_result('copy')
        
    def normal_key_pressed(self, event):
        if event.character == 'Delete':
            self.editor.remove_selection()

    def normal_right_down(self, event):
        selection_enabled = len(self.editor.selection)>0 and True or False
        modules_selected = len( self.editor.get_modules_selected() ) > 0

        menu = Menu( 
                    Action( name = 'Copy', enabled=False ),
                    Action( name = 'Paste', enabled=False ),
                    Action( name = 'Delete', enabled=selection_enabled,
                             on_perform=self.editor.remove_selection ),
                    Separator(),
                    Action( name = 'Edit Code', enabled=modules_selected,
                             on_perform=self.editor.edit_code ),
#                    Action( name = _('Help'), on_perform=self.show_module_help, enabled=self.is_only_one_module_selected() )
                    )
        popup_menu = menu.create_menu(event.window.control)
        popup_menu.show(event.x, event.window._flip_y(event.y))
        
        
    #the tools should be drawn on the overlay layer
    def _draw_container_overlay(self, gc, view_bounds=None, mode="default"):
        super(MyCanvas, self)._draw_container_mainlayer(gc, view_bounds, mode)
    
    def _draw_container_mainlayer(self, gc, view_bounds=None, mode="default"):
        return            
    
class DiagramWindow(Window):
    
    ui_dataflow = Instance(GraphicDataflowModel)
    
    canvas = Any#Instance(Canvas)
    
    diagram_object_component_dict = Dict(DiagramObjectModel, DiagramComponent)

    editor = Instance(IEditor)
    
    def __init__ ( self, parent, wid = -1, pos = None, size = None, **traits ):
        super(DiagramWindow, self).__init__(parent, wid, pos, size, **traits)
        
        
        self.canvas = MyCanvas(window = self)
        viewport = Viewport(component=self.canvas, enable_zoom=True)
        viewport.view_position = [0,0]
#        viewport.tools.append(ViewportPanTool(viewport))

        # Uncomment the following to enforce limits on the zoom
#        viewport.min_zoom = 0.2
#       viewport.max_zoom = 1.5

        scrolled = Scrolled(self.canvas,
                            inside_padding_width = 0,
                            mousewheel_scroll = False,
                            viewport_component = viewport,
                            continuous_drag_update = True)
        
        self.component = scrolled
    
    @on_trait_change('editor.selection')
    def selection_items_changed(self, event):
        if isinstance(event, list):
            for diagram_object in self.diagram_object_component_dict:
                if diagram_object not in event:
                    self.diagram_object_component_dict[diagram_object].selected = False
                else:
                    self.diagram_object_component_dict[diagram_object].selected = True
        else:
            if event.added:
                for added in event.added:
                    self.diagram_object_component_dict[added].selected = True
            if event.removed:
                for removed in event.removed:
                    self.diagram_object_component_dict[removed].selected = False
        

            
    @on_trait_change('ui_dataflow:module_geometrics')
    def modules_changed(self, event):
        if isinstance(event, TraitListEvent): ## odd
            for module_geometrics in event.added:
                self.add_module_component(module_geometrics)
            
            for module_geometrics in event.removed:
                mod_com = self.diagram_object_component_dict.pop(module_geometrics)
                self.canvas.remove(mod_com)
        self.canvas.invalidate_and_redraw()

    @on_trait_change('ui_dataflow:connection_geometrics')
    def connections_changed(self, event):
        if isinstance(event, TraitListEvent): ## odd
            for connection_geometrics in event.added:
                self.add_connection_component(connection_geometrics)

            for connection_geometrics in event.removed:
                conn_com = self.diagram_object_component_dict.pop(connection_geometrics)
                self.canvas.remove(conn_com)
        self.canvas.invalidate_and_redraw()
            

    def add_module_component(self, module_geometrics):
        module_component = ModuleComponent(module_geometrics, diagram=self)
        self.canvas.add(module_component)
        self.diagram_object_component_dict[module_geometrics] = module_component
        return module_component
        
    def add_connection_component(self, connection_geometrics):
        
        input_port = connection_geometrics.connection.input_port
        for diagram_object in self.diagram_object_component_dict:
            if diagram_object.dataflow_element == input_port.module:
                in_mod_comp = self.diagram_object_component_dict[diagram_object]
                input_port_component = in_mod_comp.port_component_dict[input_port]
        
        output_port = connection_geometrics.connection.output_port
        for diagram_object in self.diagram_object_component_dict:
            if diagram_object.dataflow_element == output_port.module:
                out_mod_comp = self.diagram_object_component_dict[diagram_object]
                output_port_component = out_mod_comp.port_component_dict[output_port]

        connection_component = ConnectionComponent(
                                                   connection_geometrics = connection_geometrics,
                                                   output_port_component = output_port_component,
                                                   input_port_component = input_port_component,
                                                   )
        
        self.canvas.add(connection_component)
        self.diagram_object_component_dict[connection_geometrics] = connection_component
        return connection_component
        

        