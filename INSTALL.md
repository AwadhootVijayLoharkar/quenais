# QuEnAIS Installation Guide

---

## Quick Setup (Recommended)

### Step 1 — Clone the repo

    git clone https://github.com/AwadhootVijayLoharkar/quenais.git
    cd quenais

### Step 2 — Create conda environment in local directory

    mamba env create -f environment.yml -p ./quenais-env

Use `-p ./quenais-env` not `--name quenais`.
This creates the environment inside the repo folder and avoids
read-only errors on shared HPC systems where `/opt/miniforge/envs/`
is not writable.

### Step 3 — Activate

    mamba activate ./quenais-env

### Step 4 — Run install script

    bash install.sh

This handles everything in the correct order:
- Base Python packages (numpy, scipy first)
- Quantum packages (pyscf, qiskit, ffsim, ...)
- block2 wrapper (generated for current environment)
- ASF (cloned and compiled from source)
- qiskit-fermions (compiled from source, requires Rust)
- quenais itself

---

## What install.sh does step by step

| Step | What | Why manual |
|---|---|---|
| 1 | `requirements-base.txt` | numpy/scipy must exist before pyscf compiles |
| 2 | `requirements-quantum.txt` | pyscf, qiskit, ffsim, openfermion |
| 3 | block2 wrapper | paths depend on current env, cannot be hardcoded |
| 4 | ASF | not on PyPI, requires `init_dmrgscf_settings.sh` after pip install |
| 5 | qiskit-fermions | requires `--no-build-isolation` + Rust compiler |
| 6 | quenais | `pip install -e .` |

---

## Manual Installation (step by step)

If you cannot use `environment.yml` or `install.sh`:

### Step 1 — System dependencies via conda

    mamba install -c conda-forge python=3.11 clang cmake openblas gfortran rust pip

### Step 2 — Base Python packages

    pip install -r requirements-base.txt

### Step 3 — Quantum packages

    pip install -r requirements-quantum.txt

### Step 4 — block2

    pip install block2==0.5.2

### Step 5 — Generate block2 wrapper

    python quenais/utils/regenerate_wrapper.py

This detects your current environment paths and writes
`~/block2main_wrapper.sh` automatically.
AMD CPUs get the MKL workaround. Intel CPUs get a simple wrapper.

### Step 6 — ASF (Active Space Finder)

    git clone https://github.com/HQSquantumsimulations/ActiveSpaceFinder.git
    cd ActiveSpaceFinder
    pip install .
    ./init_dmrgscf_settings.sh
    cd ..

### Step 7 — qiskit-fermions (requires Rust + clang)

    git clone https://github.com/Qiskit/qiskit-fermions.git
    cd qiskit-fermions
    pip install --group build
    pip install --no-build-isolation .
    cd ..

### Step 8 — Install quenais

    pip install -e .

### Step 9 — Verify

    python -c "import quenais; print(quenais.__version__)"
    python -c "import pyscf; print('pyscf ok')"
    python -c "import block2; print('block2 ok')"
    python -c "from asf.wrapper import find_from_scf; print('asf ok')"
    python -c "from qiskit_fermions.circuit import FermionicCircuit; print('qiskit-fermions ok')"
    python -c "import ffsim; print('ffsim ok')"
    pytest tests/ -v

---

## Switching conda environments

Each time you switch to a different conda environment you must
regenerate the block2 wrapper — it contains hardcoded paths to
the current environment's block2 libraries.

    mamba activate ./your-new-env
    python quenais/utils/regenerate_wrapper.py

Or with a custom path:

    python quenais/utils/regenerate_wrapper.py --path ~/block2main_wrapper.sh

Check the wrapper is correct:

    cat ~/block2main_wrapper.sh

The path inside should match your active environment.

---

## HPC / Cluster Notes

**Read-only system prefix**
If you see `Read-only file system` errors from mamba:

    # Always use -p to specify a local path
    mamba env create -f environment.yml -p ./quenais-env
    mamba activate ./quenais-env

**pkgs.lock warning**
The `Could not open lockfile '/opt/miniforge/pkgs/pkgs.lock'` warning
from mamba is harmless. Installation still completes successfully.

**Rust (cargo)**
Rust is user-local at `~/.cargo/bin/cargo` and persists across
environments. You only need to install it once per user account.

**clang**
clang must be installed in your active conda environment:

    mamba install -c conda-forge clang

**Module system (SLURM clusters)**
Some clusters use `module load` instead of conda for compilers.
If conda clang/cmake are unavailable try:

    module load gcc
    module load cmake
    module load openblas

Then proceed with pip installs.

---

## Development Setup

    pip install -r requirements-dev.txt
    pytest tests/ -v
    jupyter notebook notebooks/tutorial.ipynb

---

## Troubleshooting

**block2 MKL error on AMD CPU**

    INTEL MKL FATAL ERROR: Cannot load libmkl_def.so.1

Fix: regenerate the wrapper — it was built for a different environment.

    python quenais/utils/regenerate_wrapper.py
    cat ~/block2main_wrapper.sh   # verify paths match current env

**ASF returns 0 candidates**

Lower `entropy_threshold` in Config:

    cfg = Config(asf_params={
        3: {"entropy_threshold": 0.001, "max_norb": 16, "min_norb": 4}
    })

**qiskit-fermions build fails**

Make sure Rust and clang are both available:

    which cargo    # should print a path
    which clang    # should print a path

If cargo is missing:

    mamba install -c conda-forge rust
    # or
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

**SQD no valid configs after filter**

Switch from `su2` to `lucj` ansatz, or increase shots:

    cfg = Config(ansatz="lucj", n_shots=16384)