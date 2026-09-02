# AceDRG

[![PyPI](https://img.shields.io/pypi/v/acedrg.svg)](https://pypi.org/project/acedrg/)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://pypi.org/project/acedrg/)
[![Wheel](https://img.shields.io/pypi/wheel/acedrg.svg)](https://pypi.org/project/acedrg/#files)
[![Platforms](https://img.shields.io/badge/platform-linux%20%7C%20macOS%20%7C%20windows-lightgrey.svg)](https://pypi.org/project/acedrg/#files)
[![Downloads](https://img.shields.io/pypi/dm/acedrg.svg)](https://pypi.org/project/acedrg/)
[![Tests](https://github.com/MonomerLibrary/AceDRG/actions/workflows/test.yml/badge.svg)](https://github.com/MonomerLibrary/AceDRG/actions/workflows/test.yml)
[![DOI](https://img.shields.io/badge/DOI-10.1107%2FS2059798317000067-blue.svg)](https://doi.org/10.1107/S2059798317000067)
[![Last commit](https://img.shields.io/github/last-commit/MonomerLibrary/AceDRG.svg)](https://github.com/MonomerLibrary/AceDRG/commits/master)

AceDRG generates stereochemical descriptions (restraint dictionaries) for
ligands and links, for use in macromolecular refinement.

## Installation

```bash
pip install acedrg
```

Prebuilt wheels are available for Linux (x86_64), macOS (Apple silicon) and
Windows (x64); each wheel bundles the C++ engine (`libmol`) and the AceDRG
stereochemistry tables, so no separate CCP4 installation is required at run
time.

Optional extras:
<!-- pip install "acedrg[metal]"     # metal-site restraints via metalCoord
 -->
```bash
pip install "acedrg[tautomer]"  # tautomer handling via molvs
```

## Usage

```bash
acedrg -i "CCO" -o ethanol          # from a SMILES string (or a file of one)
acedrg -m ligand.mol -o my_ligand   # from an MDL mol file
acedrg -s ligand.sdf -o my_ligand   # from an SDF file
acedrg -c ligand.cif -o my_ligand   # from an mmCIF file
acedrg -L link_instructions.txt -o my_link   # covalent link description
acedrg --help                       # full option list
```

The bundled engine and tables are located automatically under the environment
prefix (`<prefix>/libexec/libmol`, `<prefix>/share/acedrg/tables`). If a CCP4
environment is active it is used as a fallback.

## Building from source

On platforms without a wheel, pip builds from the sdist; you can also install
from a clone:

```bash
git clone https://github.com/MonomerLibrary/AceDRG
cd AceDRG
pip install .
```

Requirements:

- A C++17 compiler and CMake (>= 3.15)
- Python >= 3.8
- An internet connection — the stereochemistry tables are fetched during the
  build from the [aceDRG-tables](https://github.com/flong-mrc/aceDRG-tables)
  repository

Python dependencies (`rdkit`, `gemmi`, `networkx`, `numpy`, `future`,
`pdbecif`, `servalcat`) are installed automatically.

## Tests

```bash
pip install ".[tautomer]" pytest
pytest -v python-tests --run-extra
```

## Citation

Long F, Nicholls RA, Emsley P, Gražulis S, Merkys A, Vaitkus A, Murshudov GN
(2017). *AceDRG: a stereochemical description generator for ligands.*
Acta Cryst. D **73**, 112–122. doi:
[10.1107/S2059798317000067](https://doi.org/10.1107/S2059798317000067)

## Contributions

### AceDRG

Fei Long, Robert A. Nicholls, Paul Emsley, Saulius Gražulis, Andrius Merkys,
Antanas Vaitkus, Garib N. Murshudov

### Pip installation of AceDRG

Jordan Dialpuri,
Lucrezia Catapano, Paul Emsley

## Contact

- AceDRG: Fei Long — <flong@mrclmb.ac.uk>
- Pip packaging and installation: Jordan Dialpuri — <jdialpuri@mrclmb.ac.uk>

Bug reports and feature requests are best raised as
[GitHub issues](https://github.com/MonomerLibrary/AceDRG/issues).
