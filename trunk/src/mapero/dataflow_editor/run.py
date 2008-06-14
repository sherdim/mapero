""" The entry point for an Envisage application. """
from enthought.etsconfig.api import ETSConfig
from enthought.envisage.workbench.workbench_application import WorkbenchApplication

# Enthought library imports.
ETSConfig.company = "mapero"

# Local imports.
from plugin_definitions import INCLUDE, PLUGIN_DEFINITIONS



def run():
    """ Runs the application. """

    # Create the application.
    application = WorkbenchApplication(
        id                 = 'mapero.dataflow_editor',
        include            = INCLUDE,
        plugin_definitions = PLUGIN_DEFINITIONS
    )

    # Run the application (this starts the application, starts the GUI event
    # loop, and when that terminates, stops the application).
    application.run()

    return


# Application entry point.
if __name__ == '__main__':
    run()

#### EOF ######################################################################
