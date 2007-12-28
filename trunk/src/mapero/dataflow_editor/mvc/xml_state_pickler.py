import enthought.persistence.state_pickler as state_pickler
#import gnosis.xml.pickle as xml_pickle
#
#class XMLStatePickler(state_pickler.StatePickler):
#    def dumps(self, value):
#        """Pickles the state of the object (`value`) and returns a
#        string.
#        """
#        return xml_pickle.dumps(self._do(value))
#    def dump(self, value, file):
#        """Pickles the state of the object (`value`) into the passed
#        file.
#        """
#        try:
#            # Store the file name we are writing to so we can munge
#            # file paths suitably.
#            self.file_name = file.name
#        except AttributeError:
#            pass
#        xml_pickle.dump(self._do(value), file)
#
#class XMLStateUnpickler(state_pickler.StateUnpickler):
#
#    def load_state(self, file):
#        """Returns the state of an object loaded from the pickled data
#        in the given file.
#        """
#        try:
#            self.file_name = file.name
#        except AttributeError:
#            pass
#        data = xml_pickle.load(file)
#        result = self._process(data)
#        return result
#
#        
#######################################################################
## Internal Utility functions.
#######################################################################
#def _get_file_read(f):
#    if hasattr(f, 'read'):
#        return f
#    elif isinstance(f, basestring):
#        return open(f, 'rb')
#    else:
#        raise TypeError, 'Given object is neither a file or String'
#
#
#def _get_file_write(f):
#    if hasattr(f, 'write'):
#        return f
#    elif isinstance(f, basestring):
#        return open(f, 'wb')
#    else:
#        raise TypeError, 'Given object is neither a file or String'
#            
#######################################################################
## Utility functions.
#######################################################################
#def dump(value, file):
#    """Pickles the state of the object (`value`) into the passed file
#    (or file name).
#    """
#    f = _get_file_write(file)
#    try:
#        XMLStatePickler().dump(value, f)
#    finally:
#        f.flush()
#        if f is not file:
#            f.close()
#            
#            
#def load_state(file):
#    """Returns the state of an object loaded from the pickled data in
#    the given file (or file name).
#    """
#    f = _get_file_read(file)
#    try:
#        state = XMLStateUnpickler().load_state(f)
#    finally:
#        if f is not file:
#            f.close()
#    return state
#
#
#def set_state(obj, state, ignore=None, first=None, last=None):
#    state_pickler.StateSetter().set(obj, state, ignore, first, last)
