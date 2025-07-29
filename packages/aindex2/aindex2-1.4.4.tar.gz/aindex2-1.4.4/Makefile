CXX = g++
# Basic compilation flags (without architecture)
BASE_CXXFLAGS = -std=c++17 -pthread -O3 -fPIC -Wall -Wextra

LDFLAGS = -shared -Wl,--export-dynamic
SRC_DIR = src
OBJ_DIR = obj
INCLUDES = $(SRC_DIR)/helpers.hpp $(SRC_DIR)/debrujin.hpp $(SRC_DIR)/read.hpp $(SRC_DIR)/kmers.hpp $(SRC_DIR)/settings.hpp $(SRC_DIR)/hash.hpp
SOURCES = $(SRC_DIR)/helpers.cpp $(SRC_DIR)/debrujin.cpp $(SRC_DIR)/read.cpp $(SRC_DIR)/kmers.cpp $(SRC_DIR)/settings.cpp $(SRC_DIR)/hash.cpp
OBJECTS = $(patsubst $(SRC_DIR)/%.cpp,$(OBJ_DIR)/%.o,$(SOURCES))
BIN_DIR = bin
PACKAGE_DIR = aindex/core
PREFIX = $(CONDA_PREFIX)
INSTALL_DIR = $(PREFIX)/bin

# 1. FIRST, determine architecture
# Check ARCHFLAGS (set by cibuildwheel)
ifdef ARCHFLAGS
    ifeq ($(findstring arm64,$(ARCHFLAGS)),arm64)
        TARGET_ARCH = arm64
    else ifeq ($(findstring x86_64,$(ARCHFLAGS)),x86_64)
        TARGET_ARCH = x86_64
    endif
endif

# Set TARGET_ARCH by default if not defined
TARGET_ARCH ?= $(shell uname -m)

# 2. THEN, determine cross-compilation flags
CROSS_COMPILE_FLAGS =
UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Darwin)
	# On Apple Silicon (arm64) when building for x86_64
    ifeq ($(TARGET_ARCH),x86_64)
        ifeq ($(shell uname -m),arm64)
            CROSS_COMPILE_FLAGS = -arch x86_64
        endif
    endif
	# On Intel (x86_64) when building for arm64
    ifeq ($(TARGET_ARCH),arm64)
        ifeq ($(shell uname -m),x86_64)
            CROSS_COMPILE_FLAGS = -arch arm64
        endif
    endif
endif

# Python configuration
PYTHON_CMD := $(shell \
    if [ -n "$$CIBUILDWHEEL" ] && which python >/dev/null 2>&1; then \
        echo python; \
    elif /opt/homebrew/opt/python@3.11/bin/python3.11 --version >/dev/null 2>&1; then \
        echo /opt/homebrew/opt/python@3.11/bin/python3.11; \
    elif python3.11 --version >/dev/null 2>&1; then \
        echo python3.11; \
    elif python3 --version >/dev/null 2>&1; then \
        echo python3; \
    elif python --version >/dev/null 2>&1; then \
        echo python; \
    else \
        echo python3; \
    fi)

