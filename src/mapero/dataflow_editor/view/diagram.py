from mapero.dataflow_editor.view.graphic_dataflow_model import GraphicDataflowModel
from mapero.dataflow_editor.view.module_geometrics import ModuleGeometrics
from math import pi
from enthought.traits.api import Bool, Float,Instance, on_trait_change, TraitListEvent, Dict, WeakRef, List, Str, Any
from enthought.enable.api import Label, Component, Container, Canvas, Viewport, Window, Scrolled, Pointer, str_to_font
from enthought.enable.tools.api import MoveTool, ViewportPanTool

CURRENT_SELECTION_VIEW = 'mapero.dataflow_editor.view.current_selection'

def round_rect(gc, radio=5, position=[100,100], bounds=[100,60], inset=3):
    dx, dy = bounds
    x, y = position
    x+=inset
    y+=inset
    dx-=2*inset
    dy-=2*inset
    gc.move_to( x+radio, y+dy)
    gc.line_to( x+dx-radio, y+dy)
    gc.arc_to( x+dx, y+dy, x+dx, y+dy-radio, radio )
    gc.line_to( x+dx, y+radio)
    gc.arc_to(x+dx, y, x+dx-radio, y, radio)
    gc.line_to( x+radio, y)
    gc.arc_to( x, y, x, y+radio, radio)
    gc.line_to( x, y+dy-radio )
    gc.arc_to( x, y+dy, x+radio, y+dy, radio)

class PortComponent(Component):
    fill_color = (0.5, 0.5, 0.5, 1.0)
    text_color = (0.0, 0.0, 0.0, 1.0)
    padding = 0
    bgcolor = 'transparent'
    bounds=[10,10]
    port = WeakRef()
    angle = Float(0.0)
    port_name = Str
    _font = Any
    def _draw_mainlayer(self, gc, view_bounds=None, mode="default"):
        dx, dy = self.bounds
        x, y = self.position
        gc.save_state()
        gc.translate_ctm(x+dx/2, y+dy/2)
        if (self.angle != 0.0):
            gc.rotate_ctm(self.angle)
        gc.set_fill_color(self.fill_color)
        gc.move_to(dx/2, dy/2)
        gc.line_to(dx/2, -dy/2)
        gc.line_to(dx*0.1, -dy*0.30)
        gc.line_to(-dx/2, -dy*0.30)
        gc.line_to(-dx/2, dy*0.30)
        gc.line_to(dx*0.1, dy*0.30)
        gc.line_to(dx/2, dy/2)
        gc.fill_path()

        if self.port_name:
            if not self._font:
                self._font = str_to_font(None, None, "modern 8")
            gc.set_font(self._font)
            (x,y,w,h) = gc.get_text_extent(self.port_name)
            if self.angle > pi/2:
                gc.translate_ctm((-2*dx -w), 0)
                gc.rotate_ctm(self.angle)
            gc.set_fill_color(self.text_color)
            gc.set_text_position(-dx -w, -h/2)
            gc.show_text(self.port_name)

        gc.restore_state()
        return
    
    def normal_mouse_enter(self, event):
        self.port_name = self.port.name
        self.request_redraw()
        
    def normal_mouse_leave(self, event):
        self.port_name = ''
        self.request_redraw()
        

