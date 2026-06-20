"""
Central configuration for QuEnAIS pipeline.
Replaces the module-level config.py from the original scripts.
"""

import os
import numpy as np


class Config:
    """
    All pipeline settings in one object.
    Pass this to every step instead of importing module-level globals.
    """

    def __init__(
        self,
        molecule          = "TiO2",
        charge            = 0,
        spin              = 0,
        basis             = "def2-svp",
        project_dir       = None,
        quantum_solver    = "sqd",
        ansatz            = "lucj",
        fermion_to_qubit  = "bk",
        backend           = "mps",
        n_shots           = 8192,
        sqd_iters         = 10,
        classical_methods = None,
        geometry_scan     = True,
        scan_atom_pair    = (0, 1),
        scan_distances    = None,
        scan_method       = "MP2",
        quantum_scan      = True,
        quantum_scan_fast = True,
        quantum_scan_shots= 2048,
        quantum_scan_iters= 4,
        lucj_num_layers   = 3,
        lucj_random_seed  = 42,
        lucj_regularization = 1e-2,
    ):
        # Molecule
        self.molecule         = molecule
        self.charge           = charge
        self.spin             = spin
        self.basis            = basis

        # Paths
        self.project_dir      = project_dir or os.getcwd()

        # Quantum solver
        self.quantum_solver   = quantum_solver
        self.ansatz           = ansatz
        self.fermion_to_qubit = fermion_to_qubit
        self.backend          = backend
        self.n_shots          = n_shots
        self.sqd_iters        = sqd_iters

        # Classical
        self.classical_methods = classical_methods or ["HF", "MP2"]

        # Geometry scan
        self.geometry_scan     = geometry_scan
        self.scan_atom_pair    = scan_atom_pair
        self.scan_distances    = (scan_distances
                                  if scan_distances is not None
                                  else np.linspace(0.9, 4.0, 20))
        self.scan_method       = scan_method
        self.quantum_scan      = quantum_scan
        self.quantum_scan_fast = quantum_scan_fast
        self.quantum_scan_shots= quantum_scan_shots
        self.quantum_scan_iters= quantum_scan_iters

        # LUCJ
        self.lucj_num_layers      = lucj_num_layers
        self.lucj_random_seed     = lucj_random_seed
        self.lucj_regularization  = lucj_regularization

        # Constants
        self.hartree_to_ev        = 27.211386245988
        self.hartree_to_kcal_mol  = 627.5094740631

    # ── Derived paths ─────────────────────────────────────────────────────────
    @property
    def results_dir(self):
        return os.path.join(self.project_dir, "results")

    @property
    def cif_dir(self):
        return os.path.join(self.project_dir, "cif_files")

    @property
    def plots_dir(self):
        return os.path.join(self.results_dir, "plots")

    @property
    def step0_file(self):
        return os.path.join(self.results_dir, "step0_classical.pkl")

    @property
    def step1_file(self):
        return os.path.join(self.results_dir, "step1_asf.pkl")

    @property
    def step2_file(self):
        return os.path.join(self.results_dir, "step2_hamiltonian.pkl")

    @property
    def step3_file(self):
        return os.path.join(self.results_dir, "step3_results.pkl")

    # ── Setup ─────────────────────────────────────────────────────────────────
    def make_dirs(self):
        """Create all output directories."""
        os.makedirs(self.results_dir, exist_ok=True)
        os.makedirs(self.cif_dir,     exist_ok=True)
        os.makedirs(self.plots_dir,   exist_ok=True)
        return self

    def validate(self):
        """Catch obvious config mistakes early."""
        assert self.spin >= 0,                    "spin must be >= 0"
        assert self.n_shots > 0,                  "n_shots must be > 0"
        assert self.ansatz in ("su2", "lucj"),     "ansatz must be su2 or lucj"
        assert self.fermion_to_qubit in ("jw","bk"), "mapping must be jw or bk"
        assert self.quantum_solver in ("sqd","skqd","sqdrift")
        return self

    def __repr__(self):
        return (f"Config(molecule={self.molecule}, basis={self.basis}, "
                f"solver={self.quantum_solver}, ansatz={self.ansatz})")