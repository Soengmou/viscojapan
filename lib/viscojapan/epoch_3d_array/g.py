import numpy as np

__author__ = 'zy'
__all__ = ['G']

from .epoch_sites_3d_array import EpochSites3DArray

class G(EpochSites3DArray):
    def __init__(self,
                 g_3d,
                 epochs,
                 sites,
                 mask_sites):

        assert epochs[0] == 0, 'The class is designed to represent slip that starts at t=0.'

        assert len(sites)*3 == g_3d.shape[1]

        super().__init__(array_3d=g_3d, epochs=epochs, sites=sites, mask_sites=mask_sites)

        self._num_subflts = g_3d.shape[2]


    def get_num_subflts(self):
        return self._num_subflts

    def get_mask(self):
        ch = super().get_mask()
        ch1 = np.asarray(ch)*3
        ch2 = np.asarray([ch1, ch1+1, ch1+2]).T.flatten()
        return ch2

    @classmethod
    def load(cls,fid,
             mask_sites = None,
             memory_mode = False # if memory_mode is True, all the data will be loaded into memory.
    ):
        if memory_mode:
            array_3d = fid[cls.HDF5_DATASET_NAME_FOR_3D_ARRAY][...]
        else:
            array_3d = fid[cls.HDF5_DATASET_NAME_FOR_3D_ARRAY]

        epochs = fid['epochs'][...]
        sites = [site.decode() for site in fid['sites'][...]]

        return cls(g_3d = array_3d,
                   epochs = epochs,
                   sites = sites,
                   mask_sites=mask_sites)
