# Enthought library imports.
from enthought.envisage.ui.action.api import Action, ActionSet, Group, Menu

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

new_network = Action(
    class_name = 'mapero.dataflow_editor.actions.NewNetwork',
    path       = 'MenuBar/File', group = 'DataflowEditorFileGroup'
)


class MaperoUIActionSet(ActionSet):
    """ The default action set for the mapero UI plugin. """

    groups  = [file_group, view_group]
    menus   = []
    actions = [ new_network ]
    