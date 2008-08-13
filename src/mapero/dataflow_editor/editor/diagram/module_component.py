# Author: Zacarias F. Ojeda <zojeda@gmail.com>
# License: new BSD Style.

from mapero.dataflow_editor.editor.model.api import ModuleGeometrics

from mapero.dataflow_editor.editor.diagram import round_rect
from mapero.dataflow_editor.editor.diagram.port_component import PortComponent

from enthought.traits.api import Bool, on_trait_change, WeakRef, List, Any, Delegate
from enthought.enable.api import Label, Container, Pointer
from enthought.enable.tools.api import MoveTool

from math import pi

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
    
    diagram = Any #Instance(DiagramWindow) 
    module_geom = WeakRef(ModuleGeometrics)
    port_components = List(PortComponent, [])
    label = Label
    
    editor = Delegate('diagram')
    port_min_separation = 5
    
    def __init__(self, module_geom , **traits):
        super(ModuleComponent, self).__init__(**traits)
        self.position = [module_geom.x, module_geom.y]
        self.bounds = [module_geom.w, module_geom.h]
        self.module_geom = module_geom
        #self.label = Label(text="Module", 
        #                   position = [self.bounds[0]/7, self.bounds[1]/1.4],
        #                   bounds=self.bounds )
        #self.add( self.label )

        self.tools.append(MoveTool(self))
        self._set_ports()
        #self._set_label()
        

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
                                 1, (4.0, 2.0), 0,
                                 (0.0,0.0,0.0), (1.0,1.0,1.0), 2)
    
    
    
    ### Interactor Interface
    def normal_left_down(self, event):
        #self.event_state = "selected"
        if event.control_down:
            self.editor.selection.append(self.module_geom.module)
        else:
            self.editor.selection = [self.module_geom.module]
        self.request_redraw()
    
    def selected_left_down(self, event):
        if event.control_down:
            #self.event_state = "normal"
            self.editor.selection.remove(self.module_geom.module)
        else:
            self.editor.selection = [self.module_geom.module]
        self.request_redraw()
