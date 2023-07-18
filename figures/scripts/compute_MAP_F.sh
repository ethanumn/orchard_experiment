#!/bin/bash

###############################################################################################################
# convert_real_data_to_npz.sh
#
# Converts the structures listed in the .hbstruct file to an equivalent .npz file for comparison.
#
###############################################################################################################

# initialize variable for /path/to/pairtree/comparison directory 
PT_CMP_DIR=$ORCH_DIR/lib/pairtree/comparison
PT_DIR=$ORCH_DIR/lib/pairtree

# initialize data directory
data_dir=$DATA_DIR

if [ ! -z "$1" ]
  then
    data_dir=$1
fi

####################################
# (1) Compute rels for ground truth
####################################
for dir in $data_dir/* ; do
    
    runid=$(basename $dir | cut -d. -f1)
    
    truthdir=$dir/truth
    resultsfn=$runid.results.npz

    python3 $PT_DIR/bin/pairtree                          \
           --params $truthdir/$runid.hbstruct.params.json \
           --parallel=32                                  \
           --phi-fitter=rprop                             \
           --phi-iterations=30000                         \
           $truthdir/$runid.ssm                           \
           $truthdir/$runid.results.npz                      \

    
    # make neutree file
    python3 $ORCH_DIR/metrics/neutree/convert_outputs.py \
                        $truthdir/$resultsfn         \
                        $truthdir/$runid.neutree.npz  

done