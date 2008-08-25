"""The various actions for the Scene plugin.

"""
# Author: Zacarias Ojeda <zojeda@gmail.com>
# License: new BSD Style.

# Enthought library imports.
from enthought.pyface.api import FileDialog, OK

from enthought.pyface.action.api import Action
from enthought.persistence import state_pickler
from mapero.core.persistence.state_setter import set_state

# Local imports.
import logging
logger = logging.getLogger()

from os.path import isfile

def shell_bind(window, name, object):
    SHELL_VIEW = 'enthought.plugins.python_shell_view'
    # Get a hold of the Python shell view.
    id = SHELL_VIEW
    py = window.get_view_by_id(id)
    if py is None:
        logger.warn('*'*80)
        logger.warn("Can't find the Python shell view to bind variables")
        return

    # Bind the script and engine instances to names on the
    # interpreter.
    try:
        py.bind(name, object)

    except AttributeError, msg:
        # This can happen when the shell is not visible.
        # FIXME: fix this when the shell plugin is improved.
        logger.warn(msg)
        logger.warn("Can't find the Python shell to bind variables")
    
######################################################################
# `NewDataflow` class.
######################################################################
class NewDataflow(Action):
    """ An action that creates a New Mapero Dataflow. """

    
    ###########################################################################
    # 'Action' interface.
    ###########################################################################
    name = "New Dataflow"
    
    def perform(self, event):
        """ Performs the action. """        
        from mapero.dataflow_editor.editor.api import DataflowDiagramEditor
        from mapero.dataflow_editor.editor.model.api import GraphicDataflowModel
        editor = self.window.edit(GraphicDataflowModel(), kind=DataflowDiagramEditor)
        
        shell_bind(self.window, editor.id, editor)

######################################################################
# `SaveAs` class.
######################################################################
class SaveAs(Action):
    """ An action that saves the Mapero Dataflow """

    name = "Save as ..."

    tooltip       = "Save current Dataflow"

    description   = "Save current Dataflow to a mprd file"
    
    ###########################################################################
    # 'Action' interface.
    ###########################################################################
    def perform(self, event):
        """ Performs the action. """
        wildcard = 'Mapero files (*.mprd)|*.mprd|' + FileDialog.WILDCARD_ALL
        dialog = FileDialog(parent=self.window.control,
                            title='Save Mapero file',
                            action='save as', wildcard=wildcard
                            )
        if dialog.open() == OK:
            from mapero.dataflow_editor.service.current_selection import CurrentSelection
            current_selection = self.window.get_service(CurrentSelection)
            
#            state = state_pickler.get_state(current_selection.graphic_dataflow)
#            print state
            state_pickler.dump(current_selection.graphic_dataflow, dialog.path)


######################################################################
# `OpenDataflow` class.
######################################################################
class OpenDataflow(Action):
    """ An action that open a dataflow definition from file. """

    name = "Open Dataflow ..."

    tooltip       = "Open saved dataflow"

    description   = "Open saved dataflow from a Mapero file"

    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    def perform(self, event):
        """ Performs the action. """
        wildcard = 'Mapero files (*.mprd)|*.mprd|' + FileDialog.WILDCARD_ALL
        parent = self.window.control
        dialog = FileDialog(parent=parent,
                            title='Open Mapero file',
                            action='open', wildcard=wildcard
                            )
        if dialog.open() == OK:
            if not isfile(dialog.path):
                logger.error("File '%s' does not exist" % dialog.path, parent)
                return
            
            # Get the state from the file.
            state = state_pickler.load_state(dialog.path)
            state_pickler.update_state(state)
            from mapero.dataflow_editor.editor.api import DataflowDiagramEditor
            from mapero.dataflow_editor.editor.model.api import GraphicDataflowModel
            graphic_dataflow_model = GraphicDataflowModel()
            editor = self.window.edit(graphic_dataflow_model, kind=DataflowDiagramEditor)
            
            shell_bind(self.window, editor.id, editor)
            
            set_state(graphic_dataflow_model, state)

            
        