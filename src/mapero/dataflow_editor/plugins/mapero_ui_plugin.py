"""The Mapero plugin.
"""
# Author: Zacarias F. Ojeda <zojeda@gmail.com>
# License: new BSD Style.

from mapero.core.catalog import Catalog

from enthought.traits.api import List, on_trait_change, HasTraits
from enthought.traits.ui.api import View, Item
from enthought.envisage.api import Plugin

# This module's package.
PKG = '.'.join(__name__.split('.')[:-1])
# The mayavi package ID.
ID = 'enthought.mayavi'

SHELL_VIEW = 'enthought.plugins.python_shell_view'
CURRENT_SELECTION_VIEW = 'mapero.dataflow_editor.view.current_selection'
CATALOG_TREE_VIEW = 'mapero.dataflow_editor.view.catalog_tree_view'

import logging
logger = logging.getLogger()


class NoneTraits(HasTraits):
    pass
    #mapero_version = ReadOnly(0.1)
###############################################################################
# `MaperoPlugin` class.
###############################################################################

current_selection_view = View(Item(
                                   style='custom', springy=True,
                                   show_label=False,),
                              resizable=True,
                              scrollable=True
                              )

class MaperoUIPlugin(Plugin):

    # Extension point Ids.
    VIEWS             = 'enthought.envisage.ui.workbench.views'
    SERVICE_OFFERS    = 'enthought.envisage.ui.workbench.service_offers'
    PREFERENCES       = 'enthought.envisage.preferences'
    ACTION_SETS       = 'enthought.envisage.ui.workbench.action_sets'

    # The plugins name.
    name = 'Mapero plugin'
    

    ###### Contributions to extension points made by this plugin ######

    action_sets = List(contributes_to=ACTION_SETS)

    def _action_sets_default(self):
        """ Trait initializer. """

        from mapero.dataflow_editor.action_set import (
            MaperoUIActionSet
        )
        
        return [MaperoUIActionSet]

    # Views.
    views = List(contributes_to=VIEWS)

    # Services we contribute.
    #service_offers = List(contributes_to=SERVICE_OFFERS)

    # Preferences.
    #preferences = List(contributes_to=PREFERENCES)


    def _views_default(self):
        """ Trait initializer. """
        return [self._catalog_tree_view_factory, self._current_selection_view_factory]

#    def _preferences_default(self):
#        """ Trait initializer. """
#        return ['pkgfile://%s/preferences/preferences.ini' % ID]
#
#
#    ######################################################################
#    # Private methods.
    def _catalog_tree_view_factory(self, window, **traits):
        """ Factory method for catalog_tree views. """
        from mapero.dataflow_editor.view.catalog_tree_view import CatalogTreeView

        print "_catalog_tree_view_factory"

        catalog = window.get_service( Catalog )
        
        print catalog
        catalog_tree_view = CatalogTreeView(obj = catalog, window = window)
        return catalog_tree_view

    def _current_selection_view_factory(self, window, **traits):
        """ Factory method for the current selection of the engine. """

        from enthought.pyface.workbench.traits_ui_view import \
                TraitsUIView
        
        noneTrait = NoneTraits()
        tui_current_view = TraitsUIView(
                                       obj = noneTrait,
                                       #view=current_selection_view,
                                       id=CURRENT_SELECTION_VIEW,
                                       name='Mapero object editor',
                                       window=window,
                                       position='bottom',
                                       relative_to=CATALOG_TREE_VIEW,
                                       **traits
                                       )
        return tui_current_view
    

#    def _service_offers_default(self):
#        """ Trait initializer. """
#        engine_service_offer = ServiceOffer(
#            protocol = 'enthought.mayavi.core.engine.Engine',
#            factory  = PKG + '.envisage_engine.EnvisageEngine'
#        )
#
#        script_service_offer = ServiceOffer(
#            protocol = 'enthought.mayavi.plugins.script.Script',
#            factory  = PKG + '.script.Script'
#        )
#        return [engine_service_offer, script_service_offer]
    ######################################################################
    # Trait handlers.
    @on_trait_change('application.gui:started')
    def _on_application_gui_started(self, obj, trait_name, old, new):
        """This is called when the application's GUI is started.  The
        method binds the `Catalog` instance on the
        interpreter.
        """
        # This is called when the application trait is set but we don't
        # want to do anything at that point.
        if trait_name != 'started' or not new:
            return

        # Get the script service.
        app = self.application
        window = app.workbench.active_window
        
        catalog = window.get_service( Catalog )
        
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
            py.bind('catalog', catalog)

        except AttributeError, msg:
            # This can happen when the shell is not visible.
            # FIXME: fix this when the shell plugin is improved.
            logger.warn(msg)
            logger.warn("Can't find the Python shell to bind variables")
