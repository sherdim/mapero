"""A preference manager mapero
"""
# Author: Zacarias F. Ojeda <zojeda@gmail.com>
# License: new BSD Style.

# Standard library imports
from os.path import join
import pkg_resources

# Enthought library imports.
from enthought.etsconfig.api import ETSConfig
from enthought.traits.api import HasTraits, Instance
from enthought.traits.ui.api import View, Group, Item
from enthought.preferences.api import (ScopedPreferences, IPreferences,
        PreferencesHelper)

# Local imports.
from enthought.mayavi.preferences.preferences_helpers import (
        RootPreferencesHelper, MlabPreferencesHelper )

# The application ID where the preferences are stored.
ID = 'enthought.mayavi_e3'


################################################################################
# `PreferenceManager` class
################################################################################
class PreferenceManager(HasTraits):
    
    # The root preferences helper for preferences of the form 
    # 'enthought.mayavi.preference'.
    root = Instance(PreferencesHelper)
    
    # The mlab preferences helper for preferences of the form 
    # 'enthought.mayavi.mlab.preference'.
    mlab = Instance(PreferencesHelper)
    
    # The preferences.
    preferences = Instance(IPreferences)

    ######################################################################
    # Traits UI view.

    traits_view = View(Group(
                             Item(name='root', style='custom'),
                             Item(name='mlab', style='custom'),
                             ),
                       resizable=True
                      )

    ######################################################################
    # `HasTraits` interface.
    ######################################################################
    def __init__(self, **traits):
        super(PreferenceManager, self).__init__(**traits)

        if 'preferences' not in traits:
            self._load_preferences()

    def _preferences_default(self):
        """Trait initializer."""
        return ScopedPreferences()

    def _root_default(self):
        """Trait initializer."""
        return RootPreferencesHelper(preferences=self.preferences)

    def _mlab_default(self):
        """Trait initializer."""
        return MlabPreferencesHelper(preferences=self.preferences)

    ######################################################################
    # Private interface.
    ######################################################################
    def _load_preferences(self):
        """Load the default preferences."""
        # Save current application_home.
        app_home = ETSConfig.application_home
        # Set it to where the mayavi preferences are temporarily.
        path = join(ETSConfig.application_data, ID)
        ETSConfig.application_home = path
        try:
            pkg = 'mapero.dataflow_editor.preferences'
            pref = 'preferences.ini'
            pref_file = pkg_resources.resource_stream(pkg, pref)

            preferences = self.preferences
            default = preferences.node('default/')
            default.load(pref_file)
            pref_file.close()
        finally:
            # Set back the application home.
            ETSConfig.application_home = app_home

    def _preferences_changed(self, preferences):
        """Setup the helpers if the preferences trait changes."""
        for helper in (self.root, ):
            helper.preferences = preferences


##########################################################
# A Global preference manager that all other modules can use.
preference_manager = PreferenceManager()
