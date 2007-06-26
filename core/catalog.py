from enthought.traits.api import List, Directory, HasTraits
from os.path import abspath, dirname, join, split, isdir, isfile
import mapero
import glob
import string
import re
import imp

#TODO: verificar mejor los paths y los nombres que se dan a los modulos

mapero_path =  abspath(dirname(mapero.__file__))
builtin_modules = join(mapero_path, 'modules')

class NotFoundInCatalogError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class ModuleNotFoundInCatalogError(NotFoundInCatalogError):
	pass

class CategorieNotFoundInCatalogError(NotFoundInCatalogError):
	pass

class Catalog(HasTraits):
	dirs = List(Directory)

	def __init__(self, **traits):
		super(Catalog, self).__init__(**traits)
		self.dirs = [builtin_modules]
		self._catalog = {'modules':({},{})}
		self.refresh()

	def refresh(self):
		def _inspect_dir (dir_name):
			paths = glob.glob(join(dir_name,'*.py'))
			for path in paths:
				if isdir(path):
					_inspect_dir(path)
				elif isfile(path):
					module_path, module_name = split(path)
					module_name = string.split(module_name,'.')[0]
					f, fn, d = imp.find_module(module_name, [module_path])
					module = imp.load_module(module_name, f, fn, d)
					if hasattr(module, 'module_info'):
						module_info = getattr(module, 'module_info')
						self._add_module(module_info['name'], module, module_path, module_info)
		for dir in self.dirs:
			_inspect_dir(dir)

	def load_module(self, module_name):
		metadata = self.get_module_metadata(module_name)
		module = getattr(metadata['python_module'],metadata['module'])()
		module.module_info = metadata['module_info']
		module.label = metadata['module']
		return module

	def reload_module(self, module_name):
		metadata = self.get_module_metadata(module_name)
		f, fn, d = imp.find_module(metadata['module'], [metadata['path']])
		metadata['python_module'] = imp.load_module(metadata['module'], f, fn, d)
		return getattr(metadata['python_module'],metadata['module'])()

	def recorrer(self):
		def cross_catalog(categories, ident):
			for categorie_name, categorie in categories.iteritems():
				print '%s categorie: %s' % ('   '*ident, categorie_name)
				for module_name in categorie[1].keys():
					print '%s module: %s' % ('   '*(ident+1), module_name)
				new_ident= ident + 1
				cross_catalog(categorie[0], new_ident)
		cross_catalog(self._catalog['modules'][0],1)

	def _add_module(self, module_name, module, path, module_info):
		def recorrer_catalog(categories, module_name, module, path):
			categorie = module_name.pop(0)
			if not categories.has_key(categorie):
				categories[categorie]=({},{})
			if len(module_name)>1:
				recorrer_catalog(categories[categorie][0], module_name, module, path)
			else:
				categories[categorie][1][module_name[0]] = \
				{'module': module_name[0], 'python_module': module, 'path': path, 'module_info': module_info}

		module_name_list = string.split(module_name, '.')
		if hasattr(module,module_name_list[-1]):
			recorrer_catalog(self._catalog['modules'][0], module_name_list, module, path)

	def get_module_metadata(self, module_name):
		def recorrer_catalog(categories, module_name):
			categorie = module_name.pop(0)
			if not categories.has_key(categorie):
				raise CategorieNotFoundInCatalogError(categorie)
			if len(module_name)>1:
				recorrer_catalog(categories[categorie][0], module_name)
			else:
				try:
					return categories[categorie][1][module_name[0]]
				except KeyError, e:
					raise ModuleNotFoundInCatalogError(module_name[0])

		module_name_list = string.split(module_name, '.')
		return recorrer_catalog(self._catalog['modules'][0], module_name_list)
	
	def get_catalog(self):
	    return self._catalog


