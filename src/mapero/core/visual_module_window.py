





class VisualModuleWindow(object):
    
    def restore(self):
        raise NotImplementedError

    def maximize(self):
        raise NotImplementedError
    
    def minimize(self):
        raise NotImplementedError
    
    
    
class VisualModuleWindowManager:

    def create_window(self, module):
        raise NotImplementedError
    
    def maximize_window(self, module):
        raise NotImplementedError

    def minimize_window(self, module):
        raise NotImplementedError

    def retore_window(self, module):
        raise NotImplementedError

    def dock_window(self, module):
        raise NotImplementedError

    def undock_window(self, module):
        raise NotImplementedError
