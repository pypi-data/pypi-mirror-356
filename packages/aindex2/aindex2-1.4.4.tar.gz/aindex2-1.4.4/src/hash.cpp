//
// Created by Aleksey Komissarov on 30/08/15.
//

#include <iostream>
#include "hash.hpp"
#include "kmers.hpp"
#include <mutex>
#include <fstream>
#include <string>
#include <sstream>
#include <algorithm>
#include <vector>
#include "emphf/common.hpp"
#include "emphf/perfutils.hpp"
#include "emphf/mphf.hpp"
#include "emphf/base_hash.hpp"
#include <atomic>
#include "emphf/common.hpp"
#include <math.h>
#include "helpers.hpp"


static std::mutex barrier;

void load_only_hash(PHASH_MAP &hash_map, std::string &hash_filename) {

    barrier.lock();
    emphf::logger() << "Hash loading.." << std::endl;
    barrier.unlock();
    std::ifstream is;
    HASHER hasher;
    hash_map.hasher = hasher;
    is.open(hash_filename, std::ios::binary);
    if (!is) {
        emphf::logger() << "Failed to open hash file: " << hash_filename << std::endl;
        exit(10);
    }
    hash_map.hasher.load(is);
    is.close();
}

void construct_hash_unordered_hash(std::string data_file, HASH_MAP &kmers) {
    // Read string steam to kmer2tf dictionary.

    barrier.lock();
    emphf::logger() << "Loading hash..." << std::endl;
    barrier.unlock();


    std::ifstream infile(data_file);
    infile.seekg(0, std::ios::end);
    uint64_t length = infile.tellg();
    char *contents = new char[length+1];
    infile.seekg(0, std::ios::beg);
    infile.read(contents, length);
    infile.close();
    contents[length] = 0;
    std::stringstream ss_contents;
    ss_contents << contents;

    barrier.lock();
    emphf::logger() << "Loaded, converting..." << std::endl;
    barrier.unlock();

    std::string line = "";
    while (std::getline(ss_contents, line)) {
        std::string kmer = "";
        int tf = 0;
        std::istringstream is(line);
        is >> kmer >> tf;
        kmers[get_dna23_bitset(kmer)] = tf;
        // std::cout << kmer << " " << (uint64_t)get_dna23_bitset(kmer) << " " << tf << " " << kmers[get_dna23_bitset(kmer)] << std::endl;
    }
    barrier.lock();
    emphf::logger() << "Kmers: done." << kmers.size() << std::endl;
    barrier.unlock();

    delete [] contents;
}


HASHER construct_emphf(const char *values_filename, const char *keys_filename, const char* hash_filename, std::atomic<uint32_t> *tf_values, uint64_t *checker, uint64_t n) {
    // Read string steam to kmer2tf dictionary.


    barrier.lock();
    emphf::logger() << "Constructing emphf-based hash..." << std::endl;
    barrier.unlock();


    uint32_t *values = new uint32_t[n];
    {
        barrier.lock();
        emphf::logger() << "Loading values into the vault" << std::endl;
        barrier.unlock();
        emphf::file_lines lines(values_filename);
        uint64_t i = 0;
        for (auto& s: lines) {
            values[i] = (uint32_t)atoi(s.data());
            i += 1;
        }
    }

    HASHER hasher;
    barrier.lock();
    emphf::logger() << "Loading mphf" << std::endl;
    barrier.unlock();

    std::ifstream is(hash_filename, std::ios::binary);
    hasher.load(is);

    barrier.lock();
    emphf::logger() << "Upload values to the vault" << std::endl;
    barrier.unlock();

    emphf::file_lines lines(keys_filename);

    uint64_t i = 0;
    for (auto& kmer: lines) {

        emphf::stl_string_adaptor str_adapter;
        uint64_t h = hasher.lookup(kmer.data(), str_adapter);

        if (tf_values[h] != 0) {
            emphf::logger() << "Conflict!!" << std::endl;
            emphf::logger() << i << " " << kmer << " " << h << " " <<  values[i] << std::endl;
            std::cin >> i;
            exit(12);
        }

        checker[h] = get_dna23_bitset(kmer); // too keep checksum for false positives
        tf_values[h] = values[i];
        i += 1;

//        std::cout << i << " " << kmer << " " << h << " " <<  values[i] << std::endl;
    }
    delete [] values;
    return hasher;
}


