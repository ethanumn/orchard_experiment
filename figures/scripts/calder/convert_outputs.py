########################################################################
# convert_outputs.py
#
# Script to convert the tree data output by CALDER to a neutree file
# that can be used to evaluate the reconstruction.
########################################################################
import os, sys, argparse, re
import numpy as np
from omicsdata.ssm import parse, supervariants, columns

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "..", "metric"))

import neutree

# CONSTANTS
LABEL = "label"
EDGE = "edge"
EOF = "eof"
HEADER = "header"
FHAT = "Fhat"
dot_fields = {
  LABEL:  r'^(v\d+) \[label="([^"]+)"\];$',
  EDGE:   r'^([a-z0-9]+) -> ([a-z0-9]+);$',
  EOF:    r'^}$',
  HEADER: r'^digraph data_tree1 {$',
}

def read_next_matrix(f):
	"""
	Reads a CALDER solution file until it reaches a specification of one of the matrices CALDER outputs.
	Then it processes the matrix and returns it as a numpy array.

	Parameters
	-----------
	f : object
		an instance of a python file object

	Returns
	--------
	str 
		name of the matrix from the solution file
	list
		a list of column labels
	list 
		a list of row labels
	ndarray
		a 2D numpy array of the matrix data
	"""
	# read lines until we reach an entry in the file (U matrix or Fhat matrix)
	name = None
	while True:
		line = next(f).strip()
		if len(line) > 0:
			name = line
			data = []
			break

	# get columns for matrix
	column_labels = next(F).strip().split(',')
	row_labels = []
	while True:
		try:
			line = next(F).strip()
		except StopIteration:
			break
		if len(line) == 0:
			break
		row = line.split(',')
		row_labels.append(row[0]) # first entry of each row is the row label
		row_vals = np.array([float(V) for V in row[1:]]) # remaining data in row is matrix entries
		data.append(row_vals)

	assert name is not None and len(column_labels) > 0 and len(row_labels) > 0
	data = np.array(data)

	return (name, column_labels, row_labels, data.T)

def read_solution(calder_sol_fn):
	"""
	Reads a CALDER solution file one matrix at a time

	Parameters
	-----------
	calder_sol_fn : str
		the path to the CALDER solution file

	Returns
	--------
	dict
		a dictionary where the keys are the names of the matrices, and the values are the data matrices
	dict
		a dictionary where the keys are the names of the matrices, and the values the labels of the rows in a matrix
	dict
		a dictionary where the keys are the names of the matrices, and the values the labels of the columns in a matrix
	"""
	data = {}
	row_labels = {}
	column_labels = {}

	with open(calder_sol_fn) as f:
		while True:
			try:
				name, row_labels_, column_labels_, data_  = read_next_matrix(f)
			except StopIteration:
				break
			data[name] = data_
			row_labels[name] = row_labels_
			col_labels[name] = column_labels_
	return (mats, row_labels, column_labels)

def dot_to_struct(svids, calder_dot_fn):
	"""
	Translates the data from a CALDER dot file to a parents vector aka struct

	Parameters
	-----------
	svids : list
		a list of supervariant 'id' values
	calder_dot_fn : str
		the path to the CALDER dot file

	Returns
	--------
	ndarray
		a parents vector aka struct
	"""

	label_map = {} # vertex label to supervariant 'id' map
	edges = []

	with open(calder_dot_fn) as f:
    	for line in f.readlines():
      		line = line.strip()

      		for field, pattern in dot_fields.items():
        		R = re.search(pattern, line)
        		if R:
          			break
			if field == HEADER:
				continue
			elif field == LABEL:
				label_map[R.group(1)] = R.group(2)
			elif field == EDGE:
				edges.append((R.group(1), R.group(2)))
			elif field == EOF:
				break
			else:
				raise Exception('Unknown line_type %s' % line_type)

  parents_dict = {label_map[v]: label_map[u] for (u,b) in edges}
  struct = np.array([vids.index(parents_dict[child]) for child in parents_dict.keys()])
  assert len(struct) == len(vids) - 1, 
  return struct

def calder_to_neutree(params, neutree_fn):
	"""
	Translates a set of CALDER output files into a Neutree file

	Parameters
	-----------
	params : dict
		the keys/values of a .params.json file loaded into a python dictionary
	neutree_fn : str
		the path to the neutree file to save the translated tree data

	Returns
	--------
	None
	"""
	mats, row_headers = read_solution(calder_mats_fn)
	svids = row_labels[FHAT][1:] # supervariant ids are 

	struct = dot_to_struct(svids, calder_trees_fn)
	ntree = neutree.Neutree(
		structs = [struct],
		phis = [mats[FHAT]],
		counts = np.array([1]),
		logscores = np.array([0.]),
		clusterings = [params[columns.PARAMS_Columns.CLUSTERS]],
		garbage = params[columns.PARAMS_Columns.GARBAGE],
	)
	neutree.save(ntree, neutree_fn)

def main():
  parser = argparse.ArgumentParser(
    description="Script for converting CALDER's reconstruction files to a Neutree file.",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
  )
  parser.add_argument("params_fn", type=str, 
                      help="Path to a parameter file (.params.json).")
  parser.add_argument("calder_sol_fn", type=str,
                      help="Path to the calder solution csv file.")
  parser.add_argument("calder_dot_fn", type=str,
                      help="Path to the calder tree structure file (.dot)")
  parser.add_argument("neutree_fn", type=str, 
                      help="Path for the neutree file to be written to containing the data for the CALDER tree")
  args = parser.parse_args()

  params = parse.load_params(args.params_fn)
  calder_to_neutree(params, args.calder_mats_fn, args.calder_trees_fn, args.neutree_fn)

if __name__ == '__main__':
  main()
