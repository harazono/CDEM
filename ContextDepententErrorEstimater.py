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
	parser.add_argument("-s", "--start", help = "start position of the region", default = 0, type = int)
	parser.add_argument("-e", "--end",   help = "end   position of the region", type = int)
	parser.add_argument("--json",        help = "If this arg is set then output results in JSON format.", action = 'store_true')
	parser.add_argument("-v", "--verbose", help = "Outputs verbose", action = 'store_true')
	args = parser.parse_args()

	ref_file_path = args.reference_genome
	bam_file_path = args.sorted_bam
	k             = args.kmer
	chrm          = args.chr
	start_pos     = args.start + k
	end_pos       = args.end
	is_json       = args.json
	ref           = pysam.FastaFile(ref_file_path)
	sam           = pysam.AlignmentFile(bam_file_path, "rb")
	reference     = ref.references[0]
	context_readbase_dict = {}
	is_verbose    = args.verbose

	reference_size = len(ref.fetch(reference = reference))
	if chrm != "":
		reference = chrm

	if is_verbose:
		print("Reference name:\t%s\nReference len :\t%s"%(reference, reference_size), file = sys.stderr)
		if end_pos != None:
			len_of_region = end_pos - start_pos
		else:
			len_of_region = reference_size - start_pos

	roop_counter = 0
	for pileupcolumn in sam.pileup(contig = reference, start = start_pos, stop = end_pos, truncate = True):
		if pileupcolumn.pos - k <= 0 or pileupcolumn.pos + 1 + k >= reference_size:
			continue

		refbase = ref.fetch(reference = reference, start = pileupcolumn.pos, end = pileupcolumn.pos + 1)
		refcon  = ref.fetch(reference = reference, start = pileupcolumn.pos - k, end = pileupcolumn.pos + 1 + k)

		if not refcon in context_readbase_dict.keys():
			context_readbase_dict[refcon] = dict(A = 0, C = 0, G = 0, T = 0, x = 0)# use x as gap

		for pileupread in pileupcolumn.pileups:
			if not pileupread.is_refskip and not pileupread.is_del:
				base = pileupread.alignment.query_sequence[pileupread.query_position]
				if base == "A" or base == "C" or base == "G" or base == "T":
					context_readbase_dict[refcon][base] += 1
			if pileupread.is_del:
				context_readbase_dict[refcon]["x"] += 1
		if is_verbose:
			roop_counter += 1
			print("%s/%s proceeded\r"%(roop_counter, len_of_region), file = sys.stderr, end = "")

	if is_json:
		pp.pprint(json.dumps(context_readbase_dict))
	else:
		pp.pprint(context_readbase_dict)

	ref.close()
	sam.close()
