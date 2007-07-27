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
import logging

from commands import *
from dataflow_editor.ui.shape.diagram import DataflowDiagram
from dataflow_editor.ui.interactor.keyboard import KeyboardInteractor
from xml.dom.minidom import Document, parse

log = logging.getLogger("mapero.logger.mvc");

_ = wx.GetTranslation

class DataflowView(wx.lib.docview.View):

	#--- Overridden methods

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
        	self.keyword_interactor = KeyboardInteractor(doc, self)
		canvas = self._diagramCtrl.GetCanvas()
		wx.EVT_KEY_UP(canvas, self.keyword_interactor.on_event)
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
		log.debug( "updating view" )
		for module, geometrics in self.GetDocument().GetModuleGeometrics().items():
			module_shape = self.GetDiagramCtrl().get_module_shape(module)
			if module_shape:
				module_shape.SetGeometrics(geometrics)
			else:
				log.debug( "adding module shape for : %s", module.name )
				self.GetDiagramCtrl().add_module_shape(module, geometrics)
		for module_shape in self.GetDiagramCtrl().module_shapes:
			if (module_shape.module not in self.GetDocument().GetModuleGeometrics().keys()):
				log.debug("removing module shape for : %s", module_shape.module.name )
				self.GetDiagramCtrl().remove_module_shape(module_shape.module)
				

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


	#--- Methods for DiagramDocument to call

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



