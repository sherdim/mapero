import wx
_ = wx.GetTranslation
import logging

log = logging.getLogger('mapero.logger.mvc')

class SimpleDVCommand(wx.lib.docview.Command):
    def __init__(self, name, dataflow_document):
        self.dataflow_document = dataflow_document
        self.controller = dataflow_document.controller

        wx.lib.docview.Command.__init__(self, True, _(name))

    def Do(self):
        doc = self.dataflow_document
        if self.SimpleDo():
            doc.Modify(True)
            doc.UpdateAllViews()
            return True

    def Undo(self):
        doc = self.dataflow_document
        if self.SimpleUndo():
            doc.Modify(True)
            doc.UpdateAllViews()
            return True

    def dataflow_document(self):
        return self.dataflow_document

class NewConnectionCommand(SimpleDVCommand):
    def __init__(self, dataflow_document, module_from, port_from, module_to, port_to):
            self.module_from = module_from
            self.port_from = port_from
            self.module_to = module_to
            self.port_to = port_to
            SimpleDVCommand.__init__(self, "New Connection", dataflow_document)

    def SimpleDo(self):
            controller = self.controller
            controller.add_connection(self.module_from, self.port_from, self.module_to, self.port_to)
            return True

    def SimpleUndo(self):
            controller = self.controller
            controller.remove_connection(self.module_from, self.port_from, self.module_to, self.port_to)
            return True

class SimpleDVModuleCommand(SimpleDVCommand):
    def __init__(self, name, dataflow_document, module):
        self.module = module
        SimpleDVCommand.__init__(self, name, dataflow_document)

class MoveCommand(SimpleDVModuleCommand):
    def __init__(self, dataflow_document, module, mx, my ):
        self._mx = mx
        self._my = my
        SimpleDVModuleCommand.__init__(self, "Move Module", dataflow_document, module)


    def SimpleUndo(self):
        controller = self.controller
        controller.move_module(self.module, -self._mx, -self._my)
        return True

    def SimpleDo(self):
        controller = self.controller
        module = self.module
        mx = self._mx
        my = self._my
        controller.move_module(module, mx, my)
        return True

class AddModuleCommand(SimpleDVModuleCommand):
    def __init__(self, dataflow_document, module, x, y):
        self._x = x
        self._y = y
        SimpleDVModuleCommand.__init__(self, "Add Module", dataflow_document, module)

    def SimpleDo(self):
        controller = self.controller
        module = self.module
        x = self._x
        y = self._y
        self.module = controller.add_module(module, x, y)
        return True

    def SimpleUndo(self):
        controller = self.controller
        module = self.module
        controller.remove_module(module)
        return True

class RemoveModuleCommand(SimpleDVModuleCommand):
    def __init__(self, dataflow_document, module, x, y):
        self._x = x
        self._y = y
        SimpleDVModuleCommand.__init__(self, "Remove Module", dataflow_document, module)

    def SimpleDo(self):
        controller = self.controller
        module = self.module
        x = self._x
        y = self._y
        log.debug("doing remove module : %s " % (module))
#        self.module = doc.remove_module(module)
        controller.remove_module(module)
        return True

    def SimpleUndo(self):
        controller = self.controller
        module = self.module
        x = self._x
        y = self._y
        log.debug("undoing remove module : %s " % (module))
        controller.add_module(module, x, y)
        return True
