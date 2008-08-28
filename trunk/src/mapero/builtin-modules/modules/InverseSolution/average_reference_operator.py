from mapero.core.api import Module
from mapero.core.api import OutputPort, InputPort
from enthought.traits.api import Array, List, Str, Any, HasTraits, Float
from numpy import array, resize

class registration_metadata(HasTraits):
    fm = Float
    channels = List(Str)

class average_reference_operator(Module):
    """ average reference operator """

    label = 'Avg Ref Op'
    
    ### Input Ports
    ip_registration_values = InputPort( trait = Array(typecode=float, shape=(None,None)) )
    ip_registration_electrode_names = InputPort( trait = List(Str) )
    ip_lead_field = InputPort( trait = Array(typecode=float, shape=(None,None)) )
    ip_lead_field_electrode_names = InputPort( trait = List(Str) )
    
    ### Output Ports
    op_registration_values_avg = OutputPort( trait = Array(typecode=float, shape=(None,None)) )
    op_registration_metadata = OutputPort( trait = Any );
    op_lead_field_avg = OutputPort( trait = Array(typecode=Float, shape=(None,None)))                                            

    def start_module(self):

        self.i_registration_values = None
        self.i_registration_electrode_names = None
        self.i_lead_field = None
        self.i_lead_field_electrode_names = None

    def execute(self):
        self.i_registration_values = self.ip_registration_values.data
        self.i_lead_field = self.ip_lead_field.data
        self.i_registration_electrode_names = self.ip_registration_electrode_names.data
        self.i_lead_field_electrode_names = self.ip_lead_field_electrode_names.data
        if (self.i_registration_values != None)  \
            and ( self.i_lead_field != None) \
            and (self.i_registration_electrode_names != None) \
            and (self.i_lead_field_electrode_names != None):
            self.process()

    def process(self):
        self.progress = 0
        i_registration_values = self.i_registration_values
        i_lead_field = self.i_lead_field
        i_registration_electrode_names = self.i_registration_electrode_names
        i_lead_field_electrode_names = self.i_lead_field_electrode_names

        i_reg_cols = i_registration_values.shape[1]
        i_lead_cols = i_lead_field.shape[1]
        o_registration_values_avg = array(())
        o_lead_field_avg = array(())
        o_registration_metadata = registration_metadata()
        
        row_counter = 0
        reg_row_counter = 0
        for reg_name in i_registration_electrode_names:
            lead_row_counter = 0
            for lead_name in i_lead_field_electrode_names:
                if reg_name == lead_name:
                    o_registration_values_avg = resize(o_registration_values_avg, (row_counter+1, i_reg_cols))
                    o_lead_field_avg = resize(o_lead_field_avg, (row_counter+1, i_lead_cols))
                    o_registration_values_avg[row_counter] = i_registration_values[reg_row_counter]
                    o_lead_field_avg[row_counter] = i_lead_field[lead_row_counter]
                    o_registration_metadata.channels.append(reg_name)
                    row_counter += 1
                lead_row_counter += 1
            reg_row_counter += 1


        o_registration_values_avg = \
            o_registration_values_avg - o_registration_values_avg.mean(0)

        o_lead_field_avg = \
            o_lead_field_avg - o_lead_field_avg.mean(0)


        self.op_registration_values_avg.data = o_registration_values_avg
        self.op_lead_field_avg.data = o_lead_field_avg
        self.progress = 100










