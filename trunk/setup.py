#import ez_setup
#ez_setup.use_setuptools()

from setuptools import setup, find_packages
setup(
    name = "mapero",
    version = "0.1a1",
    
    package_dir = {'':'src', 'builtin-modules':'src/mapero/builtin-modules'},
    packages = find_packages('src', 'src/mapero/builtin-modules'),

    dependency_links = [
        'http://code.enthought.com/enstaller/eggs/source',
        'http://code.enthought.com/enstaller/eggs/source/unstable',
        ],

    install_requires = ['enthought.chaco2>=2.0a1',
                        'enthought.pyface[tvtk]>=2.0.1b1',
                        'enthought.tvtk[wx]>=2.0b2',
                        'enthought.persistence>=2.0a1',
                        'threadec>=0.1',
                        'decorator>=2.2',
                        'wxPython>=2.6',
                        'numpy>=1.0.2',
                        'scipy>=0.5',
                        ],


    entry_points = {
        'gui_scripts': [
            'mapero-dfe = mapero.dataflow_editor.dvdataflow_editor_app.py',
        ]
    },

    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt'],
        'mapero.dataflow_editor': ['*.conf'],
        'mapero.dataflow_editor.ui' : ['images/*.png'],
        'mapero.dataflow_editor' : ['*.png'],
    },

    # metadata for upload to PyPI
    author = "Zacarias F. Ojeda",
    author_email = "zojeda@gmail.com",
    description = "Python based framework for creation of dataflow networks to build algorithms graphically.",
    license = "new BSD",
    keywords = "hello world example examples",
    url = "http://mapero.googlecode.com/",
    download_url =   "http://mapero.googlecode.com/svn/trunk/dist",
    long_description = "The solution is modeled as an interconnected set of processing modules. Simplicity is the main objective, so the creation of new modules is as easy as create a python module",
    zip_safe = False, 
    # could also include long_description, download_url, classifiers, etc.
)
