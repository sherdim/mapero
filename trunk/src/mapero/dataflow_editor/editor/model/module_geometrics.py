# Author: Zacarias F. Ojeda <zojeda@gmail.com>
# License: new BSD Style.

from enthought.traits.api import HasTraits, Float, WeakRef
from mapero.core.module import Module

class ModuleGeometrics(HasTraits):
    x = Float
    y = Float
    w = Float
    h = Float
    module = WeakRef(Module)