PYTHON_VERSION := $(shell $(PYTHON_CMD) -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")

PYTHON_CONFIG_CANDIDATES := $(shell \
    if [ -n "$$CIBUILDWHEEL" ]; then \
        echo "$(PYTHON_CMD)-config python$(PYTHON_VERSION)-config python3-config python-config"; \
    else \
        echo "$(PYTHON_CMD)-config python$(PYTHON_VERSION)-config python3-config python-config"; \
    fi)
PYTHON_CONFIG = $(shell for cmd in $(PYTHON_CONFIG_CANDIDATES); do \
    if which $$cmd >/dev/null 2>&1; then \
        echo $$cmd; \
        break; \
    fi; \
done)

ifeq ($(PYTHON_CONFIG),)
    PYTHON_CONFIG = python3-config
endif

PYTHON_INCLUDE := $(shell $(PYTHON_CMD) -c "try: import pybind11; print(pybind11.get_include());\nexcept: pass" 2>/dev/null)
PYTHON_HEADERS := $(shell $(PYTHON_CONFIG) --includes)
PYTHON_SUFFIX := $(shell $(PYTHON_CONFIG) --extension-suffix)

CXXFLAGS = $(BASE_CXXFLAGS) $(CROSS_COMPILE_FLAGS) $(PYTHON_HEADERS)

ifeq ($(UNAME_S),Darwin)
    CXXFLAGS += -stdlib=libc++
    LDFLAGS_PYBIND = -shared -undefined dynamic_lookup $(CROSS_COMPILE_FLAGS)
    MACOS = true
else
    LDFLAGS_PYBIND = -shared -Wl,--export-dynamic
    MACOS = false
endif

# Platform-specific binary extensions
ifeq ($(UNAME_S),Windows_NT)
    BIN_EXT = .exe
else
    BIN_EXT = 
endif

# Architecture-specific variables
ARM64_ENABLED = false
KMER_COUNTER_SRC = $(SRC_DIR)/count_kmers.cpp
KMER_COUNTER_FLAGS = 
COUNT_KMERS13_SRC = $(SRC_DIR)/count_kmers13.cpp
COUNT_KMERS13_FLAGS = 
COMPUTE_AINDEX13_SRC = $(SRC_DIR)/compute_aindex13.cpp
COMPUTE_AINDEX13_FLAGS = 

# ARM64/Apple Silicon optimization
ifeq ($(UNAME_S),Darwin)
    ifeq ($(TARGET_ARCH),arm64)
        ARM64_FLAGS = -mcpu=apple-m1 -mtune=apple-m1 -DARM64_OPTIMIZED
        ARM64_ENABLED = true
        KMER_COUNTER_SRC = $(SRC_DIR)/count_kmers.arm64.cpp
        KMER_COUNTER_FLAGS = $(ARM64_FLAGS)
        COUNT_KMERS13_SRC = $(SRC_DIR)/count_kmers13.arm64.cpp
        COUNT_KMERS13_FLAGS = $(ARM64_FLAGS)
        COMPUTE_AINDEX13_SRC = $(SRC_DIR)/compute_aindex13.arm64.cpp
        COMPUTE_AINDEX13_FLAGS = $(ARM64_FLAGS)
    else ifeq ($(TARGET_ARCH),aarch64)
        ARM64_FLAGS = -mcpu=apple-m1 -mtune=apple-m1 -DARM64_OPTIMIZED
        ARM64_ENABLED = true
        KMER_COUNTER_SRC = $(SRC_DIR)/count_kmers.arm64.cpp
        KMER_COUNTER_FLAGS = $(ARM64_FLAGS)
        COUNT_KMERS13_SRC = $(SRC_DIR)/count_kmers13.arm64.cpp
        COUNT_KMERS13_FLAGS = $(ARM64_FLAGS)
        COMPUTE_AINDEX13_SRC = $(SRC_DIR)/compute_aindex13.arm64.cpp
        COMPUTE_AINDEX13_FLAGS = $(ARM64_FLAGS)
    endif
endif

OBJ_CXXFLAGS = $(BASE_CXXFLAGS) $(CROSS_COMPILE_FLAGS)

# Binary targets
BINARIES = $(BIN_DIR)/compute_index$(BIN_EXT) $(BIN_DIR)/compute_aindex$(BIN_EXT) $(BIN_DIR)/compute_reads$(BIN_EXT) $(BIN_DIR)/kmer_counter$(BIN_EXT) $(BIN_DIR)/generate_all_13mers$(BIN_EXT) $(BIN_DIR)/build_13mer_hash$(BIN_EXT) $(BIN_DIR)/count_kmers13$(BIN_EXT) $(BIN_DIR)/compute_aindex13$(BIN_EXT) $(BIN_DIR)/compute_mphf_seq$(BIN_EXT)

all: debug-info clean $(BIN_DIR) $(OBJ_DIR) local-scripts $(BINARIES) pybind11 copy-to-package

# Debug target
debug-info:
	@echo "=== Build Configuration ==="
	@echo "UNAME_S: $(UNAME_S)"
	@echo "UNAME_M: $(shell uname -m)"
	@echo "TARGET_ARCH: $(TARGET_ARCH)"
	@echo "ARCHFLAGS: $$ARCHFLAGS"
	@echo "CIBUILDWHEEL: $$CIBUILDWHEEL"
	@echo "ARM64_ENABLED: $(ARM64_ENABLED)"
	@echo "CROSS_COMPILE_FLAGS: $(CROSS_COMPILE_FLAGS)"
	@echo "PYTHON_CMD: $(PYTHON_CMD)"
	@echo "PYTHON_CONFIG: $(PYTHON_CONFIG)"
	@echo "PYTHON_SUFFIX: $(PYTHON_SUFFIX)"
	@echo "CXXFLAGS: $(CXXFLAGS)"
	@echo "LDFLAGS_PYBIND: $(LDFLAGS_PYBIND)"
	@echo "==========================="

# Alternative build with external dependencies (deprecated - use 'all' instead)
all-external: clean external $(BIN_DIR) $(OBJ_DIR) $(BINARIES) pybind11 copy-to-package

# Alternative simplified build for problematic platforms (deprecated)
simple-all: clean external-safe $(BIN_DIR) $(OBJ_DIR) $(BINARIES) pybind11 copy-to-package

# Build only object files for debugging
objects: $(OBJ_DIR) $(OBJECTS)

$(BIN_DIR):
	mkdir -p $(BIN_DIR)

$(OBJ_DIR):
	mkdir -p $(OBJ_DIR)

$(BIN_DIR)/compute_index$(BIN_EXT): $(SRC_DIR)/compute_index.cpp $(OBJECTS) | $(BIN_DIR)
	$(CXX) $(OBJ_CXXFLAGS) $^ -o $@

$(BIN_DIR)/compute_aindex$(BIN_EXT): $(SRC_DIR)/compute_aindex.cpp $(OBJECTS) | $(BIN_DIR)
	$(CXX) $(OBJ_CXXFLAGS) $^ -o $@

$(BIN_DIR)/compute_reads$(BIN_EXT): $(SRC_DIR)/compute_reads.cpp $(OBJECTS) | $(BIN_DIR)
	$(CXX) $(OBJ_CXXFLAGS) $^ -o $@

$(BIN_DIR)/kmer_counter$(BIN_EXT): $(KMER_COUNTER_SRC) | $(BIN_DIR)
ifeq ($(ARM64_ENABLED),true)
	@echo "Building k-mer counter with ARM64 optimizations..."
	$(CXX) $(OBJ_CXXFLAGS) $(KMER_COUNTER_FLAGS) $< -o $@
else
	@echo "Building standard k-mer counter..."
	$(CXX) $(OBJ_CXXFLAGS) $(KMER_COUNTER_FLAGS) $< -o $@
endif

$(BIN_DIR)/generate_all_13mers$(BIN_EXT): $(SRC_DIR)/generate_all_13mers.cpp $(OBJ_DIR)/kmers.o | $(BIN_DIR)
	$(CXX) $(OBJ_CXXFLAGS) $^ -o $@

$(BIN_DIR)/build_13mer_hash$(BIN_EXT): $(SRC_DIR)/build_13mer_hash.cpp $(OBJECTS) | $(BIN_DIR)
	$(CXX) $(OBJ_CXXFLAGS) -I$(SRC_DIR) $^ -o $@

$(BIN_DIR)/count_kmers13$(BIN_EXT): $(COUNT_KMERS13_SRC) $(OBJECTS) | $(BIN_DIR)
ifeq ($(ARM64_ENABLED),true)
	@echo "Building 13-mer counter with ARM64 optimizations..."
	$(CXX) $(OBJ_CXXFLAGS) $(COUNT_KMERS13_FLAGS) -I$(SRC_DIR) $< $(OBJECTS) -o $@
else
	@echo "Building standard 13-mer counter..."
	$(CXX) $(OBJ_CXXFLAGS) $(COUNT_KMERS13_FLAGS) -I$(SRC_DIR) $^ -o $@
endif

$(BIN_DIR)/compute_aindex13$(BIN_EXT): $(COMPUTE_AINDEX13_SRC) $(OBJECTS) | $(BIN_DIR)
ifeq ($(ARM64_ENABLED),true)
	@echo "Building AIndex13 with ARM64 optimizations..."
	$(CXX) $(OBJ_CXXFLAGS) $(COMPUTE_AINDEX13_FLAGS) -I$(SRC_DIR) $< $(OBJECTS) -o $@
else
	@echo "Building standard AIndex13..."
	$(CXX) $(OBJ_CXXFLAGS) $(COMPUTE_AINDEX13_FLAGS) -I$(SRC_DIR) $< $(OBJECTS) -o $@
endif

$(BIN_DIR)/compute_mphf_seq$(BIN_EXT): $(SRC_DIR)/emphf/compute_mphf_seq.cpp | $(BIN_DIR)
	@echo "Building compute_mphf_seq from local sources..."
	$(CXX) $(OBJ_CXXFLAGS) -I$(SRC_DIR) $< -o $@

# Copy Python scripts to bin directory for local build
local-scripts: | $(BIN_DIR)
	@echo "Copying Python scripts to bin directory..."
	cp scripts/compute_aindex.py $(BIN_DIR)/
	cp scripts/compute_index.py $(BIN_DIR)/
	cp scripts/reads_to_fasta.py $(BIN_DIR)/
	@echo "Python scripts copied successfully."

$(OBJ_DIR)/%.o: $(SRC_DIR)/%.cpp $(INCLUDES) | $(OBJ_DIR)
	$(CXX) $(OBJ_CXXFLAGS) -c $< -o $@

# Pybind11 module
pybind11: $(OBJECTS) $(SRC_DIR)/python_wrapper.cpp | $(PACKAGE_DIR)
	@echo "=== Building Python extension ==="
	@echo "Target Arch: $(TARGET_ARCH)"
	@echo "ARCHFLAGS: $$ARCHFLAGS"
	@echo "Cross-compile flags: $(CROSS_COMPILE_FLAGS)"
	@echo "Python command: $(PYTHON_CMD)"
	@# Dynamically get pybind11 path right before compilation
	@PYBIND11_INCLUDE=$$($(PYTHON_CMD) -c "import pybind11; print(pybind11.get_include())" 2>/dev/null) && \
	if [ -z "$$PYBIND11_INCLUDE" ]; then \
		echo "Error: pybind11 not found. Please install pybind11: pip install pybind11"; \
		exit 1; \
	else \
		echo "pybind11 include path: $$PYBIND11_INCLUDE"; \
		echo "Final CXXFLAGS: $(CXXFLAGS) -I$$PYBIND11_INCLUDE"; \
		echo "Pybind LDFLAGS: $(LDFLAGS_PYBIND)"; \
		$(CXX) $(CXXFLAGS) -I$$PYBIND11_INCLUDE -I$(SRC_DIR) $(LDFLAGS_PYBIND) -o $(PACKAGE_DIR)/aindex_cpp$(PYTHON_SUFFIX) $(SRC_DIR)/python_wrapper.cpp $(OBJECTS); \
	fi
	
external:
	@echo "Setting up external dependencies..."
	mkdir -p ${BIN_DIR}
	mkdir -p external
	mkdir -p $(PACKAGE_DIR)
	@if [ ! -d "external/emphf" ]; then \
		echo "Cloning emphf repository..."; \
		cd external && git clone https://github.com/ad3002/emphf.git || { \
			echo "Failed to clone emphf repository. Please check your internet connection."; \
			exit 1; \
		}; \
		echo "Applying CMake version patch..."; \
		cd emphf && patch -p1 < ../../patches/emphf_cmake_version.patch; \
	fi
	@echo "Building emphf using original build process..."
	@echo "Platform: $(shell uname -s) $(shell uname -m)"
	cd external/emphf && env -i PATH="$$PATH" HOME="$$HOME" cmake . && env -i PATH="$$PATH" HOME="$$HOME" make
	@echo "Copying emphf binaries to our bin directory..."
	@if [ -f "external/emphf/compute_mphf_seq" ]; then \
		echo "✓ compute_mphf_seq found"; \
		cp external/emphf/compute_mphf_seq $(BIN_DIR)/; \
		echo "✓ Binary copied to $(BIN_DIR)/"; \
	else \
		echo "✗ compute_mphf_seq not found"; \
		ls -la external/emphf/compute_mphf* || echo "No compute_mphf* files found"; \
		exit 1; \
	fi
	@echo "Copying our Python scripts..."
	cp scripts/compute_aindex.py $(BIN_DIR)/
	cp scripts/compute_index.py $(BIN_DIR)/
	cp scripts/reads_to_fasta.py $(BIN_DIR)/
	@echo "External dependencies setup complete."

