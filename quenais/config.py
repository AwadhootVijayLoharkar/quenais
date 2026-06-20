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
        # ... existing params ...

        # block2
        blockexe_wrapper    = None,

        # ASF / tier classification
        spin_contamination_tier2_threshold   = 1.3,
        spin_contamination_singlet_threshold = 0.05,
        homo_lumo_tier2_threshold_ev         = 1.0,
        gap_min_norb        = 2,
        gap_max_norb        = 16,
        core_occ_threshold  = 1.95,
        asf_params          = None,

        # DMET
        bath_tolerance      = 1e-8,
        min_bath_orbs       = 0,
        max_embed_orbs      = 24,

        # SU2
        ansatz_reps         = 3,

        # SKQD
        skqd_krylov_dim     = 5,
        skqd_dt             = 0.9,
        skqd_trotter_reps   = 1,
        skqd_shots          = 8192,

        # SqDRIFT
        sqdrift_num_circuits = 70,
        sqdrift_num_groups   = 100,
        sqdrift_time         = 2.0,
        sqdrift_iters        = 10,
        sqdrift_shots        = 8192,

        # MPS backend
        mps_max_bond_dim    = 256,
        mps_trunc_thresh    = 1e-6,

        # IBM backend
        ibm_backend_name        = None,
        ibm_optimization_level  = 1,
        ibm_max_circuit_depth   = 3000,
    ):
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
        self.bath_tolerance  = bath_tolerance
        self.min_bath_orbs   = min_bath_orbs
        self.max_embed_orbs  = max_embed_orbs

        # SU2
        self.ansatz_reps     = ansatz_reps

        # SKQD
        self.skqd_krylov_dim  = skqd_krylov_dim
        self.skqd_dt          = skqd_dt
        self.skqd_trotter_reps= skqd_trotter_reps
        self.skqd_shots       = skqd_shots

        # SqDRIFT
        self.sqdrift_num_circuits = sqdrift_num_circuits
        self.sqdrift_num_groups   = sqdrift_num_groups
        self.sqdrift_time         = sqdrift_time
        self.sqdrift_iters        = sqdrift_iters
        self.sqdrift_shots        = sqdrift_shots

        # MPS backend
        self.mps_max_bond_dim = mps_max_bond_dim
        self.mps_trunc_thresh = mps_trunc_thresh

        # IBM backend
        self.ibm_backend_name       = ibm_backend_name
        self.ibm_optimization_level = ibm_optimization_level
        self.ibm_max_circuit_depth  = ibm_max_circuit_depth


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