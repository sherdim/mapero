from wx.lib import docview
from mapero.dataflow_editor.mvc.controller import DataflowEditorController
import logging
#import xml_state_pickler as state_pickler
from enthought.persistence import state_pickler as state_pickler


log = logging.getLogger("mapero.logger.mvc");

class DataflowDocument(docview.Document):
    
    def __init__(self):
        log.debug( "creating document" )
        
        super(DataflowDocument,self).__init__(self)
        self._inModify = False
        self.controller = DataflowEditorController(document=self)
    

    def SaveObject(self, fileObject):
        dataflow_editor_model = self.controller.dataflow_editor_model
        state_pickler.dump(dataflow_editor_model, fileObject)
#        doc = Document();
#        diagram = doc.createElement("diagram")
#        doc.appendChild(diagram)
#        module_id = 0
#        module_id_dict = {}
#        for module, geometric in self._module_geometrics.items():
#            xml = XMLStatePickler().dumps(module)
#            print xml
#
#            
#            module_id += 1
#            module_element = doc.createElement("module")
#            module_element.setAttribute("id", str(module_id))
#            module_info_element = doc.createElement("module_info")
#            module_element.appendChild(module_info_element)
#            module_id_dict[module] = module_id
#
#            geometric_element = doc.createElement("geometric");
#            geometric_element.setAttribute("h", str(geometric.GetHeight()));
#            geometric_element.setAttribute("w", str(geometric.GetWidth()));
#            geometric_element.setAttribute("y", str(geometric.GetY()));
#            geometric_element.setAttribute("x", str(geometric.GetX()));
#            module_element.appendChild(geometric_element)
#
#            diagram.appendChild(module_element)
#
#        for connection, geometric in self._connection_geometrics.items():
#            connection_element = doc.createElement("connection")
#            output_port_element = doc.createElement("output_port")
#            output_port_element.setAttribute("name", connection.output_port.name)
#            output_port_element.setAttribute("module_id", str(module_id_dict[connection.output_port.module]))
#            connection_element.appendChild(output_port_element)
#            diagram.appendChild(connection_element)
#
#            input_port = doc.createElement("input_port")
#            input_port.setAttribute("name", connection.input_port.name)
#            input_port.setAttribute("module_id", str(module_id_dict[connection.input_port.module]))
#            connection_element.appendChild(input_port)
#            diagram.appendChild(connection_element)
#        doc.writexml(fileObject, "",  "\t", "\n")
        return True


    def LoadObject(self, fileObject):
        state = state_pickler.load_state(fileObject)
        self.controller.create_dataflow_model(state)
#        doc = parse(fileObject)
#        module_id_dict = {}
#        for module_element in doc.getElementsByTagName("module"):
#            id = int(module_element.getAttribute("id"))
#            for module_info_element in module_element.getElementsByTagName("module_info"):
#                module_name = module_info_element.getAttribute("name")
#            for geometric_element in module_element.getElementsByTagName("geometric"):
#                h = int(geometric_element.getAttribute("h"))
#                w = int(geometric_element.getAttribute("w"))
#                x = float(geometric_element.getAttribute("x"))
#                y = float(geometric_element.getAttribute("y"))
#
#            module = self.add_module(module_name, x, y, w, h)
#            module_id_dict[id] = module
#
#        for connection_element in doc.getElementsByTagName("connection"):
#            for output_port_element in connection_element.getElementsByTagName("output_port"):
#                output_port_name = str(output_port_element.getAttribute("name"))
#                module_from = module_id_dict[int(output_port_element.getAttribute("module_id"))]
#            for input_port_element in connection_element.getElementsByTagName("input_port"):
#                input_port_name = str(input_port_element.getAttribute("name"))
#                module_to = module_id_dict[int(input_port_element.getAttribute("module_id"))]
#            self.add_connection(module_from, output_port_name, module_to, input_port_name)

        return True

        

