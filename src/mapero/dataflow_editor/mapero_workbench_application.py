"""MaperoDataflowEditor specific workbench application.
"""
# Author: Zacarias F. Ojeda <zojeda@gmail.com>
# License: new BSD Style.

# Standard library imports.
from os.path import dirname

# Enthought library imports.
from enthought.envisage.ui.workbench.api import WorkbenchApplication
from enthought.pyface.api import AboutDialog, ImageResource, SplashScreen

# Local imports.
import mapero.dataflow_editor
from mapero.dataflow_editor.preferences.preferences_manager import preference_manager

IMG_DIR = dirname(mapero.dataflow_editor.__file__)


class MaperoDataflowEditorWorkbenchApplication(WorkbenchApplication):
    """ The mapero application. """

    #### 'IApplication' interface #############################################

    # The application's globally unique Id.
    id = 'mapero.dataflow_editor'

    #### 'WorkbenchApplication' interface #####################################

    # Branding information.
    #
    # The icon used on window title bars etc.
    icon = ImageResource('icon.ico', search_path=[IMG_DIR])

    # The name of the application (also used on window title bars etc).
    name = 'Mapero Dataflow Editor'

    ###########################################################################
    # 'WorkbenchApplication' interface.
    ###########################################################################

    def _about_dialog_default(self):
        """ Trait initializer. """
        about_dialog = AboutDialog(
            parent = self.workbench.active_window.control,
            image  = ImageResource('about.png',
                                   search_path=[IMG_DIR]),
            additions = ['Authors: Zacarias F. Ojeda',
                            '',
                            'Mapero Dataflow Editor version %s' % 0.1],
        )

        return about_dialog

    def _splash_screen_default(self):
        """ Trait initializer. """
        if preference_manager.root.show_splash_screen:
            splash_screen = SplashScreen(
                image             = ImageResource('splash.jpg',
                                                  search_path=[IMG_DIR]),
                show_log_messages = True,
            )
        else:
            splash_screen = None

        return splash_screen
