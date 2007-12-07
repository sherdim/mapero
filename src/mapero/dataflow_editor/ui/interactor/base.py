

#from mapero.dataflow_editor.config import Config

class BaseInteractor(object):
    def __init__(self, document, view, config_name):
	self.document = document
	self.view = view
#	self.config = Config().getConfig(config_name);

    def on_event(event):
        pass
