//
// Created by Aleksey Komissarov on 29/08/15.
//

#ifndef STIRKA_READ_H
#define STIRKA_READ_H

#include <string>
#include <vector>
#include <tuple>
#include <math.h>
#include <bitset>
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h> // memchr
#include <fcntl.h>
#include <atomic>

#include "settings.hpp"
#include "hash.hpp"
#include "dna_bitseq.hpp"


const int MINIMAL_PHRED = 33;
const int MAXIMAL_PHRED = 125;

typedef std::atomic<uint64_t> ATOMIC_uint64_t;

namespace READS {

    struct CorrectionErrors {

        std::atomic<int> simple_ok;
        std::atomic<int> simple_n0;
        std::atomic<int> simple_nM;
        std::atomic<int> indel;
        std::atomic<int> small_indel;
        std::atomic<int> indel_stuck;


        std::atomic<int> uindel;
        std::atomic<int> uindel_multiple;
        std::atomic<int> uindel_stuck;


        std::atomic<int> indel_multiple;


        std::atomic<int> small_indel_stuck;
        std::atomic<int> small_indel_multiple;

        std::atomic<int> dead_right_end;

        CorrectionErrors() {
            simple_ok = 0;
            simple_n0 = 0;
            simple_nM = 0;

            uindel = 0;
            small_indel = 0;
            indel_stuck = 0;
            indel_multiple = 0;

            small_indel = 0;

            uindel = 0;
            uindel_stuck = 0;
            uindel_multiple = 0;

            small_indel_stuck = 0;
            small_indel_multiple = 0;
            dead_right_end = 0;
        }


        void print() {
            emphf::logger() << "simple_ok: " << simple_ok.load()
                    << " simple_n0: " << simple_n0.load()
                    << " simple_nM: " << simple_nM.load()
                    << " small_indel: " << small_indel.load()
                    << " indel: " << indel.load()
                    << " indel_stuck: " << indel_stuck.load()
                    << " indel_multiple: " << indel_multiple.load()
                    << " uindel: " << uindel.load()
                    << " uindel_stuck: " << uindel_stuck.load()
                    << " uindel_multiple: " << uindel_multiple.load()
                    << " small_indel_stuck: " << indel_stuck.load()
                    << " small_indel_multiple: " << indel_multiple.load()
                    << " dead_right_end: " << dead_right_end.load()
                    << std::endl;
        }
    };

    struct Correction {

        std::string type = "unknown";
        std::string prev_type = "unknown";
        uint32_t start_position = 0;
        uint32_t end_position = 0;
        uint32_t stop_point = 0;
        uint32_t position = 0;
        std::vector<int> fixed;
        int status = 0;

        Correction();

        Correction(const std::string& _type, const std::string& _prev_type, uint32_t _start_position) {
            type = _type;
            prev_type = _prev_type;
            start_position = _start_position;
        }
    };

    static int total_rid = 0;

    struct READ {

        uint64_t rid = 0;
        std::string head;
        std::string seq;
        std::string strand;
        std::string Q;
        uint *fm;
        uint *am;
        std::string cov = "";
        int status = 0;
        int position = 0;
        std::vector<int> fixed;
        std::vector<int> adapters;
        int left_status = 0;
        int right_status = 0;
        int left_position = 0;
        int meanq = 0;
        int solution = 0;
        int mi = 0;
        int ma = 0;
        int lmi = 0;
        int lma = 0;
        int rmi = 0;
        int rma = 0;
        bool is_string = false;
        uint64_t n = 0;

        int start_position = 0;
        int end_position = 0;

        std::vector<Correction> corrections;

        READ() {
            head = "";
            seq = "";
            strand = "";
            Q = "";

            fm = nullptr;
            am = nullptr;

        }

        READ(const std::string &line_head, const std::string &line_seq, const std::string &line_strand, const std::string &line_Q) {

            head = line_head;
            seq = line_seq;
            strand = line_strand;
            Q = line_Q;

            fm = new uint[seq.length()];
            am = new uint[seq.length()];

            for (uint64_t i = 0; i < seq.length(); i++) {
                fm[i] = 0;
                am[i] = MAXIMAL_PHRED;
            }

            rid = total_rid;
            total_rid += 1;

        }

        uint64_t vlength() {
            return right_status - left_status;
        }

        void reverse() {
            std::string rev = seq;
            get_revcomp(seq, rev);
            seq = rev;
            uint64_t temp = left_status;
            left_status = seq.length() - right_status;
            right_status = seq.length() - temp;
        }

        void only_reverse_seq() {
            std::string rev = seq;
            get_revcomp(seq, rev);
            seq = rev;
        }

