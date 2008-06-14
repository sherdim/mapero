""" The absolute filenames of the plugin definitions used in the application.

The only reason that we put this in a separate module is that it often entails
lots of path and filename manipulation code that tends to clutter up 'run'.

The important thing to realise is that all we are doing is defining a list of
strings which are the absolute filenames of the plugin definition used in the
application!

"""
from enthought.envisage.util import find_definition


# Enthought library imports.
#from enthought.envisage.core_plugin import CorePlugin
#from enthought.envisage.ui.workbench.workbench_plugin import WorkbenchPlugin
#from enthought.plugins.python_shell.python_shell_plugin import PythonShellPlugin
#from mapero.dataflow_editor.mapero_dataflow_plugin_definition import DataflowEditorPluginDefinition
#from enthought.tvtk.plugins.scene.scene_plugin import ScenePlugin
#from enthought.tvtk.plugins.scene.ui.scene_ui_plugin import SceneUIPlugin

# The plugin definitions that make up the application.
PLUGIN_DEFINITIONS = [
    # Envisage plugins.
    find_definition('enthought.envisage.core.core_plugin_definition'),
    find_definition('enthought.envisage.resource.resource_plugin_definition'),

    find_definition('enthought.envisage.action.action_plugin_definition'),
    find_definition('enthought.envisage.workbench.workbench_plugin_definition'),
    find_definition('enthought.envisage.workbench.action.action_plugin_definition'),
    find_definition('enthought.envisage.workbench.preference.preference_plugin_definition'),
    
 
    # Enthought plugins.
    find_definition('enthought.plugins.python_shell.python_shell_plugin_definition'),
    #find_definition('enthought.plugins.text_editor.text_editor_plugin_definition'),

    # Dataflow Editor plugins.
    find_definition('mapero.dataflow_editor.mapero_dataflow_plugin_definition'),
#    CorePlugin(),
#    WorkbenchPlugin(),
    #MayaviPlugin(),
    #MayaviUIPlugin(),
    #ScenePlugin(),
    #SceneUIPlugin(),
#    PythonShellPlugin(),

    # Debugging.
    #find_definition('enthought.envisage.internal.internal_plugin_definition'),
    #find_definition('enthought.plugins.debug.fbi_plugin_definition'),
]

# The plugin definitions that we want to import from but don't want as part of
# the application.
INCLUDE = []

#### EOF ######################################################################
