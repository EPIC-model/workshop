#!/bin/bash

# specify where to download and install (please do not change)
WORK_DIR="/work/d185/d185/$USER"
PREFIX="${WORK_DIR}/epic"
SRC_DIR="${WORK_DIR}/source"

# load necessary modules
module use /work/d185/d185/shared/modules
module load gcc/10.2.0
module load openmpi/4.1.6
module load hdf5-epic
module load netcdf-epic
module load libtool

# ensure EPIC is able to find MPI
if [[ "$MPI_DIR" == "" ]]; then
    mpi_compiler=$(which mpif90)
    export MPI_DIR=${mpi_compiler%/*/*}
fi

# download source
mkdir -p "$SRC_DIR"
cd $SRC_DIR
git clone https://github.com/EPIC-model/epic.git

# configure
cd "$SRC_DIR/epic"
./bootstrap
mkdir -p "$SRC_DIR/epic/build"
cd "$SRC_DIR/epic/build"
$SRC_DIR/epic/configure \
    --enable-verbose    \
    --enable-3d         \
    --prefix=${PREFIX}

# compile
make
make install