HASHER construct_emphf_fast(const char *dat_filename, const char* hash_filename, std::atomic<uint32_t> *tf_values, uint64_t *checker, uint64_t n) {
    // Read string steam to kmer2tf dictionary.

    barrier.lock();
    emphf::logger() << "Constructing emphf-based hash..." << std::endl;
    barrier.unlock();

    std::ifstream infile(dat_filename);
    if (!infile) {
        std::cerr << "Cannot open file with values: " << dat_filename << std::endl;
        exit(15);
    }

    barrier.lock();
    emphf::logger() << "Loading values from file" << std::endl;
    barrier.unlock();

    infile.seekg(0, std::ios::end);
    uint64_t length = infile.tellg();
    char *contents = new char[length + 1];
    if (contents == nullptr) {
        emphf::logger() << "Failed to allocate memory for file content (char): " << length << std::endl;
        exit(10);
    }
    infile.seekg(0, std::ios::beg);
    infile.read(contents, length);
    infile.close();
    contents[length] = 0;
    std::stringstream ss_contents;
    ss_contents << contents;

    std::string line = "";

    barrier.lock();
    emphf::logger() << "Loading mphf" << std::endl;
    barrier.unlock();

    HASHER hasher;
    std::ifstream is(hash_filename, std::ios::binary);
    if (!is) {
        emphf::logger() << "Failed to open hash file: " << hash_filename << std::endl;
        exit(10);
    }
    hasher.load(is);
    is.close();

    barrier.lock();
    emphf::logger() << "Processign data to indexes" << std::endl;
    barrier.unlock();

    uint64_t i = 0;

    emphf::stl_string_adaptor str_adapter;

    while (std::getline(ss_contents, line)) {
        std::string kmer = "";
        uint32_t tf = 0;
        std::istringstream is(line);
        is >> kmer >> tf;

        if (i % 1000000 == 0) {
            barrier.lock();
            emphf::logger() << "Hasher: processed " << i << " values " << " from " << n << std::endl;
            barrier.unlock();
        }

        uint64_t h = hasher.lookup(kmer, str_adapter);

        if (tf_values[h] != 0) {
            emphf::logger() << "Conflict!!" << std::endl;
            emphf::logger() << i << " " << kmer << " " << h << " " <<  tf << std::endl;
            std::cin >> i;
            exit(12);
        }

        checker[h] = get_dna23_bitset(kmer);
        tf_values[h] = tf;

        i++;
    }
    delete [] contents;
    barrier.lock();
    emphf::logger() << "Hasher: completed." << std::endl;
    barrier.unlock();
    return hasher;
}

HASHER construct_emphf_for_qmers(const char *dat_filename, const char* hash_filename, uint64_t *checker, uint64_t n) {
    // Read string steam to kmer2tf dictionary.

    barrier.lock();
    emphf::logger() << "Constructing emphf-based hash..." << std::endl;
    barrier.unlock();

    std::ifstream infile(dat_filename);
    if (!infile) {
        std::cerr << "Cannot open file with values: " << dat_filename << std::endl;
        exit(15);
    }

    barrier.lock();
    emphf::logger() << "Loading values from file" << std::endl;
    barrier.unlock();

    infile.seekg(0, std::ios::end);
    uint64_t length = infile.tellg();
    char *contents = new char[length + 1];
    infile.seekg(0, std::ios::beg);
    infile.read(contents, length);
    infile.close();
    contents[length] = 0;
    std::stringstream ss_contents;
    ss_contents << contents;

    std::string line = "";

    barrier.lock();
    emphf::logger() << "Loading mphf" << std::endl;
    barrier.unlock();

    HASHER hasher;
    std::ifstream is(hash_filename, std::ios::binary);
    hasher.load(is);
    is.close();

    barrier.lock();
    emphf::logger() << "Processign data to indexes" << std::endl;
    barrier.unlock();

    uint64_t i = 0;

    emphf::stl_string_adaptor str_adapter;

    while (std::getline(ss_contents, line)) {
        std::string kmer = "";
        uint32_t tf = 0;
        std::istringstream is(line);
        is >> kmer >> tf;

        if (i % 1000000 == 0) {
            barrier.lock();
            emphf::logger() << "Hasher: processed " << i << " values " << " from " << n << std::endl;
            barrier.unlock();
        }

        uint64_t h = hasher.lookup(kmer, str_adapter);
        checker[h] = get_dna23_bitset(kmer);
        i++;
    }
    delete [] contents;
    return hasher;
}


