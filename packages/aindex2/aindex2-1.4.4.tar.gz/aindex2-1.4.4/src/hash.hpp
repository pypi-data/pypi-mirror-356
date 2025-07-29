//
// Created by Aleksey Komissarov on 30/08/15.
//

#ifndef STIRKA_HASH_H
#define STIRKA_HASH_H

#include <unordered_map>
#include <string>
#include "emphf/common.hpp"
#include "emphf/perfutils.hpp"
#include "emphf/mphf.hpp"
#include "emphf/base_hash.hpp"
#include <atomic>
#include "kmers.hpp"
#include <stdint.h>
#include "settings.hpp"
#include <mutex>
#include <thread>
#include <functional>
#include <vector>
#include <algorithm>
#include <string_view>

typedef emphf::mphf<emphf::jenkins64_hasher> HASHER;
typedef int *VAULT;

typedef std::atomic<uint32_t> ATOMIC;
typedef std::atomic<unsigned long> ATOMIC_LONG;

typedef std::atomic<uint8_t> ATOMIC8;
typedef std::atomic<uint64_t> ATOMIC64;

typedef std::unordered_map<uint64_t, int> HASH_MAP;
typedef std::unordered_map<std::string, int> HASH_MAP13;


struct Stats {

    uint64_t zero = 0;
    uint64_t unique = 0;
    uint64_t distinct = 0;
    uint64_t total = 0;
    uint64_t max_count = 0;
    uint64_t coverage = 0;

    int *profile;

    Stats() {
        profile = nullptr;
    }

    void init(uint64_t coverage) {
        zero = 0;
        unique = 0;
        distinct = 0;
        total = 0;
        max_count = 0;
        if (profile != nullptr) {
            delete [] profile;
            profile = nullptr;
        }
        profile = new int[coverage+coverage/2];
        for (uint64_t i=0; i<coverage+coverage/2; i++) {
            profile[i] = 0;
        }

//
//        for (uint64_t i=0; i < coverage+coverage/2; ++i) {
//            std::cout << i << " " << profile[i] << std::endl;
//        }
    }

    ~Stats() {
        if (profile != nullptr) {
            delete [] profile;
        }

    }
};

struct PHASH_MAP {

    HASHER hasher;
    ATOMIC *tf_values;
    ATOMIC_LONG *left_qtf_values;
    ATOMIC_LONG *right_qtf_values;
    uint64_t *checker;
    std::vector<std::string> checker_string;
    uint64_t n = 0;

    Stats stats;

    emphf::stl_string_adaptor str_adapter;

    PHASH_MAP() {
        tf_values = nullptr;
        left_qtf_values = nullptr;
        right_qtf_values = nullptr;
        checker = nullptr;
        n = 0;

    }

    uint64_t get_n() {
        return n;
    }

    uint64_t size() {
        return n;
    }

    ~PHASH_MAP() {
        if (tf_values != nullptr) {
            delete [] tf_values;
            tf_values = nullptr;
        }
        if (left_qtf_values != nullptr) delete [] left_qtf_values;
        if (right_qtf_values != nullptr) delete [] right_qtf_values;
        if (checker != nullptr) delete [] checker;
    }

    inline uint32_t get_freq(uint64_t kmer) {
        std::string _kmer = "NNNNNNNNNNNNNNNNNNNNNNN";
        std::string _rev_kmer = "NNNNNNNNNNNNNNNNNNNNNNN";
        get_bitset_dna23(kmer, _kmer);
        auto h1 = hasher.lookup(_kmer, str_adapter);
        // try to find forward
        if (h1 < n && checker[h1] == kmer) {
            return tf_values[h1].load();
        }
        // else try to find reverse
        uint64_t rev_kmer = reverseDNA(kmer);
        get_bitset_dna23(rev_kmer, _rev_kmer);
        auto h2 = hasher.lookup(_rev_kmer, str_adapter);
        if (h2 < n && checker[h2] == rev_kmer) {
            return tf_values[h2].load();
        }
        return 0;
    }

    inline uint64_t get_hash_value(std::string_view kmer) {
        return hasher.lookup(kmer, str_adapter);
    }

    inline uint64_t get_index_unsafe(std::string_view kmer) {
        return hasher.lookup(kmer, str_adapter);
    }