        void only_reverse_seq_and_q() {
            std::string rev = seq;
            get_revcomp(seq, rev);
            seq = rev;
            std::reverse(Q.begin(), Q.end());
        }


        READ(const std::string &line_seq, const std::string &line_Q) {

            seq = line_seq;
            Q = line_Q;

            rid = total_rid;
            total_rid += 1;

            fm = nullptr;
            am = nullptr;
        }

        READ(const std::string &line_seq) {

            seq = line_seq;

            rid = total_rid;
            total_rid += 1;

            fm = nullptr;
            am = nullptr;
        }

        uint64_t length() {
            return seq.length();
        }

        ~READ() {
            if (fm != nullptr) delete[] fm;
            if (am != nullptr) delete[] am;
        }

        void save_as_fastq(std::ofstream &fh) {
            fh << head << "\n";
            fh << seq << "\n";
            fh << strand << " " << status << "\n";
            fh << Q << "\n";
        }

        void save_as_read(std::ofstream &fh) {
            fh << seq << "\n";
        }

        void save_as_stats(std::ofstream &fh) {

            fh << "0 0 0 0 0 0 S" << status << " " << position << " " << left_status << " " << left_position << " " << meanq;
            if (adapters.size() > 0) {
                fh << " A ";
                for (uint64_t p = 0; p < adapters.size(); p++) {
                    fh << adapters[p] << " ";
                }
            }
            fh << "\n";
            fh << seq << "\n";
            for (uint64_t p = 0; p < seq.length() - Settings::K+1; p++) {
                fh << (char) am[p];
            }
            fh << "\n";
            for (uint64_t p = 0; p < seq.length()-Settings::K+1; p++) {
                fh << 1;
                if (p != seq.length()-Settings::K) {
                    fh << ',';
                }
            }
            fh << "\n";
            for (uint64_t p = 0; p < seq.length()-Settings::K+1; p++) {
                fh << fm[p];
                if (p != seq.length()-Settings::K) {
                    fh << ',';
                }
            }
            fh << "\n";
        }

        bool set_fm(PHASH_MAP &kmers) {

            bool correct_one = true;

            if (fm == nullptr) {
                fm = new uint[seq.length()];
            }
            for (uint64_t i = 0; i < seq.length() - Settings::K + 1; i++) {
                std::string kmer = seq.substr(i, Settings::K);
                fm[i] = kmers.get_freq(kmer);
                if (fm[i] <= Settings::TRUE_ERRORS) {
                    correct_one = false;
                }

            }
            for (uint64_t i = seq.length() - Settings::K + 1; i < seq.length(); i++) {
                fm[i] = 0;
            }

            return correct_one;

        }

        void set_am(int coverage) {
            /*
             *   Convert Q to freqQ.
             */
            if (am == nullptr) {
                am = new uint[seq.length()];
            }
            for (uint64_t i = 0; i < seq.length() - Settings::K + 1; i++) {
                am[i] = std::min( (int)std::round(fm[i]/coverage), 9);
            }
            for (uint64_t i = seq.length() - Settings::K + 1; i < seq.length(); i++) {
                am[i] = 0;
            }
        }

        void cut_end_from(uint64_t position) {
            if (position == 0) {
                Q = "";
                seq = "";
                return;
            }
            seq = seq.substr(0, position);
            if (Q.length()) Q = Q.substr(0, position);

        }

        void cut_start_to(uint64_t position) {
            if (position+1 >= seq.length()) {
                Q = "";
                seq = "";
                return;
            }
            seq = seq.substr(position+1);
            if (Q.length()) Q = Q.substr(position+1);
        }

        char at(uint64_t pos) {
            return seq[pos];
        }

        char atq(uint64_t pos) {
            return (int)Q[pos]-33;
        }
    };

    struct STUPID_READ {

        int rid = 0;
        std::string seq;
        int status = 1000;
        int start_position = 0;
        int end_position = 0;
        uint32_t position = 0;
        uint64_t n = 0;

        STUPID_READ() {
            seq = "";
        }

        STUPID_READ(const std::string &line_seq) {
            seq = line_seq;
            rid = total_rid;
            total_rid += 1;
        }

        void reverse() {
            std::string rev = seq;
            get_revcomp(seq, rev);
            seq = rev;
        }

        uint64_t length() {
            return seq.length();
        }

        ~STUPID_READ() {
        }

        void save_as_read(std::ofstream &fh) {
            fh << seq << "\n";
        }


        bool set_fm(PHASH_MAP &kmers) {

            for (uint64_t i = 0; i < seq.length() - Settings::K + 1; i++) {
                std::string kmer = seq.substr(i, Settings::K);
                if (kmers.get_freq(kmer) <= Settings::TRUE_ERRORS) {
                    return false;
                }

            }
            return true;
        }


