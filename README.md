# acedrg

`acedrg` generates stereochemical descriptions (restraint dictionaries) for
ligands and links, for use in macromolecular refinement.

## Installation

```bash
pip install .
```

This builds the bundled C++ engine (`libmol`) with CMake and packages it
together with the acedrg stereochemistry tables, so no separate CCP4
installation is required at run time. The tables are fetched automatically from
the [aceDRG-tables](https://github.com/flong-mrc/aceDRG-tables) repository
during the build, so an internet connection is needed when installing.

### Requirements

- A C++17 compiler and CMake (>= 3.15)
- Python >= 3.8

Python dependencies (`rdkit`, `gemmi`, `networkx`, `numpy`, `future`,
`pdbecif`, `servalcat`) are installed automatically. 

## Usage

```bash
acedrg -i "<SMILES>" -o my_ligand
acedrg -m ligand.mol -o my_ligand
acedrg --help
```

After installation the bundled engine and tables are found automatically under
the environment prefix (`<prefix>/libexec/libmol`,
`<prefix>/share/acedrg/tables`). If a CCP4 environment is active it is used as
a fallback.

## Contributions

### AceDRG

Fei Long, Robert A Nicholls, Paul Emsley, Saulius Gražulis, Andrius Merkys, Antanas Vaitkus, Garib N Murshudov 

### Pip installation of AceDRG
Jordan Dialpuri, Lucrezia Catapano, Paul Emsley 