class ModuleComponent(Container):

    normal_pointer = Pointer("arrow")
    moving_pointer = Pointer("hand")
  
    fill_color = (0.9, 0.77, 0.14, 1.0)
    moving_color = (0.0, 0.8, 0.1, 1.0)
    line_color = (0.1, 0.1, 0.1, 0.5)
    

    selected = Bool(False)
    
    padding = 10
    resizable = ""
    bgcolor = 'transparent'
    
    diagram = Any
    module_geom = WeakRef(ModuleGeometrics)
    port_components = List(PortComponent, [])
    label = Label
    
    port_min_separation = 5
    
    def __init__(self, module_geom , **traits):
        super(ModuleComponent, self).__init__(**traits)
        self.position = [module_geom.x, module_geom.y]
        self.bounds = [module_geom.w, module_geom.h]
        self.module_geom = module_geom
        self.label = Label(text="Module", 
                           position = [self.bounds[0]/7, self.bounds[1]/1.4],
                           bounds=self.bounds )
        self.add( self.label )

        self.tools.append(MoveTool(self))
        self._set_ports()
        self._set_label()
        

    @on_trait_change('module_geom.module.input_ports_items')
    def module_input_ports_changed(self, event):
        print "module_input_ports_changed", event
        
    @on_trait_change('module_geom.module.output_ports_items')
    def module_output_ports_changed(self, event):
        print "module_out_ports_changed", event

    @on_trait_change('module_geom.module.label')
    def module_label_changed(self, label):
        self.label.text = label
        self.request_redraw()
    
    @on_trait_change('module_geom.module.progress')
    def module_progress_changed(self, event):
        print "module_progress_changed", event
        
    def _set_ports(self):
        for port in self.port_components:
            self.remove(port)
        self.port_components = []
        
        ## input ports
        input_ports_len = len(self.module_geom.module.input_ports)
        sep = self.height / ( input_ports_len + 1)
        y_port = sep
        for input_port in self.module_geom.module.input_ports:
            self.add(PortComponent(port = input_port,
                                   position=[0 ,y_port],
                                   angle=pi
                                   ))
            y_port += sep
            
        ## output ports
        output_ports_len = len(self.module_geom.module.output_ports)
        sep = self.height / ( output_ports_len + 1)
        y_port = sep
        for output_port in self.module_geom.module.output_ports:
            self.add(PortComponent(port = output_port,
                                   position=[self.width-10 ,y_port]
                                   )) #TODO: port width is hardcoded
            y_port += sep

        self.request_redraw()
        
    def _set_label(self):
        self.label.text = self.module_geom.module.label
        self.request_redraw()
        
        
        
        
        
    def _draw_container_mainlayer(self, gc, view_bounds=None, mode="default"):
        gc.save_state()
        gc.set_fill_color(self.fill_color)
        gc.set_stroke_color(self.line_color)
        round_rect(gc, radio=5, position=self.position, bounds=self.bounds)
        gc.draw_path()
        gc.restore_state()
        return
    
    def _draw_container_overlay(self, gc, view_bounds=None, mode="default"):
        if self.event_state=="selected":
            self.draw_select_box(gc, self.position, self.bounds,
                                 1, (0.7,0.3,0.7,0.3), 0,
                                 (0.0,0.0,0.0), (0.0,0.0,0.0), 2)
    
    def normal_left_down(self, event):
        self.event_state = "selected"
        view = self.diagram.editor.window.get_view_by_id(CURRENT_SELECTION_VIEW)
        if view:
            view.obj = self.module_geom.module
            view.ui.reset()
            #view.create_control(view.ui.control)
            self.module_geom.module.edit_traits(parent=view.ui.control, kind='subpanel')
        self.request_redraw()
    
    def selected_left_down(self, event):
        if event.control_down:
            self.event_state = "normal"
            self.request_redraw()
        
        
       
class MyCanvas(Canvas):
    bgcolor = (1.0, 0.95, 0.71, 1.0)
    draw_axes=True
    
    def normal_dropped_on(self, event):
        position = [event.x,event.y]
        self.window.editor.add_module( event.obj.module_info.clazz.canonical_name, position=position  )
        
    def normal_drag_over(self, event):
        self.window.set_drag_result('copy')
            
    
class Diagram(Window):
    
    dataflow_with_geom = Instance(GraphicDataflowModel)
    
    canvas = Instance(Canvas)
    
    module_geom_component_map = Dict(ModuleGeometrics, ModuleComponent)
    
    def normal_drag_over(self, event):
        print "normal_drag_over"
    
    def __init__ ( self, parent, wid = -1, pos = None, size = None, **traits ):
        super(Diagram, self).__init__(parent, wid, pos, size, **traits)
        
        
        self.canvas = MyCanvas(window=self)
        viewport = Viewport(component=self.canvas, enable_zoom=True)
        viewport.view_position = [0,0]
        viewport.tools.append(ViewportPanTool(viewport))

        # Uncomment the following to enforce limits on the zoom
        viewport.min_zoom = 0.2
        viewport.max_zoom = 2.0

        scrolled = Scrolled(self.canvas, fit_window = True,
                            inside_padding_width = 0,
                            mousewheel_scroll = False,
                            viewport_component = viewport,
                            always_show_sb = True,
                            continuous_drag_update = True)
        
        self.component = scrolled
        
    @on_trait_change('dataflow_with_geom.module_geometrics_items')
    def modules_changed(self, event):
        if isinstance(event, TraitListEvent): ## odd
            for module_geometrics in event.added:
                mod_component = self.add_module_component(module_geometrics)
                self.module_geom_component_map[module_geometrics] = mod_component
            
    def add_module_component(self, module_geometrics):
        module_component = ModuleComponent(module_geometrics, diagram=self)
        self.canvas.add(module_component)
        self.canvas.invalidate_and_redraw()
        return module_component
        

        