        void cut_end_from(uint64_t position) {
            if (position == 0) {
                seq = "";
                return;
            }
            seq = seq.substr(0, position);

        }

        void cut_start_to(uint64_t position) {
            if (position+1 >= seq.length()) {
                seq = "";
                return;
            }
            seq = seq.substr(position+1);

        }

        char at(uint64_t pos) {
            return seq[pos];
        }

    };

    struct SIMPLE_READ {

        int rid = 0;
        dna_bitset* bitdna;
        uint64_t n = 0;

        SIMPLE_READ(std::string &line_seq) {

            bitdna = new dna_bitset(line_seq.c_str(), line_seq.length());

        }

        uint64_t length() {
            return bitdna->length();
        }

        ~SIMPLE_READ() {
            delete bitdna;
        }

        char at(uint64_t pos) {
            return bitdna->at(pos);
        }

        void save_as_read(std::ofstream &fh) {
            fh << bitdna->to_string() << "\n";
        }

        void cut_end_from(uint64_t position) {

            if (position == 0) {
                delete bitdna;
                bitdna = new dna_bitset("\0", 0);

                return;
            }
            std::string read = std::string(bitdna->to_string());
            read = read.substr(0, position);

            bitdna = new dna_bitset(read.c_str(), bitdna->length());
        }

        void cut_start_to(uint64_t position) {
            if (position+1 >= bitdna->length()) {
                delete bitdna;
                bitdna = new dna_bitset("\0", 0);

                return;
            }
            std::string read = std::string(bitdna->to_string());
            read = read.substr(position+1);

            bitdna = new dna_bitset(read.c_str(), bitdna->length());
        }

        std::string seq() {
            return std::string(bitdna->to_string());
        }

    };

    struct SPRING {

        int rid = 0;
        std::string seq;
        int mi = 0;
        int ma = 0;
        int lmi = 0;
        int lma = 0;
        int rmi = 0;
        int rma = 0;

        SPRING() {
            seq = "";

        }

        SPRING(std::string &line_seq) {

            seq = line_seq;


            rid = total_rid;
            total_rid += 1;

        }

        uint64_t length() {
            return seq.length();
        }

        ~SPRING() {

        }

    };

    struct SPRING_PAIR {

        READ *read1;
        READ *read2;


        int rid = 0;
        std::string seq;
        int mi = 0;
        int ma = 0;
        int lmi = 0;
        int lma = 0;
        int rmi = 0;
        int rma = 0;

        SPRING_PAIR() {
            seq = "";

        }

        SPRING_PAIR(std::string &line_seq) {

            seq = line_seq;


            rid = total_rid;
            total_rid += 1;

            int pos = seq.find('~', 0);
            std::string seq1 = seq.substr(0, pos);
            std::string seq2 = seq.substr(pos+1);
            read1 = new READ(seq1);
            read2 = new READ(seq2);
        }

        SPRING_PAIR(READS::READ* read1, READS::READ* read2) {
            rid = total_rid;
            total_rid += 1;
            read1 = new READ(read1->seq);
            read2 = new READ(read2->seq);
        }

        uint64_t length() {
            return read1->length() + read2->length();
        }

        ~SPRING_PAIR() {

        }

        void save_as_read(std::ofstream &fh) {
            if (read1->length() >= Settings::MINIMAL_READ_LENGTH) {
                fh << read1->seq;
            }
            if (read1->length() >= Settings::MINIMAL_READ_LENGTH && read2->length() >= Settings::MINIMAL_READ_LENGTH) {
                fh << "~";
            }
            if (read2->length() >= Settings::MINIMAL_READ_LENGTH) {
                fh << read2->seq;
            }
            fh << "\n";

        }

        void save_for_jellyfish(std::ofstream &fh) {

            if (read1->length() < Settings::MINIMAL_READ_LENGTH && read2->length() < Settings::MINIMAL_READ_LENGTH) {
                return;
            }

            fh << ">" << rid << "\n";

            if (read1->length() >= Settings::MINIMAL_READ_LENGTH) {
                fh << read1->seq;
            }
            if (read1->length() >= Settings::MINIMAL_READ_LENGTH && read2->length() >= Settings::MINIMAL_READ_LENGTH) {
                fh << "N";
            }
            if (read2->length() >= Settings::MINIMAL_READ_LENGTH) {
                fh << read2->seq;
            }
            fh << "\n";

        }

