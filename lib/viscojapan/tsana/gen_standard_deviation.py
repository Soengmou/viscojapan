import shutil
from os.path import join, exists

import numpy as np

import viscojapan as vj

def copy_and_revise_sd_file(file_sd_original, file_seafloor_sd, file_sd_out, sd = None):
    assert not exists(file_sd_out)
    assert exists(file_sd_original)
    assert exists(file_seafloor_sd)
    shutil.copyfile(file_sd_original, file_sd_out)
    ep = vj.EpochalDisplacementSD(file_sd_out)
    seafloor = np.loadtxt(file_seafloor_sd, '4a,i, 3f')

    for ii in seafloor:
        site = ii[0].decode()
        day = ii[1]
        if sd is None:
            sd = ii[2]
        assert len(sd) == 3
        print(site, day, sd)

        ep.set_value_at_site(site, 'e', day, sd[0])
        ep.set_value_at_site(site, 'n', day, sd[1])
        ep.set_value_at_site(site, 'u', day, sd[2])

class GenSD(object):
    def __init__(self,
                 dir_linres,
                 sites,
                 days
                 ):
        self.dir_linres = dir_linres
        self.sites = sites
        self.num_sites = len(self.sites)
        self.days = days

    def _read_file_linres(self, site, cmpt):
        tp = np.loadtxt(
            join(self.dir_linres, '%s.%s.lres'%(site.decode(), cmpt)))
        t = tp[:,0]
        assert np.all(np.diff(t)) > 0
        sd = tp[:,3]
        return t, sd

    def _interp_standard_deviation(self, site, cmpt):        
        t_eq = 55631
        t, sd = self._read_file_linres(site, cmpt)       
        sd_interp = np.interp(self.days + t_eq, t, sd)
        return sd_interp

    def _gen_data_matrix(self):
        print('Generating data matrix ...')
        data = np.zeros([self.num_sites*3, len(self.days)])
        for nth, site in enumerate(self.sites):
            print(nth, site)
            for mth, cmpt in enumerate(['e', 'n', 'u']):
                sd = self._interp_standard_deviation(site, cmpt)
                data[nth*3+mth, :] = sd
        self.data = data

    def save(self, fn):
        self._gen_data_matrix()
        for day in self.days:
            ep = vj.EpochalData(fn)
            ep[int(day)] = self.data[:,(day,)]
        ep['sites'] = self.sites
        ep['max sd'] = np.amax(self.data)
        ep['min sd'] = np.amin(self.data)
        ep['mean sd'] = np.mean(self.data)
        ep['median sd'] = np.median(self.data)
