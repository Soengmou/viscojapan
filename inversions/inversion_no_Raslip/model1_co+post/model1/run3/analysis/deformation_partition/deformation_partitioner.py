import viscojapan as vj

result_file = '../../outs/best_result.h5'

partitioner = vj.inv.gen_deformation_partitioner_no_Raslip_for_result_fiel(
    file_G0 = '../../../green_function/G0_He50km_VisM6.3E18_Rake83.h5',
    result_file = result_file,
    files_Gs = ['../../../green_function/G1_He50km_VisM1.0E19_Rake83.h5',
                '../../../green_function/G2_He60km_VisM6.3E18_Rake83.h5',
                '../../../green_function/G3_He50km_VisM6.3E18_Rake90.h5'
                ],
    file_slip0 = '../../slip0/slip0.h5',
    )
partitioner.save('deformation_partition.h5')


    
