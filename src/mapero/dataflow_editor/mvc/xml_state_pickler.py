import enthought.persistence.state_pickler as state_pickler
import gnosis.xml.pickle as xml_pickle

class XMLStatePickler(state_pickler.StatePickler):
    def dumps(self, value):
        """Pickles the state of the object (`value`) and returns a
        string.
        """
        return xml_pickle.dumps(self._do(value))
    def dump(self, value, file):
        """Pickles the state of the object (`value`) into the passed
        file.
        """
        try:
            # Store the file name we are writing to so we can munge
            # file paths suitably.
            self.file_name = file.name
        except AttributeError:
            pass
        xml_pickle.dump(self._do(value), file)