        void save_as_am(std::ofstream &fh) {

            if (read1->length() >= Settings::MINIMAL_READ_LENGTH) {
                for (uint64_t i = 0; i < read1->length(); i++) {
                    fh << read1->am[i];
                }
            }
            if (read1->length() >= Settings::MINIMAL_READ_LENGTH && read2->length() >= Settings::MINIMAL_READ_LENGTH) {
                fh << "~";
            }
            if (read2->length() >= Settings::MINIMAL_READ_LENGTH) {
                for (uint64_t i = 0; i < read2->length(); i++) {
                    fh << read2->am[i];
                }
            }
            fh << "\n";
        }

        void save_as_fm(std::ofstream &fh) {

            int tf = 0;
            if (read1->length() >= Settings::MINIMAL_READ_LENGTH) {
                for (uint64_t i = 0; i < read1->length(); i++) {
                    tf = read1->fm[i];
                    fh << tf;
                    if (i < read1->length()-1) {
                        fh << " ";
                    }
                }
            }


            if (read1->length() >= Settings::MINIMAL_READ_LENGTH && read2->length() >= Settings::MINIMAL_READ_LENGTH) {
                fh << "~";
            }
            if (read2->length() >= Settings::MINIMAL_READ_LENGTH) {
                for (uint64_t i = 0; i < read2->length(); i++) {
                    tf = read2->fm[i];
                    fh << tf;
                    if (i < read2->length()-1) {
                        fh << " ";
                    }
                }
            }
            fh << "\n";

        }

    };

    struct STUPID_SPRING_PAIR {

        STUPID_READ *read1;
        STUPID_READ *read2;

        int rid = 0;

        STUPID_SPRING_PAIR() {

        }

        STUPID_SPRING_PAIR(std::string &line_seq) {

            rid = total_rid;
            total_rid += 1;
            int pos = line_seq.find('~', 0);
            std::string seq1 = line_seq.substr(0, pos);
            std::string seq2 = line_seq.substr(pos+1);
            read1 = new STUPID_READ(seq1);
            read2 = new STUPID_READ(seq2);
        }

        uint64_t length() {
            return read1->length()+read2->length();
        }

        ~STUPID_SPRING_PAIR() {
        }

        void save_as_read(std::ofstream &fh) {
            if (read1->length() >= Settings::MINIMAL_READ_LENGTH) {
                fh << read1->seq;
            }
            if (read1->length() >= Settings::MINIMAL_READ_LENGTH && read2->length() >= Settings::MINIMAL_READ_LENGTH) {
                fh << "~";
            }
            if (read2->length() >= Settings::MINIMAL_READ_LENGTH) {
                fh << read2->seq;
            }
            fh << "\n";

        }
    };

    struct SIMPLE_SPRING_PAIR {

        SIMPLE_READ *read1;
        SIMPLE_READ *read2;

        int rid = 0;
        std::string seq;

        SIMPLE_SPRING_PAIR() {
            seq = "";
        }

        SIMPLE_SPRING_PAIR(std::string &line_seq) {

            seq = line_seq;
            rid = total_rid;
            total_rid += 1;

            int pos = seq.find('~', 0);
            std::string seq1 = seq.substr(0, pos);
            std::string seq2 = seq.substr(pos+1);
            read1 = new SIMPLE_READ(seq1);
            read2 = new SIMPLE_READ(seq2);

        }


        uint64_t length() {
            return seq.length();
        }

        ~SIMPLE_SPRING_PAIR() {

        }

        void save_as_read(std::ofstream &fh) {
            if (read1->length() >= Settings::MINIMAL_READ_LENGTH) {
                fh << read1->seq();
            }
            if (read1->length() >= Settings::MINIMAL_READ_LENGTH && read2->length() >= Settings::MINIMAL_READ_LENGTH) {
                fh << "~";
            }
            if (read2->length() >= Settings::MINIMAL_READ_LENGTH) {
                fh << read2->seq();
            }
            fh << "\n";

        }

    };

    struct INDEXER {

        uint64_t n_reads = 0;
        uint64_t batch_size = 0;

        uint64_t *index = nullptr;
        std::vector<std::vector<std::tuple<std::string,int,int>>> scenarios;

        const uint64_t BUFSIZE = 1024 * 1024;

        uint64_t * result = nullptr;
        uint64_t * uint64_t_result = nullptr;
        ATOMIC_uint64_t *atomic_result = nullptr;

        void init_int_result(uint64_t size) {
            result = new uint64_t[n_reads*size]; // status1 start1 end1 status2 start2 end2
            for (uint64_t i=0; i<n_reads*size; ++i) {
                result[i] = 0;
            }
        }

