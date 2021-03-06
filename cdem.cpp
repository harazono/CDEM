#include <stdio.h>
#include <cstdlib>
#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <map>
#include <getopt.h>
#include <math.h>
#include <omp.h>
#include <stdexcept>
#include "cpas_debug.h"
#include "cpas_tsv.h"
#include "htslib/htslib/sam.h"
#include "htslib/htslib/hts.h"

using namespace std;


void printUsageAndExit(){
  fprintf(stderr, "cdem <reference.fa> <aligned_reads.sort.bam>\n");
  exit(2);
}

int main(int argc, char *argv[]){
/*
  GDB_On_SEGV g(argv[0]);
  struct option longopts[] = {
    { "csv"       , no_argument       , NULL , 'c' } ,
    // { "delete" , optional_argument , NULL , 'd' } ,
    { "kmer"      , required_argument , NULL , 'k' } ,
    { "binary"    , required_argument , NULL , 'b' } ,
    { 0           , 0                 , 0    , 0  }  ,
  };
  /// PARAMETERS ///

  int kmer_size = 1;
  bool output_in_csv = false;
  string binary_output_file_name;

  //////////////////

  int opt;
  int longindex;
  while ((opt = getopt_long(argc, argv, "k:", longopts, &longindex)) != -1) {
    switch (opt) {
      case 'b':
        binary_output_file_name = optarg;
        break;
      case 'c':
        output_in_csv = true;
        break;
      case 'k':
        kmer_size = atoi(optarg);
        if(kmer_size < 1 || 10 < kmer_size) {
          //error("kmer size must be 1-10");
        }
        break;
      default:
        MYASSERT_NEVERREACH();
    }
  }
  const int NUM_REQUIRED_ARGUMENTS = 2;
  if(optind + NUM_REQUIRED_ARGUMENTS != argc) {
    printUsageAndExit();
  }*/
  if(argc < 3){
    printUsageAndExit();
  }
  const int    optind = 0;
  const char* reference_genome_filename = argv[1];
  const char* aligned_reads_filename    = argv[2];
  fprintf(stderr, "reference_genome_filename \t= %s\n", reference_genome_filename);
  fprintf(stderr, "aligned_reads_filename    \t= %s\n", aligned_reads_filename);
  htsFile *in_sam = NULL;
  in_sam = sam_open(aligned_reads_filename, "r");
  if(in_sam == NULL){
    fprintf(stderr, "failed to open %s\n", aligned_reads_filename);
    return 2;
  }else{
    fprintf(stderr, "get sam\n");
    sam_close(in_sam);
  }
  string name_of_the_only_reference_sequence;
  return 0;
}

