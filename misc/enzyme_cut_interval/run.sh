date

# for raw genome fasta file, convert from mutiple line of sequence per record to one line of sequence per record
python script/multi_to_one_line_fasta_yeming.py ref/mm10_genome.fa ref/mm10_genome.fa.one_line 1

# plot the distribution of given cut site interval on given genome
enzyme='DpnII'
site='GATC'
genome='mm10'
python script/cut_site_locus.py -s ${site} -g ref/${genome}_genome.fa.one_line \
-o output/${enzyme}_${site}_${genome}_interval \
-d 2 -a 1 -L 1 -p kde -w 0.1 -t ${enzyme}_${site}_${genome}_interval

date
############## archive ##############
# /usr/bin/makeblastdb -in blastn_db_mm10/genome.fa -dbtype nucl -out blastn_db_mm10/genome.fa
# /usr/bin/blastn -query cut_site_fa/DpnII.fa -db blastn_db_mm10/genome.fa -dust no -outfmt 6 -evalue 1e-5 -num_alignments 1 -num_descriptions 1 -num_threads 2 -out DpnII.blast_out
#/usr/bin/blastn -query cut_site_fa/DpnII.fa -db blastn_db_mm10/genome.fa -dust no -outfmt 6 -perc_identity 100 -max_target_seqs 1000000000 -out DpnII.blast_out -word_size 4 -ungapped
