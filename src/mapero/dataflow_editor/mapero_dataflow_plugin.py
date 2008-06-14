""" example plugin. """


# Enthought library imports.
from enthought.envisage import Plugin


class DataflowEditorPlugin(Plugin):
    """ An example plugin. """

    # The shared plugin instance.
    instance = None

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, **kw):
        """ Creates a new plugin. """

        # Base-class constructor.
        super(DataflowEditorPlugin, self).__init__(**kw)

        # Set the shared instance.
        DataflowEditorPlugin.instance = self
        
        return

    ###########################################################################
    # 'Plugin' interface.
    ###########################################################################

    def start(self, application):
        """ Starts the plugin.

        Can be called manually, but is usually called exactly once when the
        plugin is first required.

        """
        print "STARTING PLUGIN"
        pass
    
    def stop(self, application):
        """ Stops the plugin.

        Can be called manually, but is usually called exactly once when the
        application exits.

        """

        self.save_preferences()
        
        return

#### EOF ######################################################################