HASHER construct_emphf_fast_wo_kmers(const char *dat_filename, const char* hash_filename, std::atomic<uint32_t> *tf_values, uint64_t n) {
    // Read string steam to kmer2tf dictionary.

    barrier.lock();
    emphf::logger() << "Constructing emphf-based hash..." << std::endl;
    barrier.unlock();

    std::ifstream infile(dat_filename);
    if (!infile) {
        std::cerr << "Cannot open file with values: " << dat_filename << std::endl;
        exit(15);
    }

    barrier.lock();
    emphf::logger() << "Loading values from file" << std::endl;
    barrier.unlock();

    infile.seekg(0, std::ios::end);
    uint64_t length = infile.tellg();
    char *contents = new char[length + 1];
    infile.seekg(0, std::ios::beg);
    infile.read(contents, length);
    infile.close();
    contents[length] = 0;
    std::stringstream ss_contents;
    ss_contents << contents;

    std::string line = "";

    barrier.lock();
    emphf::logger() << "Loading mphf" << std::endl;
    barrier.unlock();

    HASHER hasher;
    std::ifstream is(hash_filename, std::ios::binary);
    hasher.load(is);
    is.close();

    barrier.lock();
    emphf::logger() << "Processign data to indexes" << std::endl;
    barrier.unlock();

    uint64_t i = 0;


    emphf::stl_string_adaptor str_adapter;

    while (std::getline(ss_contents, line)) {
        uint32_t tf = 0;
        std::string kmer = "";

        std::istringstream is(line);
        is >> kmer >> tf;


        uint64_t h = hasher.lookup(kmer, str_adapter);

        if (i % 1000000 == 0) {
            barrier.lock();
            emphf::logger() << "Hasher: processed " << i << " values " << " from " << n << std::endl;
            barrier.unlock();
        }
        tf_values[h] = tf;
        i++;
    }
    delete [] contents;
    return hasher;
}


