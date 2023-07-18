########################################################################
# convert_inputs.py
#
# Script to convert a simple somatic mutation file (SSM) to a file
# that can be read by CALDER.
########################################################################
import sys, os, argparse
import numpy as np
from omicsdata.ssm import parse, supervariants, columns, constants

def extract_data(variants, keys):
	"""
	Extracts a set of key/value pairs from the variants dictionary

	Parameters
	-----------
	variants : dictionary 
		a dictionary where the keys are 'id' values for the supervariants and the values are 
		a dictionary containing the read count data for the variant
	keys : list
		a list of keys to extract ifrom the variants dictionary

	Returns 
	---------
	dict
		a dictionary containing all of the key/value pairs extracted from the variants dictionary
	"""
	vids = sorted(variants.keys(), key = lambda vid: int(vid[1:]))
	data = {constants.Variants_Keys.ID: vids}
	for k in keys:
		arr = np.array([variants[K][key] for K in vids])
		data[k] = arr

  return data

def write_calder_fmt(data, samples, calder_input_fn):
	"""
	Writes out a calder format (see https://github.com/raphael-group/calder/blob/master/CLL003_clustered.txt)
	
	Parameters
	-----------
	data : dict
		a dictionary containing the read count data
	samples : list
		a list of sample names
	calder_input_fn : str
		the name of the file to write the calder format to 

	Returns
	--------
	None
	"""
	assert (constants.Variants_Keys.VAR_READS in data) and (constants.Variants_Keys.REF_READS in data), \
			"Data are missing for converting to CALDER format"
	vids = data[constants.Variants_Keys.ID], 
	var_reads = data[constants.Variants_Keys.VAR_READS], 
	ref_reads = data[constants.Variants_Keys.REF_READS]
	N, S = var_reads.shape
	assert ref_reads.shape == var_reads.shape, "Reference reads array has incorrect shape"
	assert len(samples) == S, "Incorrect number of samples in data"
	assert len(vids) == N, "Incorrect number of variants"

	# write data to file
	with open(calder_input_fn, 'w') as f:

		# print header
		header = [vid for vid in vids for _ in range(2)]
		print(*header, sep="\t", file=f)

		# print 
		for s in range(S):
			row = [sampnames[s]]
			for i in range(N):
				for reads in (ref_reads, var_reads):
					row.append(str(reads[i,s]))
			print(*row, sep="\t", file=F)

def main():
	parser = argparse.ArgumentParser(
		description='Script to convert a simple somatic mutation file to a file that can be inputted to CALDER',
		formatter_class=argparse.ArgumentDefaultsHelpFormatter
	)

    parser.add_argument("ssm_fn", type=str, 
                        help="Path to a simple somatic mutation file (.ssm).")
    parser.add_argument("params_fn", type=str, 
                        help="Path to a parameter file (.params.json).")
	parser.add_argument('calder_input_fn', type=str,
						help="Path to write the CALDER input file to.")
	args = parser.parse_args()

	# grab data from input files
	variants = parse.load_ssm(ssm_fn)
	params = parse.load_params(params_fn)
	clusters = params[columns.PARAMS_Columns.CLUSTERS]
	samples = params[columns.PARAMS_Columns.SAMPLES]

	# extract necessary read count data
	supervars = supervariants.clusters_to_supervars(clusters, variants)
	data = extract_data(supervars, [constants.Variants_Keys.VAR_READS, constants.Variants_Keys.REF_READS])

	# write calder input file
	write_calder_fmt(data, samples, args.calder_input_fn)

if __name__ == '__main__':
	main()
