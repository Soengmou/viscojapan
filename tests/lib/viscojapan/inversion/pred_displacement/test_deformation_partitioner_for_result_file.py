__author__ = 'zy'

import unittest
from os.path import join

import viscojapan as vj

class Test_DeformPartitionerForResultFile(vj.test_utils.MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()

    def test1(self):
        res_file = join(self.share_dir, 'nrough_05_naslip_11.h5')
        res_reader = vj.inv.ResultFileReader(res_file)

        fault_file = join(self.share_dir, 'fault_bott80km.h5')


        pred = vj.inv.DeformPartitionerForResultFile(
            result_file = res_file,
            fault_file = fault_file,
            file_G0 = join(self.share_dir, 'G0_He50km_VisM6.3E18_Rake83.h5'),
            files_Gs = [join(self.share_dir, 'G1_He50km_VisM1.0E19_Rake83.h5'),
                        join(self.share_dir, 'G2_He60km_VisM6.3E18_Rake83.h5'),
                        join(self.share_dir, 'G3_He50km_VisM6.3E18_Rake90.h5')
                        ],
            file_incr_slip0 = join(self.share_dir, 'slip0.h5')
        )

        disp = pred.E_co()
        disp = pred.E_aslip(10)
        disp = pred.R_nth_epoch(3, 500)
        disp = pred.R_co(500)
        disp = pred.R_aslip(500)

        pred.save(join(self.outs_dir, 'partition_based_on_result_file.h5'))




if __name__ == '__main__':
    unittest.main()