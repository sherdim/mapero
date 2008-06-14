""" A file system tree. """


# Enthought library imports.
from enthought.pyface.image_resource import ImageResource
from enthought.traits.api import Instance, HasTraits, HasPrivateTraits


from mapero.core.catalog import Catalog, Categorie, ModuleInfo
from enthought.envisage.workbench.traits_ui_view import TraitsUIView
from enthought.traits.ui.api import TreeEditor, TreeNodeObject, ObjectTreeNode, View, Item, Group


from mapero.dataflow_editor.services import ICATALOG

class CatalogNode (TreeNodeObject):
    catalog = Instance(Catalog)
    #########################################################################
    # 'TreeNodeObject' interface.
    #########################################################################

    #---------------------------------------------------------------------------
    #  Returns whether chidren of this object are allowed or not:  
    #---------------------------------------------------------------------------

    def tno_allows_children ( self, node ):
        """ Returns whether chidren of this object are allowed or not.
        """
        return True
    
    #---------------------------------------------------------------------------
    #  Returns whether or not the object has children:  
    #---------------------------------------------------------------------------

    def tno_has_children ( self, node = None ):
        """ Returns whether or not the object has children.
        """
        return (len( self.tno_get_children( node ) ) > 0)
        
    def tno_get_children(self, node):
        """ Returns the children of a node. """
        #childrens = node.values()[1][1].keys()
        if isinstance(node, list):
            return node
        else: 
            children = []
            for categorie in self.catalog.categories:
                children.append( CategorieNode(categorie = categorie)  ) 
                 
        return children
    
    
class CategorieNode ( TreeNodeObject ):
    categorie = Instance(Categorie)

    def tno_get_label( self, node ):
        return self.categorie.name
    #---------------------------------------------------------------------------
    #  Returns whether chidren of this object are allowed or not:  
    #---------------------------------------------------------------------------

    def tno_allows_children ( self, node ):
        """ Returns whether chidren of this object are allowed or not.
        """
        return True
    
    #---------------------------------------------------------------------------
    #  Returns whether or not the object has children:  
    #---------------------------------------------------------------------------

    def tno_has_children ( self, node = None ):
        """ Returns whether or not the object has children.
        """
        return (len( self.tno_get_children( node ) ) > 0)
        
    def tno_get_children(self, node):
        """ Returns the children of a node. """
        #childrens = node.values()[1][1].keys()
        if isinstance(node, list):
            return node
        else: 
            children = []
            for categorie in self.categorie.categories:
                children.append( CategorieNode(categorie = categorie)  ) 

            for module in self.categorie.modules:
                children.append( ModuleNode(module = module)  ) 
                 
        return children
#-------------------------------------------------------------------------------
#  'Module' class:  
#-------------------------------------------------------------------------------
        
class ModuleNode ( TreeNodeObject ):
    module = Instance(ModuleInfo)
    #---------------------------------------------------------------------------
    #  Returns whether chidren of this object are allowed or not:  
    #---------------------------------------------------------------------------
    def tno_get_label( self, node ):
        return self.module.name
    
    def tno_allows_children ( self, node ):
        """ Returns whether chidren of this object are allowed or not.
        """
        return False
 
    

catalog_tree_editor =  TreeEditor(orientation='vertical', editable=False, 
                nodes = [
                    
                        ObjectTreeNode(node_for   = [ CatalogNode ], 
                                        auto_open  = True, 
                                        label      = '=Catalog'), 
                        ObjectTreeNode(node_for   = [ CategorieNode ], 
                                        auto_close = True, 
                                        label      = 'name'), 
                        ObjectTreeNode(node_for   = [ ModuleNode ], 
                                        label      = 'name')
                        ]
                       )


class CatalogView (HasPrivateTraits):
    catalog = Instance(Catalog)
    root = Instance(CatalogNode)
    #---------------------------------------------------------------------------
    #  Traits view definitions:  
    #---------------------------------------------------------------------------
    def _catalog_changed(self, catalog ):
        self.root = CatalogNode(catalog = catalog)
        
    traits_view = View( 
        Item( name       = 'root', 
              editor     = catalog_tree_editor,
              show_label = False
        )
    )
    
class CatalogTreeView(TraitsUIView):
    
    uol = ICATALOG
    



    
    def create_ui(self, parent):
        """ Creates the traits UI that represents the view. """

        catalog = self._get_target_object()
        catalog_view = CatalogView(catalog=catalog)
        return catalog_view.edit_traits(parent=parent, kind='subpanel')
    
##### EOF #####################################################################
