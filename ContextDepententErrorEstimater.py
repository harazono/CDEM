#! /usr/bin/env python3
import sys
import pysam
import pprint
import json
import argparse
pp = pprint.PrettyPrinter(indent=4)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description = 'count occurences of each pair of context((2*k+1)-mer) and single base(1-mer)')
	parser.add_argument("reference_genome", help = "The reference genome. The format should be FASTA")
	parser.add_argument("sorted_bam",       help = "Aligned reads to be counted. BAM should be sorted by position")
	parser.add_argument("-k", "--kmer",  help = "k-mer size. Default is 0", default = 0, type = int)
	parser.add_argument("-c", "--chr",   help = "chromosome or contig to be considered", default = "")
	parser.add_argument("-s", "--start", help = "start position of the region", default = 100,  type = int)
	parser.add_argument("-e", "--end",   help = "end   position of the region", default = 101, type = int)
	parser.add_argument("--json",        help = "If this arg is set then output results in JSON format.", action = 'store_true')

	args = parser.parse_args()

	ref_file_path = args.reference_genome
	bam_file_path = args.sorted_bam
	k             = args.kmer
	chrm          = args.chr
	start_pos     = args.start
	end_pos       = args.end
	is_json       = args.json
	ref           = pysam.FastaFile(ref_file_path)
	sam           = pysam.AlignmentFile(bam_file_path, "rb")
	reference     = ref.references[0]
	context_readbase_dict = {}

	if chrm != "":
		reference = chrm

	for pileupcolumn in sam.pileup(contig = reference, start = start_pos, stop = end_pos, truncate = True):
		refbase = ref.fetch(reference = reference, start = pileupcolumn.pos, end = pileupcolumn.pos + 1)
		refcon  = ref.fetch(reference = reference, start = pileupcolumn.pos - k, end = pileupcolumn.pos + 1 + k)

		if not refcon in context_readbase_dict.keys():
			context_readbase_dict[refcon] = dict(A = 0, C = 0, G = 0, T = 0)
		for pileupread in pileupcolumn.pileups:
			if not pileupread.is_del and not pileupread.is_refskip:
				base = pileupread.alignment.query_sequence[pileupread.query_position]
				context_readbase_dict[refcon][base] += 1
	if is_json:
		pp.pprint(json.dumps(context_readbase_dict))
	else:
		pp.pprint(context_readbase_dict)

	ref.close()
	sam.close()