# Alternative build for problematic platforms
external-safe: 
	@echo "Setting up external dependencies with safe mode..."
	mkdir -p ${BIN_DIR}
	mkdir -p external
	mkdir -p $(PACKAGE_DIR)
	@if [ ! -d "external/emphf" ]; then \
		echo "Cloning emphf repository..."; \
		cd external && git clone https://github.com/ad3002/emphf.git || { \
			echo "Failed to clone emphf repository. Please check your internet connection."; \
			exit 1; \
		}; \
		echo "Applying CMake version patch..."; \
		cd emphf && patch -p1 < ../../patches/emphf_cmake_version.patch; \
	fi
	@echo "Building emphf with POPCOUNT disabled for compatibility..."
	@echo "Platform: $(shell uname -s) $(shell uname -m)"
	cd external/emphf && env -i PATH="$$PATH" HOME="$$HOME" cmake -DEMPHF_USE_POPCOUNT=OFF . && env -i PATH="$$PATH" HOME="$$HOME" make
	@echo "Copying emphf binaries to our bin directory..."
	@if [ -f "external/emphf/compute_mphf_seq" ]; then \
		echo "✓ compute_mphf_seq found"; \
		cp external/emphf/compute_mphf_seq $(BIN_DIR)/; \
		echo "✓ Binary copied to $(BIN_DIR)/"; \
	else \
		echo "✗ compute_mphf_seq not found"; \
		ls -la external/emphf/compute_mphf* || echo "No compute_mphf* files found"; \
		exit 1; \
	fi
	@echo "Copying our Python scripts..."
	cp scripts/compute_aindex.py $(BIN_DIR)/
	cp scripts/compute_index.py $(BIN_DIR)/
	cp scripts/reads_to_fasta.py $(BIN_DIR)/
	@echo "Safe external dependencies setup complete."

