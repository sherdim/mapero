""" A file system tree. """


# Standard library imports.
from os import listdir
from os.path import basename, isdir, join

# Enthought library imports.
from enthought.pyface.image_resource import ImageResource
from enthought.pyface.tree.tree import Tree
from enthought.pyface.tree.tree_model import TreeModel
from enthought.traits.api import Instance

import string

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
	childrens = node[1][0].items() + [node[0]+ '.'+module_name for module_name in node[1][1].keys()]
	
        return childrens

	#return childrens

    def has_children(self, node):
        """ Returns True if a node has children, otherwise False. """
	if isinstance(node, str):
	    has_children = False
	else:
	    has_children = True
        return has_children

    def get_image(self, node, selected, expanded):
        """ Returns the label image for a node. """

	if isinstance(node,str):
	    image = self.DOCUMENT
	else:
		image =  expanded and self.OPEN_FOLDER or self.CLOSED_FOLDER

        return image

    def get_text(self, node):
        """ Returns the label text for a node. """
	#fbi()
	node_name = ''
	if isinstance(node,str):
	    node_name = string.split(node,'.')[-1]
	elif isinstance(node[0],str):
	    node_name = node[0]
	else:
	    node_name = 'modulos'

        return node_name


class CatalogTree(Tree):
    """ A file system tree. """

    #### 'Tree' interface #####################################################

    # The model that provides the data for the tree.
    model = Instance(CatalogTreeModel, ())

##### EOF #####################################################################

