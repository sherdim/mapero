# Function to convert simple ETS project names and versions to a requirements
# spec that works for both development builds and stable builds.  Allows
# a caller to specify a max version, which is intended to work along with
# Enthought's standard versioning scheme -- see the following write up:
#    https://svn.enthought.com/enthought/wiki/EnthoughtVersionNumbers
def etsdep(p, min, max=None, literal=False):
    require = '%s >=%s.dev' % (p, min)
    if max is not None:
        if literal is False:
            require = '%s, <%s.a' % (require, max)
        else:
            require = '%s, <%s' % (require, max)
    return require


# Declare our ETS project dependencies.
APPTOOLS = etsdep('AppTools', '3.0.0')  # -- imports of persistence and resource in many places
ENTHOUGHTBASE = etsdep('EnthoughtBase', '3.0.0')    # The 'plugin' extra is required by loose-coupling in the mayavi ui plugin definition's default pespective.
ENVISAGECORE = etsdep('EnvisageCore', '3.0.0')
ENVISAGEPLUGINS = etsdep('EnvisagePlugins', '3.0.0')
TRAITSBACKENDWX = etsdep('TraitsBackendWX', '3.0.1')
TRAITSBACKENDQT = etsdep('TraitsBackendQt', '3.0.1')
CHACO = etsdep('Chaco', '3.0.0')
TRAITSGUI = etsdep('TraitsGUI', '3.0.1')
TRAITS_UI = etsdep('Traits[ui]', '3.0.1')


# A dictionary of the pre_setup information.
INFO = {
    'extras_require': {
        'ui': [
            ENVISAGECORE,
            ENVISAGEPLUGINS,
            ],
        'util': [
            TRAITSBACKENDQT,
            ],
        },

        # All non-ets dependencies should be in this extra to ensure users can
        # decide whether to require them or not.
        'nonets': [
                        'threadec>=0.1',
                        'decorator>=2.2',
#                        'wxPython>=2.6',
#                        'numpy>=1.0.2',
                        'IoC',
            #'VTK',  # fixme: VTK is not available as an egg on all platforms.
            #'wxPython',  # Not everyone uses WX.
            ],
    'install_requires': [
        APPTOOLS,
        ENTHOUGHTBASE,
        TRAITSGUI,
        TRAITS_UI,
        CHACO,
        ],
    'name': 'Mapero',
    'version': '0.1.1b1',
    }
