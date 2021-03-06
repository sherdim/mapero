# Author: Zacarias Ojeda <zojeda@gmail.com>
# License: new BSD Style.

# Enthought library imports.
from enthought.envisage.ui.action.api import Action, ActionSet, Group

#### Groups ###################################################################

file_group = Group(
    id='DataflowEditorFileGroup',
    path='MenuBar/File', before='ExitGroup'
)

view_group = Group(
    id='DataflowEditorViewGroup',
    path='MenuBar/Tools', before='PreferencesGroup'
)

#### Menus ####################################################################


#### Actions ##################################################################

new_dataflow  = Action(
    class_name = 'mapero.dataflow_editor.editor.actions.NewDataflow',
    path       = 'MenuBar/File', group = 'DataflowEditorFileGroup'
)

open_dataflow = Action(
    class_name = 'mapero.dataflow_editor.editor.actions.OpenDataflow',
    path       = 'MenuBar/File', group = 'DataflowEditorFileGroup'
)

save_dataflow = Action(
    class_name = 'mapero.dataflow_editor.editor.actions.SaveAs',
    path       = 'MenuBar/File', group = 'DataflowEditorFileGroup'
)

class MaperoUIActionSet(ActionSet):
    """ The default action set for the mapero UI plugin. """

    groups  = [file_group, view_group]
    menus   = []
    actions = [ new_dataflow, open_dataflow, save_dataflow ]
    