void load_hash(PHASH_MAP &hash_map, const std::string &hash_filename, const std::string &tf_file, const std::string &kmers_bin_file, const std::string &kmers_text_file) {

    barrier.lock();
    emphf::logger() << "Hash loading.." << std::endl;
    barrier.unlock();

    HASHER hasher = HASHER();
    std::ifstream is;
    hash_map.hasher = hasher;
    is.open(hash_filename, std::ios::binary);
    if (!is) {
        emphf::logger() << "Failed to open hash file: " << hash_filename << std::endl;
        exit(10);
    }
    hash_map.hasher.load(is);
    is.close();
    emphf::logger() << "\tDone." << std::endl;

    uint64_t pos = 0;
    if (Settings::K == 23) {
        is.open(kmers_bin_file, std::ios::binary);
        is.seekg(0, std::ios::end);
        uint64_t length = is.tellg();
        is.close();
        uint64_t n = length / sizeof(uint64_t);

        std::cout << "\tfile: " << kmers_bin_file << " size: " << length << " n=" << n << std::endl;
        hash_map.n = n;
        hash_map.checker = new uint64_t[n];

        uint64_t f = 0;

        emphf::logger() << "Loading kmers to checker..." << std::endl;

        std::ifstream fout3(kmers_bin_file, std::ios::in | std::ios::binary);
        emphf::logger() << "\tkmer array size: " << hash_map.n <<  std::endl;
        while(fout3.read(reinterpret_cast<char *>(&f), sizeof(f))) {
            if (pos && pos % 100000000 == 0) {
                double progress = static_cast<double>(pos) / hash_map.n;
                printProgressBar(progress);                
            }
            hash_map.checker[pos] = f;
            pos += 1;
        }
        printProgressBar(1.0);
        fout3.close();

        emphf::logger() << "\tDone." << std::endl;

    } else {
        std::string kmer;
        std::ifstream myfile(kmers_text_file);
        if (!myfile) {
            emphf::logger() << "Failed to open kmers text file: " << kmers_text_file << std::endl;
            exit(10);
        }

        while (std::getline(myfile, kmer)) {
            hash_map.checker_string.push_back(kmer);
        }
        hash_map.n = hash_map.checker_string.size();
        myfile.close();
    }

    emphf::logger() << "Loading tf to hash..." << std::endl;
    hash_map.tf_values = new ATOMIC[hash_map.n];
    uint32_t f2 = 0;
    pos = 0;
    std::ifstream fout4(tf_file, std::ios::in | std::ios::binary);
    emphf::logger() << "Kmer array size: " << hash_map.n <<  std::endl;
    while(fout4.read(reinterpret_cast<char *>(&f2), sizeof(f2))) {
        if (pos && pos % 100000000 == 0) {
            double progress = static_cast<double>(pos) / hash_map.n;
            printProgressBar(progress);                
        }
        hash_map.tf_values[pos] = f2;
        pos += 1;
    }
    printProgressBar(1.0);
    fout4.close();
    emphf::logger() << "\tDone." << std::endl;


}

void load_hash_only_pf(PHASH_MAP &hash_map, std::string &kmers_bin_file, std::string &hash_filename, bool load_checker) {

    barrier.lock();
    emphf::logger() << "Hash loading.." << std::endl;
    barrier.unlock();

    std::ifstream is;
    is.open(kmers_bin_file, std::ios::binary);
    is.seekg(0, std::ios::end);
    uint64_t length = is.tellg();
    is.close();
    std::cout << length << std::endl;
    hash_map.n = length / sizeof(uint64_t);

    if (load_checker) {

        hash_map.checker = new uint64_t[hash_map.n];
        uint64_t f = 0;
        uint64_t pos = 0;
        std::ifstream fout3(kmers_bin_file, std::ios::in | std::ios::binary);
        emphf::logger() << "Kmer array size: " << hash_map.n << std::endl;
        while (fout3.read(reinterpret_cast<char *>(&f), sizeof(f))) {
            hash_map.checker[pos] = f;
            pos += 1;
        }
        fout3.close();
    }

    HASHER hasher = HASHER();
    hash_map.hasher = hasher;
    is.open(hash_filename, std::ios::binary);
    if (!is) {
        emphf::logger() << "Failed to open hash file: " << hash_filename << std::endl;
        exit(10);
    }
    hash_map.hasher.load(is);
    is.close();
}

void load_hash_full_tf(PHASH_MAP &hash_map, std::string &tf_file, std::string &hash_filename) {

    barrier.lock();
    emphf::logger() << "Hash loading.." << std::endl;
    barrier.unlock();

    std::ifstream is;
    is.open(tf_file, std::ios::binary);
    is.seekg (0, std::ios::end);
    uint64_t length = is.tellg();
    is.close();

    uint64_t n = length / sizeof(uint32_t);
    hash_map.n = n;

    hash_map.tf_values = new ATOMIC[n];
    uint32_t f2 = 0;
    uint64_t pos = 0;
    std::ifstream fout4(tf_file, std::ios::in | std::ios::binary);
    emphf::logger() << "Kmer array size: " << n <<  std::endl;
    while(fout4.read(reinterpret_cast<char *>(&f2), sizeof(f2))) {
        hash_map.tf_values[pos] = f2;
        pos += 1;
    }
    fout4.close();

    HASHER hasher;
    hash_map.hasher = hasher;
    is.open(hash_filename, std::ios::binary);
    if (!is) {
        emphf::logger() << "Failed to open hash file: " << hash_filename << std::endl;
        exit(10);
    }
    hash_map.hasher.load(is);
    is.close();
}

