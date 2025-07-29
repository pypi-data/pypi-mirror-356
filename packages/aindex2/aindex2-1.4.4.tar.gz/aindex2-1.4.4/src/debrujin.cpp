//
// Created by Aleksey Komissarov on 30/08/15.
//
#include "debrujin.hpp"
#include "kmers.hpp"
#include <stdint.h>
#include "hash.hpp"
#include "read.hpp"

namespace DEBRUJIN {

    int get_freq(uint64_t kmer, PHASH_MAP &kmers) {

//    HASH_MAP::const_iterator got = kmers.find(kmer);
//    if (got == kmers.end() ) {
//        kmer = reverseDNA(kmer);
//
//        got = kmers.find(kmer);
//        if (got == kmers.end() ) {
//            return 0;
//        }
//        return got->second;
//    }
//    return got->second;

        return kmers.get_freq(kmer);
    }


    void print_next(uint64_t kmer, PHASH_MAP &kmers, CONT &cont, uint32_t cutoff = 0) {
        /*
        */
        cont.n = 0;
        uint64_t kmer_A = ((kmer << 2) | ((uint64_t) 0 & 3)) & 0x00003fffffffffff;
        uint64_t kmer_C = ((kmer << 2) | ((uint64_t) 1 & 3)) & 0x00003fffffffffff;
        uint64_t kmer_G = ((kmer << 2) | ((uint64_t) 2 & 3)) & 0x00003fffffffffff;
        uint64_t kmer_T = ((kmer << 2) | ((uint64_t) 3 & 3)) & 0x00003fffffffffff;

        cont.A = kmers.get_freq(kmer_A);
        cont.C = kmers.get_freq(kmer_C);
        cont.G = kmers.get_freq(kmer_G);
        cont.T = kmers.get_freq(kmer_T);

        if (cutoff > 0) {
            if (cont.A <= cutoff) cont.A = 0;
            if (cont.C <= cutoff) cont.C = 0;
            if (cont.G <= cutoff) cont.G = 0;
            if (cont.T <= cutoff) cont.T = 0;
        }

        cont.sum = cont.A + cont.C + cont.G + cont.T;
        cont.n = (uint32_t) (bool) cont.A + (uint32_t) (bool) cont.C + (uint32_t) (bool) cont.G +
                 (uint32_t) (bool) cont.T;

        if (cont.A >= cont.C && cont.A >= cont.G && cont.A >= cont.T) {
            cont.best_hit = 'A';
            cont.best_ukmer = kmer_A;
            cont.best_hit_tf = cont.A;
        }
        if (cont.C >= cont.A && cont.C >= cont.G && cont.C >= cont.T) {
            cont.best_hit = 'C';
            cont.best_ukmer = kmer_C;
            cont.best_hit_tf = cont.C;
        }
        if (cont.G >= cont.C && cont.G >= cont.A && cont.G >= cont.T)  {
            cont.best_hit = 'G';
            cont.best_ukmer = kmer_G;
            cont.best_hit_tf = cont.G;
        }
        if (cont.T >= cont.C && cont.T >= cont.G && cont.T >= cont.A)  {
            cont.best_hit = 'T';
            cont.best_ukmer = kmer_T;
            cont.best_hit_tf = cont.T;
        }
    }

//    void print_next_findex(uint64_t kmer, uint16_t* positions, assembly_n, assembly_id, CONT &cont, uint32_t cutoff = 0) {
//        /*
//        */
//        cont.n = 0;
//        uint64_t kmer_A = ((kmer << 2) | ((uint64_t) 0 & 3)) & 0x00003fffffffffff;
//        uint64_t kmer_C = ((kmer << 2) | ((uint64_t) 1 & 3)) & 0x00003fffffffffff;
//        uint64_t kmer_G = ((kmer << 2) | ((uint64_t) 2 & 3)) & 0x00003fffffffffff;
//        uint64_t kmer_T = ((kmer << 2) | ((uint64_t) 3 & 3)) & 0x00003fffffffffff;
//
//        cont.A = positions[h1*assembly_n + assembly_id];
//        cont.C = kmers.get_freq(kmer_C);
//        cont.G = kmers.get_freq(kmer_G);
//        cont.T = kmers.get_freq(kmer_T);
//
//        if (cutoff > 0) {
//            if (cont.A <= cutoff) cont.A = 0;
//            if (cont.C <= cutoff) cont.C = 0;
//            if (cont.G <= cutoff) cont.G = 0;
//            if (cont.T <= cutoff) cont.T = 0;
//        }
//
//        cont.sum = cont.A + cont.C + cont.G + cont.T;
//        cont.n = (uint32_t) (bool) cont.A + (uint32_t) (bool) cont.C + (uint32_t) (bool) cont.G +
//                 (uint32_t) (bool) cont.T;
//
//        if (cont.A >= cont.C && cont.A >= cont.G && cont.A >= cont.T) {
//            cont.best_hit = 'A';
//            cont.best_ukmer = kmer_A;
//        }
//        if (cont.C >= cont.A && cont.C >= cont.G && cont.C >= cont.T) {
//            cont.best_hit = 'C';
//            cont.best_ukmer = kmer_C;
//        }
//        if (cont.G >= cont.C && cont.G >= cont.A && cont.G >= cont.T)  {
//            cont.best_hit = 'G';
//            cont.best_ukmer = kmer_G;
//        }
//        if (cont.T >= cont.C && cont.T >= cont.G && cont.T >= cont.A)  {
//            cont.best_hit = 'T';
//            cont.best_ukmer = kmer_T;
//        }
//    }