local:
	@echo "Installing aindex package and CLI..."
	@echo "Building package wheel..."
	$(PYTHON_CMD) -m pip install --upgrade build
	$(PYTHON_CMD) -m build --wheel
	@echo "Installing package..."
	$(PYTHON_CMD) -m pip install --force-reinstall dist/aindex2-*.whl
	@echo "Installation complete. You can now use 'aindex' command."


install: all
	mkdir -p ${BIN_DIR}
	mkdir -p $(PACKAGE_DIR)
	mkdir -p $(INSTALL_DIR)
	@echo "Installing binaries to $(INSTALL_DIR)..."
	cp bin/compute_index$(BIN_EXT) $(INSTALL_DIR)/
	cp bin/compute_aindex$(BIN_EXT) $(INSTALL_DIR)/
	cp bin/compute_reads$(BIN_EXT) $(INSTALL_DIR)/
	cp bin/kmer_counter$(BIN_EXT) $(INSTALL_DIR)/
	cp bin/generate_all_13mers$(BIN_EXT) $(INSTALL_DIR)/
	cp bin/build_13mer_hash$(BIN_EXT) $(INSTALL_DIR)/
	cp bin/compute_aindex13$(BIN_EXT) $(INSTALL_DIR)/
	cp bin/count_kmers13$(BIN_EXT) $(INSTALL_DIR)/
	cp bin/compute_mphf_seq$(BIN_EXT) $(INSTALL_DIR)/
	@echo "Installing Python package with aindex CLI..."
	$(PYTHON_CMD) -m pip install -e .
	@echo "Installation complete. You can now use 'aindex' command and all binaries."

