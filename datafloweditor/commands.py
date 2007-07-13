import wx
_ = wx.GetTranslation


class SimpleDVCommand(wx.lib.docview.Command):
    def __init__(self, name, dataflowDocument):
        self._dataflowDocument = dataflowDocument
        wx.lib.docview.Command.__init__(self, True, _(name))

    def Do(self):
        doc = self.GetDataflowDocument()
        if self.SimpleDo():
            doc.Modify(True)
            doc.UpdateAllViews()
            return True

    def Undo(self):
        doc = self.GetDataflowDocument()
        if self.SimpleUndo():
            doc.Modify(True)
            doc.UpdateAllViews()
            return True

    def GetDataflowDocument(self):
        return self._dataflowDocument

class NewConnectionCommand(SimpleDVCommand):
    def __init__(self, dataflowDocument, module_from, port_from, module_to, port_to):
            self._module_from = module_from
            self._port_from = port_from
            self._module_to = module_to
            self._port_to = port_to
            SimpleDVCommand.__init__(self, "New Connection", dataflowDocument)

    def SimpleDo(self):
            doc = self._dataflowDocument
            doc.add_connection(self._module_from, self._port_from, self._module_to, self._port_to)
            return True

    def SimpleUndo(self):
            doc = self._dataflowDocument
            doc.remove_connection(self._module_from, self._port_from, self._module_to, self._port_to)
            return True

class SimpleDVModuleCommand(SimpleDVCommand):
    def __init__(self, name, dataflowDocument, module):
        self._module = module
        SimpleDVCommand.__init__(self, name, dataflowDocument)

    def GetModule(self):
        return self._module

class MoveCommand(SimpleDVModuleCommand):
    def __init__(self, dataflowDocument, module, mx, my ):
        self._mx = mx
        self._my = my
        SimpleDVModuleCommand.__init__(self, "Move Module", dataflowDocument, module)


    def SimpleUndo(self):
        doc = self._dataflowDocument
        doc.move_module(self._module, -self._mx, -self._my)
        return True

    def SimpleDo(self):
        doc = self.GetDataflowDocument()
        module = self.GetModule()
        mx = self._mx
        my = self._my
        doc.move_module(module, mx, my)
        return True

class AddModuleCommand(SimpleDVModuleCommand):
    def __init__(self, dataflowDocument, module, x, y):
        self._x = x
        self._y = y
        SimpleDVModuleCommand.__init__(self, "Add Module", dataflowDocument, module)

    def SimpleDo(self):
        doc = self.GetDataflowDocument()
        module = self.GetModule()
        x = self._x
        y = self._y
        self._module = doc.add_module(module, x, y)
        return True

    def SimpleUndo(self):
        doc = self.GetDataflowDocument()
        module = self.GetModule()
        doc.remove_module(module)
        return True