void load_full_hash(PHASH_MAP &hash_map, std::string &hash_filename, int k, uint64_t n) {

    barrier.lock();
    emphf::logger() << "Hash loading.." << std::endl;
    barrier.unlock();

    if (n == 0) {
        n = pow(4, k);
    }
    hash_map.n = n;

    hash_map.tf_values = new ATOMIC[n](); // Value-initialize the array
    if (hash_map.tf_values == nullptr) {
        emphf::logger() << "Failed to allocate tf array: " << n << std::endl;
        exit(10);
    }
    emphf::logger() << "Set all zeros for tf array with size: " << n <<  std::endl;

    emphf::logger() << "Loading hash file: " << hash_filename << std::endl;
    HASHER hasher = HASHER();
    hash_map.hasher = hasher;
    std::ifstream is;
    is.open(hash_filename, std::ios::binary);
    if (!is) {
        emphf::logger() << "Failed to open hash file: " << hash_filename << std::endl;
        exit(10);
    }
    hash_map.hasher.load(is);
    is.close();
    emphf::logger() << "Done." << std::endl;
}


void index_hash(PHASH_MAP &hash_map, std::string &dat_filename, std::string &hash_filename) {

    barrier.lock();
    emphf::logger() << "Hash loading.." << std::endl;
    barrier.unlock();

    emphf::logger() << "Computing a number of kmers..." << std::endl;
    uint64_t n = 0;
    std::string line;
    std::ifstream myfile(dat_filename);
    myfile.seekg(0, std::ios::end);
    uint64_t length = myfile.tellg();
    char *contents = new char[length + 1];
    myfile.seekg(0, std::ios::beg);
    myfile.read(contents, length);
    myfile.close();
    contents[length] = 0;
    std::stringstream ss_contents;
    ss_contents << contents;

    while (std::getline(ss_contents, line)) {
        ++n;
    }

    myfile.close();
    emphf::logger() << "\tkmers: " << n << std::endl;

    hash_map.tf_values = new ATOMIC[n];
    if (!hash_map.tf_values) {
        std::cerr << "Failed to create tf_values: " << n << std::endl;
        exit(5);
    }

    hash_map.checker = new uint64_t[n];
    if (!hash_map.checker) {
        std::cerr << "Failed to create tf_values: " << n << std::endl;
        exit(5);
    }
    hash_map.n = n;

    emphf::logger() << "Init values..." << std::endl;
    for (uint64_t i=0; i < n; i++) {
        hash_map.tf_values[i] = 0;
        hash_map.checker[i] = 0;
    }

    barrier.lock();
    emphf::logger() << "Constructing emphf-based hash..." << std::endl;
    barrier.unlock();

    barrier.lock();
    emphf::logger() << "Loading mphf" << std::endl;
    barrier.unlock();

    HASHER hasher;
    hash_map.hasher = hasher;
    std::ifstream is(hash_filename, std::ios::binary);
    if (!is) {
        emphf::logger() << "Failed to open hash file: " << hash_filename << std::endl;
        exit(10);
    }
    hash_map.hasher.load(is);
    is.close();

    barrier.lock();
    emphf::logger() << "Processign data to indexes" << std::endl;
    barrier.unlock();

    uint64_t i = 0;

    std::stringstream ss_contents2;
    ss_contents2 << contents;
    emphf::stl_string_adaptor str_adapter;

    while (std::getline(ss_contents2, line)) {
        std::string kmer = "";
        uint32_t tf = 0;
        std::istringstream is(line);
        is >> kmer >> tf;

        if (i % 1000000 == 0) {
            barrier.lock();
            emphf::logger() << "Hasher: processed " << i << " values " << " from " << n << std::endl;
            barrier.unlock();
        }

        uint64_t h = hash_map.hasher.lookup(kmer, str_adapter);

        if (hash_map.tf_values[h] != 0) {
            emphf::logger() << "Conflict!!" << std::endl;
            emphf::logger() << i << " " << kmer << " " << h << " " <<  tf << std::endl;
            std::cin >> i;
            exit(12);
        }

        hash_map.checker[h] = get_dna23_bitset(kmer);
        hash_map.tf_values[h] = tf;

//        std::cout << i << " " << kmer << " " << tf << " " << h << std::endl;

        i++;
    }
    delete [] contents;
    barrier.lock();
    emphf::logger() << "Hasher: completed." << std::endl;
    barrier.unlock();

}


