""" A file system tree. """


# Standard library imports.
# Enthought library imports.
from enthought.pyface.image_resource import ImageResource
from enthought.pyface.tree.tree import Tree
from enthought.pyface.tree.tree_model import TreeModel
from enthought.traits.api import Instance
from mapero.core.catalog import Categorie
from mapero.core.catalog import ModuleInfo
from compiler.ast import Node
from platform import node

class CatalogTreeModel(TreeModel):
    """ A tree model for local file systems. """

    # The image used to represent folders that are NOT expanded.
    CLOSED_FOLDER = ImageResource('closed_folder')

    # The image used to represent folders that ARE expanded.
    OPEN_FOLDER = ImageResource('open_folder')

    # The image used to represent documents (ie. NON-'folder') nodes.
    DOCUMENT = ImageResource('document')

    #########################################################################
    # 'TreeModel' interface.
    #########################################################################

    def get_children(self, node):
        """ Returns the children of a node. """
        #childrens = node.values()[1][1].keys()
        if isinstance(node, list):
            return node
        else: 
            children = node.categories + node.modules
        return children

    #return childrens

    def has_children(self, node):
        """ Returns True if a node has children, otherwise False. """
        if isinstance(node, Categorie) or isinstance(node, list):
            has_children = True
        else:
            has_children = False
        return has_children

    def get_image(self, node, selected, expanded):
        """ Returns the label image for a node. """
        if isinstance(node,ModuleInfo):
            image = self.DOCUMENT
        else:
            image =  expanded and self.OPEN_FOLDER or self.CLOSED_FOLDER
        return image

    def get_text(self, node):
        """ Returns the label text for a node. """
    #fbi()
        if (hasattr(node, 'name')):
            node_name = getattr(node, 'name')
        else:
            node_name = 'modulos'
        return node_name


class CatalogTree(Tree):
    """ A file system tree. """

    #### 'Tree' interface #####################################################

    # The model that provides the data for the tree.
    model = Instance(CatalogTreeModel, ())

##### EOF #####################################################################

