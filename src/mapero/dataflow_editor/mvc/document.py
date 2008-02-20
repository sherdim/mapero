from mapero.dataflow_editor.decorators.thread import threaded_process
from mapero.dataflow_editor.mvc.controller import DataflowEditorController

from wx.lib import docview
from enthought.persistence import state_pickler as state_pickler


import logging
log = logging.getLogger("mapero.logger.mvc");

class DataflowDocument(docview.Document):
    
    def __init__(self):
        log.debug( "creating document" )
        
        super(DataflowDocument,self).__init__(self)
        self._inModify = False
        self.controller = DataflowEditorController(document=self)
        
        self.controller.on_trait_event(self.update_views, 'network_updated')
    
    def update_views(self):
        self.Modify(True)
        self.UpdateAllViews()

    
    def SaveObject(self, fileObject):
        dataflow_editor_model = self.controller.dataflow_editor_model
        log.debug("saving file")
        state_pickler.dump(dataflow_editor_model, fileObject)
        log.debug("file saved")
        return True


    def LoadObject(self, fileObject):
        log.debug("loading state from file: ")
        state = state_pickler.load_state(fileObject)
        log.debug("creating dataflow from state")
        self.controller.create_dataflow_model(state)
        log.debug("dataflow created")
        self.UpdateAllViews(self)
        
        return True

        

