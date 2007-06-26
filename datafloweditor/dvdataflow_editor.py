#----------------------------------------------------------------------------
# Name:         DataflowtEditor.py
# Purpose:      Dataflow Diagram Editor for pydocview
#
# Author:       Zacarias Ojeda
#
#----------------------------------------------------------------------------
import wx
import wx.lib.docview
import wx.lib.pydocview
import string
from dataflowdiagram import DataflowDiagram
from mapero.core.modulemanager import ModuleManager
from xml.dom.minidom import Document, parse

_ = wx.GetTranslation

class Point2D:
	def __init__(self, x, y):
		self.x = x
		self.y = y

class ConnectionGeometrics:
	def __init__(self, points = None):
		self.points = points

class ModuleGeometrics:

	def __init__(self, x, y, w,h):
		self.x = x
		self.y = y
		self.w = w
		self.h = h

	def GetHeight(self):
			return self.h

	def GetWidth(self):
			return self.w

	def GetX(self):
			return self.x

	def GetY(self):
			return self.y

class DataflowDocument(wx.lib.docview.Document):

	def __init__(self):
		wx.lib.docview.Document .__init__(self)
		self._inModify = False
		self._module_manager = ModuleManager()
		self._module_geometrics = {}
		self._connection_geometrics = {}

	def GetModuleManager(self):
		return self._module_manager

	def GetModuleGeometrics(self):
		return self._module_geometrics

	def GetConnectionGeometrics(self):
		return self._connection_geometrics

	def SaveObject(self, fileObject):
		doc = Document();
		diagram = doc.createElement("diagram")
		doc.appendChild(diagram)
		module_id = 0
		module_id_dict = {}
		for module, geometric in self._module_geometrics.items():
			module_id += 1
			module_element = doc.createElement("module")
			module_element.setAttribute("id", str(module_id))
			module_info_element = doc.createElement("module_info")
			module_info_element.setAttribute("name", module.module_info['name'])
			module_element.appendChild(module_info_element)
			module_id_dict[module] = module_id

			geometric_element = doc.createElement("geometric");
			geometric_element.setAttribute("h", str(geometric.GetHeight()));
			geometric_element.setAttribute("w", str(geometric.GetWidth()));
			geometric_element.setAttribute("y", str(geometric.GetY()));
			geometric_element.setAttribute("x", str(geometric.GetX()));
			module_element.appendChild(geometric_element)

			diagram.appendChild(module_element)

		for connection, geometric in self._connection_geometrics.items():
			connection_element = doc.createElement("connection")
			output_port_element = doc.createElement("output_port")
			output_port_element.setAttribute("name", connection.output_port.name)
			output_port_element.setAttribute("module_id", str(module_id_dict[connection.output_port.module]))
			connection_element.appendChild(output_port_element)
			diagram.appendChild(connection_element)

			input_port = doc.createElement("input_port")
			input_port.setAttribute("name", connection.input_port.name)
			input_port.setAttribute("module_id", str(module_id_dict[connection.input_port.module]))
			connection_element.appendChild(input_port)
			diagram.appendChild(connection_element)

		print doc.writexml(fileObject, "",  "\t", "\n")
		return True


	def LoadObject(self, fileObject):
		doc = parse(fileObject)
		module_id_dict = {}
		for module_element in doc.getElementsByTagName("module"):
			id = int(module_element.getAttribute("id"))
			for module_info_element in module_element.getElementsByTagName("module_info"):
				module_name = module_info_element.getAttribute("name")
			for geometric_element in module_element.getElementsByTagName("geometric"):
				h = int(geometric_element.getAttribute("h"))
				w = int(geometric_element.getAttribute("w"))
				x = float(geometric_element.getAttribute("x"))
				y = float(geometric_element.getAttribute("y"))

			module = self.add_module(module_name, x, y, w, h)
			module_id_dict[id] = module

		for connection_element in doc.getElementsByTagName("connection"):
			for output_port_element in connection_element.getElementsByTagName("output_port"):
				output_port_name = str(output_port_element.getAttribute("name"))
				module_from = module_id_dict[int(output_port_element.getAttribute("module_id"))]
			for input_port_element in connection_element.getElementsByTagName("input_port"):
				input_port_name = str(input_port_element.getAttribute("name"))
				module_to = module_id_dict[int(input_port_element.getAttribute("module_id"))]
			self.add_connection(module_from, output_port_name, module_to, input_port_name)

		return True

	def add_module(self, module_name, x, y, w = 151, h = 91):
		self._module_manager.set(trait_change_notify = False)
		print "------------ module_name", module_name
		print "------------ geometrics", x, " " , y, " " , w, " " , h
		module = self._module_manager.add(module_name)
		self._module_geometrics[module] = ModuleGeometrics(x, y, w, h)
		return module

	def add_connection(self, module_from, output_port_name, module_to, input_port_name):
		connection = self._module_manager.connect(module_from, output_port_name, module_to, input_port_name)
		self._connection_geometrics[connection] = ConnectionGeometrics()
