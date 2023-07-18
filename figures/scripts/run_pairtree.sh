#!/bin/bash

###############################################################################################################
# run_pairtree.sh
#
# Performs the following:
#   (1) Runs Pairtree on each folder in the provided directory $1, otherwise it defaults to $DATA_DIR 
#   (2) Converts the output from Pairtree to a format that can be compared to other reconstructions
#
###############################################################################################################


# initialize variable to /path/to/pairtree directory
PT_DIR=$ORCH_DIR/lib/pairtree
SCRIPTS_DIR=$ORCH_DIR/metrics/neutree

# initialize data directory
data_dir=$DATA_DIR

if [ ! -z "$1" ]
  then
    data_dir=$1
fi

##############################
# (1) Run Pairtree
##############################

for dir in $data_dir/* ; 
do
    
    runid=$(basename $dir | cut -d. -f1)
    ptdir=$dir/pairtree
    truthdir=$dir/truth
    resultsfn=$runid.results.npz

    mkdir $ptdir    
    
    time ( python3 $PT_DIR/bin/pairtree \
           --params $truthdir/$runid.params.json \
           --trees-per-chain=5000 \
           --parallel=8 \
           $truthdir/$runid.ssm \
           $ptdir/$runid.results.npz ) \
           2>> $ptdir/$runid.out 

done


##############################
# (2) Convert Outputs
##############################
for dir in $data_dir/* ; 
do
    
    runid=$(basename $dir | cut -d. -f1)
    
    ptdir=$dir/pairtree
    truthdir=$dir/truth 
    resultsfn=$runid.results.npz
    
    python3 $SCRIPTS_DIR/convert_outputs.py \
                        $ptdir/$resultsfn \
                        $ptdir/$runid.neutree.npz 

done


