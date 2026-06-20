#!/bin/bash
set -e

echo "=== QuEnAIS Installation ==="

# Check requirements
command -v python  || { echo "ERROR: python not found"; exit 1; }
command -v pip     || { echo "ERROR: pip not found"; exit 1; }
command -v cargo   || { echo "ERROR: cargo not found. Install Rust first."; exit 1; }
command -v clang   || { echo "ERROR: clang not found"; exit 1; }

# Step 1: Core pip packages
echo "[1/5] Installing pyscf and block2..."
pip install pyscf block2

# Step 2: Generate block2 wrapper
echo "[2/5] Generating block2 wrapper..."
python quenais/utils/generate_wrapper.py

# Step 3: Install ASF
echo "[3/5] Installing ASF..."
ASF_TMP=$(mktemp -d)
git clone https://github.com/HQSquantumsimulations/ActiveSpaceFinder.git "$ASF_TMP"
pip install "$ASF_TMP"
"$ASF_TMP/init_dmrgscf_settings.sh"
rm -rf "$ASF_TMP"

# Step 4: Install qiskit-fermions
echo "[4/5] Installing qiskit-fermions..."
QF_TMP=$(mktemp -d)
git clone https://github.com/Qiskit/qiskit-fermions.git "$QF_TMP"
cd "$QF_TMP"
pip install --group build
pip install --no-build-isolation .
cd -
rm -rf "$QF_TMP"

# Step 5: Install quenais
echo "[5/5] Installing quenais..."
pip install -e ".[quantum]"

echo ""
echo "=== Verifying ==="
python -c "import quenais;   print('  quenais ok')"
python -c "import pyscf;     print('  pyscf ok')"
python -c "import block2;    print('  block2 ok')"
python -c "from asf.wrapper import find_from_scf; print('  asf ok')"
python -c "from qiskit_fermions.circuit import FermionicCircuit; print('  qiskit-fermions ok')"

echo "=== Done ==="