void worker_for_fill_index(PHASH_MAP &hash_map, std::string dat_filename, int mock_dat, uint64_t start, uint64_t end, uint64_t step) {

    barrier.lock();
    emphf::logger() << "Processign data to indexes" << std::endl;
    barrier.unlock();

    uint64_t i = 0;
    std::string line;
    emphf::stl_string_adaptor str_adapter;

    std::ifstream myfile(dat_filename);
    while (std::getline(myfile, line)) {

        if (i < start) {
            i += 1;
            continue;
        }
        if (i >= end) {
            break;
        }


        std::string kmer = "";
        uint32_t tf = 0;
        std::istringstream is(line);
        if (!mock_dat) {
            is >> kmer >> tf;
        } else {
            is >> kmer;
        }


        if (i % 1000000 == 0) {
            barrier.lock();
            emphf::logger() << "Hasher: processed " << i << " values " << " from " << end << " in thread: " << step+1 << " or " << 100*(i-start)/(end-start) << "%" <<  std::endl;
            barrier.unlock();
        }

        uint64_t h = hash_map.hasher.lookup(kmer, str_adapter);

        if (hash_map.tf_values[h] != 0) {
            emphf::logger() << "Conflict!!" << std::endl;
            emphf::logger() << i << " " << kmer << " " << h << " " <<  tf << std::endl;
            std::cin >> i;
            exit(12);
        }

        hash_map.checker[h] = get_dna23_bitset(kmer);
        hash_map.tf_values[h] = tf;
        i++;
    }
    myfile.close();
}


void worker_for_fill_index_any(PHASH_MAP &hash_map, std::string dat_filename, int mock_dat, uint64_t start, uint64_t end, uint64_t step) {

    barrier.lock();
    emphf::logger() << "Processign data to indexes" << std::endl;
    barrier.unlock();

    uint64_t i = 0;
    std::string line;
    emphf::stl_string_adaptor str_adapter;

    std::ifstream myfile(dat_filename);
    while (std::getline(myfile, line)) {

        if (i < start) {
            i += 1;
            continue;
        }
        if (i >= end) {
            break;
        }


        std::string kmer = "";
        uint32_t tf = 0;
        std::istringstream is(line);
        if (!mock_dat) {
            is >> kmer >> tf;
        } else {
            is >> kmer;
        }


        if (i % 1000000 == 0) {
            barrier.lock();
            emphf::logger() << "Hasher: processed " << i << " values " << " from " << end << " in thread: " << step+1 << " or " << 100*(i-start)/(end-start) << "%" <<  std::endl;
            barrier.unlock();
        }

        uint64_t h = hash_map.hasher.lookup(kmer, str_adapter);

        if (hash_map.tf_values[h] != 0) {
            emphf::logger() << "Conflict!!" << std::endl;
            emphf::logger() << i << " " << kmer << " " << h << " " <<  tf << std::endl;
            std::cin >> i;
            exit(12);
        }

        hash_map.tf_values[h] = tf;
        i++;
    }
    myfile.close();
}

