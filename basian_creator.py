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
allimages_r1 = open("dataset/allimages1.dat","rb")
allimages_r2 = open("dataset/allimages2.dat","rb")
allimages_r3 = open("dataset/allimages3.dat","rb")
allimages_r4 = open("dataset/allimages4.dat","rb")
allimages_r5 = open("dataset/allimages5.dat","rb")
bicount_r = csv.reader(open("dataset/bicounts.dat"), delimiter="\t")
allwords_r = open("dataset/allwords.dat","rb")
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

allimages_d = {}
tot_images = 0
for line in allimages_r1:
	temp = map(int, line.split())
	tot_images += len(temp)
	for t in temp:
		if t not in allimages_d:
			allimages_d[t] = 1
		else:
			allimages_d[t] += 1

for line in allimages_r2:
	temp = map(int, line.split())
	tot_images += len(temp)
	for t in temp:
		if t not in allimages_d:
			allimages_d[t] = 1
		else:
			allimages_d[t] += 1

for line in allimages_r3:
	temp = map(int, line.split())
	tot_images += len(temp)
	for t in temp:
		if t not in allimages_d:
			allimages_d[t] = 1
		else:
			allimages_d[t] += 1

for line in allimages_r4:
	temp = map(int, line.split())
	tot_images += len(temp)
	for t in temp:
		if t not in allimages_d:
			allimages_d[t] = 1
		else:
			allimages_d[t] += 1

for line in allimages_r5:
	temp = map(int, line.split())
	tot_images += len(temp)
	for t in temp:
		if t not in allimages_d:
			allimages_d[t] = 1
		else:
			allimages_d[t] += 1

for k in allimages_d.keys():
	allimages_d[k] = allimages_d[k] / (tot_images * 1.0)

bicount_d = {}
for row in bicount_r:
	if row[0] not in bicount_d:
		bicount_d[row[0]] = {row[1]:float(row[2])}
	else:
		bicount_d[row[0]][row[1]] = float(row[2])

allwords_d = {}
start_d = {}
tot_chars = 0
for line in allwords_r.readlines():
	tot_chars += len(line[:-1])
	if line[0] not in start_d:
		start_d[line[0]] = 1
	else:
		start_d[line[0]] += 1

	for c in line[:-1]:
		if c not in allwords_d:
			allwords_d[c] = 1
		else:
			allwords_d[c] += 1

for c in CHARS:
	start_d[c] = start_d[c] / 2188.0

bicount_d['null'] = start_d

for c in CHARS:
	allwords_d[c] = allwords_d[c] / (tot_chars * 1.0)


first = []
for c in CHARS:
	first.append(bicount_d['null'][c])

bicount_mat = []
for c1 in CHARS:
	temp = []
	for c2 in CHARS:
		temp.append(bicount_d[c1][c2])
	bicount_mat.append(temp)

IMAGES = allimages_d.keys()

images_mat = []
for c in CHARS:
	temp = []
	for img in IMAGES:
		temp.append(allimages_d[img] * ocr_d[img][c] / allwords_d[c])
	images_mat.append(temp)


out = {}
p = 0
for d in data_l:
	#print d
	out["V"] = [str(i) for i in range(2 * len(d))]
	temp = []
	for i in range(0,2*len(d)-2,2):
		temp.append([str(i),str(i+2)])
	for i in range(0,2*len(d),2):
		temp.append([str(i),str(i+1)])
	out["E"] = temp
	temp = {}
	for i in range(0,2*len(d),2):
		t = {}
		t["ord"] = i
		t["numoutcomes"] = 10
		t["vals"] = CHARS
		if i == 0:
			t["parents"] = None
		else:
			t["parents"] = [str(i-2)]
		if i == 2 * len(d) - 2:
			t["children"] = [str(i + 1)]
		else:
			t["children"] = [str(i + 2),str(i+1)]
		if i == 0:
			t["cprob"] = first
		else:
			tt = {}
			for j in range(10):
				tt[str([CHARS[j]])] = bicount_mat[j]
			t["cprob"] = tt
		temp[str(i)] = t   

	for i in range(1,2*len(d),2):
		t = {}
		t["ord"] = i
		t["numoutcomes"] = len(IMAGES)
		t["vals"] = [str(img) for img in IMAGES]
		t["parents"] = [str(i-1)]
		t["children"] = None
		tt = {}
		for j in range(10):
			tt[str([CHARS[j]])] = images_mat[j]
		t["cprob"] = tt
		temp[str(i)] = t
	out["Vdata"] = temp
	#pp.pprint(out)
	with open("bayes_net/"+str(p)+".txt","w") as outfile:
		json.dump(out, outfile)
	p += 1