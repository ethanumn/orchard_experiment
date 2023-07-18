#!/bin/bash

###############################################################################################################
# run_calder.sh
#
# Performs the following:
#   (1) Converts the inputs from .ssm and .params to a .txt file that CALDER can use
#   (2) Runs CALDER on each folder in the provided directory $1, otherwise it defaults to $DATA_DIR 
#   (3) Converts the output from CALDER to a format that can be compared to other reconstructions
#
###############################################################################################################


# initialize variable to /path/to/calder directory
CALDER_DIR=$ORCH_DIR/lib/calder

# initialize variable to CALDER i/o scripts
CALDER_SCRIPTS=$ORCH_DIR/figures/scripts/calder

# initialize data directory
data_dir=$DATA_DIR

if [ ! -z "$1" ]
  then
    data_dir=$1
fi

##############################
# (1) Convert inputs 
##############################
for dir in $data_dir/* ; 
do
    
    runid=$(basename $dir | cut -d. -f1)
    calderdir=$dir/calder
    truthdir=$dir/truth

    mkdir $calderdir
    
    resultsfn=$runid.results.npz
    
    python3 $CALDER_SCRIPTS/convert_inputs.py \
                          $truthdir/$runid.ssm \
                          $truthdir/$runid.params.json \
                          $calderdir/data.csv

done


##############################
# (2) Run CALDER
##############################
for dir in $data_dir/* ; 
do
    
    runid=$(basename $dir | cut -d. -f1)
    calderdir=$dir/calder
    truthdir=$dir/truth
        
    time ( java -jar $CALDER_DIR/calder.jar -i $calderdir/data.csv -o $calderdir/output -N ) 2>> $calderdir/$runid.out 

done


##############################
# (3) Convert Outputs
##############################
for dir in $data_dir/* ; 
do
    
    runid=$(basename $dir | cut -d. -f1)
    calderdir=$dir/calder
    truthdir=$dir/truth 
    resultsfn=$runid.neutree.npz
    
    python3 $CALDER_SCRIPTS/convert_outputs.py \
                        $truthdir/$runid.params.json \
                        $calderdir/output/data_soln1.csv \
                        $calderdir/output/data_tree1.dot \
                        $calderdir/$resultsfn

done