void index_hash_pp(PHASH_MAP &hash_map, std::string &dat_filename, std::string &hash_filename, int num_threads, int mock_dat) {

    barrier.lock();
    emphf::logger() << "Hash loading.." << std::endl;
    barrier.unlock();

    emphf::logger() << "Computing a number of kmers..." << std::endl;
    uint64_t n = 0;
    std::string line;
    std::ifstream myfile(dat_filename);
    while (std::getline(myfile, line)) {
        ++n;
    }
    myfile.close();


    emphf::logger() << "\tkmers: " << n << std::endl;

    hash_map.tf_values = new ATOMIC[n];
    if (!hash_map.tf_values) {
        std::cerr << "Failed to create tf_values: " << n << std::endl;
        exit(5);
    }
    hash_map.checker = new uint64_t[n];
    if (!hash_map.checker) {
        std::cerr << "Failed to create tf_values: " << n << std::endl;
        exit(5);
    }
    hash_map.n = n;

    barrier.lock();
    emphf::logger() << "Loading mphf" << std::endl;
    barrier.unlock();

    HASHER hasher = HASHER();
    hash_map.hasher = hasher;
    std::ifstream is(hash_filename, std::ios::binary);
    if (!is) {
        emphf::logger() << "Failed to open hash file: " << hash_filename << std::endl;
        exit(10);
    }
    hash_map.hasher.load(is);
    is.close();

    barrier.lock();
    emphf::logger() << "Fill tf and checkers with zeros " << std::endl;
    barrier.unlock();

    for (uint64_t i=0; i < n; i++) {
        hash_map.tf_values[i] = 0;

        if (Settings::K == 23) {
            hash_map.checker[i] = 0;
        } else {
            ;
        }
    }

    emphf::logger() << "4. Fill index concurrently..." << std::endl;
    uint64_t batch_size;
    batch_size = (n / num_threads) + 1;
    std::vector<std::thread> t;

    emphf::logger() << "\t init result array..." << std::endl;
    for (int i = 0; i < num_threads; ++i) {
        uint64_t start = i * batch_size;
        uint64_t end = (i + 1) * batch_size;

        if (end > n) {
            end = n;
        }

        if (Settings::K == 23) {
            t.push_back(std::thread(worker_for_fill_index,
                                    std::ref(hash_map),
                                    std::ref(dat_filename),
                                    mock_dat,
                                    start,
                                    end,
                                    i
            ));
        } else {
            t.push_back(std::thread(worker_for_fill_index_any,
                                    std::ref(hash_map),
                                    std::ref(dat_filename),
                                    mock_dat,
                                    start,
                                    end,
                                    i
            ));
        }


    }

    for (int i = 0; i < num_threads; ++i) {
        t[i].join();
    }

    barrier.lock();
    emphf::logger() << "Hasher: completed." << std::endl;
    barrier.unlock();
}




void load_hash_for_qkmer(PHASH_MAP &hash_map, uint64_t n, std::string &data_filename, std::string &hash_filename) {

    barrier.lock();
    emphf::logger() << "Hash loading.." << std::endl;
    barrier.unlock();

    hash_map.left_qtf_values = new ATOMIC_LONG[n];
    hash_map.right_qtf_values = new ATOMIC_LONG[n];
    if (!hash_map.left_qtf_values) {
        std::cerr << "Failed to create left_qtf_values: " << n << std::endl;
        exit(5);
    }
    if (!hash_map.right_qtf_values) {
        std::cerr << "Failed to create right_qtf_values: " << n << std::endl;
        exit(5);
    }

    hash_map.checker = new uint64_t[n];
    if (!hash_map.checker) {
        std::cerr << "Failed to create tf_values: " << n << std::endl;
        exit(5);
    }
    hash_map.n = n;

    for (uint64_t i=0; i < n; i++) {
        hash_map.left_qtf_values[i] = 0;
        hash_map.right_qtf_values[i] = 0;
        hash_map.checker[i] = 0;
    }
    hash_map.hasher = construct_emphf_for_qmers(data_filename.c_str(), hash_filename.c_str(), hash_map.checker, n);

}

