#!/usr/bin/env python3
from numpy import inf

import sys
sys.path.append('/home/zy/workspace/greens/lib/')
from greens.reform_pollitz_outputs2hdf5 import ReformPollitzOutputs2HDF5

reform = ReformPollitzOutputs2HDF5()

# intializing the object:
reform.days_of_epochs = range(0,1201,60)
reform.no_of_subfaults = 250
reform.pollitz_outputs_dir = 'outs/outs/'
reform.output_filename_hdf5 = 'G.h5'
reform.file_stations_in = './stations.in'
reform.He = 50
reform.visM = 2E19
reform.visK = inf
reform.lmax = 810

# go
reform()
