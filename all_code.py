import csv
import itertools
from math import log

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

#print ocr_d
ocr_correct_prob_acc = 0.0
trans_correct_prob_acc = 0.0
comb_correct_prob_acc = 0.0

ocr_scores = []
ocr_words = []
ocr_probs = []
trans_scores = []
trans_words = []
trans_probs = []
comb_scores = []
comb_words = []
comb_probs = []

for d in range(len(data_l)):
	all_perms = list(itertools.product(CHARS, repeat=len(data_l[d])))
	uniques = {}
	for word in all_perms:
		if ''.join(word) not in uniques:
			uniques[''.join(word)] = 0.0

	probs = []
	for ID in data_l[d]:
		probs.append(ocr_d[ID])

	ocr_temp_score = 0.0
	ocr_temp_word = ''

	trans_temp_score = 0.0
	trans_temp_word = ''

	comb_temp_score = 0.0
	comb_temp_word = ''

	ocr_z = 0.0
	trans_z = 0.0
	comb_z = 0.0

	for word in uniques.keys():
		temp_prob = 1.0
		for k in range(len(word)):
			#print word[k]
			#print probs[k]
			temp_prob *= probs[k][word[k]]

		if ocr_temp_score <= temp_prob:
			ocr_temp_score = temp_prob
			ocr_temp_word = word

		if ocr_temp_word == truth_l[d]:
			ocr_correct_prob_acc += log(ocr_temp_score)

		ocr_z += temp_prob

		for k in range(len(word)-1):
			temp_prob *= trans_d[word[k]][word[k+1]]

		if trans_temp_score <= temp_prob:
			trans_temp_score = temp_prob
			trans_temp_word = word

		if trans_temp_word == truth_l[d]:
			trans_correct_prob_acc += log(trans_temp_score)

		trans_z += temp_prob

		for i in range(len(word)):
			for j in range(i + 1, len(word)):
				if data_l[d][i] == data_l[d][j] and word[i] == word[j]:
					temp_prob *= 5

		uniques[word] = temp_prob
		if comb_temp_score <= temp_prob:
			comb_temp_score = temp_prob
			comb_temp_word = word

		if comb_temp_word == truth_l[d]:
			comb_correct_prob_acc += log(comb_temp_score)

		comb_z += temp_prob

	ocr_scores.append(ocr_temp_score)
	ocr_words.append(ocr_temp_word)
	ocr_probs.append(ocr_temp_score / ocr_z)

	trans_scores.append(trans_temp_score)
	trans_words.append(trans_temp_word)
	trans_probs.append(trans_temp_score / trans_z)

	comb_scores.append(comb_temp_score)
	comb_words.append(comb_temp_word)
	comb_probs.append(comb_temp_score / comb_z)

	print d

ocr_out = csv.writer(open("ocr_output.dat","wb"), delimiter = '\t')
trans_out = csv.writer(open("trans_output.dat","wb"), delimiter = "\t")
comb_out = csv.writer(open("comb_output.dat","wb"), delimiter = "\t")

tot_chars = 0

ocr_char_correct_count = 0
ocr_word_correct_count = 0

trans_char_correct_count = 0
trans_word_correct_count = 0

comb_char_correct_count = 0
comb_word_correct_count = 0

for i in range(len(truth_l)):
	ocr_out.writerow([ocr_words[i], ocr_scores[i], ocr_probs[i]])
	trans_out.writerow([trans_words[i], trans_scores[i], trans_probs[i]])
	comb_out.writerow([comb_words[i], comb_scores[i], comb_probs[i]])

	for j in range(len(truth_l[i])):
		tot_chars += 1
		if truth_l[i][j] == ocr_words[i][j]:
			ocr_char_correct_count += 1

		if truth_l[i][j] == trans_words[i][j]:
			trans_char_correct_count += 1

		if truth_l[i][j] == comb_words[i][j]:
			comb_char_correct_count += 1

	if truth_l[i] == ocr_words[i]:
		ocr_word_correct_count += 1

	if truth_l[i] == trans_words[i]:
		trans_word_correct_count += 1

	if truth_l[i] == comb_words[i]:
		comb_word_correct_count += 1

print "Ocr Model : Char accuracy = " + str(ocr_char_correct_count / (tot_chars * 1.0)) + ", Word accuracy = " + str(ocr_word_correct_count / (len(truth_l) * 1.0)) + ", Log Likelihood = " + str(ocr_correct_prob_acc / (len(truth_l) * 1.0))
print "Transition Model : Char accuracy = " + str(trans_char_correct_count / (tot_chars * 1.0)) + ", Word accuracy = " + str(trans_word_correct_count / (len(truth_l) * 1.0)) + ", Log Likelihood = " + str(trans_correct_prob_acc / (len(truth_l) * 1.0))
print "Combined Model : Char accuracy = " + str(comb_char_correct_count / (tot_chars * 1.0)) + ", Word accuracy = " + str(comb_word_correct_count / (len(truth_l) * 1.0)) + ", Log Likelihood = " + str(comb_correct_prob_acc / (len(truth_l) * 1.0))