    inline uint64_t get_pfid(std::string_view _kmer) {
        uint64_t kmer = get_dna23_bitset(_kmer);
        std::string _rev_kmer = "NNNNNNNNNNNNNNNNNNNNNNN";
        uint64_t rev_kmer = reverseDNA(kmer);
        get_bitset_dna23(rev_kmer, _rev_kmer);
        if (_kmer.compare(_rev_kmer) <= 0) {
            uint64_t h1 = hasher.lookup(_kmer, str_adapter);
            if (h1 < n && checker[h1] == kmer) {
                return h1;
            } else {
                return n;
            }
        } else {
            uint64_t h1 = hasher.lookup(_rev_kmer, str_adapter);
            if (h1 < n && checker[h1] == rev_kmer) {
                return h1;
            } else {
                return n;
            }
        }
    }

    inline uint64_t get_pfid_by_umer_safe(uint64_t kmer) {

        std::string _kmer = "NNNNNNNNNNNNNNNNNNNNNNN";
        get_bitset_dna23(kmer, _kmer, Settings::K);

        std::string _rev_kmer = "NNNNNNNNNNNNNNNNNNNNNNN";
        uint64_t rev_kmer = reverseDNA(kmer);
        get_bitset_dna23(rev_kmer, _rev_kmer);
        if (_kmer.compare(_rev_kmer) <= 0) {
            uint64_t h1 = hasher.lookup(_kmer, str_adapter);
            if (h1 < n && checker[h1] == kmer) {
                return h1;
            } else {
                return n;
            }
        } else {
            uint64_t h1 = hasher.lookup(_rev_kmer, str_adapter);
            if (h1 < n && checker[h1] == rev_kmer) {
                return h1;
            } else {
                return n;
            }
        }
    }

    inline uint64_t get_pfid_by_umer_unsafe(uint64_t kmer) {
        std::string _kmer = "NNNNNNNNNNNNNNNNNNNNNNN";
        get_bitset_dna23(kmer, _kmer);
        return hasher.lookup(_kmer, str_adapter);
    }

    inline uint32_t get_freq(std::string_view kmer) {
        uint64_t _kmer = get_dna23_bitset(kmer);
        return get_freq(_kmer);
    }

    inline uint64_t get_kmer(uint64_t p) {
        return checker[p];
    }

    inline std::string get_kmer_string(uint64_t p) {
        std::string _kmer = "NNNNNNNNNNNNNNNNNNNNNNN";
        get_bitset_dna23(checker[p], _kmer, Settings::K);
        return _kmer;
    }

    inline ATOMIC& get_atomic(uint64_t kmer) {
        std::string _kmer = "NNNNNNNNNNNNNNNNNNNNNNN";
        get_bitset_dna23(kmer, _kmer);
        return tf_values[hasher.lookup(_kmer, str_adapter)];
    }

    inline void increase(std::string &kmer) {
        auto h1 = hasher.lookup(kmer, str_adapter);
        uint64_t _kmer = get_dna23_bitset(kmer);
        if (h1 < n && checker[h1] == _kmer) {
            tf_values[h1]++;
        } else {
            std::string _rev_kmer = "NNNNNNNNNNNNNNNNNNNNNNN";
            uint64_t rev_kmer = reverseDNA(_kmer);
            get_bitset_dna23(rev_kmer, _rev_kmer);
            auto h2 = hasher.lookup(_rev_kmer, str_adapter);
            if (h2 < n && checker[h2] == rev_kmer) {
                tf_values[h2]++;
            }
        }
    }

    inline void increase_raw(std::string &kmer) {
        auto h1 = hasher.lookup(kmer, str_adapter);
        tf_values[h1]++;
    }

    inline void decrease(std::string &kmer) {
        auto h1 = hasher.lookup(kmer, str_adapter);
        uint64_t _kmer = get_dna23_bitset(kmer);
        if (h1 < n && checker[h1] == _kmer && tf_values[h1].load()>0) {
            if (tf_values[h1] > 0) tf_values[h1]--;
        } else {
            std::string _rev_kmer = "NNNNNNNNNNNNNNNNNNNNNNN";
            uint64_t rev_kmer = reverseDNA(_kmer);
            get_bitset_dna23(rev_kmer, _rev_kmer);
            auto h2 = hasher.lookup(_rev_kmer, str_adapter);
            if (h2 < n && checker[h2] == rev_kmer) {
                if (tf_values[h2] > 0) tf_values[h2]--;
            }
        }
    }

