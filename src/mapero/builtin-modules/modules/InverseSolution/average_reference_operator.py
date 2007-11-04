from mapero.core.module import Module
from mapero.core.port import OutputPort, InputPort
from numpy.oldnumeric.precision import Float, Int
from enthought.traits import api as traits
from numpy import array, resize

module_info = {'name': 'InverseSolution.average_reference_operator',
                'desc': ""}

class registration_metadata(traits.HasTraits):
    fm = traits.Float
    channels = traits.List(traits.Str)

class average_reference_operator(Module):
    """ average reference operator """

    def __init__(self, **traitsv):
        super(average_reference_operator, self).__init__(**traitsv)
        self.name = 'Avg Ref Op'

        registration_values_trait = traits.Array(typecode=Float, shape=(None,None))
        self.ip_registration_values = InputPort(
                                                data_type = registration_values_trait,
                                                name = 'registration values',
                                                module = self
                                                )
        self.input_ports.append(self.ip_registration_values)
        self.i_registration_values = None

        electrode_names_trait =  traits.List(traits.Str)
        self.ip_registration_electrode_names = InputPort(
                                                         data_type = electrode_names_trait,
                                                         name = 'reg electrode names',
                                                         module = self
                                                         )
        self.input_ports.append(self.ip_registration_electrode_names)
        self.i_registration_electrode_names = None

        lead_field_trait = traits.Array(typecode=Float, shape=(None,None))
        self.ip_lead_field = InputPort(
                                       data_type = lead_field_trait,
                                       name = 'lead field',
                                       module = self
                                       )
        self.input_ports.append(self.ip_lead_field)
        self.i_lead_field = None

        self.ip_lead_field_electrode_names = InputPort(
                                                       data_type = electrode_names_trait,
                                                       name = 'lead field electrode names',
                                                       module = self
                                                       )
        self.input_ports.append(self.ip_lead_field_electrode_names)
        self.i_lead_field_electrode_names = None

        self.op_registration_values_avg = OutputPort(
                                                     data_type = registration_values_trait,
                                                     name = 'registration values avg',
                                                     module = self
                                                     )
        self.output_ports.append(self.op_registration_values_avg)

        registration_metadata_trait = traits.Trait()
        self.op_registration_metadata = OutputPort(
                                                   data_type = registration_metadata_trait,
                                                   name = 'registration metadata',
                                                   module = self
                                                   )
        self.output_ports.append(self.op_registration_metadata)

        self.op_lead_field_avg = OutputPort(
                                            data_type = lead_field_trait,
                                            name = 'lead field avg',
                                            module = self
                                            )
        self.output_ports.append(self.op_lead_field_avg)

    def update(self, input_port, old, new):
        if input_port == self.ip_registration_values:
            self.i_registration_values = input_port.data
        if input_port == self.ip_lead_field:
            self.i_lead_field = input_port.data
        if input_port == self.ip_registration_electrode_names:
            self.i_registration_electrode_names = input_port.data
        if input_port == self.ip_lead_field_electrode_names:
            self.i_lead_field_electrode_names = input_port.data
        if (self.i_registration_values != None)  \
            and ( self.i_lead_field != None) \
            and (self.i_registration_electrode_names != None) \
            and (self.i_lead_field_electrode_names != None):
            self.process()

    def _process(self):
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










