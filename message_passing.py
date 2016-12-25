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


for d in data_l:
    word = []
    for i in range(len(d))
        