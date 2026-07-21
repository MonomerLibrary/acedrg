"""
Pytest suite for acedrg — one test per (subdir category, input file).

Each category picks N_EXAMPLES input files from the corresponding Tests_*/
subdirectory and asserts that acedrg produces the expected .cif output.

Environment variable overrides (all optional):
  ACEDRG_BIN          path to the acedrg executable
  ACEDRG_TESTS_DIR    path to the Tests/ directory (default: <repo-root>/Tests)
  ACEDRG_N_EXAMPLES   number of input files to test per category (default 3)
"""
import glob
import os
import shutil
import subprocess
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).parent

# -- acedrg binary -----------------------------------------------------------
# Priority: env var > PATH > local venv fallback
def _find_acedrg() -> str:
    if "ACEDRG_BIN" in os.environ:
        return os.environ["ACEDRG_BIN"]
    found = shutil.which("acedrg")
    if found:
        return found
    return str(_REPO_ROOT / ".venv" / "bin" / "acedrg")

ACEDRG = _find_acedrg()

# -- Tests directory ---------------------------------------------------------
TESTS_DIR = os.environ.get(
    "ACEDRG_TESTS_DIR",
    str(_REPO_ROOT / "Tests"),
)

# -- Number of examples per subdir -------------------------------------------
N_EXAMPLES = int(os.environ.get("ACEDRG_N_EXAMPLES", "3"))

# -- Runtime environment -----------------------------------------------------
# If servalcat (called by acedrg internally) is not already on PATH, add the
# same bin/ directory that contains the acedrg binary so it can be found.
_env = os.environ.copy()
if not shutil.which("servalcat"):
    _acedrg_bin_dir = str(Path(ACEDRG).parent)
    _env["PATH"] = f"{_acedrg_bin_dir}:{_env.get('PATH', '')}"
    _env["VIRTUAL_ENV"] = str(Path(ACEDRG).parent.parent)


def _run(args, cwd=None):
    return subprocess.run(
        [ACEDRG] + args,
        capture_output=True,
        text=True,
        cwd=cwd,
        env=_env,
    )


def _assert_cif(path, result):
    assert os.path.isfile(path), (
        f"Expected output not found: {path}\n"
        f"stdout: {result.stdout}\n"
        f"stderr: {result.stderr}"
    )


# ---------------------------------------------------------------------------
# Tests_Mol  (acedrg -m <file.mol>)
# ---------------------------------------------------------------------------
_mol_files = sorted(glob.glob(f"{TESTS_DIR}/Tests_Mol/inMol/*.mol"))[:N_EXAMPLES]


@pytest.mark.parametrize(
    "mol_file", _mol_files, ids=[os.path.basename(f) for f in _mol_files]
)
def test_mol(mol_file, tmp_path):
    stem = os.path.splitext(os.path.basename(mol_file))[0]
    out = str(tmp_path / f"Test_{stem}")
    result = _run(["-m", mol_file, "-o", out])
    _assert_cif(f"{out}.cif", result)


# ---------------------------------------------------------------------------
# Tests_Smi  (acedrg -i <file.smiles>)
# ---------------------------------------------------------------------------
_smi_files = sorted(glob.glob(f"{TESTS_DIR}/Tests_Smi/inSmi/*.smiles"))[:N_EXAMPLES]


@pytest.mark.parametrize(
    "smi_file", _smi_files, ids=[os.path.basename(f) for f in _smi_files]
)
def test_smi(smi_file, tmp_path):
    stem = os.path.splitext(os.path.basename(smi_file))[0]
    out = str(tmp_path / f"Test_{stem}")
    result = _run(["-i", smi_file, "-o", out])
    _assert_cif(f"{out}.cif", result)


# ---------------------------------------------------------------------------
# Tests_Mol2  (acedrg -g <file.mol2>)
# ---------------------------------------------------------------------------
_mol2_files = sorted(glob.glob(f"{TESTS_DIR}/Tests_Mol2/inMol2/*.mol2"))[:N_EXAMPLES]


@pytest.mark.parametrize(
    "mol2_file", _mol2_files, ids=[os.path.basename(f) for f in _mol2_files]
)
def test_mol2(mol2_file, tmp_path):
    stem = os.path.splitext(os.path.basename(mol2_file))[0]
    out = str(tmp_path / f"Test_{stem}")
    result = _run(["-g", mol2_file, "-o", out])
    _assert_cif(f"{out}.cif", result)


# ---------------------------------------------------------------------------
# Tests_Mmcif / CCD  (acedrg -c <file.cif>)
# ---------------------------------------------------------------------------
_ccd_files = sorted(
    glob.glob(f"{TESTS_DIR}/Tests_Mmcif/inFilesCCD/*.cif")
)[:N_EXAMPLES]


@pytest.mark.parametrize(
    "cif_file", _ccd_files, ids=[os.path.basename(f) for f in _ccd_files]
)
def test_mmcif_ccd(cif_file, tmp_path):
    stem = os.path.splitext(os.path.basename(cif_file))[0]
    out = str(tmp_path / f"Test_{stem}")
    result = _run(["-c", cif_file, "-o", out])
    _assert_cif(f"{out}.cif", result)


# ---------------------------------------------------------------------------
# Tests_Mmcif / CCP4ML  (acedrg -c <file.cif>)
# ---------------------------------------------------------------------------
_ccp4ml_files = sorted(
    glob.glob(f"{TESTS_DIR}/Tests_Mmcif/inFilesCCP4ML/*.cif")
)[:N_EXAMPLES]


