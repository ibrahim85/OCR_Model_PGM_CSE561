import csv
import itertools
from math import log
from os import listdir
import pprint
import json

pp = pprint.PrettyPrinter(indent=4)

CHARS = ['d', 'o', 'i', 'r', 'a', 'h', 't', 'n', 's', 'e']
ocr_r = csv.reader(open("dataset/ocr.dat","rb"), delimiter='\t')
truth_r = csv.reader(open("dataset/truth.dat","rb"), delimiter='\t')
trans_r = csv.reader(open("dataset/trans.dat","rb"), delimiter='\t')

data_r = open("dataset/data.dat","rb")

data_l = []
for line in data_r.readlines():
	data_l.append(map(int, line.split()))

ocr_d = {}
temp = {}
i = 1

for row in ocr_r:
	#print row
	temp[row[1]] = float(row[2])
	if i % 10 == 0:
		temp[row[1]] = float(row[2])
		ocr_d[int(row[0])] = temp
		temp = {}
	i += 1

trans_d = {}
for row in trans_r:
	if row[0] not in trans_d:
		trans_d[row[0]] = {row[1]:float(row[2])}
	else:
		trans_d[row[0]][row[1]] = float(row[2])

truth_l = []
for row in truth_r:
	truth_l.append(row[0])


out = {}
for d in range(len(data_l)):
	out["V"] = ['i' + str(i) for i in range(len(data_l[d]))] + ['c' + str(i) for i in range(len(data_l[d]))]
	temp = []
	for i in range(len(data_l[d])):
		temp.append(['i' + str(i), 'c' + str(i)])

	for i in range(len(data_l[d])-1):
		temp.append(['c' + str(i), 'c' + str(i+1)])

	out["E"] = temp

	temp = {}

	for i in range(len(out["V"])):
		t = {"ord" : i}
		if i % 2 == 0:
			t["numoutcomes"] = 2
			t["vals"] = CHARS
			t["parents"] = None
			t["children"] = ["c" + str(i/2)]
			cprob = {}
			for c in CHARS:
				cprob[str([c])] = [ocr_d[data_l[d][i/2]][c], 1-ocr_d[data_l[d][i%2]][c]]
			t["cprob"] = cprob
		else:
			t["numoutcomes"] = 2
			t["vals"] = CHARS
			if i == 1:
				t["parents"] = ["i" + str(i/2)]
				cprob = {}
				for c in CHARS:
					cprob[str([c])] = [ocr_d[data_l[d][i/2]][c], 1-ocr_d[data_l[d][i%2]][c]]
				t["cprob"] = cprob
			else:
				t["parents"] = ["i" + str(i/2), "c" + str(i/2-1)]
				cprob = {}
				for k in trans_d.keys():
					for c in CHARS:
						cprob[str([k,c])] = [trans_d[k][c] * ocr_d[data_l[d][i/2]][c],1-trans_d[k][c] * ocr_d[data_l[d][i/2]][c]]
				t["cprob"] = cprob
			if i == len(out["V"]) -1:
				t["children"] = None
			else:
				t["children"] = ["c" + str(i/2+1)]
			

		if i % 2 == 0:
			temp["i" + str(i/2)] = t
		else:
			temp["c" + str(i/2)] = t
	out["Vdata"] = temp
	break

pp.pprint(out)
with open("0.json","w") as outfile:
	json.dump(out, outfile)