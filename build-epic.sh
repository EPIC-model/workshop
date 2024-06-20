#!/bin/bash

if [[ "$PREFIX" == "" ]]; then
    echo "Missing 'PREFIX' environment variable. Please set this variable."
    return
fi

if [[ "$SRC_DIR" == "" ]]; then
    echo "Missing 'SRC_DIR' environment variable. Please set this variable."
    return
fi

if [[ "$MPI_DIR" == "" ]]; then
   export MPI_DIR=/work/y07/shared/cirrus-software/openmpi/4.1.6
fi

mkdir -p "$SRC_DIR"

# load necessary modules
module use /work/d185/d185/shared/modules
module load gcc/10.2.0
module load openmpi/4.1.6
module load hdf5-epic
module load netcdf-epic
module load libtool

cd $SRC_DIR
git clone https://github.com/EPIC-model/epic.git
cd epic
./bootstrap
mkdir -p build
cd build
$SRC_DIR/epic/configure \
    --enable-verbose    \
    --enable-3d         \
    --prefix=${PREFIX}

make
make install
