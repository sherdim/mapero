"""A Network Editor that is placed in the work area.

"""
# Author: Zacarias Ojeda <zojeda@gmail.com>
# License: new BSD Style.

# Enthought library imports.
from enthought.envisage.core.plugin import Plugin
from enthought.traits.api import Instance, Str, Event

from enthought.envisage.workbench.api import Editor

# Mapero library imports
from mapero.core.network import Network

# Local imports.
from mapero.dataflow_editor.view.diagram import DataflowDiagram

##############################################################################
# Handy functions
def _id_generator():
    """Returns a sequence of numbers for the title of the network editor
    window."""
    n = 1
    while True:
        yield(n)
        n += 1

_id_generator = _id_generator()


##############################################################################
# NetworkEditor class
class NetworkEditor(Editor):

    # The mapero network object.
    network = Instance(Network)

    # The Network plugin that we are part of.
    plugin = Instance(Plugin)

    # Our name -- this is really for compatibility with the UI plugin.
    # The workbench plugin's editor already defines a name trait.
    name = Str

    # Our id -- this is really for compatibility with the UI plugin.
    # The workbench plugin's editor already defines an 'id' trait.
    id = Str
    
    #### Events #####

    ## FIXME: These are temporary and should be removed once (and if)
    ## Martin adds them to the framework.

    # The editor has been activated.
    activated = Event

    # The editor is being closed.
    closing = Event

    # The editor has been closed.
    closed = Event

    ######################################################################
    # `object` interface
    ######################################################################
    def __init__(self, **traits):
        super(NetworkEditor, self).__init__(**traits)

        # The plugin trait is only set when _create_contents is
        # called.  This is because self.window is None in __init__.

        # We add ourselves to the plugin's `editors` attribute only
        # when the widget is created in `_create_contents`.

        # Set our name with a suitable id.
        self.id = self.name = 'Network %d'%(_id_generator.next())        

    ###########################################################################
    # 'Window' interface.
    ###########################################################################
    def preferences_changed(self, value):
        """This is called when any of the plugin preferences changed."""
        key, old, new = value.key, value.old, value.new
        network = self.network
        if key == 'background_color':
            network.renderer.background = new
        if key == 'foreground_color':
            network.foreground = new
        if key == 'magnification':
            network.magnification = new            
        #network.render()
    
    ###########################################################################
    # FIXME: these should be changed when the framework's editor has
    # lifecycle events added.
    # 'Editor' interface
    ###########################################################################
    def destroy_control(self):
        """ Destroys the toolkit-specific control that represents the
        editor.  This is overridden from parent Editor class to add
        lifecyle events.
        """
        if self.control is not None:
            self.closing = self
            
        super(NetworkEditor, self).destroy_control()

        if self.control is not None:
            self.closed = self

    def set_focus(self):
        """ Sets the focus to the appropriate control in the editor.

        By default we set the focus to be the editor's top-level control.
        Override this method if you need to give focus to some other child
        control.
        """
        super(NetworkEditor, self).set_focus()
        if self.control is not None:
            self.activated = self

    ###########################################################################
    # Protected 'Window' interface.
    ###########################################################################
    def _create_control(self, parent):
        """ Create the toolkit-specific control that represents the window.

        This method is intended to be overridden if necessary.  By default we
        just create an empty frame.

        """
        frame = super(NetworkEditor, self)._create_control(parent)
        frame.SetSize((500, 500))
        return frame

    def _create_contents(self, parent):
        """ Creates the window contents. """
        # Make sure that the plugin we are part of is started.
        app = self.window.application
        #self.plugin = app.get_service(ITVTKSCENE)
        #plugin = self.plugin
        
        #prefs = plugin.preferences
        network = Network()
        diagram = DataflowDiagram(parent)
        self.diagram = diagram
        #network.renderer.background = prefs.get('background_color')

        #network.render()        
        self.network = network

        # Add this editor to the plugin's editors.  We do this only
        # here and not at initialization time because the browser
        # plugin listens for this and requires that the network
        # attribute be set.
        #plugin.editors.append(self)
        #plugin.current_editor = self

        return self.diagram.GetCanvas()
    
    create_control = _create_contents

    def _closing_fired(self, event):
        """This event fires when the window closes."""
        # Remove ourselves from the plugin at this time.
        self.plugin.editors.remove(self)

    def _activated_fired(self, event):
        """This event fires when this frame/editor is activated."""
        self.plugin.current_editor = self


