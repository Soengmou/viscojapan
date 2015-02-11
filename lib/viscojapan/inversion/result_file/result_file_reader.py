from os.path import exists

import h5py

from ...file_io_base import FileIOBase
from ...slip import Slip
from ...displacement import Disp
from ...fault_model import FaultFileReader
from ...sites_db import SitesDB

__all__ = ['ResultFileReader']

class ResultFileReader(FileIOBase):
    def __init__(self, file_name):
        super().__init__(file_name)        


    def open(self):
        assert exists(self.file_name)
        return h5py.File(self.file_name,'r')

    @property
    def roughening_norm(self):
        return self.fid['regularization/roughening/norm'][...]

    @property
    def Bm(self):
        Bm = self.fid['Bm'][...]
        return Bm

    @property
    def m(self):
        m = self.fid['m'][...]
        return m

    @property
    def d_pred(self):
        m = self.fid['d_pred'][...]
        return m

    @property
    def d_obs(self):
        m = self.fid['d_obs'][...]
        return m

    @property
    def sites(self):
        m = self.fid['sites'][...]
        sites = [site.decode() for site in m]
        return SitesDB().gets(sites)

    @property
    def num_sites(self):
        return int(len(self.sites))

    @property
    def num_nlin_pars(self):
        return int(self.fid['nlin_pars/num_nlin_pars'][...])

    @property
    def incr_slip(self):
        if self.num_nlin_pars == 0:
            return self.Bm
        else:
            num_nlin_pars = self.num_nlin_pars
            if num_nlin_pars ==0:
                return self.Bm
            return self.Bm[:-num_nlin_pars]

    ####
    # Nonlinear parameters
    @property
    def nlin_pars(self):
        self.nlin_par_solved_values()

    @property
    def nlin_par_solved_values(self):
        if self.num_nlin_pars == 0:
            return []
        else:
            return self.fid['nlin_pars/nlin_par_solved_values'][...]

    @property
    def nlin_par_initial_values(self):
        if self.num_nlin_pars == 0:
            return []
        else:
            return self.fid['nlin_pars/nlin_par_initial_values'][...]

    @property
    def nlin_par_names(self):
        return list(self.fid['nlin_pars/nlin_par_names'][...])

    def get_nlin_par_solved_value(self, pn):
        idx = list(self.nlin_par_names).index(pn)
        return self.nlin_par_solved_values[idx]

    @property
    def log10_He_(self):
        return self.get_nlin_par_solved_value('log10(He)')

    @property
    def log10_visM_(self):
        return self.get_nlin_par_solved_value('log10(visM)')

    @property
    def rake(self):
        return self.get_nlin_par_solved_value('rake')

    ########

    @property
    def epochs(self):
        return [int(ii) for ii in self.fid['epochs'][...]]

    @property
    def num_epochs(self):
        return len(self.epochs)

    @property
    def residual_norm_weighted(self):
        return self.fid['misfit/norm_weighted'][...]

    @property
    def rms(self):
        return float(self.fid['misfit/rms'][...])

    @property
    def rms_inland(self):
        return float(self.fid['misfit/rms_inland'][...])

    @property
    def rms_inland_at_epoch(self):
        return self.fid['misfit/rms_inland_at_epoch'][...]

    def get_rms_at_sites(self,cmpt):
        return self.fid['misfit/at_sites/%s'%cmpt][...]   


    def get_slip(self,
                 fault_file = None,
                 num_subflt_along_strike = None,
                 num_subflt_along_dip = None,
    ):
        if fault_file is not None:
            reader = FaultFileReader(fault_file)
            num_subflt_along_strike = reader.num_subflt_along_strike
            num_subflt_along_dip = reader.num_subflt_along_dip

        nx = num_subflt_along_strike
        ny = num_subflt_along_dip

        slip = self.incr_slip
        slip = slip.reshape([self.num_epochs, ny, nx])

        return Slip(incr3d=slip,
             epochs=self.epochs)

    def get_pred_disp(self):
        return self._get_disp(self.d_pred)

    def get_obs_disp(self):
        return self._get_disp(self.d_obs)

    def _get_disp(self, disp_arr):
        disp3d = disp_arr.reshape([self.num_epochs, self.num_sites,3])
        return Disp(cumu_disp3d= disp3d,
                    epochs = self.epochs,
                    sites = self.sites)





    
        