@pytest.mark.parametrize(
    "cif_file", _ccp4ml_files, ids=[os.path.basename(f) for f in _ccp4ml_files]
)
def test_mmcif_ccp4ml(cif_file, tmp_path):
    stem = os.path.splitext(os.path.basename(cif_file))[0]
    out = str(tmp_path / f"Test_{stem}")
    result = _run(["-c", cif_file, "-o", out])
    _assert_cif(f"{out}.cif", result)


# ---------------------------------------------------------------------------
# Tests_Option_r — run each file twice: without -r, then with -r <RRR>
# The original script uses the first letter of the ligand name repeated 3×
# as the residue-name override.
# ---------------------------------------------------------------------------
_option_r_files = sorted(
    glob.glob(f"{TESTS_DIR}/Tests_Option_r/inOption_r/*.cif")
)[:N_EXAMPLES]


@pytest.mark.parametrize(
    "cif_file", _option_r_files, ids=[os.path.basename(f) for f in _option_r_files]
)
def test_option_r_without(cif_file, tmp_path):
    stem = os.path.splitext(os.path.basename(cif_file))[0]
    out = str(tmp_path / f"Test_{stem}_no_r")
    result = _run(["-c", cif_file, "-o", out, "-p"])
    _assert_cif(f"{out}.cif", result)


@pytest.mark.parametrize(
    "cif_file", _option_r_files, ids=[os.path.basename(f) for f in _option_r_files]
)
def test_option_r_with(cif_file, tmp_path):
    stem = os.path.splitext(os.path.basename(cif_file))[0]
    r_val = stem[0] * 3
    out = str(tmp_path / f"Test_{stem}_with_r")
    result = _run(["-c", cif_file, "-o", out, "-r", r_val, "-p"])
    _assert_cif(f"{out}.cif", result)


# ---------------------------------------------------------------------------
# Tests_Links  (acedrg -L <instruct_*.txt>)
# Instruction files may contain FILE-1/FILE-2 paths relative to Tests_Links/,
# so we set cwd there.
# ---------------------------------------------------------------------------
_link_files = sorted(
    glob.glob(f"{TESTS_DIR}/Tests_Links/inLink/instruct_*.txt")
)[:N_EXAMPLES]
_links_cwd = f"{TESTS_DIR}/Tests_Links"


@pytest.mark.parametrize(
    "instruct_file",
    _link_files,
    ids=[os.path.basename(f) for f in _link_files],
)
def test_links(instruct_file, tmp_path):
    stem = os.path.basename(instruct_file).removeprefix("instruct_").removesuffix(".txt")
    out = str(tmp_path / f"Test_{stem}")
    result = _run(["-L", instruct_file, "-o", out], cwd=_links_cwd)
    _assert_cif(f"{out}_link.cif", result)


# ---------------------------------------------------------------------------
# Tests_Metal  (acedrg -c <file.cif> -p)
# Reads metalLigands.list and picks the first N single-CIF-only entries.
# ---------------------------------------------------------------------------
def _metal_codes(n: int) -> list[str]:
    list_path = f"{TESTS_DIR}/Tests_Metal/inFiles/metalLigands.list"
    codes = []
    with open(list_path) as fh:
        for line in fh:
            parts = line.strip().split()
            if len(parts) == 1:
                codes.append(parts[0])
                if len(codes) == n:
                    break
    return codes


_metal_codes_list = _metal_codes(N_EXAMPLES)


@pytest.mark.parametrize("code", _metal_codes_list)
def test_metal(code, tmp_path):
    cif = f"{TESTS_DIR}/Tests_Metal/inFiles/{code}.cif"
    out = str(tmp_path / f"Test_{code}_p")
    result = _run(["-c", cif, "-o", out, "-p"])
    _assert_cif(f"{out}.cif", result)


# ---------------------------------------------------------------------------
# Tests_Aroma  (acedrg -c <file.cif>)
# ---------------------------------------------------------------------------
_aroma_files = sorted(
    glob.glob(f"{TESTS_DIR}/Tests_Aroma/inFiles/*.cif")
)[:N_EXAMPLES]


@pytest.mark.parametrize(
    "cif_file", _aroma_files, ids=[os.path.basename(f) for f in _aroma_files]
)
def test_aroma(cif_file, tmp_path):
    stem = os.path.splitext(os.path.basename(cif_file))[0]
    out = str(tmp_path / f"Test_{stem}")
    result = _run(["-c", cif_file, "-o", out])
    _assert_cif(f"{out}.cif", result)


# ---------------------------------------------------------------------------
# Tests_Carborns  (acedrg -c <file.cif>)
# ---------------------------------------------------------------------------
_carborn_files = sorted(
    glob.glob(f"{TESTS_DIR}/Tests_Carborns/inFiles/*.cif")
)[:N_EXAMPLES]


@pytest.mark.parametrize(
    "cif_file", _carborn_files, ids=[os.path.basename(f) for f in _carborn_files]
)
def test_carborns(cif_file, tmp_path):
    stem = os.path.splitext(os.path.basename(cif_file))[0]
    out = str(tmp_path / f"Test_{stem}")
    result = _run(["-c", cif_file, "-o", out])
    _assert_cif(f"{out}.cif", result)
