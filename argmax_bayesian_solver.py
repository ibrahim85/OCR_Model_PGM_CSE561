import json
import csv
import itertools
from libpgm.nodedata import NodeData
from libpgm.graphskeleton import GraphSkeleton
from libpgm.discretebayesiannetwork import DiscreteBayesianNetwork
from copy import deepcopy
from os import listdir

files = listdir("bayes_net/")

CHARS = ['d', 'o', 'i', 'r', 'a', 'h', 't', 'n', 's', 'e']
truth_r = csv.reader(open("dataset/truth.dat","rb"), delimiter='\t')
data_r = open("dataset/data.dat","rb")


data_l = []
for line in data_r.readlines():
	data_l.append(map(int, line.split()))

truth_l = []
for row in truth_r:
	truth_l.append(row[0])

w = csv.writer(open("bayesian_outcome.txt", "wb"))

count = 0

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
	dic1 = {}
	k = 1
	for c in data_l[i]:
		dic1[str(k)] = str(c)
		k += 2
	
	print dic1
	k = 2 * len(data_l[i]) - 2
	dic2 = {}
	word = ''
	while k >= 0:
		maxx = 0
		char = ''
		temp = deepcopy(dic2)
		for c in CHARS:
			temp[str(k)] = [c]
			curr = bn.specificquery(temp, dic1)
			if curr > maxx:
				maxx = curr
				dic2[str(k)] = [c]
				char = c
		word = char + word
		k -= 2

	if word == truth_l[i]:
		count += 1	


	w.writerow([word, maxx])

print count