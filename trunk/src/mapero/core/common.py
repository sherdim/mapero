# Standard library imports.
import sys
import traceback
import logging

from enthought.pyface import api as pyface

# Setup a logger for this module.
logger = logging.getLogger('')

#### Mayavi exception in common
def exception(msg='Exception', parent=None):
    """This function handles any exception derived from Exception and
    prints out an error.  The optional `parent` argument is passed
    along to the dialog box.  The optional `msg` is printed and sent
    to the logger.  So you could send extra information here.
    """
    try:
        type, value, tb = sys.exc_info()
        info = traceback.extract_tb(tb)
        filename, lineno, function, text = info[-1] # last line only
#        exc_msg = "%s\nIn %s:%d\n%s: %s (in %s)" %\
#                  (msg, filename, lineno, type.__name__, str(value),
#                   function)
        # Log and display the message.
        logger.exception(msg)
        pyface.error(parent, msg, title='Exception')
    finally:
        type = value = tb = None # clean up