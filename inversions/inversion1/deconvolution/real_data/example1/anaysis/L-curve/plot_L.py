from pylab import show, legend, savefig
import h5py

from viscojapan.plots import plot_L

from alphas import alphas
from betas import betas

plot_L('../../outs_log/res_a??_b??.h5',
       'weighted_residual_norm', 'spatial_roughness',
       ls='None', marker='.', color='gray')


plot_L('../../outs_log/res_a??_b19.h5',
       'weighted_residual_norm', 'spatial_roughness',)

##for bno in 0, 10, 19:
##    with h5py.File('../../outs_log/res_a00_b%02d.h5'%bno) as fid:
##        alpha = fid['alpha'][...]
##        beta = fid['beta'][...]
##        
##    plot_L('../../outs_alpha_beta/res_a??_b%02d.h5'%bno,
##               'residual_norm', 'spatial_roughness',
##               ls='--', label='bno=%02d, beta=%f'%(bno,beta))
##ano = 16
##with h5py.File('../../outs_alpha_beta/res_a%02d_b00.h5'%ano) as fid:
##    alpha = fid['alpha'][...]
##plot_L('../../outs_alpha_beta/res_a%02d_b??.h5'%ano,
##       'residual_norm', 'spatial_roughness',
##       ls='-', label='ano=%02d, alpha=%f'%(ano,alpha), lw=4, color='red')

legend()
savefig('L-curve.png')
show()