    void print_prev(uint64_t kmer, PHASH_MAP &kmers, CONT &cont, uint32_t cutoff = 0) {
        /*
        */
        cont.n = 0;
        uint64_t kmer_A = (kmer >> 2) | (((uint64_t) 0 & 3) << 44);
        uint64_t kmer_C = (kmer >> 2) | (((uint64_t) 1 & 3) << 44);
        uint64_t kmer_G = (kmer >> 2) | (((uint64_t) 2 & 3) << 44);
        uint64_t kmer_T = (kmer >> 2) | (((uint64_t) 3 & 3) << 44);

        cont.A = kmers.get_freq(kmer_A);
        cont.C = kmers.get_freq(kmer_C);
        cont.G = kmers.get_freq(kmer_G);
        cont.T = kmers.get_freq(kmer_T);

        if (cutoff > 0) {
            if (cont.A <= cutoff) cont.A = 0;
            if (cont.C <= cutoff) cont.C = 0;
            if (cont.G <= cutoff) cont.G = 0;
            if (cont.T <= cutoff) cont.T = 0;
        }

        cont.sum = cont.A + cont.C + cont.G + cont.T;

        if (cont.A >= cont.C && cont.A >= cont.G && cont.A >= cont.T) {
            cont.best_hit = 'A';
            cont.best_ukmer = kmer_A;
            cont.best_hit_tf = cont.A;
        }
        if (cont.C >= cont.A && cont.C >= cont.G && cont.C >= cont.T) {
            cont.best_hit = 'C';
            cont.best_ukmer = kmer_C;
            cont.best_hit_tf = cont.C;
        }
        if (cont.G >= cont.C && cont.G >= cont.A && cont.G >= cont.T)  {
            cont.best_hit = 'G';
            cont.best_ukmer = kmer_G;
            cont.best_hit_tf = cont.G;
        }
        if (cont.T >= cont.C && cont.T >= cont.G && cont.T >= cont.A)  {
            cont.best_hit = 'T';
            cont.best_ukmer = kmer_T;
            cont.best_hit_tf = cont.T;
        }

        cont.n = (uint32_t) (bool) cont.A + (uint32_t) (bool) cont.C + (uint32_t) (bool) cont.G +
                 (uint32_t) (bool) cont.T;
    }

    void set_fm_for_read(READS::READ &read, PHASH_MAP &kmers) {
        for (uint64_t i = 0; i < read.seq.length() - Settings::K + 1; i++) {
            std::string kmer = read.seq.substr(i, 23);
            read.fm[i] = kmers.get_freq(kmer);
        }
    }

    void set_fm_for_read(READS::READ &read, PHASH_MAP &kmers, uint64_t from, uint64_t to) {
        if (from > read.seq.length()) { // hot fix possible overflow
            from = 0;
        }
        if (to > read.seq.length()) {
            to = read.seq.length();
        }
        for (uint64_t i = from; i < to; i++) {
            std::string kmer = read.seq.substr(i, Settings::K);
            read.fm[i] = kmers.get_freq(kmer);
        }
    }
}