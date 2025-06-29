import re
import sys
import os
# python multi_to_one_line_fasta_yeming.py [input] [output] [upper:0,1]
with open(sys.argv[1],'r') as f_sample:
	line = f_sample.read().splitlines()
geneID = []
sequence = []

a = 0
for a in range(0,len(line)):
	if line[a].startswith(">"):
		geneID += line[a:a+1]
		sequence += '>'
	else:
		sequence += line[a:a+1]
	a += 1

sequence_string = ''.join(sequence)
line2 = sequence_string.split('>')
line1 = line2[1:]
out_sample = open(sys.argv[2],'w')

a = 0
if sys.argv[3] == '0':
	for a in range(0,len(geneID)):
		out_sample.write(geneID[a] + '\n' + line1[a] + '\n')
		a += 1
if sys.argv[3] == '1':
	for a in range(0,len(geneID)):
		out_sample.write(geneID[a] + '\n' + line1[a].upper() + '\n')
		a += 1
out_sample.close
