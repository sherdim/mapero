"""The various actions for the Scene plugin.

"""
# Author: Zacarias Ojeda <zojeda@gmail.com>
# License: new BSD Style.

# Enthought library imports.
from enthought.pyface.action.api import Action

# Local imports.
import logging
logger = logging.getLogger()

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
# `NewNetwork` class.
######################################################################
class NewNetwork(Action):
    """ An action that creates a New Mapero Network. """

    
    ###########################################################################
    # 'Action' interface.
    ###########################################################################
    name = "New Network"
    
    def perform(self, event):
        """ Performs the action. """        
        from mapero.dataflow_editor.editor.api import DataflowDiagramEditor
        from mapero.dataflow_editor.editor.model.api import GraphicDataflowModel
        editor = self.window.edit(GraphicDataflowModel(), kind=DataflowDiagramEditor)
        
        shell_bind(self.window, editor.id, editor)
        