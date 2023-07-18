#!/bin/bash

###############################################################################################################
# sim_to_neutree.sh
#
# Unpacks the ground-truth simulated data from a Pearsim (https://github.com/morrislab/pearsim) simulated 
# data file. This may take a long time if the folder passed in contains many datasets.
#
###############################################################################################################

# initialize data directory
data_dir=$DATA_DIR

if [ ! -z "$1" ]
  then
    data_dir=$1
fi

####################################
# (1) Unpack pickle data
####################################
for dir in $data_dir/* ; do

    runid=$(basename $dir | cut -d. -f1)
    picklefn=$dir/truth/$runid.truth.pickle
    neutreefn=$dir/truth/$runid.neutree.npz

    python3 $ORCH_DIR/metrics/neutree/sim_to_neutree.py $picklefn $neutreefn
        
done