"""The Mapero Envisage application.
"""
# Author: Zacarias F. Ojeda <zojeda@gmail.com>
# License: new BSD Style.

# Standard library imports.
import sys
import os.path
import logging

# Enthought library imports.
from enthought.logger.api import LogFileHandler, FORMATTER
from enthought.etsconfig.api import ETSConfig
from enthought.traits.api import (HasTraits, Instance, Int,
    on_trait_change)

# Local imports.
from mapero_workbench_application import MaperoDataflowEditorWorkbenchApplication
from mapero.dataflow_editor.preferences.preferences_manager import preference_manager

# GLOBALS
logger = logging.getLogger()

######################################################################
# Useful functions.
######################################################################
def setup_logger(logger, fname, stream=True, mode=logging.ERROR):
    """Setup a log file and the logger.  If the given file name is not
    absolute, put the log file in `ETSConfig.application_home`, if not
    it will create it where desired.

    Parameters:
    -----------

    fname -- file name the logger should use.  If this is an absolute
    path it will create the log file as specified, if not it will put it
    in `ETSConfig.application_home`.

    stream -- Add a stream handler.

    mode -- the logging mode.
    
    """
    if not os.path.isabs(fname):
        path = os.path.join(ETSConfig.application_home, fname)
    else:
        path = fname
    handler = LogFileHandler(path)
    logger.addHandler(handler)
    if stream:
        s = logging.StreamHandler()
        s.setFormatter(FORMATTER)
        logger.addHandler(s)
    logger.info("*"*80)
    logger.info("logfile is: '%s'", os.path.abspath(path))
    logger.info("*"*80)
    logger.setLevel(mode)


def get_plugins():
    """Get list of default plugins to use for Mapero."""
    from enthought.envisage.core_plugin import CorePlugin
    from enthought.envisage.ui.workbench.workbench_plugin import WorkbenchPlugin
    from enthought.plugins.python_shell.python_shell_plugin import PythonShellPlugin
    from enthought.tvtk.plugins.scene.scene_plugin import ScenePlugin
#    from enthought.tvtk.plugins.scene.ui.scene_ui_plugin import SceneUIPlugin
    from mapero.dataflow_editor.plugins.mapero_plugin import MaperoPlugin
    from mapero.dataflow_editor.plugins.mapero_ui_plugin import MaperoUIPlugin
    from enthought.plugins.refresh_code.refresh_code_plugin import RefreshCodePlugin
    #from enthought.plugins.text_editor.text_editor_plugin import TextEditorPlugin
    plugins = [CorePlugin(),
               WorkbenchPlugin(),
               MaperoPlugin(),
               MaperoUIPlugin(),
               ScenePlugin(),
               RefreshCodePlugin(),
               #SceneUIPlugin(),
               #TextEditorPlugin(), 
               PythonShellPlugin(),
               ]
    return plugins

def get_non_gui_plugins():
    """Get list of basic mapero plugins that do not add any views or
    actions."""
    from enthought.envisage.core_plugin import CorePlugin
    from enthought.envisage.ui.workbench.workbench_plugin import WorkbenchPlugin
    from enthought.tvtk.plugins.scene.scene_plugin import ScenePlugin
    from mapero.dataflow_editor.plugins.mapero_plugin import MaperoPlugin
    plugins = [CorePlugin(),
               WorkbenchPlugin(),
               MaperoPlugin(),
               ScenePlugin(),
               ]
    return plugins


###########################################################################
# `MaperoDataflowEditor` class.
###########################################################################
class MaperoDataflowEditor(HasTraits):
    """The MaperoDataflowEditor application class.

    This class may be easily subclassed to do something different.
    For example, one way to script MayaVi (as a standalone application
    and not interactively) is to subclass this and do the needful.
    """

    # The main envisage application.
    application = Instance('enthought.envisage.ui.workbench.api.WorkbenchApplication')

    # The MayaVi Script instance.
    script = Instance('enthought.mapero.plugins.script.Script')

    # The logging mode.
    log_mode = Int(logging.INFO, desc='the logging mode to use')

    def main(self, argv=None, plugins=None):
        """The main application is created and launched here.

        Parameters
        ----------

        - argv : `list` of `strings`

          The list of command line arguments.  The default is `None`
          where no command line arguments are parsed.  To support
          command line arguments you can pass `sys.argv[1:]`.

        - plugins : `list` of `Plugin`s

          List of plugins to start.  If none is provided it defaults to
          something meaningful.

        - log_mode : The logging mode to use.

        """
        # Parse any cmd line args.
        if argv is None:
            argv = []
        self.parse_command_line(argv)

        if plugins is None:
            plugins = get_plugins()

        #plugins += get_custom_plugins()

        # Create the application
        prefs = preference_manager.preferences
        app = MaperoDataflowEditorWorkbenchApplication(plugins=plugins,
                                         preferences=prefs)
        self.application = app

        # Setup the logger.
        self.setup_logger()

        # Start the application.
        app.run()

    def setup_logger(self):
        """Setup logging for the application."""
        setup_logger(logger, 'mapero.log', mode=self.log_mode)

    def parse_command_line(self, argv):
        """Parse command line options.

        Parameters
        ----------

        - argv : `list` of `strings`

          The list of command line arguments.
        """
        from optparse import OptionParser
        usage = "usage: %prog [options]"
        parser = OptionParser(usage)

        (options, args) = parser.parse_args(argv)

    def run(self):
        """This function is called after the GUI has started.
        Override this to do whatever you want to do as a Mapero
        script.  If this is not overridden then an empty Mapero
        application will be started.

        """
        pass

    ######################################################################
    # Non-public interface.
    ######################################################################
    @on_trait_change('application.gui:started')
    def _on_application_gui_started(self, obj, trait_name, old, new):
        """This is called as soon as  the Envisage GUI starts up.  The
        method is responsible for setting our script instance.   
        """
        if trait_name != 'started' or not new:
            return
        app = self.application
        #from enthought.mapero.plugins.script import Script
        window = app.workbench.active_window
        # Set our script instance.
        #self.script = window.get_service(Script)
        # Call self.run from the GUI thread.
        app.gui.invoke_later(self.run)
  

def main(argv=None):
    """Simple helper to start up the mapero application.  This returns
    the running application."""
    m = MaperoDataflowEditor()
    m.main(argv)
    return m

if __name__ == '__main__':
    main(sys.argv[1:])