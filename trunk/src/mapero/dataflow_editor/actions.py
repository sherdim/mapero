"""The various actions for the Scene plugin.

"""
# Author: Zacarias Ojeda <zojeda@gmail.com>
# License: new BSD Style.

# Enthought library imports.
from enthought.pyface.api import FileDialog, OK
from enthought.traits.api import Str
from enthought.envisage.workbench.action import WorkbenchAction

# Local imports.
from mapero.dataflow_editor.network_editor import NetworkEditor

######################################################################
# `NewNetwork` class.
######################################################################
class NewNetwork(WorkbenchAction):
    """ An action that creates a new Mapero network. """

    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    def perform(self):
        """ Performs the action. """        
        network_editor = NetworkEditor(parent=self.window.control)
        network_editor.window = self.window
        self.window.add_editor(network_editor)