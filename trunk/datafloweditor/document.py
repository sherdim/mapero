import wx
from mapero.core.module_manager import ModuleManager
from xml.dom.minidom import Document, parse



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
#        self._connection_geometrics.

    def move_module(self, module, mx, my):
        geometric = self.GetModuleGeometrics()[module]
        geometric.x += mx
        geometric.y += my
        print "moved module: ", module.name, " (", mx, " , ", my, ")"

    def remove_module(self, module):
        self._module_manager.remove(module)
        del self._module_geometrics[module]
