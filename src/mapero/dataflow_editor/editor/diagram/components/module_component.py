# Author: Zacarias F. Ojeda <zojeda@gmail.com>
# License: new BSD Style.

from mapero.dataflow_editor.editor.model.api import ModuleGeometrics

from mapero.dataflow_editor.editor.diagram import round_rect
from mapero.dataflow_editor.editor.diagram.components.diagram_component import DiagramComponent
from mapero.dataflow_editor.editor.diagram.components.port_component import PortComponent

from enthought.traits.api import Bool, on_trait_change, Instance, Any, \
                                 Delegate, Dict, Range, TraitListEvent

from enthought.enable.api import Label, Container, Pointer

from math import pi

class ModuleComponent(DiagramComponent, Container):

    
    normal_pointer = Pointer("arrow")
    moving_pointer = Pointer("hand")
  
    fill_color = (0.9, 0.77, 0.14, 1.0)
    moving_color = (0.0, 0.8, 0.1, 1.0)
    line_color = (0.1, 0.1, 0.1, 0.5)

    selected = Bool(False)
    
    padding = 10
    resizable = ""
    bgcolor = 'transparent'
    #font = KivaFont("Modern 10")
     
    diagram = Any #Instance(DiagramWindow) 
    module_geom = Instance(ModuleGeometrics)
    
    label = Label
    progress = Range(0,100)
    
    port_component_dict = Dict(Any, PortComponent)
    
    editor = Delegate('diagram')
    port_min_separation = 5
    
    def __init__(self, module_geom , **traits):
        super(ModuleComponent, self).__init__(**traits)
        self.position = module_geom.position
        self.bounds = module_geom.bounds
        self.module_geom = module_geom
        self.label = Label(text="Module", 
                           position = [self.bounds[0]/7, self.bounds[1]/1.4],
                           bounds=self.bounds, 
                           )#font = self.font)
        self.add( self.label )
        self._create_ports()
        self._set_label()        

    def _create_ports(self):
        for input_port in self.module_geom.module.input_ports:
            port_component = PortComponent(
                                           port = input_port,
                                           angle=pi,
                                           type="input"
                                   )
            self.add(port_component)
            self.port_component_dict[input_port] = port_component
        
        for output_port in self.module_geom.module.output_ports:
            port_component = PortComponent(
                                           port = output_port,
                                           type="output"
                                   )
            self.add(port_component)
            self.port_component_dict[output_port] = port_component
        
        self._set_positions()
        
    @on_trait_change('module_geom.module:input_ports_items')
    def module_input_ports_changed(self, event):
        if not isinstance(event, TraitListEvent):
            return
        for input_port in event.added:
            port_component = PortComponent(
                                           port = input_port,
                                           angle=pi,
                                           type="input"
                                   )
            self.add(port_component)
            self.port_component_dict[input_port] = port_component
            
        for input_port in event.removed:
            port_component = self.port_component_dict.pop(input_port)
            self.remove(port_component)
            
        self._set_positions()
        
    @on_trait_change('module_geom.module:output_ports_items')
    def module_output_ports_changed(self, event):
        if not isinstance(event, TraitListEvent):
            return
        for output_port in event.added:
            port_component = PortComponent(
                                           port = output_port,
                                           type="output"
                                   )
            self.add(port_component)
            self.port_component_dict[output_port] = port_component
            
        for output_port in event.removed:
            port_component = self.port_component_dict.pop(output_port)
            self.remove(port_component)
            
        self._set_positions()
        
    @on_trait_change('module_geom:module:[label,id]')
    def module_label_changed(self, label):
        self._set_label()
        self.request_redraw()
    
    @on_trait_change('module_geom:module.progress')
    def module_progress_changed(self, progress):
        if progress:
            self.progress = progress
        else:
            self.progress = 0 
        self.request_redraw()
        
    def _set_positions(self):
        self.label.position = [self.bounds[0]/7, self.bounds[1]/1.4]

        ## input ports
        input_ports_len = len(self.module_geom.module.input_ports)
        sep = self.height / ( input_ports_len + 1)
        y_port = self.height - sep - 5
        for input_port in self.module_geom.module.input_ports:
            self.port_component_dict[input_port].position = 0, y_port,
            y_port -= sep
            
        ## output ports
        output_ports_len = len(self.module_geom.module.output_ports)
        sep = self.height / ( output_ports_len + 1)
        y_port = self.height - sep - 5
        for output_port in self.module_geom.module.output_ports:
            self.port_component_dict[output_port].position = self.width-10 ,y_port
            y_port -= sep

        self.request_redraw()
        
    def _set_label(self):
        if self.module_geom.module:
            text = "[%d] %s" % (self.module_geom.module.id,self.module_geom.module.label)
            self.label.text = text
        self.request_redraw()
        
    @on_trait_change('module_geom:position')
    def on_module_geom_position_change(self, position):
        self.position = position
        self._set_positions()
        
    @on_trait_change('module_geom:bounds')
    def on_module_geom_bounds_change(self, bounds):
        self.bounds = bounds
        self._set_positions()
    #### DiagramComponent interface ##########################
    
    def _get_diagram_object_model(self):
        return self.module_geom

        
    def draw_diagram_component(self, gc):
        gc.save_state()
        gc.set_fill_color(self.fill_color)
        gc.set_stroke_color(self.line_color)
        round_rect(gc, radio=5, position=self.position, bounds=self.bounds)
        gc.draw_path()
        
        #drawing progress
        gc.set_fill_color((0.5,0.5,0.5,1.0))
        bar_height = self.height*0.25
        bar_width = self.width*0.7
        round_rect(gc, radio=2, position=[self.x+10,self.y+10], bounds=[bar_width, bar_height])
        gc.fill_path()
        gc.set_fill_color((0.2,0.2,1.0,1.0))
        bar_height -= 2
        bar_width = (bar_width-2)*self.progress/100
        round_rect(gc, radio=2, position=[self.x+11,self.y+11], bounds=[bar_width, bar_height])
        gc.fill_path()

        gc.restore_state()
        return
    
    ##########################################################

    def draw_diagram_component_border(self, gc):
        if self.selected:
            self.draw_select_box(gc, self.position, self.bounds,
                             1, (4.0, 2.0), 0,
                                 (0.0,0.0,0.0), (1.0,1.0,1.0), 2)
        