void construct_hash_unordered_hash_illumina(std::string data_file, HASH_MAP13 &kmers) {

    barrier.lock();
    emphf::logger() << "Loading custom map hash..." << std::endl;
    barrier.unlock();

    std::ifstream infile(data_file);

    if (!infile) {
        barrier.lock();
        std::cerr << "Cannot open file for reading: " << data_file << std::endl;
        barrier.unlock();
        return;
    }

    infile.seekg(0, std::ios::end);
    uint64_t length = infile.tellg();
    char *contents = new char[length+1];


    infile.seekg(0, std::ios::beg);
    infile.read(contents, length+1);
    infile.close();
    contents[length] = 0;
    std::stringstream ss_contents;
    ss_contents << contents;

    std::string line = "";
    while (std::getline(ss_contents, line)) {
        std::string kmer = "";
        int tf = 0;
        std::istringstream is(line);
        is >> kmer >> tf;
        std::transform(kmer.begin(), kmer.end(),kmer.begin(), ::toupper);
        kmers[kmer] = tf;
    }

    delete [] contents;

}

void lu_compressed_worker(int worker_id, uint64_t start, uint64_t end, char *contents,  ATOMIC64 *positions, ATOMIC64 *ppositions, uint64_t* indices, PHASH_MAP &hash_map) {

    emphf::stl_string_adaptor str_adapter2;
    static std::mutex barrier2;

    int k = Settings::K;
    char ckmer[k+1];

    uint64_t total = end - start;
    int pcompleted = 0;
    int last_value = 0;
    uint64_t done = 0;
    uint64_t nreads = 0;

    // move start if kmer contains new line or separators
    while (start < end-k+1) {
        bool found = false;
        for (uint64_t i = start; i < start+k; ++i) {
            if (contents[i] == '\n' || contents[i] == '~' || contents[i] == '?') {
                start = i+1;
                found = true;
                break;
            }
        }
        if (!found) {
            break;
        }
    }

    barrier2.lock();
    emphf::logger() << "Worker " << worker_id << " started" <<  std::endl;
    barrier2.unlock();

    for (uint64_t i = start; i < end-k+1; ++i) {

        // progress bar
        done += 1;
        pcompleted = int((100 * done)/total);
        if (pcompleted % 5 == 0 && pcompleted != last_value) {
            barrier2.lock();
            emphf::logger() << "Worker " << worker_id << " completed " << pcompleted << "%, total " << nreads <<  std::endl;
            barrier2.unlock();
            last_value = pcompleted;
        }

        // move start if kmer contains a new line or separators
        bool skip = false;
        for(int j=0; j<k; ++j) {
            if (contents[i+j] == '\n' || contents[i+j] == '~' || contents[i+j] == 'N') {
                skip = true;
                break;
            }
        }
        if (skip) {
            continue;
        }

        std::memcpy(ckmer, &contents[i], k);
        ckmer[k] = '\0';
        std::string kmer(ckmer);

        if (k == 13) {

            auto h1 = hash_map.hasher.lookup(kmer, str_adapter2);
            uint64_t h2 = ppositions[h1].fetch_add(1, std::memory_order_seq_cst);
            positions[indices[h1]+h2] = i+1;

        } else {
            uint64_t ukmer = get_dna23_bitset(kmer);
            std::string rev_kmer = "NNNNNNNNNNNNNNNNNNNNNNN";
            uint64_t urev_kmer = reverseDNA(ukmer);
            get_bitset_dna23(urev_kmer, rev_kmer);
            if (ukmer <= urev_kmer) {
                auto h1 = hash_map.hasher.lookup(kmer, str_adapter2);
                if (h1 >= hash_map.n || hash_map.checker[h1] != ukmer) {
                    continue;
                }
                uint64_t h2 = ppositions[h1].fetch_add(1, std::memory_order_seq_cst);
                if (h2 >= hash_map.tf_values[h1]) {
                    continue;
                }
                positions[indices[h1]+h2] = i+1;
            } else {
                auto h1 = hash_map.hasher.lookup(rev_kmer, str_adapter2);
                if (h1 >= hash_map.n || hash_map.checker[h1] != urev_kmer) {
                    continue;
                }
                uint64_t h2 = ppositions[h1].fetch_add(1, std::memory_order_seq_cst);
                if (h2 >= hash_map.tf_values[h1]) {
                    continue;
                }
                positions[indices[h1]+h2] = i+1;
            }
        }
    }

    barrier2.lock();
    emphf::logger() << "Worker " << worker_id << " finished." << std::endl;
    barrier2.unlock();
    return;
}