        void init_result(uint64_t size) {
            result = new uint64_t[n_reads*size]; // status1 start1 end1 status2 start2 end2
            for (uint64_t i=0; i<n_reads*size; ++i) {
                result[i] = 0;
            }
            std::cout << "result array init done: " << n_reads*size << std::endl;
        }

        void init_atomic_result(uint64_t size) {
            atomic_result = new ATOMIC_uint64_t[n_reads*size]; // status1 start1 end1 status2 start2 end2
            for (uint64_t i=0; i<n_reads*size; ++i) {
                atomic_result[i] = 0;
            }
            std::cout << "result array init done: " << n_reads*size << std::endl;
        }



        void init_uint64_t_result(uint64_t size) {
            uint64_t_result = new uint64_t[n_reads*size]; // status1 start1 end1 status2 start2 end2
            for (uint64_t i=0; i<n_reads*size; ++i) {
                uint64_t_result[i] = 0;
            }
        }

        void init_scenarios() {
            for (uint64_t i=0; i<n_reads; ++i) {
                std::vector<std::tuple<std::string,int,int> > s;
                scenarios.push_back(s);
            }
        }

        void set_result(uint64_t pos, int reg, int val) {
            result[n_reads*reg+pos] = val;
        }

        void set_atomic_result(int reg, uint64_t rid, uint64_t val) {
            atomic_result[n_reads*reg + rid] = val;
        }

        void inc_atomic_result(uint64_t pos, int reg, int val) {
            atomic_result[n_reads*reg+pos] += val;
        }

        void set_result(uint64_t pos, int val) {

            result[pos] = val;
        }

        void set_result(uint64_t pos, uint64_t val) {

            result[pos] = val;
        }

        uint64_t get_int_val(uint64_t pos) {
            return result[pos];
        }

        uint64_t get_atomic_val(int reg, uint64_t rid) {
            return atomic_result[n_reads*reg+rid].load();
        }

        INDEXER(const INDEXER& that) = delete;

        
        void save_index(std::string index_file) {
            emphf::logger() << "Saving index array..." << std::endl;
            std::ofstream fout(index_file, std::ios::out | std::ios::binary);
            emphf::logger() << "Index array size: " << sizeof(uint64_t) * n_reads << std::endl;
            fout.write(reinterpret_cast<const char *> (index), sizeof(uint64_t) * n_reads);
            fout.close();
            emphf::logger() << "Done." << std::endl;
        }

        void load_index(std::string index_file) {

            std::ifstream fout(index_file, std::ios::in | std::ios::binary);
            fout.seekg(0, std::ios::end);
            uint64_t length = fout.tellg();
            fout.close();

            FILE* in = std::fopen(index_file.c_str(), "rb");
            index = (uint64_t*)mmap(NULL, length, PROT_READ, MAP_PRIVATE, fileno(in), 0);
            if (index == nullptr) {
                std::cerr << "Failed index loading" << std::endl;
                exit(10);
            }
            fclose(in);
        }

        void load_index_raw(std::string index_file) {
            uint64_t f = 0;
            uint64_t pos = 0;
            index = new uint64_t[n_reads];
            std::ifstream fout(index_file, std::ios::in | std::ios::binary);
            emphf::logger() << "Loading index array..." << std::endl;
            while(fout.read(reinterpret_cast<char *>(&f), sizeof(f))) {
                index[pos] = f;
                pos += 1;
                if (pos && pos % 1000000 == 0) {
                    emphf::logger() << "\tcomputed: " << pos << std::endl;
                }
            }
            fout.close();
            emphf::logger() << "Done." << std::endl;
        }

        uint64_t build_fastq_index(std::string fastq_file1) {

            emphf::logger() << "\tComputing lines new way... " << std::endl;
            n_reads = 0;

//            if (has_ending(fastq_file1, ".gz") {
//
//            } else {
//                fp = open(fastq_file1.c_str(), O_RDONLY);
//            }

            int fp;
            fp = open(fastq_file1.c_str(), O_RDONLY);
            if (!fp) {
                exit(12);
            }

            std::ifstream fout(fastq_file1, std::ios::in | std::ios::binary);
            fout.seekg(0, std::ios::end);
            uint64_t length = fout.tellg();
            fout.close();

            char buf[BUFSIZE+1];
            int bytes_read;
            uint64_t readed = 0;

            while((bytes_read = read(fp, buf, BUFSIZE)) > 0){
                char* p = buf;
                while ((p = static_cast<char*>(memchr (p, '\n', (buf + bytes_read) - p)))) {
                    ++p;
                    ++n_reads;

                    if (n_reads && n_reads % 100000000 == 0) {
                        emphf::logger() << "\tcomputed lines (first iteration): " << n_reads << " or " << 100*BUFSIZE*readed/length << "%" << std::endl;
                    }
                }
                readed += 1;
            }
            close(fp);
            n_reads /= 4;

            emphf::logger() << n_reads << " reads" << std::endl;

            index = new uint64_t[n_reads];
            fp = open(fastq_file1.c_str(), O_RDONLY);

            uint64_t read_n = 0;
            uint64_t prev_pos = 0;
            readed = 0;


            while((bytes_read = read(fp, buf, BUFSIZE)) > 0){
                char* p = buf;
                while ((p = static_cast<char*>(memchr (p, '\n', (buf + bytes_read) - p)))) {
                    ++p;
                    if (read_n % 4 == 0) {
                        index[read_n/4] = prev_pos;
                    }
                    if (read_n && read_n % 100000000 == 0) {
                        emphf::logger() << "\tcomputed lines (second iteration): " << read_n << " from " << n_reads * 4 << " or " <<
                        100 * (read_n) / (n_reads * 4) << "%" << std::endl;
                    }
                    ++read_n;
                    prev_pos = BUFSIZE*readed + p - buf;
                }

                readed += 1;
            }
            close(fp);
            return n_reads;
        }

