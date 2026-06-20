"""
Central configuration for QuEnAIS pipeline.
"""

import os
import numpy as np
from quenais.utils.cif_parser import load_geometry as _load_geometry


class Config:

    def __init__(
        self,
        # Molecule
        molecule          = "TiO2",
        charge            = 0,
        spin              = 0,
        basis             = "def2-svp",
        project_dir       = None,
        # Quantum solver
        quantum_solver    = "sqd",
        ansatz            = "lucj",
        fermion_to_qubit  = "bk",
        backend           = "mps",
        n_shots           = 8192,
        sqd_iters         = 10,
        ansatz_reps       = 3,
        # Classical
        classical_methods = None,
        # Geometry scan
        geometry_scan     = True,
        scan_atom_pair    = (0, 1),
        scan_distances    = None,
        scan_method       = "MP2",
        quantum_scan      = True,
        quantum_scan_fast = True,
        quantum_scan_shots= 2048,
        quantum_scan_iters= 4,
        # LUCJ
        lucj_num_layers      = 3,
        lucj_random_seed     = 42,
        lucj_regularization  = 1e-2,
        # block2
        blockexe_wrapper     = None,
        # Tier classification
        spin_contamination_tier2_threshold   = 1.3,
        spin_contamination_singlet_threshold = 0.05,
        homo_lumo_tier2_threshold_ev         = 1.0,
        gap_min_norb         = 2,
        gap_max_norb         = 16,
        core_occ_threshold   = 1.95,
        asf_params           = None,
        # DMET
        bath_tolerance       = 1e-8,
        min_bath_orbs        = 0,
        max_embed_orbs       = 24,
        # SKQD
        skqd_krylov_dim      = 5,
        skqd_dt              = 0.9,
        skqd_trotter_reps    = 1,
        skqd_shots           = 8192,
        # SqDRIFT
        sqdrift_num_circuits = 70,
        sqdrift_num_groups   = 100,
        sqdrift_time         = 2.0,
        sqdrift_iters        = 10,
        sqdrift_shots        = 8192,
        # MPS backend
        mps_max_bond_dim     = 256,
        mps_trunc_thresh     = 1e-6,
        # IBM backend
        ibm_backend_name        = None,
        ibm_optimization_level  = 1,
        ibm_max_circuit_depth   = 3000,
    ):
        # Molecule
        self.molecule    = molecule
        self.charge      = charge
        self.spin        = spin
        self.basis       = basis
        self.project_dir = project_dir or os.getcwd()

        # Quantum solver
        self.quantum_solver   = quantum_solver
        self.ansatz           = ansatz
        self.fermion_to_qubit = fermion_to_qubit
        self.backend          = backend
        self.n_shots          = n_shots
        self.sqd_iters        = sqd_iters
        self.ansatz_reps      = ansatz_reps

        # Classical
        self.classical_methods = classical_methods or ["HF", "MP2"]

        # Geometry scan
        self.geometry_scan     = geometry_scan
        self.scan_atom_pair    = scan_atom_pair
        self.scan_distances    = (scan_distances if scan_distances is not None
                                  else np.linspace(0.9, 4.0, 20))
        self.scan_method       = scan_method
        self.quantum_scan      = quantum_scan
        self.quantum_scan_fast = quantum_scan_fast
        self.quantum_scan_shots= quantum_scan_shots
        self.quantum_scan_iters= quantum_scan_iters

        # LUCJ
        self.lucj_num_layers     = lucj_num_layers
        self.lucj_random_seed    = lucj_random_seed
        self.lucj_regularization = lucj_regularization

        # block2
        self.blockexe_wrapper = (blockexe_wrapper or
                                  os.path.expanduser("~/block2main_wrapper.sh"))

        # TM elements
        self.tm_elements = {
            'Sc','Ti','V','Cr','Mn','Fe','Co','Ni','Cu','Zn',
            'Y','Zr','Nb','Mo','Tc','Ru','Rh','Pd','Ag','Cd',
            'La','Hf','Ta','W','Re','Os','Ir','Pt','Au','Hg',
            'Ce','Pr','Nd','Pm','Sm','Eu','Gd','Tb','Dy','Ho',
            'Er','Tm','Yb','Lu','Ac','Th','Pa','U','Np','Pu',
        }

        # Tier classification
        self.spin_contamination_tier2_threshold   = spin_contamination_tier2_threshold
        self.spin_contamination_singlet_threshold = spin_contamination_singlet_threshold
        self.homo_lumo_tier2_threshold_ev         = homo_lumo_tier2_threshold_ev
        self.gap_min_norb       = gap_min_norb
        self.gap_max_norb       = gap_max_norb
        self.core_occ_threshold = core_occ_threshold
        self.asf_params         = asf_params or {
            1: {"entropy_threshold": 0.05,  "max_norb": 12, "min_norb": 2},
            2: {"entropy_threshold": 0.02,  "max_norb": 14, "min_norb": 2},
            3: {"entropy_threshold": 0.005, "max_norb": 16, "min_norb": 4},
        }

        # DMET
        self.bath_tolerance = bath_tolerance
        self.min_bath_orbs  = min_bath_orbs
        self.max_embed_orbs = max_embed_orbs

        # SKQD
        self.skqd_krylov_dim   = skqd_krylov_dim
        self.skqd_dt           = skqd_dt
        self.skqd_trotter_reps = skqd_trotter_reps
        self.skqd_shots        = skqd_shots

        # SqDRIFT
        self.sqdrift_num_circuits = sqdrift_num_circuits
        self.sqdrift_num_groups   = sqdrift_num_groups
        self.sqdrift_time         = sqdrift_time
        self.sqdrift_iters        = sqdrift_iters
        self.sqdrift_shots        = sqdrift_shots

        # MPS
        self.mps_max_bond_dim = mps_max_bond_dim
        self.mps_trunc_thresh = mps_trunc_thresh

        # IBM
        self.ibm_backend_name       = ibm_backend_name
        self.ibm_optimization_level = ibm_optimization_level
        self.ibm_max_circuit_depth  = ibm_max_circuit_depth

        # Constants
        self.hartree_to_ev       = 27.211386245988
        self.hartree_to_kcal_mol = 627.5094740631

        # Geometry (populated by load_geometry())
        self.geometry  = None
        self.atom_syms = None
        self.n_atoms   = None

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

    # ── Methods ───────────────────────────────────────────────────────────────
    def load_geometry(self):
        """Load and cache geometry from CIF file."""
        self.geometry  = _load_geometry(self.molecule, self.cif_dir)
        self.atom_syms = [a[0] for a in self.geometry]
        self.n_atoms   = len(self.geometry)
        return self

    def make_dirs(self):
        """Create all output directories."""
        os.makedirs(self.results_dir, exist_ok=True)
        os.makedirs(self.cif_dir,     exist_ok=True)
        os.makedirs(self.plots_dir,   exist_ok=True)
        return self

    def validate(self):
        """Catch obvious config mistakes early."""
        assert self.spin >= 0
        assert self.n_shots > 0
        assert self.ansatz in ("su2", "lucj")
        assert self.fermion_to_qubit in ("jw", "bk")
        assert self.quantum_solver in ("sqd", "skqd", "sqdrift")
        return self

    def __repr__(self):
        return (f"Config(molecule={self.molecule}, basis={self.basis}, "
                f"solver={self.quantum_solver}, ansatz={self.ansatz})")