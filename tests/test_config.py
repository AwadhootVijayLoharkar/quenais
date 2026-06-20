"""
Basic tests for QuEnAIS package.
Tests only core functionality that requires no heavy dependencies.
"""

import os
import numpy as np
import pytest
from quenais.config import Config
from quenais.utils.cif_parser import load_geometry


# ── Config tests ──────────────────────────────────────────────────────────────

def test_config_defaults():
    cfg = Config()
    assert cfg.molecule       == "TiO2"
    assert cfg.basis          == "def2-svp"
    assert cfg.charge         == 0
    assert cfg.spin           == 0
    assert cfg.quantum_solver == "sqd"
    assert cfg.ansatz         == "lucj"
    assert cfg.n_shots        == 8192


def test_config_custom():
    cfg = Config(molecule="H2", basis="sto-3g", spin=0, n_shots=1024)
    assert cfg.molecule == "H2"
    assert cfg.basis    == "sto-3g"
    assert cfg.n_shots  == 1024


def test_config_validate_passes():
    cfg = Config()
    cfg.validate()


def test_config_validate_fails_bad_ansatz():
    cfg = Config()
    cfg.ansatz = "invalid"
    with pytest.raises(AssertionError):
        cfg.validate()


def test_config_validate_fails_bad_solver():
    cfg = Config()
    cfg.quantum_solver = "invalid"
    with pytest.raises(AssertionError):
        cfg.validate()


def test_config_validate_fails_bad_mapping():
    cfg = Config()
    cfg.fermion_to_qubit = "invalid"
    with pytest.raises(AssertionError):
        cfg.validate()


def test_config_validate_fails_negative_spin():
    cfg = Config()
    cfg.spin = -1
    with pytest.raises(AssertionError):
        cfg.validate()


def test_config_paths():
    cfg = Config(project_dir="/tmp/quenais_test")
    assert cfg.results_dir == "/tmp/quenais_test/results"
    assert cfg.cif_dir     == "/tmp/quenais_test/cif_files"
    assert cfg.plots_dir   == "/tmp/quenais_test/results/plots"
    assert cfg.step0_file  == "/tmp/quenais_test/results/step0_classical.pkl"
    assert cfg.step3_file  == "/tmp/quenais_test/results/step3_results.pkl"


def test_config_make_dirs(tmp_path):
    cfg = Config(project_dir=str(tmp_path))
    cfg.make_dirs()
    assert os.path.isdir(cfg.results_dir)
    assert os.path.isdir(cfg.cif_dir)
    assert os.path.isdir(cfg.plots_dir)


def test_config_repr():
    cfg = Config()
    r   = repr(cfg)
    assert "TiO2"   in r
    assert "sqd"    in r
    assert "lucj"   in r


def test_config_constants():
    cfg = Config()
    assert abs(cfg.hartree_to_ev - 27.211386245988) < 1e-6
    assert abs(cfg.hartree_to_kcal_mol - 627.5094740631) < 1e-4


def test_config_tm_elements():
    cfg = Config()
    assert "Ti" in cfg.tm_elements
    assert "Fe" in cfg.tm_elements
    assert "H"  not in cfg.tm_elements
    assert "C"  not in cfg.tm_elements
    assert len(cfg.tm_elements) == 50


def test_config_asf_params():
    cfg = Config()
    assert 1 in cfg.asf_params
    assert 2 in cfg.asf_params
    assert 3 in cfg.asf_params
    for tier in [1, 2, 3]:
        p = cfg.asf_params[tier]
        assert "entropy_threshold" in p
        assert "max_norb"          in p
        assert "min_norb"          in p
        assert p["max_norb"] >= p["min_norb"]


def test_config_scan_distances_default():
    cfg = Config()
    assert len(cfg.scan_distances) == 20
    assert cfg.scan_distances[0]  < cfg.scan_distances[-1]


def test_config_blockexe_wrapper():
    cfg = Config()
    assert "block2main_wrapper.sh" in cfg.blockexe_wrapper


# ── CIF parser tests ──────────────────────────────────────────────────────────

CIF_DIR = os.path.join(os.path.dirname(__file__), "..", "cif_files")


def test_tio2_geometry():
    geom = load_geometry("TiO2", CIF_DIR)
    assert len(geom) == 3
    syms = [a[0] for a in geom]
    assert "Ti" in syms
    assert syms.count("O") == 2


def test_geometry_no_duplicates():
    geom   = load_geometry("TiO2", CIF_DIR)
    coords = [np.array(a[1]) for a in geom]
    for i in range(len(coords)):
        for j in range(i + 1, len(coords)):
            dist = np.linalg.norm(coords[i] - coords[j])
            assert dist > 0.5, \
                f"Atoms {i} and {j} too close: {dist:.3f} Å"


def test_geometry_cartesian_coords():
    geom = load_geometry("TiO2", CIF_DIR)
    for sym, coord in geom:
        assert len(coord) == 3
        for c in coord:
            assert isinstance(float(c), float)


def test_missing_cif_raises():
    with pytest.raises(FileNotFoundError):
        load_geometry("DOESNOTEXIST", CIF_DIR)