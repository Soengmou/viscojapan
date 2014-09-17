import glob
import numpy as np

import h5py
from pylab import plt
from numpy import log10, amin, amax
import matplotlib

import viscojapan as vj


files  = glob.glob('../outs/seasd_01_nrough_*.h5')

model_ch = []
for file in sorted(files):
    with h5py.File(file, 'r') as fid:
        Bm = fid['Bm'][...]
        slip = Bm[:-3]
        slip_max = np.max(slip)
        if slip_max<50:
            model_ch.append(file)

nreses =[]
visMs = []
Hes = []
rakes = []
nroughs = []
 

for file in model_ch:
    with h5py.File(file,'r') as fid:
    #with h5py.File('outs/cno_%02d.h5'%ano,'r') as fid:
        nres = fid['residual_norm_weighted'][...]
        nreses.append(nres)

        m = fid['m'][...]
        visMs.append(m[-3])
        Hes.append(m[-2])
        rakes.append(m[-1])

        nrough = fid['regularization/roughening/norm'][...]
        nroughs.append(nrough)

x1 = amin(nreses)
x2 = amax(nreses)
dx = x2 - x1
xlim = (x1-dx*0.02, x2+dx*0.2)
xticks = range(int(x1), int(x2),5)

plt.subplot(411)    
plt.semilogx(nreses, visMs,'o')
plt.xlim(xlim)
plt.gca().set_xticks(xticks)
plt.axhline(18.8, color='red')
plt.grid('on')
plt.ylabel('log10(visM/(Pa.s))')

plt.subplot(412)    
plt.semilogx(nreses, Hes,'o')
plt.xlim(xlim)
plt.gca().set_xticks(xticks)
plt.axhline(40, color='red')
plt.grid('on')
plt.ylabel('He/km')

plt.subplot(413)    
plt.semilogx(nreses, rakes,'o')
plt.xlim(xlim)
plt.gca().set_xticks(xticks)
plt.axhline(83, color='red')
plt.ylabel('rake')
plt.grid('on')

plt.subplot(414)
vj.plot_L(nreses, nroughs)
plt.xlim(xlim)
plt.gca().set_xticks(xticks)
plt.gca().get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
plt.ylabel('roughening')
plt.xlabel('Residual Norm')
plt.grid('on')

plt.savefig('plots/nlin_par_curve_weighted.png')
plt.show()