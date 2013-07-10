# Base parser for OONIProbix
# Heavily modified from the example_parser.py script in the OONIProbe repo

# TO-DO: Look at the request headers.  Why they couldn't have stored them as
# dictionaries is beyond me.  Displaying this is a separete problem, but much
# more of a pain now.  
from pprint import pprint
import yaml
import sys
print "Opening %s" % sys.argv[1]
f = open(sys.argv[1])
yamloo = yaml.safe_load_all(f)

report_header = yamloo.next()
for k in report_header:
	print k

def walk_dict(dictionary,tabs):
	ks = dictionary.keys()
	for k in ks:
		if type(dictionary[k]) is dict:
			print '\t' * tabs + k
			walk_dict(dictionary[k],tabs+1)
		elif type(dictionary[k]) is list:
			print '\t' * tabs + k
			walk_list(dictionary[k],tabs+1)
		else:
			print '\t' * tabs + k
		

def walk_list(lst,tabs):
	for l in lst:
		if type(l) is dict:
			walk_dict(l,tabs+1)
		elif type(l) is list:
			walk_list(l,tabs+1)
		else:
			pass

for report_entry in yamloo:
	ks = report_entry.keys()
	print '---'
	for k in ks:
		if type(report_entry[k]) is dict:
			print k
			walk_dict(report_entry[k],1)
		elif type(report_entry[k]) is list:
			print k
			walk_list(report_entry[k],1)
		else:
			print k

f.close()
