""" Wizard example. """


# Standard library imports.
import os, sys
import wx

# Enthought library imports.
from enthought.pyface.api import GUI, OK
from enthought.pyface.wizard.api import SimpleWizard, WizardPage
from enthought.traits.api import HasTraits, Int, Str, List

class PortDetails(HasTraits):
    """ Details needed to create a port"""
    trait = Str
    name = Str
    description = Str

class ModuleDetails(HasTraits):
    """ Data to create a Module """

    name = Str
    package = Str
    documentation = Str
    
class ListPortsDetails(HasTraits):
    """" A list of port details"""
    ports_details = List(Str)
    
class ModuleWizardPage(WizardPage):

    name = Str
    package = Str
    documentation = Str
    ###########################################################################
    # 'WizardPage' interface.
    ###########################################################################

    def create_page(self, parent):
        """ Create the wizard page. """

        module_details = ModuleDetails(name=self.name, package=self.package, documentation=self.documentation)
        module_details.on_trait_change(self._on_mod_det_changed)
  
        return module_details.edit_traits(parent=parent, kind='subpanel').control
    
    def _on_mod_det_changed(self, new):
        self.complete = len(new.strip()) > 0

class PortWizardPage(WizardPage):

    ports =  ListPortsDetails()
    ###########################################################################
    # 'WizardPage' interface.
    ###########################################################################

    def create_page(self, parent):
        """ Create the wizard page. """

        ports_details = ListPortsDetails()
        ports_details.on_trait_change(self._on_ports_det_changed)
  
        return ports_details.edit_traits(parent=parent, kind='subpanel').control
    
    def _on_ports_det_changed(self):
        self.complete = True


# Application entry point.
if __name__ == '__main__':
    # Create the GUI (this does NOT start the GUI event loop).
    gui = GUI()

    wizard = SimpleWizard(
        parent = None,
        title  = 'Create a new module',
        pages  = [
            ModuleWizardPage(id='module_info'),
            PortWizardPage(id='input_ports'),
            PortWizardPage(id='output_ports')
        ]
    )

    # Create and open the wizard.
    if wizard.open() == OK:
        print 'Wizard completed successfully'

    else:
        print 'Wizard cancelled'

    # Start the GUI event loop!
    gui.start_event_loop()

##### EOF #############################