    void save_values(std::string &file_name, bool SKIP_ZEROS) {
        std::ofstream fh(file_name);

        if (!fh) {
            std::cerr << "Cannot open file for writting.";
            exit(12);
        }

        uint64_t zeros = 0;
        uint64_t ones = 0;
        uint64_t other = 0;
        for (uint64_t i=0; i < n; i++) {
            std::string kmer = "NNNNNNNNNNNNNNNNNNNNNNN";
            get_bitset_dna23(checker[i], kmer);
            uint64_t tf = tf_values[i].load();
            if (tf == 1) ones += 1;
            if (tf == 0) zeros += 1;
            if (tf > 1) other += 1;
            if (tf > 0 || !SKIP_ZEROS) {
                fh << kmer << "\t" << tf << "\n";
            }
        }
        fh.close();

        std::cout << "\tZeros: " << zeros << std::endl;
        std::cout << "\tOnes: " << ones << std::endl;
        std::cout << "\tOther: " << other << std::endl;

    }

    void reset_tf() {
        for (uint64_t i=0; i < n; i++) {
            tf_values[i] = 0;
        }
    }

    void set_stats(uint64_t coverage) {

        stats.init(coverage);

        uint64_t max_coverage = coverage + coverage/2;

        for (uint64_t i=0; i < n; i++) {
            stats.total += tf_values[i];
            if (tf_values[i] == 0) {
                stats.zero += 1;
            }
            if (tf_values[i] == 1) {
                stats.unique += 1;
            }
            if (tf_values[i] > 0) {
                stats.distinct += 1;
            }
            if (tf_values[i] < max_coverage) {
                stats.profile[tf_values[i]] += 1;
            } else {
                stats.profile[max_coverage-1] += 1;
            }
            if (tf_values[i] > stats.max_count) {
                stats.max_count = tf_values[i];
            }
        }
    }

    void print_stats() {

        std::cout << "Zero: " << stats.zero << std::endl;
        std::cout << "Unique: " << stats.unique << std::endl;
        std::cout << "Distinct: " << stats.distinct << std::endl;
        std::cout << "Total: " << stats.total << std::endl;
        std::cout << "Coverage: " << stats.coverage << std::endl;
        std::cout << "Max value: " << stats.max_count << std::endl;

    }

    void print_stats_profile(uint64_t coverage) {
        for (uint64_t i=0; i<coverage+coverage/2;i++) {
            std::cout << i << ":" << stats.profile[i] << " ";
        }
        std::cout << std::endl;
    }

    std::string print_and_set_coverage(uint64_t coverage) {
        set_stats(coverage);
        print_stats_profile(coverage);
        std::string res = "Z: " + std::to_string(stats.zero) + " U: " + std::to_string(stats.unique) + " D: " + std::to_string(stats.distinct) + " T: " + std::to_string(stats.total) + " C: " + std::to_string(stats.coverage) + " M: " + std::to_string(stats.max_count);
        std::cout << res << std::endl;
        return res;
    }

private:

};

void lu_compressed_worker(int worker_id, uint64_t start, uint64_t end, char *contents,  ATOMIC64 *positions, ATOMIC64 *ppositions, uint64_t* indices, PHASH_MAP &hash_map);

struct AIndexCompressed {

    uint64_t* indices; // position indices
    ATOMIC64* ppositions; // position completness
    ATOMIC64* positions; // position itself
    uint64_t total_size = 0;
    uint64_t max_tf = 0;

    AIndexCompressed(PHASH_MAP &hash_map) {

        emphf::logger() << "...Allocate indices..." << std::endl;
        indices = new uint64_t[hash_map.n+1];
        if (indices == nullptr) {
            emphf::logger() << "Failed to allocate memory for positions: " << hash_map.n+1 << std::endl;
            exit(10);
        }
        indices[0] = 0;
        for (uint64_t i=1; i<hash_map.n+1; ++i) {
            indices[i] = indices[i-1] + hash_map.tf_values[i-1];
            total_size += hash_map.tf_values[i-1];
            max_tf = std::max(max_tf, (uint64_t)hash_map.tf_values[i-1]);
        }
        std::cout << "\tmax_tf: " << max_tf << std::endl;
        std::cout << "\ttotal_size: " << total_size << std::endl;
        emphf::logger() << "...Done." << std::endl;

        std::cout << "...Allocate ppositions..." << std::endl;
        ppositions = new ATOMIC64[hash_map.n](); // Value-initialize the array
        if (ppositions == nullptr) {
            emphf::logger() << "Failed to allocate memory for positions: " << hash_map.n << std::endl;
            exit(10);
        }
        emphf::logger() << "...Done." << std::endl;

        std::cout << "...Allocate positions..." << std::endl;
        positions = new ATOMIC64[total_size](); // Value-initialize the array
        if (positions == nullptr) {
            emphf::logger() << "Failed to allocate memory for positions: " << total_size << std::endl;
            exit(10);
        }
        emphf::logger() << "...Done." << std::endl;
        emphf::logger() << "Done." << std::endl;
    }

