from os.path import join

from numpy import logspace
from numpy.random import normal

from viscojapan.inversion import Deconvolution
from viscojapan.inversion.regularization import \
     TemporalRegularization, Roughening, Composite
from viscojapan.inversion.basis_function import BasisMatrix

from epochs_log import epochs as epochs_log
from alphas import alphas
from betas import betas

file_G = '../../../greens_function/G.h5'
file_d = 'cumu_post_with_seafloor.h5'
file_sd = 'sites_sd.h5'
file_sites_filter = 'sites_with_seafloor'

fault_file = '../../../fault_model/fault_He50km_east.h5'

basis = BasisMatrix.create_from_fault_file(fault_file)

def create_roughening_temporal_regularization(rough, temp):

    reg_rough = Roughening.create_from_fault_file(fault_file)
    reg_temp = TemporalRegularization.create_from_fault_file(fault_file, epochs_log)
    
    reg = Composite().\
          add_component(reg_rough, arg=rough, arg_name='roughening').\
          add_component(reg_temp, arg=temp, arg_name='temporal')
    
    return reg
    
inv = Deconvolution(
    file_G = file_G,
    file_d = file_d,
    file_sd = file_sd,
    file_sites_filter = file_sites_filter,
    epochs = epochs_log,
    regularization = None,
    basis = basis
    )
inv.set_data_except_L()

for ano, alpha in enumerate(alphas):
    for bno, beta in enumerate(betas):
        inv.regularization = \
            create_roughening_temporal_regularization(alpha, beta)
        inv.set_data_L()
        inv.run()
        inv.save('outs/ano_%02d_bno_%02d.h5'%(ano, bno), overwrite=True)
        
