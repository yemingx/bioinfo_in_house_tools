import re
import sys
import os
import argparse
from operator import itemgetter
import matplotlib.pyplot as plt
#%matplotlib inline
import numpy as np
import seaborn as sns

parser = argparse.ArgumentParser(description='')
parser.add_argument('-s', '--site', required=True, help = '')
parser.add_argument('-g', '--genome', required=True, help = '')
#parser.add_argument('-e', '--enzyme', required=True, help = '')
#parser.add_argument('-l', '--locus_out', required=True, help = '')
parser.add_argument('-o', '--output', required=True, help = 'output')
parser.add_argument('-b', '--binwidth', required=False, help = '')
parser.add_argument('-l', '--xlimleft', required=False, help = '')
parser.add_argument('-r', '--xlimright', required=False, help = '')
parser.add_argument('-d', '--decimal', required=False, help = '')
parser.add_argument('-a', '--abline', required=False, help = '[1,0]')
parser.add_argument('-L', '--log', required=False, help = '[1,0]')
parser.add_argument('-p', '--plot_type', required=False, help = '[hist,kde]')
parser.add_argument('-w', '--bw', required=False, help = 'kde smooth parameter')
parser.add_argument('-t','--title',required=True,help='title of plot')
args = parser.parse_args()

if __name__ == '__main__':
	with open(args.genome, 'r') as f:
		genome = f.read().strip().split('\n')
	site = args.site
	site_len = len(site)

	final_arr = np.array([],dtype=np.int32)
	for i in range(len(genome)):
		if genome[i].startswith('>'):
			chr = genome[i][4:]
			seq = genome[i+1]
			list_tmp = []
			for j in range(len(seq)):
			#for j in range(100000):
				if seq[j:j+site_len] != 'NNNNNN':
					if seq[j:j+site_len] == site:
						list_tmp.append(j)
						#locus_out.write(chr + '\t' + str(j+1) + '\n')
			arr_tmp = np.diff(np.asarray(list_tmp))
			final_arr = np.append(final_arr,arr_tmp)

	if args.log == '1':
		total_1d_array = np.log10(np.asarray(final_arr))
	else:
		total_1d_array = np.asarray(final_arr)

	decimal_num = int(args.decimal)
	max_num = str(round(np.amax(total_1d_array), decimal_num))
	min_num = str(round(np.amin(total_1d_array), decimal_num))
	median_num = str(round(np.median(total_1d_array), decimal_num))
	pct_25_num = str(round(np.percentile(total_1d_array, 25), decimal_num))
	pct_75_num = str(round(np.percentile(total_1d_array, 75), decimal_num))
	mean_num = str(round(np.mean(total_1d_array), decimal_num))
	pct_5_num = str(round(np.percentile(total_1d_array, 5), decimal_num))
	pct_95_num = str(round(np.percentile(total_1d_array, 95), decimal_num))

	if args.title:
		title_str = ' '.join(['\n', args.title, '\n', 'min', min_num, ' mean', mean_num, ' max', max_num, '\n'])
	else:
		title_str = ' '.join(['min', min_num, ' mean', mean_num, ' max', max_num, '\n'])

	print(title_str)
	print(' '.join([' pct_5', pct_5_num, ' pct_25', pct_25_num, ' median', median_num, ' pct_75', pct_75_num, ' pct_95',
					pct_95_num, '\n']))

	if args.plot_type == 'kde':
		sns.kdeplot(x=total_1d_array, bw_method=float(args.bw))
		if args.xlimleft and args.xlimright:
			xlim_left, xlim_right = int(args.xlimleft), int(args.xlimright)
			plt.xlim([xlim_left, xlim_right])
		plt.title(title_str)
		if args.abline == '1':
			plt.axvline(x=np.percentile(total_1d_array, 5), color='brown', linewidth=0.5, label='5%, ' + pct_5_num)
			plt.axvline(x=np.percentile(total_1d_array, 25), color='red', linewidth=0.5, label='25%, ' + pct_25_num)
			plt.axvline(x=np.percentile(total_1d_array, 50), color='green', linewidth=0.5, label='50%, ' + median_num)
			plt.axvline(x=np.percentile(total_1d_array, 75), color='blue', linewidth=0.5, label='75%, ' + pct_75_num)
			plt.axvline(x=np.percentile(total_1d_array, 95), color='purple', linewidth=0.5, label='95%, ' + pct_95_num)
			plt.legend()
		if args.log == '1':
			plt.xlabel('log10')
		plt.show()
		plt.savefig(args.output + '_kdeplot.pdf')
		plt.close()

	if args.plot_type == 'hist':
		bin_width = int(args.binwidth)
		sns.histplot(x=total_1d_array, binwidth=bin_width)
		if args.xlimleft and args.xlimright:
			xlim_left, xlim_right = int(args.xlimleft), int(args.xlimright)
			plt.xlim([xlim_left, xlim_right])
		plt.title(title_str)
		if args.abline == '1':
			plt.axvline(x=np.percentile(total_1d_array, 5), color='brown', linewidth=0.5, label='5%, ' + pct_5_num)
			plt.axvline(x=np.percentile(total_1d_array, 25), color='red', linewidth=0.5, label='25%, ' + pct_25_num)
			plt.axvline(x=np.percentile(total_1d_array, 50), color='green', linewidth=0.5, label='50%, ' + median_num)
			plt.axvline(x=np.percentile(total_1d_array, 75), color='blue', linewidth=0.5, label='75%, ' + pct_75_num)
			plt.axvline(x=np.percentile(total_1d_array, 95), color='purple', linewidth=0.5, label='95%, ' + pct_95_num)
			plt.legend()
		if args.log == '1':
			plt.xlabel('log10')
		plt.title(title_str)
		plt.show()
		# plt.ylim(reversed(plt.ylim()))
		plt.savefig(args.output + '_histplot.pdf')
		plt.close()