    ~AIndexCompressed() {
        if (indices != nullptr) delete [] indices;
        if (ppositions != nullptr) delete [] ppositions;
        if (positions != nullptr) delete [] positions;
    }

    void fill_index_from_reads(char *contents, uint64_t length, uint num_threads, PHASH_MAP &hash_map) {

        emphf::logger() << "Building index..." << " " << length << " " <<  num_threads << " " << Settings::K << std::endl;

        uint64_t batch_size = (length / num_threads) + 1;
        std::vector<std::thread> t;

        for (uint64_t worker_id = 0; worker_id < num_threads; ++worker_id) {
            uint64_t start = worker_id * batch_size;
            uint64_t end = (worker_id + 1) * batch_size;
            if (end > length) {
                end = length;
            }
            // inner worker takes kmers from start..end-k+1
            if (start > Settings::K) {
                start -= (Settings::K-1);
            }

            t.push_back(std::thread(
                    lu_compressed_worker,
                    worker_id,
                    start,
                    end,
                    contents,
                    std::ref(positions),
                    std::ref(ppositions),
                    std::ref(indices),
                    std::ref(hash_map)
            )
            );
        }

        for (uint64_t worker_id = 0; worker_id < num_threads; ++worker_id) {
            t[worker_id].join();
        }

        emphf::logger() << "\tDone." << std::endl;
    }

    void get_positions(std::string kmer, uint32_t* r, PHASH_MAP &hash_map) {

        memset(r, 0, max_tf * sizeof(uint32_t));
        auto h1 = hash_map.get_pfid(kmer);
        uint64_t j = 0;
        uint64_t start = indices[h1];
        uint64_t end = indices[h1+1];
        for (uint64_t i=start; i < end; ++i) {
            r[j] = positions[i];
            j += 1;
        }
    }

    void set_positions(std::string kmer, uint32_t* r, PHASH_MAP &hash_map) {
        auto h1 = hash_map.get_pfid(kmer);
        uint64_t j = 0;
        uint64_t start = indices[h1];
        uint64_t end = indices[h1+1];
        for (uint64_t i=start; i < end; ++i) {
            positions[i] = r[j];
            j += 1;
        }
    }

    void save(std::string index_bin_file, std::string indices_bin_file, PHASH_MAP &hash_map) {
        //
        
        emphf::logger() << "Saving index.bin array..." << std::endl;
        std::ofstream fout3(index_bin_file, std::ios::out | std::ios::binary);
        emphf::logger() << "Positions array size: " << sizeof(uint64_t) * total_size << std::endl;
        fout3.write(reinterpret_cast<const char *> (positions), sizeof(uint64_t) * total_size);
        fout3.close();

        emphf::logger() << "Saving indices array..." << std::endl;
        std::ofstream fout4(indices_bin_file, std::ios::out | std::ios::binary);
        emphf::logger() << "Indices array size: " << sizeof(uint64_t) * total_size << std::endl;
        fout4.write(reinterpret_cast<const char *> (indices), sizeof(uint64_t) * (hash_map.n+1));
        fout4.close();

        emphf::logger() << "\tDone." << std::endl;
    }

private:

};

struct AtomicCounter {

    std::atomic<uint32_t> value;

    void increment(){
        ++value;
    }

    void decrement(){
        --value;
    }

    int get(){
        return value.load();
    }
};

extern void load_hash(PHASH_MAP &hash_map, const std::string &hash_filename, const std::string &tf_file, const std::string &kmers_bin_file, const std::string &kmers_text_file);
extern void load_only_hash(PHASH_MAP &hash_map, std::string &hash_filename);
void construct_hash_unordered_hash_illumina(std::string data_file, HASH_MAP13 &kmers);
void load_hash_for_qkmer(PHASH_MAP &hash_map, uint64_t n, std::string &data_filename, std::string &hash_filename);
void index_hash(PHASH_MAP &hash_map, std::string &dat_filename, std::string &hash_filename);
void index_hash_pp(PHASH_MAP &hash_map, std::string &dat_filename, std::string &hash_filename, int num_threads, int mock_dat=0);
void load_hash_only_pf(PHASH_MAP &hash_map, std::string &kmers_bin_file, std::string &hash_filename, bool load_checker=true);
void load_full_hash(PHASH_MAP &hash_map, std::string &hash_filename, int k, uint64_t n);
void load_hash_full_tf(PHASH_MAP &hash_map, std::string &tf_file, std::string &hash_filename);


#endif //STIRKA_HASH_H
