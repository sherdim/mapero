from mapero.core.module import Module
from mapero.core.port import OutputPort, InputPort
from mapero.dataflow_editor.decorators.thread import threaded_process
from numpy.oldnumeric.precision import Float, Int
from enthought.traits.api import Array, Enum
from enthought.traits.ui.api import Group

import numpy
from numpy import matrix, array, power
from scipy.linalg import pinv
from scipy import square, identity, reshape, sparse

module_info = {'name': 'InverseSolution.inverse_solution',
                    'desc': ""}

class inverse_solution(Module):
    """ inverse solution """

    method = Enum( "WMN", "MN", "LORETA")

    view = Group('method')

    def __init__(self, **traits):
        super(inverse_solution, self).__init__(**traits)
        self.name = 'Inverse Solution'

        lead_field_trait = Array(typecode=Float, shape=(None,None))
        self.ip_lead_field_avg = InputPort(
                                           data_type = lead_field_trait,
                                           name = 'lead field avg',
                                           module = self
                                           )
        self.input_ports.append(self.ip_lead_field_avg)
        self.i_lead_field_avg = None

        inverse_solution_trait = Array(typecode=Float, shape=(None,None))
        self.op_inverse_solution = OutputPort(
                                              data_type = inverse_solution_trait,
                                              name = 'inverse solution',
                                              module = self
                                              )
        self.output_ports.append(self.op_inverse_solution)


    def update(self, input_port, old, new):
        if input_port == self.ip_lead_field_avg:
            self.i_lead_field_avg = input_port.data
        if (self.i_lead_field_avg != None):
            self.process()
            


    @threaded_process
    def process(self):
	self.progress = 0
        def calqomega_x_i(K):
            sum = K.sum(0)
            sum2 = array(square(sum))
            sum22 = reshape(sum2 ,[sum2.shape[1]])
            sum3 = sparse.lil_matrix((sum22.shape[0], sum22.shape[0]))
            sum3.setdiag(sum22)
            omega_x_i = sparse.csc_matrix(sum3)
            return omega_x_i

        def getKW(K):
            KW = matrix(K, numpy.float64)
            if self.method == "WMN":
                sum = power(KW,2).sum(0)
                print "max sum : " ,  sum.max()
                print "min sum : " ,  sum.min()
                sum[sum==0.0]=1

                for r in range(K.shape[0]):
                    KW[r] = K[r]/sum
            return KW

        def getM1xM2t(M1, M2=None):
            if M2  == None:
                m2 = M1
            else:
                m2 = M2
            return M1*m2.T

        K =  matrix(self.i_lead_field_avg)
        method = self.method

        KW = getKW(K)
        print "KW.shape: ", KW.shape
        self.progress = 20

        KWKt = getM1xM2t(KW, K)
        print "KWKt.shape: ", KWKt.shape
        self.progress = 40

        KWKt_inv = pinv(KWKt)
        print "KWKt_inv.shape: ", KWKt_inv.shape
        self.progress = 80

        T = KW.T * KWKt_inv
        print "T.shape: ",T.shape

        self.progress = 100
        self.op_inverse_solution.data = T


    def _method_changed(self):
        if (self.i_lead_field_avg != None):
            self.process()
