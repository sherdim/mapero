from mapero.core.module import Module
from mapero.dataflow_editor.mvc.controller import DataflowEditorController 
from enthought.traits import api as traits
from enthought.traits.ui import api as traits_ui
from enthought.traits.ui.menu import Action
from enthought.traits.ui.menu import OKButton

class ModuleEditorHandler(traits_ui.Handler):
    def do_refresh(self, ui_info):
        editor = ui_info.ui.context['object']
        controller = editor.controller
        module_code = editor.module_code
        module_file = editor.module_file
        module = editor.module
        file = open(module_file, 'w')
        file.writelines(module_code)
        file.close()
        controller.refresh_module(module)
            
refresh_module_code = Action(name="Refresh", action="do_refresh")
    
class ModuleEditor ( traits.HasTraits ): 
    """ This class specifies the details of the CodeEditor demo.
    """
    module_code = traits.Code
    module_file = traits.Str
    module = traits.Trait(Module)
    controller = traits.Trait(DataflowEditorController)
    
    view = traits_ui.View(
                        traits_ui.Group(
                                                    traits_ui.Item( 'module_code'),
                                                    label='Code',
                                                    show_labels=False
                                                ) ,
                        width=800, height=600,
                        handler = ModuleEditorHandler(),
                        buttons = [OKButton, refresh_module_code]
                        )
    
    def __init__(self, modules, controller):
        if (modules != None and len(modules)>0 ) :
            module = modules[0]
            self.module_file = module.source_code_file
            self.module = module
            self.controller = controller
            file = open(self.module_file, 'r')
            code = ""
            for line in file:
                code += line
            self.module_code = code
            file.close()
    