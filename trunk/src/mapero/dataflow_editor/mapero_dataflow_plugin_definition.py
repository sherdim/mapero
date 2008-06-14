# Enthought library imports.
from enthought.envisage.api import PluginDefinition
from enthought.envisage.core.core_plugin_definition import ApplicationObject, Preferences
from enthought.envisage.workbench.workbench_plugin_definition import Workbench,View
from enthought.envisage.workbench.preference.preference_plugin_definition import PreferencePages, Page
from enthought.envisage.workbench.workbench_plugin_definition import Branding

from enthought.envisage.workbench.action.action_plugin_definition import \
     Action, Location, Menu, WorkbenchActionSet

# Local imports.
from mapero.dataflow_editor.services import ICATALOG

# The plugin's globally unique identifier (also used as the prefix for all
# identifiers defined in this module).
ID = 'mapero.dataflow_editor'





###################################################ddddddd#####################
# Extensions.
###############################################################################
df_views = []
df_extensions = []
###############################################################################
# Catalog Definitions
###############################################################################
catalog = ApplicationObject( class_name='mapero.core.catalog.Catalog', uol=ICATALOG )

catalog_view =  View(name = 'Catalog',
                     id = 'mapero.catalog' ,
                     class_name = ID + '.view.catalog_tree_view.CatalogTreeView',
                     #traits_ui_view = 'mapero.dataflow_editor.catalog_plugin.CatalogTreeView',
                     position='left')

df_views.append( catalog_view )
df_extensions.append( catalog )

#### Preferences ##############################################################

preferences = Preferences(
    defaults = {
        'flip_the_flop'    : True,
        'explode_on_exit'  : True,
        'background_color' : 'red',
        'label_font'       : '',
        'catalog_dirs'     : [],
    }
)
df_extensions.append(preferences)
#### Preference pages #########################################################

preference_pages = PreferencePages(
    pages = [
        Page(
            id         = ID + "CatalogPreferencePage",
            class_name = ID + '.preferences.catalog_preferences_page.CatalogPreferencesPage',
            name       = "Catalog",
            category   = "",
        )
    ]
)
df_extensions.append(preference_pages)
#### Branding #################################################################

branding =  Branding(
    about_additions = ['Author: Zacarias F. Ojeda'],

    # The about box image.
    about_image = 'about.png',

    # The application icon.
    application_icon = 'application.ico',

    # The application name.
    application_name = 'Mapero Dataflow Editor'
)
df_extensions.append( branding )

########################################
# Menus/Actions.

new_menu = Menu(
    id     = "NewMenu",
    name   = "&New",
    location = Location(path="MenuBar/FileMenu/additions"),
    )

new_network = Action(
    id            = "NewScene",
    class_name    = ID + ".actions.NewNetwork",
    name          = "&Network",
    tooltip       = "Create a new Network",
    description   = "Create a new Network",
    locations = [Location(path="MenuBar/FileMenu/NewMenu/additions")]
)


action_set = WorkbenchActionSet(
    id = ID + '.action_set',
    name = 'SceneActionSet',
    menus = [new_menu],

    actions = [
        new_network
    ]
)
df_extensions.append( action_set )

workbench = Workbench ( views=df_views )
df_extensions.append( workbench )
###############################################################################
# The plugin definition.
###############################################################################

class DataflowEditorPluginDefinition(PluginDefinition):
    """ The main charm plugin. """
    
    # The plugin's globally unique identifier.
    id = ID

    # The name of the class that implements the plugin.
    #class_name = ID + '.plugin_implementation.DataflowEditorPlugin'

    # General information about the plugin.
    name          = 'Dataflow Editor'
    version       = '0.0.1'
    provider_name = 'zojeda@gmail.com'
    provider_url  = 'mapero.googlecode.com'
    autostart     = True

    # The Id's of the plugins that this plugin requires.
    requires = [
        'enthought.envisage.workbench',
        'enthought.plugins.python_shell',
    ]

    class_name = ID + '.mapero_dataflow_plugin.DataflowEditorPlugin'
    # The extension points offered by this plugin.
    extension_points = []

    # The contributions that this plugin makes to extension points offered by
    # either itself or other plugins.
    extensions = df_extensions