import csv
import itertools

CHARS = ['d', 'o', 'i', 'r', 'a', 'h', 't', 'n', 's', 'e']
ocr_r = csv.reader(open("dataset/ocr.dat","rb"), delimiter='\t')
truth_r = csv.reader(open("dataset/truth.dat","rb"), delimiter='\t')
#trans_r = csv.reader(open("trans.data","rb"))

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

#print ocr_d
res_scores = []
res_words = []
res_prob = []

for data in data_l:
	all_perms = list(itertools.product(CHARS, repeat=len(data)))
	uniques = {}
	for word in all_perms:
		if ''.join(word) not in uniques:
			uniques[''.join(word)] = 0.0

	probs = []
	for ID in data:
		probs.append(ocr_d[ID])

	temp_result_score = 0.0
	temp_result_word = ''
	temp_prob = 0
	for word in uniques.keys():
		temp_factor = 1.0
		for k in range(len(word)):
			temp_factor *= probs[k][word[k]]
		uniques[word] = temp_factor

		temp_prob = temp_prob + temp_factor
		if temp_result_score <= temp_factor:
			temp_result_score = temp_factor
			temp_result_word = word

	res_scores.append(temp_result_score)
	res_words.append(temp_result_word)
	res_prob.append(temp_result_score/temp_prob)
	print temp_result_word

p = 0
i = 0
for row in truth_r:
	if row[0] == res_words[i]:
		p += 1
	i += 1

print p

# print res_prob