import h5py
from numpy import median 
import scipy.sparse as sparse

from .least_square import LeastSquare
from ..utils import delete_if_exists

class Inversion(object):
    def __init__(self,
                 regularization = None,
                 basis = None,
                 ):
        self.regularization = regularization
        self.basis = basis

    def set_data_sd(self):
        raise NotImplementedError()
        
    def set_data_W(self):
        _sd = self.sd / median(self.sd)
        self.W = sparse.diags(1./_sd.flatten(), offsets=0)        

    def set_data_G(self):
        raise NotImplementedError()

    def set_data_d(self):
        raise NotImplementedError()

    def set_data_B(self):
        self.B = self.basis()

    def set_data_L(self):
        self.L = self.regularization()

    def set_data_all(self):
        self.set_data_sd()
        self.set_data_W()
        self.set_data_G()
        self.set_data_d()
        self.set_data_B()        
        self.set_data_L()

    def set_data_except_L(self):
        self.set_data_sd()
        self.set_data_W()
        self.set_data_G()
        self.set_data_d()
        self.set_data_B()

    def invert(self):        
        self.least_square = LeastSquare(
            G = self.G,
            d = self.d,
            L = self.L,
            W = self.W,
            B = self.B,
            )

        self.least_square.invert()

    def predict(self):
        self.least_square.predict()

    def run(self):
        self.invert()
        self.predict()

    def save(self, fn, overwrite = False):
        if overwrite:
            delete_if_exists(fn)
        ls = self.least_square
        with h5py.File(fn) as fid:
            fid['m'] = ls.m
            fid['Bm'] = ls.Bm
            fid['d_pred'] = ls.d_pred
            fid['residual_norm'] = ls.get_residual_norm()
            fid['residual_norm_weighted'] = ls.get_residual_norm_weighted()

            for par, name in zip(self.regularization.args,
                                 self.regularization.arg_names):
                fid['regularization/%s/coef'%name] = par
                
            for nsol, name in zip(self.regularization.components_solution_norms(ls.Bm),
                                  self.regularization.arg_names):
                fid['regularization/%s/norm'%name] = nsol

    

        

        