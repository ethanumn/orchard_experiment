#!/bin/bash

###############################################################################################################
# folderize_data.sh
#
# Performs the following:
#   (1) For each unique .ssm file in some folder, create a folder with that basename and place
#       all files with a matching basename in the folder
#
###############################################################################################################

data_dir=""

if [ ! -z "$1" ]
  then
    data_dir=$1
fi

# iterate through each unique ssm file, create a folder with the base name of that ssm file
# then move all files into that folder
for fn in $data_dir/*.ssm; do 
    ssm=$(basename $fn | cut -d . -f 1)
    mkdir $data_dir/$ssm
    mkdir $data_dir/$ssm/truth 
    mv $data_dir/$ssm.* $data_dir/$ssm/truth
done