#		self._connection_geometrics.

	def move_module(self, module, mx, my):
		geometric = self.GetModuleGeometrics()[module]
		geometric.x += mx
		geometric.y += my
		print "moved module: ", module.name, " (", mx, " , ", my, ")"

	def remove_module(self, module):
		self._module_manager.remove(module)
		del self._module_geometrics[module]


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


class DataflowView(wx.lib.docview.View):

	#----------------------------------------------------------------------------
	# Overridden methods
	#----------------------------------------------------------------------------

	def __init__(self):
		wx.lib.docview.View.__init__(self)
		self._diagramCtrl = None
		self._wordWrap = wx.ConfigBase_Get().ReadInt("DiagramEditorWordWrap", True)


	def OnCreate(self, doc, flags):
		frame = wx.GetApp().CreateDocumentFrame(self, doc, flags)
		sizer = wx.BoxSizer()
		font, color = self._GetFontAndColorFromConfig()
		self._diagramCtrl = self._BuildDiagramCtrl(frame, font, color = color)
		sizer.Add(self._diagramCtrl.GetCanvas(), 1, wx.EXPAND, 0)
		frame.SetSizer(sizer)
		frame.Layout()
		frame.Show(True)
		self.Activate()
		return True


	def OnModify(self, event):
		self.GetDocument().Modify(True)


	def _BuildDiagramCtrl(self, parent, font, color = wx.BLACK, value = "", selection = [0, 0]):
		if self._wordWrap:
				wordWrapStyle = wx.TE_WORDWRAP
		else:
				wordWrapStyle = wx.TE_DONTWRAP
		module_manager = self.GetDocument().GetModuleManager()
		diagramCtrl = DataflowDiagram(parent, module_manager, None, self)
		return diagramCtrl


	def _GetFontAndColorFromConfig(self):
		font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
		config = wx.ConfigBase_Get()
		fontData = config.Read("DiagramEditorFont", "")
		if fontData:
			nativeFont = wx.NativeFontInfo()
			nativeFont.FromString(fontData)
			font.SetNativeFontInfo(nativeFont)
		color = wx.BLACK
		colorData = config.Read("DiagramEditorColor", "")
		if colorData:
			red = int("0x" + colorData[0:2], 16)
			green = int("0x" + colorData[2:4], 16)
			blue = int("0x" + colorData[4:6], 16)
			color = wx.Color(red, green, blue)
		return font, color


	def OnCreateCommandProcessor(self):
		# Don't create a command processor, it has its own
		pass


	def OnActivateView(self, activate, activeView, deactiveView):
		if activate and self._diagramCtrl:
			# In MDI mode just calling set focus doesn't work and in SDI mode using CallAfter causes an endless loop
			if self.GetDocumentManager().GetFlags() & wx.lib.docview.DOC_SDI:
				self._diagramCtrl.SetFocus()
			else:
				def SetFocusToDiagramCtrl():
					if self._diagramCtrl:  # Need to make sure it is there in case we are in the closeall mode of the MDI window
						self._diagramCtrl.GetCanvas().SetFocus()
				wx.CallAfter(SetFocusToDiagramCtrl)


	def OnUpdate(self, sender = None, hint = None):
		if wx.lib.docview.View.OnUpdate(self, sender, hint):
			return
		print "UPDATE !!!"
		for module, geometrics in self.GetDocument().GetModuleGeometrics().items():
			module_shape = self.GetDiagramCtrl().get_module_shape(module)
			if module_shape:
				module_shape.SetGeometrics(geometrics)
			else:
				print "adding module shape"
				self.GetDiagramCtrl().add_module_shape(module, geometrics)

		for connection, geometrics in self.GetDocument().GetConnectionGeometrics().items():
			connection_shape = self.GetDiagramCtrl().get_connection_shape(connection)
			if connection_shape:
				connection_shape.SetGeometrics(geometrics)
				module_from = connection.output_port.module
				module_to = connection.input_port.module
				module_from_shape = self.GetDiagramCtrl().get_module_shape(module_from)
				module_to_shape = self.GetDiagramCtrl().get_module_shape(module_to)
				module_from_geometrics = self.GetDocument().GetModuleGeometrics()[module_from]
				module_to_geometrics = self.GetDocument().GetModuleGeometrics()[module_to]
				module_from_shape.SetGeometrics(module_from_geometrics)
				module_to_shape.SetGeometrics(module_to_geometrics)

			else:
				print "adding connection shape"
				self.GetDiagramCtrl().add_connection_shape(connection)

		self.GetDiagramCtrl().GetCanvas().Refresh()



	def OnClose(self, deleteWindow = True):
		if not wx.lib.docview.View.OnClose(self, deleteWindow):
			return False
		self.Activate(False)
		if deleteWindow and self.GetFrame():
			self.GetFrame().Destroy()
		return True


	# Since ProcessEvent is not virtual, we have to trap the relevant events using this pseudo-ProcessEvent instead of EVT_MENU
	def ProcessEvent(self, event):
		id = event.GetId()
		doc = self.GetDocument()
		if id == wx.ID_UNDO:
			if not self._diagramCtrl:
				return False
			doc.GetCommandProcessor().Undo()
			self.GetDiagramCtrl().GetCanvas().Refresh()
			return True
		elif id == wx.ID_REDO:
			if not self._diagramCtrl:
				return False
			doc.GetCommandProcessor().Redo()
			self.GetDiagramCtrl().GetCanvas().Refresh()
			return True
		elif id == wx.ID_CUT:
			if not self._diagramCtrl:
				return False
			self._diagramCtrl.Cut()
			return True
		elif id == wx.ID_COPY:
			if not self._diagramCtrl:
				return False
			self._diagramCtrl.Copy()
			return True
		elif id == wx.ID_PASTE:
			if not self._diagramCtrl:
				return False
			self._diagramCtrl.Paste()
			return True
		elif id == wx.ID_CLEAR:
			if not self._diagramCtrl:
				return False
			self._diagramCtrl.Replace(self._diagramCtrl.GetSelection()[0], self._diagramCtrl.GetSelection()[1], '')
			return True
		elif id == wx.ID_SELECTALL:
			if not self._diagramCtrl:
				return False
			self._diagramCtrl.SetSelection(-1, -1)
			return True
		else:
			return wx.lib.docview.View.ProcessEvent(self, event)


	def ProcessUpdateUIEvent(self, event):
		if not self._diagramCtrl:
			return False

		return wx.lib.docview.View.ProcessUpdateUIEvent(self, event)


	#----------------------------------------------------------------------------
	# Methods for DiagramDocument to call
	#----------------------------------------------------------------------------

	def GetDiagramCtrl(self):
		return self._diagramCtrl

	def move_module(self, module, mx, my):
		doc = self.GetDocument()
		move_command = MoveCommand(doc, module, mx, my)
		doc.GetCommandProcessor().Submit(move_command)

	def add_module(self, module_name, x, y):
		doc = self.GetDocument()
		add_module_command = AddModuleCommand(doc, module_name, x, y)
		doc.GetCommandProcessor().Submit(add_module_command)

	def new_connection(self, module_from, port_from, module_to, port_to):
		doc = self.GetDocument()
		new_connection_command = NewConnectionCommand(doc, module_from, port_from, module_to, port_to)
		doc.GetCommandProcessor().Submit(new_connection_command)