uninstall:
	@echo "Removing aindex binaries from $(INSTALL_DIR)..."
	rm -f $(INSTALL_DIR)/compute_index$(BIN_EXT)
	rm -f $(INSTALL_DIR)/compute_aindex$(BIN_EXT)
	rm -f $(INSTALL_DIR)/compute_reads$(BIN_EXT)
	rm -f $(INSTALL_DIR)/kmer_counter$(BIN_EXT)
	rm -f $(INSTALL_DIR)/generate_all_13mers$(BIN_EXT)
	rm -f $(INSTALL_DIR)/build_13mer_hash$(BIN_EXT)
	rm -f $(INSTALL_DIR)/compute_aindex13$(BIN_EXT)
	rm -f $(INSTALL_DIR)/count_kmers13$(BIN_EXT)
	rm -f $(INSTALL_DIR)/compute_mphf_seq$(BIN_EXT)
	@echo "Uninstalling Python package and aindex CLI..."
	$(PYTHON_CMD) -m pip uninstall -y aindex2
	@echo "Uninstall complete."

clean:
	rm -rf $(OBJ_DIR) $(SRC_DIR)/*.so $(BIN_DIR) $(PACKAGE_DIR)/python_wrapper.so $(PACKAGE_DIR)/aindex_cpp*.so
	rm -rf external
	rm -rf aindex/bin

# ARM64 target for Apple Silicon Macs  
arm64: debug-info clean $(PACKAGE_DIR) $(OBJ_DIR) $(BIN_DIR)
	@echo "Building ARM64-optimized version for Apple Silicon..."
	@echo "Forcing TARGET_ARCH=arm64 for ARM64 build"
	$(MAKE) all TARGET_ARCH=arm64

# macOS simplified target for testing without emphf dependencies
macos-simple: clean $(PACKAGE_DIR) $(OBJ_DIR)
	@echo "Building simplified version for macOS (testing only)..."
	mkdir -p $(PACKAGE_DIR)
	mkdir -p $(OBJ_DIR)
	g++ -c -std=c++11 -fPIC $(SRC_DIR)/python_wrapper_simple.cpp -o $(OBJ_DIR)/python_wrapper_simple.o
	g++ -shared -Wl,-install_name,python_wrapper.so -o $(PACKAGE_DIR)/python_wrapper.so \
		$(OBJ_DIR)/python_wrapper_simple.o
	@echo "macOS simplified build complete! python_wrapper.so created in $(PACKAGE_DIR)/"

# Create package directory
$(PACKAGE_DIR):
	mkdir -p $(PACKAGE_DIR)

# Copy binaries to package directory for inclusion in wheel
copy-to-package: $(BINARIES)
	@echo "Copying binaries to package directory..."
	mkdir -p aindex/bin
	cp -f $(BIN_DIR)/* aindex/bin/ 2>/dev/null
	@echo "✓ Binaries copied to aindex/bin/"
	@ls -la aindex/bin/ || echo "No files in aindex/bin/"

# Test targets
test:
	@echo "Running full regression tests..."
	$(PYTHON_CMD) test_aindex_functionality.py
	$(PYTHON_CMD) test_aindex_functionality_k13.py

test-all:
	@echo "Running full regression tests..."
	$(PYTHON_CMD) test_aindex_functionality.py
	$(PYTHON_CMD) test_aindex_functionality_k13.py

# Debug target for cross-platform issues
debug-platform:
	@echo "=== Platform Debug Information ==="
	@echo "OS: $(shell uname -s)"
	@echo "Architecture: $(shell uname -m)"
	@echo "Compiler: $(CXX)"
	@echo "C++ Standard Library:"
	@$(CXX) --version
	@echo "Python: $(PYTHON_CMD)"
	@$(PYTHON_CMD) --version
	@echo "Python Config: $(PYTHON_CONFIG)"
	@echo "CMake version:"
	@cmake --version 2>/dev/null || echo "CMake not found"
	@echo "=== Build Flags ==="
	@echo "CXXFLAGS: $(CXXFLAGS)"
	@echo "LDFLAGS: $(LDFLAGS)"
	@echo "=================================="

# Help target
help:
	@echo "Available targets:"
	@echo "  all              - Build all binaries and Python extension (using local emphf sources)"
	@echo "  all-external     - Build with external emphf repository (deprecated)"
	@echo "  simple-all       - Build with safe external dependencies (deprecated)"
	@echo "  clean            - Clean build artifacts"
	@echo "  pybind11         - Build only the Python extension"
	@echo "  test             - Run Python API tests"
	@echo "  test-all         - Run Python API tests"
	@echo "  debug-platform   - Display platform and build environment information"
	@echo "  install          - Install binaries to system (requires CONDA_PREFIX)"
	@echo "  uninstall        - Remove installed binaries from system"
	@echo "  arm64            - Build ARM64-optimized version for Apple Silicon"
	@echo "  help             - Show this help message"
	@echo ""
	@echo "Platform-specific targets:"
ifeq ($(ARM64_ENABLED),true)
	@echo "  arm64            - ARM64-optimized build for Apple Silicon (AVAILABLE)"
else
	@echo "  arm64            - ARM64-optimized build for Apple Silicon (not available on this platform)"
endif
	@echo ""
	@echo "Recommended usage:"
	@echo "  make all         - Complete build using local emphf sources (RECOMMENDED)"
ifeq ($(ARM64_ENABLED),true)
	@echo "  make arm64       - Optimized build for Apple Silicon (recommended for M1/M2 Macs)"
endif
	@echo "  make test-all    - Complete test suite for new users/CI"
	@echo ""
	@echo "Cross-platform debugging:"
	@echo "  make debug-platform - Show platform information"
	@echo ""
	@echo "Legacy targets (deprecated):"
	@echo "  make all-external - Build with external emphf repository"
	@echo "  make simple-all   - Safe build for problematic platforms"
	@echo ""
	@echo "Documentation:"
	@echo "  See CROSS_PLATFORM.md for cross-platform compatibility details"
	@echo ""
	@echo "Python version detected: $(PYTHON_VERSION)"
	@echo "Python config: $(PYTHON_CONFIG)"
	@echo "Extension suffix: $(PYTHON_SUFFIX)"
ifeq ($(ARM64_ENABLED),true)
	@echo "ARM64 optimization: ENABLED (Apple Silicon detected)"
else
	@echo "ARM64 optimization: DISABLED (not Apple Silicon)"
endif

# Debug target to print variables
debug-vars:
	@echo "=== Makefile Variables ==="
	@echo "CXX: $(CXX)"
	@echo "CXXFLAGS: $(CXXFLAGS)"
	@echo "OBJ_CXXFLAGS: $(OBJ_CXXFLAGS)"
	@echo "SRC_DIR: $(SRC_DIR)"
	@echo "OBJ_DIR: $(OBJ_DIR)"
	@echo "BIN_DIR: $(BIN_DIR)"
	@echo "SOURCES: $(SOURCES)"
	@echo "OBJECTS: $(OBJECTS)"
	@echo "BINARIES: $(BINARIES)"
	@echo "PYTHON_CMD: $(PYTHON_CMD)"
	@echo "PYTHON_VERSION: $(PYTHON_VERSION)"
	@echo "PYTHON_CONFIG: $(PYTHON_CONFIG)"
	@echo "PYTHON_INCLUDE: $(PYTHON_INCLUDE)"
	@echo "PYTHON_HEADERS: $(PYTHON_HEADERS)"
	@echo "PYTHON_SUFFIX: $(PYTHON_SUFFIX)"
	@echo "============================="

.PHONY: all local all-external simple-all clean external external-safe install uninstall macos macos-simple arm64 test test-all debug-platform help debug-vars copy-to-package objects local-scripts