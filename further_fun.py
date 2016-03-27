import csv
import itertools
from math import log
import mn
from os import listdir

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
	if i % 10 == 0:
		temp[row[1]] = float(row[2])
		ocr_d[int(row[0])] = temp
		temp = {}
	else:
		temp[row[1]] = float(row[2])
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


data_words = []
for d in range(len(data_l)):
	all_perms = list(itertools.product(CHARS, repeat=len(data_l[d])))
	data_words.append(all_perms)

for d in range(len(data_l)):
	fout = open("probs/" + str(d) + ".prob", "w")

	fout.write("MARKOV\n")
	fout.write(str(len(data_l[d])) + "\n")
	fout.write(' '.join(['10' for x in range(len(data_l[d]))]) + "\n")
	fout.write(str(2 * len(data_l[d]) - 1) + "\n")

	for j in range(len(data_l[d])):
			fout.write("1 " + str(j) + "\n")
			if j < len(data_l[d]) - 1:
				fout.write("2 " + str(j) + " " + str(j + 1) + "\n")

	for j in range(2 * len(data_l[d]) - 1):
		if j % 2 == 0:
			fout.write("\n10\n")
			temp = ocr_d[data_l[d][j / 2]]
			for c in CHARS:
				fout.write(" " + str(temp[c]))
			fout.write("\n")
		else:
			fout.write("\n100\n")
			for c in CHARS:
				for ch in CHARS:
					fout.write(" " + str(trans_d[c][ch]))
				fout.write("\n")

	fout.close()

fout = open('trans_outcome_JTA.dat','w')

count = 0
for i in range(104):
	print i
	reload(mn)
	mn.loadParseUAIFile("probs/" + str(i) + ".prob")
	mn.loopyBeliefPropagation()
	res = mn.computeMAP4MN()
	word = ''
	for k in res:
		word += CHARS[k[1]]
	if word == truth_l[i]:
		count += 1
	
	fout.write(word + "\n")
	fout.write("Partition Function, z : " + str(mn.computePR4MN()) + "\n\n")

fout.close()
print count

