# Installation

## Recommended: one-step setup

### Step 1 — Create conda environment (handles all system deps)

    mamba env create -f environment.yml -p ./quenais-env
    mamba activate quenais

This installs Python 3.11, clang, cmake, openblas, gfortran, Rust,
and all pip-installable dependencies automatically.

### Step 2 — Run the install script

    bash install.sh

This installs ASF, qiskit-fermions, and quenais itself.

---

## Manual installation (if you cannot use environment.yml)

### Step 1 — System dependencies

    mamba install -c conda-forge python=3.11 clang cmake openblas gfortran rust

OR load cluster modules:

    module load gcc openblas cmake
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

### Step 2 — Base Python packages

    pip install -r requirements-base.txt

### Step 3 — Quantum packages

    pip install -r requirements-quantum.txt

### Step 4 — ASF

    git clone https://github.com/HQSquantumsimulations/ActiveSpaceFinder.git
    cd ActiveSpaceFinder
    pip install .
    ./init_dmrgscf_settings.sh

### Step 5 — qiskit-fermions

    git clone https://github.com/Qiskit/qiskit-fermions.git
    cd qiskit-fermions
    pip install --group build
    pip install --no-build-isolation .

### Step 6 — block2 wrapper

    # Generated automatically by install.sh
    # Or run manually:
    python -c "
    import block2, os, sys
    libs = os.path.dirname(block2.__file__) + '.libs'
    exe  = os.path.join(os.path.dirname(sys.executable), 'block2main')
    print('BLOCK2_LIBS:', libs)
    print('block2main :', exe)
    "

### Step 7 — Install quenais

    pip install -e .

---

## HPC notes (erebos / SLURM clusters)

If miniforge/mamba pkgs.lock error appears, it is a permissions issue
on the shared package cache. It is harmless — installation still works.

cargo (Rust) is user-local at ~/.cargo/bin/cargo — it persists across
environments and does not need reinstalling.