        uint64_t build_fastq_index_v2(std::string fastq_file1, uint64_t expected_n_reads) {

            emphf::logger() << "\tComputing lines new way... " << std::endl;
            n_reads = expected_n_reads;

            int fp;
            fp = open(fastq_file1.c_str(), O_RDONLY);
            if (!fp) {
                exit(12);
            }

            std::ifstream fout(fastq_file1, std::ios::in | std::ios::binary);
            fout.seekg(0, std::ios::end);
            // uint64_t length = fout.tellg();
            fout.close();

            char buf[BUFSIZE+1];
            int bytes_read;
            uint64_t readed = 0;

            emphf::logger() << "\treads: " << n_reads << " reads" << std::endl;

            index = new uint64_t[n_reads];
            fp = open(fastq_file1.c_str(), O_RDONLY);

            uint64_t total_reads = 0;
            uint64_t read_n = 0;
            uint64_t prev_pos = 0;
            readed = 0;

            while((bytes_read = read(fp, buf, BUFSIZE)) > 0){
                char* p = buf;
                while ((p = static_cast<char*>(memchr (p, '\n', (buf + bytes_read) - p)))) {
                    ++p;
                    if (read_n % 4 == 0) {
                        index[read_n/4] = prev_pos;
                        total_reads += 1;
                    }
                    if (read_n && read_n % 100000000 == 0) {
                        emphf::logger() << "\tcomputed lines (second iteration): " << read_n << " from " << n_reads * 4 << " or " <<
                                        100 * (read_n) / (n_reads * 4) << "%" << std::endl;
                    }
                    ++read_n;
                    prev_pos = BUFSIZE*readed + p - buf;
                }

                readed += 1;
            }
            close(fp);
            return total_reads;
        }

//        uint64_t build_fasta_index(std::string fai_file) {
//
//            emphf::logger() << "\tbuilding index from fai file... " << std::endl;
//
//            std::ifstream fia_file(fai_file);
//
//            std::string header = "";
//            std::string line;
//            std::vector
//            while (std::getline(infile, line)) {
//                if (line[0] == ">") {
//
//                } else {
//
//                }
//            }
//
//
//            uint64_t length, offset, linebases, linewidth;
//            while (fia_file >> header >> offset >> linebases >> linewidth) {
//
//            }
//
//            fia_file.close();
//
//
//
//
//            n_reads = 0;
//
//            int fp = open(fasta_file.c_str(), O_RDONLY);
//
//            if (!fp) {
//                exit(12);
//            }
//
//            std::ifstream fout(fasta_file, std::ios::in | std::ios::binary);
//            fout.seekg(0, std::ios::end);
//            uint64_t length = fout.tellg();
//            fout.close();
//
//            char buf[BUFSIZE+1];
//            int bytes_read;
//            uint64_t readed = 0;
//
//            while((bytes_read = read(fp, buf, BUFSIZE)) > 0){
//                char* p = buf;
//                while ((p = static_cast<char*>(memchr (p, '\n', (buf + bytes_read) - p)))) {
//                    ++p;
//
//                    if (buf[0] == '>') {
//                        ++n_reads;
//                    }
//
//                    if (n_reads && n_reads % 10000000 == 0) {
//                        emphf::logger() << "\tcomputed: " << n_reads << " or " << 100*BUFSIZE*readed/length << "%" << std::endl;
//                    }
//                }
//                readed += 1;
//            }
//            close(fp);
//            emphf::logger() << n_reads << " sequences" << std::endl;
//
//            index = new uint64_t[n_reads];
//            fp = open(reads_file.c_str(), O_RDONLY);
//
//            uint64_t read_n = 0;
//            uint64_t prev_pos = 0;
//            readed = 0;
//
//            while((bytes_read = read(fp, buf, BUFSIZE)) > 0){
//                char* p = buf;
//                while ((p = static_cast<char*>(memchr (p, '\n', (buf + bytes_read) - p)))) {
//                    ++p;
//                    index[read_n] = prev_pos;
//                    if (read_n && read_n % 10000000 == 0) {
//                        emphf::logger() << "\tcomputed: " << read_n << " from " << n_reads << " or " <<
//                                        100 * (read_n) / (n_reads) << "%" << std::endl;
//                    }
//                    ++read_n;
//                    prev_pos = BUFSIZE*readed + p - buf;
//                }
//
//                readed += 1;
//            }
//            close(fp);
//            return n_reads;
//        }

