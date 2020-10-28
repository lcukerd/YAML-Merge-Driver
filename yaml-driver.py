#!/usr/bin/python

# Changes in sheet number and name will not be merged
# Copy style of header

import yaml
import sys

conflicts = [];
changed = [];

def open_files(paths):
	files = [];
	for path in paths:
		file = open(path)
		file = yaml.load(file, Loader=yaml.FullLoader)
		files.append(file)
	return files

def correct_ele(ours, base, theirs):
	if ours == base:
		return theirs
	elif theirs == base:
		return ours
	elif ours == theirs:
		return ours
	else:
		return -1

def read_files(ours, base, theirs):
	out = []
	for i in range(len(base)):
		ele = correct_ele(ours[i], base[i], theirs[i])
		
		if (ele == -1):
			conflicts.append((i, ours[i]))
		else:
			out.append(ele)

	for i in range(len(base), len(theirs)):
		out.append(theirs[i])

	for i in range(len(base), len(ours)):
		ele = ours[i]
		changed.append((ele['Row'], len(out) + 1))
		ele['Row'] = len(out) + 1
		out.append(ele)

	return out;



def write_file(out, path):
	if (len(conflicts) == 0):
		print ('Custom Merging files')
		yaml_out = yaml.dump(out, sort_keys = False)
		yaml_out = yaml_out.replace('-','\n-').splitlines(True)

		with open(path, 'w') as file:
			file.writelines(yaml_out[1:])

		print ('Below were moved:')
		for change in changed:
			print ('{} -> {}'.format(change[0], change[1]))
		sys.exit(0)
	else:
		print ("Conflicts below, please merge manually")
		for conflict in conflicts:
			print ('Conflict at row: {} for {}'.format(conflict[0], conflict[1]))
			sys.exit(1)


files = open_files(sys.argv[1:])
out = read_files(files[0], files[1], files[2])
write_file(out, sys.argv[1])
