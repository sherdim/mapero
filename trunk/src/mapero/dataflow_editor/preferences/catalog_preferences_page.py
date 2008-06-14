"""The preference page for the Catalog

"""
# Author: Zacarias Ojeda <zojeda@gmail.com>
# License: new BSD Style.

# Enthought library imports.
from enthought.envisage.workbench.preference import WorkbenchPreferencePage
from enthought.traits.api import Color, Bool, Font, List, Directory, Str
from enthought.traits.ui.api import View, Item, Group

# Local imports.
from mapero.dataflow_editor.services import ICATALOG
from mapero.dataflow_editor.mapero_dataflow_plugin import DataflowEditorPlugin

##############################################################################
# `CatalogPreferencesPage` class.
##############################################################################
class CatalogPreferencesPage(WorkbenchPreferencePage):

    """ An example preference page. """

    # Should the computer explode when the application exits?
    explode_on_exit = Bool

    # Should flips always be flopped?
    flip_the_flop = Bool

    # The background colour for nothing in particular.
    background_color = Color('white')

    # A font that us not used anywhere!
    label_font = Font
    
    # Catalog Dirs
    catalog_dirs = List(Directory)
    
    # The default view.
    traits_view = View(
        Group(
            Item(name= 'catalog_dirs', style='custom', show_label=False),
            label='Catalog', show_border=False, show_left=False,
        ),

        Group(
            Item(name= 'flip_the_flop'), Item(name='explode_on_exit'),
            label='Simple', show_border=False, show_left=False,
        ),

        Group(
            Item(name='background_color'),
            Item(name='label_font'),
            label='Advanced', show_border=False, style='simple'
        )
    )

    ###########################################################################
    # Protected 'WorkbenchPreferencePage' interface.
    ###########################################################################
    def _get_preferences(self):
        """ Returns the preferences that this page is editing. """
        return DataflowEditorPlugin.instance.preferences
    
    
    def __getstate__(self):
        state = super(CatalogPreferencesPage, self).__getstate__()
        del state['_application']
        return state