        uint64_t build_reads_index(const std::string& reads_file) {

            emphf::logger() << "\tComputing lines new way... " << std::endl;
            n_reads = 0;
            int fp = open(reads_file.c_str(), O_RDONLY);

            if (!fp) {
                exit(12);
            }

            std::ifstream fout(reads_file, std::ios::in | std::ios::binary);
            fout.seekg(0, std::ios::end);
            uint64_t length = fout.tellg();
            fout.close();

            char buf[BUFSIZE+1];
            int bytes_read;
            uint64_t readed = 0;

            while((bytes_read = read(fp, buf, BUFSIZE)) > 0){
                char* p = buf;
                while ((p = static_cast<char*>(memchr (p, '\n', (buf + bytes_read) - p)))) {
                    ++p;
                    ++n_reads;

                    if (n_reads && n_reads % 10000000 == 0) {
                        emphf::logger() << "\tcomputed: " << n_reads << " or " << 100*BUFSIZE*readed/length << "%" << std::endl;
                    }
                }
                readed += 1;
            }
            close(fp);
            emphf::logger() << n_reads << " reads" << std::endl;

            index = new uint64_t[n_reads];
            fp = open(reads_file.c_str(), O_RDONLY);

            uint64_t read_n = 0;
            uint64_t prev_pos = 0;
            readed = 0;

            while((bytes_read = read(fp, buf, BUFSIZE)) > 0){
                char* p = buf;
                while ((p = static_cast<char*>(memchr (p, '\n', (buf + bytes_read) - p)))) {
                    ++p;
                    index[read_n] = prev_pos;
                    if (read_n && read_n % 10000000 == 0) {
                        emphf::logger() << "\tcomputed: " << read_n << " from " << n_reads << " or " <<
                        100 * (read_n) / (n_reads) << "%" << std::endl;
                    }
                    ++read_n;
                    prev_pos = BUFSIZE*readed + p - buf;
                }

                readed += 1;
            }
            close(fp);
            return n_reads;
        }

        // void save_fastq_to_file(std::ifstream &l_file,  uint64_t rid) {
        //     std::string line_head = "";
        //     std::string line_seq = "";
        //     std::string line_strand = "";
        //     std::string line_Q = "";

        //     r_file.seekg(index[rid]);

        //     std::getline(r_file, line_head);
        //     std::getline(r_file, line_seq);
        //     std::getline(r_file, line_strand);
        //     std::getline(r_file, line_Q);

        //     READS::READ * read = new READS::READ(line_head, line_seq, line_strand, line_Q);

        //     return read;

        // }

        READS::READ * get_fastq_reads(std::ifstream &r_file, uint64_t rid) {
            std::string line_head = "";
            std::string line_seq = "";
            std::string line_strand = "";
            std::string line_Q = "";

            r_file.seekg(index[rid]);

            std::getline(r_file, line_head);
            std::getline(r_file, line_seq);
            std::getline(r_file, line_strand);
            std::getline(r_file, line_Q);

            READS::READ * read = new READS::READ(line_head, line_seq, line_strand, line_Q);

            return read;

        }

