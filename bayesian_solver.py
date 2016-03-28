import json
import csv
from libpgm.nodedata import NodeData
from libpgm.graphskeleton import GraphSkeleton
from libpgm.discretebayesiannetwork import DiscreteBayesianNetwork

from os import listdir

files = listdir("bayes_net/")

truth_r = csv.reader(open("dataset/truth.dat","rb"), delimiter='\t')
data_r = open("dataset/data.dat","rb")


data_l = []
for line in data_r.readlines():
	data_l.append(map(int, line.split()))

truth_l = []
for row in truth_r:
	truth_l.append(row[0])

fout = open("bayesian_outcome.txt", "wb")

for  i in range(104):
	nd = NodeData()
	skel = GraphSkeleton()
	nd.load('bayes_net/'+str(i)+".txt")    # any input file
	skel.load('bayes_net/'+str(i)+".txt")

	# topologically order graphskeleton
	skel.toporder()

	# load bayesian network
	# load bayesian network
	bn = DiscreteBayesianNetwork(skel, nd)

	#print bn.E,bn.V
	bn.dictload('bayes_net/0.txt')


	dic1 = {}
	k = 1
	for c in data_l[i]:
		dic1[str(k)] = str(c)
		k += 2

	dic2 = {}
	k = 0
	for c in truth_l[i]:
		dic2[str(k)] = [c]
		k += 2

	#print dic2, dic1
	fout.write(str(bn.specificquery(dic2,dic1))+"\n")

fout.close()
