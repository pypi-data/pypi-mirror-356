# AEFG (Atomic Environment-based Functional Group)

## Overview

AEFG is an advanced cheminformatics algorithm for molecular fragmentation that decomposes small molecules into their constituent functional groups based on atomic environment analysis. This tool provides a systematic approach to break down molecular structures into chemically meaningful substructures, enabling functional group-level analysis of chemical compounds.

## Installation

### Prerequisites

- Python 3.6+

- RDKit (2021.03 or later)

```python
pip install aefg
```

## Basic Usage

```python
from AEFG import molecule_fg
from AEFG import rxn_fg

# Fragment a molecule
smlies = "NH2][C@@H](CC(=O)O)C(=O)O"
results = molecule_fg("smlies")
# output:[C@@H]N, C, O=CO, O=CO]

# Fragment a reaction
rxn_smlies= 'N[C@@H](CC(O)=O)C(=O)O.O=C(O)CCC(=O)C(=O)O>>N[C@@H](CCC(O)=O)C(=O)O.O=C(O)CC(=O)C(=O)O'
results = rxn_fg(rxn_smlies)

```

## License

AEFG is released under the MIT License.