        READS::SPRING_PAIR * get_spring_read(std::ifstream &r_file, uint64_t rid) {
            std::string line_seq = "";
            r_file.seekg(index[rid]);
            std::getline(r_file, line_seq);
            READS::SPRING_PAIR *read = new SPRING_PAIR(line_seq);
            return read;
        }

//        uint64_t build_reads_index_pp(std::string reads_file, int num_threads) {
//
//            /// compute file size
//
//            emphf::logger() << "\tComputing lines new way... " << std::endl;
//            n_reads = 0;
//            int fp = open(reads_file.c_str(), O_RDONLY);
//            if (!fp) {
//                exit(12);
//            }
//            std::ifstream fout(reads_file, std::ios::in | std::ios::binary);
//            fout.seekg(0, std::ios::end);
//            uint64_t length = fout.tellg();
//            fout.close();
//
//            /// split it in batches
//
//            uint64_t batch_size;
//            batch_size = (length / num_threads) + 1;
//            std::vector<std::thread> t;
//            void* results = operator new(num_threads);
//
//            for (uint64_t i = 0; i < num_threads; ++i) {
//                std::vector<uint64_t> t;
//                results[i] = &t;
//            }
//
//            for (uint64_t i = 0; i < num_threads; ++i) {
//                uint64_t start = i * batch_size;
//                uint64_t end = (i + 1) * batch_size;
//
//                if (end > n_reads) {
//                    end = n_reads;
//                }
//
//                t.push_back(std::thread(worker_count_lines,
//                                        std::ref(read_file),
//                                        std::ref(results[i]),
//                                        start,
//                                        end,
//                                        i
//                ));
//            }
//            for (uint64_t i = 0; i < num_threads; ++i) {
//                t[i].join();
//            }
//            emphf::logger() << "\tDone." << std::endl;
//
//            operator delete(results);
//
//            return 0;
//
//
//            char buf[BUFSIZE+1];
//            int bytes_read;
//            uint64_t readed = 0;
//
//            while((bytes_read = read(fp, buf, BUFSIZE)) > 0){
//                char* p = buf;
//                while ((p = static_cast<char*>(memchr (p, '\n', (buf + bytes_read) - p)))) {
//                    ++p;
//                    ++n_reads;
//
//                    if (n_reads && n_reads % 1000000 == 0) {
//                        emphf::logger() << "\tcomputed: " << n_reads << " or " << 100*BUFSIZE*readed/length << "%" << std::endl;
//                    }
//                }
//                readed += 1;
//            }
//            close(fp);
//            emphf::logger() << n_reads << " reads" << std::endl;
//
//            index = new uint64_t[n_reads];
//            fp = open(reads_file.c_str(), O_RDONLY);
//
//            uint64_t read_n = 0;
//            uint64_t prev_pos = 0;
//            readed = 0;
//
//            while((bytes_read = read(fp, buf, BUFSIZE)) > 0){
//                char* p = buf;
//                while ((p = static_cast<char*>(memchr (p, '\n', (buf + bytes_read) - p)))) {
//                    ++p;
//                    index[read_n] = prev_pos;
//                    if (read_n && read_n % 1000000 == 0) {
//                        emphf::logger() << "\tcomputed: " << read_n << " from " << n_reads * 4 << " or " <<
//                        100 * (read_n) / (n_reads * 4) << "%" << std::endl;
//                    }
//                    ++read_n;
//                    prev_pos = BUFSIZE*readed + p - buf;
//                }
//
//                readed += 1;
//            }
//            close(fp);
//            return n_reads;
//        }

        INDEXER() {

        }

        ~INDEXER() {
            if (index != nullptr) {
                delete [] index;
            }
            if (result != nullptr) {
                delete [] result;
            }
            if (uint64_t_result != nullptr) {
                delete [] uint64_t_result;
            }

            if (atomic_result != nullptr) {
                delete [] atomic_result;
            }
        }
    };

    struct READ_PAIR {

        READ *read1;
        READ *read2;
        bool spring;

        READ_PAIR(READ *_read1, READ *_read2) {
            read1 = _read1;
            read2 = _read2;
            spring = false;
        }

        ~READ_PAIR() {
            delete read1;
            delete read2;
        }

        int save_as_fastq(std::ofstream &fh1, std::ofstream &fh2) {
            if (read1->length() >= Settings::MINIMAL_READ_LENGTH && read2->length() >= Settings::MINIMAL_READ_LENGTH) {
                read1->save_as_fastq(fh1);
                read2->save_as_fastq(fh2);
                return 1;
            }
            return 0;
        }
    };

    void read_sreads(std::string file_name, std::vector<READ *> &reads);

    void read_springs(std::string file_name, std::vector<SPRING *> &reads);

    void read_reads(std::string file_name, std::vector<READ *> &reads, uint64_t n);

    void read_pair_reads(std::string file_name1, std::string file_name2, std::vector<READ_PAIR *> &read_pairs);

    void print_read(READ &read, int coverage);

    int get_fm_mode(READ &read);

    void read_spring_pairs(std::string file_name, std::vector<SPRING_PAIR *> &reads, uint64_t n_reads);

    template<typename T>
    uint64_t read_simple_spring_pairs(std::string file_name, std::vector<T *> &reads);

}

#endif //STIRKA_READ_H
