#!/usr/bin/env python
#
# Author: Zacarias F. Ojeda <zojeda@gmail.com>
# License: new BSD Style.


"""
Mapero
======

Mapero is a python based framework for creation of dataflow networks
to build algorithms graphically.

The solution is modeled as an interconnected set of processing modules.
Simplicity is the main objective, so the creation of new modules is as
easy as create a python module 
"""


# NOTE: Setuptools must be imported BEFORE numpy.distutils or else
# numpy.distutils does the Wrong(TM) thing.
import setuptools


from distutils.command.clean import clean

from numpy.distutils import log
from numpy.distutils.command.build import build as distbuild
from numpy.distutils.command.install_data import install_data
from numpy.distutils.core import setup
from pkg_resources import DistributionNotFound, parse_version, require, \
    VersionConflict
from setup_data import INFO
from setuptools.command.sdist import sdist
from setuptools.command.develop import develop
from setuptools.command.install_scripts import install_scripts
from traceback import print_exc
import os
import shutil
import zipfile


##############################################################################
# Pull the description values for the setup keywords from our file docstring.
##############################################################################
DOCLINES = __doc__.split("\n")


class my_install_scripts(install_scripts):
    """ Hook to rename the  mapero script to a Mapero.pyw script on win32.
    """
    def run(self):
        install_scripts.run(self)
        if os.name != 'posix':
            # Rename <script> to <script>.pyw. Executable bits
            # are already set in install_scripts.run().
            for file in self.get_outputs():
                if file[-4:] != '.pyw':
                    if file[-7:] == 'mapero':
                        new_file = file[:-7] + 'Mapero.pyw'
                    else:
                        new_file = os.path.splitext(file)[0] + '.pyw'
                    self.announce("renaming %s to %s" % (file, new_file))
                    if not self.dry_run:
                        if os.path.exists(new_file):
                            os.remove (new_file)
                        os.rename (file, new_file)


##############################################################################
# The actual setup call
##############################################################################
setup(
    author = "Zacarias F. Ojeda",
    author_email = "zojeda@gmail.com",
    classifiers = [c.strip() for c in """\
        Development Status :: 4 - Beta
        Intended Audience :: Developers
        Intended Audience :: Science/Research
        License :: OSI Approved :: new BSD License
        Operating System :: MacOS
        Operating System :: Microsoft :: Windows
        Operating System :: OS Independent
        Operating System :: POSIX
        Operating System :: Unix
        Programming Language :: Python
        Topic :: Scientific/Engineering
        Topic :: Software Development
        Topic :: Software Development :: Libraries
        """.splitlines() if len(c.split()) > 0],
    cmdclass = {
        # Work around a numpy distutils bug by forcing the use of the
        # setuptools' sdist command.
        'sdist': sdist,

        'install_scripts': my_install_scripts,
        },
    
    package_dir = {'':'src'},
    packages = setuptools.find_packages('src'),
        
    dependency_links = [
        'http://code.enthought.com/enstaller/eggs/source',
        ],
    description = DOCLINES[1],
    entry_points = {
        'console_scripts': [
            'mapero-dfe = mapero.dataflow_editor.dataflow_editor_app:main',
            ],

        },
    extras_require = INFO['extras_require'],
    include_package_data = True,
    install_requires = INFO['install_requires'] + INFO['nonets'],
    license = "new BSD",
    long_description = '\n'.join(DOCLINES[3:]),
    name = INFO['name'],
#    namespace_packages = [
#        "mapero",
#        ],
    platforms = ["Windows", "Linux", "Mac OS-X", "Unix", "Solaris"],
    url = "http://mapero.googlecode.com/",
    download_url =   "http://mapero.googlecode.com/svn/trunk/dist",
    version = INFO['version'],
    zip_safe = False,
    )
