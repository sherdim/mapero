import mapero
import mapero.modules
import mapero.datatypes
from enthought.traits import api as traits
from os.path import abspath, join, split, isfile, realpath, walk
import os 
import glob
import sys
import imp
#TODO: verificar mejor los paths y los nombres que se dan a los modulos
cwd1 = realpath(__file__)
cwd2 = split(cwd1)[0]
cwd3 = split(cwd2)[0]
cwd4 = split(cwd3)[0]

mapero_path =  abspath(cwd3)
print mapero_path
builtin_modules = join(mapero_path, 'builtin-modules')

import logging
log = logging.getLogger("mapero.logger.engine");

class NotFoundInCatalogError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class ModuleNotFoundInCatalogError(NotFoundInCatalogError):
    pass

class CategorieNotFoundInCatalogError(NotFoundInCatalogError):
    pass

class ModuleInfo(traits.HasTraits):
    name = traits.Str
    description = traits.Str
    clazz = traits.Trait
    canonical_name = traits.Property(traits.Str)
    
    def __init__(self, **traits):
        super(ModuleInfo, self).__init__(**traits)
        if self.clazz != None:
            self.name = self.clazz.__name__
            self.description = self.clazz.__doc__
        
    def _get_canonical_name(self):
        return self.clazz.__module__[len(mapero.modules.__name__)+1:]
    
    def _clazz_changed(self, value):
        self.name = self.clazz.__name__
        self.description = self.clazz.__doc__
    
class Categorie(traits.HasTraits):
    name = traits.Str
    modules = traits.List(ModuleInfo)
    
Categorie.add_class_trait('categories', traits.List(Categorie))

class Catalog(traits.HasTraits):
    dirs = traits.List(traits.Directory)
    modules = traits.List(Categorie)

    def __init__(self, **traits):
        super(Catalog, self).__init__(**traits)
        self.dirs.append(builtin_modules)
        self._catalog = {'modules':({},{})}
#        mapero.__path__ = mapero.__path__ + self.dirs
        for dir in self.dirs:
            mapero.modules.__path__.append( join(dir,'modules') )
            mapero.datatypes.__path__.append(  join(dir,'datatypes') )
        self.refresh()

    def refresh(self):
        def _inspect_dir (arg, dir_name, names):
            for entry in dir_name.split(os.sep):
                if entry.startswith("."):
                    return
            if not split(dir_name)[1].startswith("."):
                log.debug("inspecting dir: %s" % dir_name)
                paths = glob.glob(join(dir_name,'*.py'))
                for path in paths:
                    if isfile(path):
                        for dir in self.dirs:
                            if path.startswith(dir):
                                module_name = path[len(dir):].replace(os.sep, '.')
                                suff_index = module_name.rfind(".py")
                                module_name = module_name[1:suff_index]
                                if not (module_name.endswith("__")):
                                    py_module = self.import_module(module_name)
                                    self.__add_modules(py_module)
                                    
                        
#                        f, fn, d = imp.find_module(module_name, [module_path])
#                        module = imp.load_module(module_name, f, fn, d)
#                        if hasattr(module, 'module_info'):
#                            module_info = getattr(module, 'module_info')
#                            self._add_module(module_info['name'], module, module_path, module_info)
        for dir in self.dirs:
            walk(dir, _inspect_dir, None)

    def load_module(self, module_name):
        module_class = self._get_module_class(module_name)
        module = module_class()
        return module

    def _get_module_class(self, module_name):
        def cross_catalog(categorie):
            for cat in categorie.categories:
                returned_mod = cross_catalog(cat)
                if returned_mod != None:
                    return returned_mod
            for mod in categorie.modules:
                if (mod.canonical_name == module_name):
                    return mod.clazz
        for categorie in self.modules:
            returned_mod = cross_catalog(categorie)
            if returned_mod != None:
                return returned_mod
        
        
    def reload_module(self, module_name):
        metadata = self.get_module_metadata(module_name)
        f, fn, d = imp.find_module(metadata['module'], [metadata['path']])
        metadata['python_module'] = imp.load_module(metadata['module'], f, fn, d)
        return getattr(metadata['python_module'],metadata['module'])()

    def recorrer(self):
        print "================ recorriendo =================="
        def cross_catalog(categorie, ident):
            print '\t'*ident + '['+ categorie.name +']'
            for cat in categorie.categories:
                cross_catalog(cat, ident+1)
            for mod in categorie.modules:
                print '\t'*(ident+1) + str(mod.name)
        for categorie in self.modules:
            cross_catalog(categorie,0)
        print "================ recorrido =================="
    
    def import_module(self, tail):
            m = mapero
            while tail:
                i = tail.find('.')
                if i < 0: i = len(tail)
                head, tail = tail[:i], tail[i+1:]
                mname = "%s.%s" % (m.__name__, head)
                m = import_module(head, mname, m)
                if not m:
                    raise ImportError, "No module named " + mname
            return m
    
    def __add_modules(self, py_module):
        def _recorrer_categories(current_cat, tail_cats, module):
            if len(tail_cats)==0:
                new_module_info = ModuleInfo(clazz = module)
                current_cat.modules.append(new_module_info)
                return
            
            other_cat = tail_cats.pop(0)
            other_cat_in_current_cat = False
            if current_cat:
                for cat in current_cat.categories:
                    if cat.name == other_cat:
                        other_cat_in_current_cat = True
                        _recorrer_categories(cat, tail_cats, module)
                if not other_cat_in_current_cat:
                    new_categorie = Categorie(name = other_cat)
                    current_cat.categories.append(new_categorie)
                    _recorrer_categories(new_categorie, tail_cats, module)
                        
            else:
                other_cat_in_current_cat = False
                for cat in self.modules:
                    if other_cat == cat.name:
                        other_cat_in_current_cat = True
                        _recorrer_categories(cat, tail_cats, module)
                if not other_cat_in_current_cat:
                    new_categorie = Categorie(name = other_cat)
                    self.modules.append(new_categorie)
                    _recorrer_categories(new_categorie, tail_cats, module)
                 
        py_name = py_module.__name__
        modules_name =mapero. modules.__name__
        i = py_name.rfind('.')
        module_name = py_name[i+1:]
        categories = py_name[len(modules_name)+1:i].split('.')
        
#        print "========"
#        print "module_name: ", module_name
#        print "categories: ", categories 
#        print "========"
        mapero_module = getattr(py_module, module_name)
        _recorrer_categories(None, categories, mapero_module)
    
def import_module(partname, fqname, parent):
    log.debug( "import_module: partname: %s\t fqname:%s\t parent:%s" % (partname, fqname, parent) )
    try:
        m = sys.modules[fqname]
        return m
    except KeyError:
        pass
    try:
        fp, pathname, stuff = imp.find_module(partname, parent and parent.__path__)
    except ImportError:
        return None
    try:
        m = imp.load_module(fqname, fp, pathname, stuff)
    finally:
        if fp: fp.close()
    if parent:
        setattr(parent, partname, m)
    return m
