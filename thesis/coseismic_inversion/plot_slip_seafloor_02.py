from os.path import join
from subprocess import check_call
import tempfile

import numpy as np

import pGMT
import viscojapan as vj

gmt = pGMT.GMT()
gmt.gmtset('ANNOT_FONT_SIZE_PRIMARY','9',
           'LABEL_FONT_SIZE','9',
           'FONT_ANNOT_PRIMARY','6',
           'MAP_FRAME_TYPE','plain')

gplt = pGMT.GMTPlot()

gplt.psbasemap(
    R = '140/145/35/41.5',       # region
    JB = '142.5/38.5/35/41.5/14c', # projection
    B = '2', U='18/25/0',
    P='',K='',
    )

vj.gmt.plot_etopo1(gplt, A='-80/10',
                   file_topo_cpt=vj.gmt.topo_cpts['afrikakarte'])


# plot slip
base_dir = '/home/zy/workspace/viscojapan/inversions/static_inversion/static_inversion2'
res_file = join(
    base_dir,
    'coseismic/run2_seafloor_01/outs/nrough_14_ntop_02.h5')
fault_file = join(
    base_dir,
    'fault_model/fault_bott60km.h5')
earth_file = join(
    base_dir,
    'earth_model_nongravity/He63km_VisM1.0E19/earth.model_He63km_VisM1.0E19')

plt_slip = vj.gmt.GMTInversionResultFileSlipPlotter(
    gplt,
    res_file,
    fault_file,
    earth_file,
    I='5k')
plt_slip.plot_slip()
plt_slip.plot_slip_contour(contours=[40,35,20,10,5])
plt_slip.plot_scale()
plt_slip.plot_legend()

# plot coast
gplt.pscoast(
    R = '', J = '',
    D = 'h', N = 'a/faint,150,-.',
    W = 'faint,50',A='1000',L='144.3/36/38/50+lkm+jt',
    O = '', K='')

vj.gmt.plot_seafloor_stations(gplt, marker_size=0.4)

# plot plate boundary
vj.gmt.plot_plate_boundary(gplt)
# plot focal mechanism
vj.gmt.plot_Tohoku_focal_mechanism(gplt,scale=0.4, K=None)

gplt.save('inverted_coseismic_slip_seafloor_02.pdf')

gplt.save_shell_script('shell.sh', output_file=' > out.ps')
