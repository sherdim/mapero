"""The Mapero plugin.
"""
# Author: Zacarias F. Ojeda <zojeda@gmail.com>
# License: new BSD Style.


from enthought.traits.api import List
from enthought.envisage.api import Plugin, ServiceOffer

# This module's package.
PKG = '.'.join(__name__.split('.')[:-1])
# The mayavi package ID.
ID = 'enthought.mayavi'

###############################################################################
# `MaperoPlugin` class.
###############################################################################
class MaperoPlugin(Plugin):

    # Extension point Ids.
    SERVICE_OFFERS = 'enthought.envisage.ui.workbench.service_offers'
    PREFERENCES       = 'enthought.envisage.preferences'

    # The plugins name.
    name = 'Mapero plugin'

    ###### Contributions to extension points made by this plugin ######

    # Services we contribute.
    service_offers = List(contributes_to=SERVICE_OFFERS)

    # Preferences.
    #preferences = List(contributes_to=PREFERENCES)

#    def _preferences_default(self):
#        """ Trait initializer. """
#        return ['pkgfile://%s/preferences/preferences.ini' % ID]
#
#
    ######################################################################
    # Private methods.
    def _service_offers_default(self):
        """ Trait initializer. """
        print "_service_offers_default"
        catalog_service_offer = ServiceOffer(
            protocol = 'mapero.core.catalog.Catalog',
            factory  = self._catalog_factory
        )
        return [catalog_service_offer]
        
    def _catalog_factory(self, window, **traits):
        from mapero.core.catalog import Catalog
        catalog = Catalog()
        print "_catalog_factory"
        return catalog
        
