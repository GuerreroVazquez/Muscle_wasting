# Import Graph — Essential Modules

> Generated: 2026-04-09  
> Scope: modules classified as **KEEP** in `file_inventory.md`  
> Tool: manual static analysis of `import` / `from … import` statements

---

## Notation

```
A  ──►  B          A imports B (internal module)
A  ··►  B          A imports B (external / stdlib package)
A  ══►  B          A imports B (config/data file loaded at runtime)
```

Arrows point from the importer to the imported dependency.

---

## Module dependency graph (text representation)

```
network/main_pipeline.py
  ──►  cytoscape/                     (import cytoscape as ct)
  ──►  network/network_processing.py  (import network_processing as ntp)
  ──►  network/node_evaluation.py     (import node_evaluation as ne)
  ──►  Constants.py                   (import Constants)
  ··►  pandas
  ··►  py4cytoscape
  ··►  os, os.path [stdlib]

network/network_processing.py
  ──►  database_analysis/sql_operations.py   (from database_analysis import sql_operations as sql)
  ──►  cytoscape/                            (from cytoscape import read_cytoscape_json,
       |                                      format_cytoscape_json, create_cytoscape_node,
       |                                      create_cytoscape_edge, protein_name)
  ··►  networkx
  ··►  numpy
  ··►  pandas
  ··►  random, sys, os [stdlib]

network/node_evaluation.py
  ──►  network/network_processing.py   (import network_processing as nx  ← NOTE: shadows networkx alias)
  ··►  networkx
  ··►  numpy

network/walking_network.py
  ──►  network/network_processing.py   (import network_processing as nx)

cytoscape/__init__.py
  ──►  cytoscape/cytoscape.py          (re-exports public symbols)
  ──►  cytoscape/element.py
  ──►  cytoscape/enum_network_sources.py

cytoscape/cytoscape.py
  ──►  cytoscape/element.py            (internal)
  ──►  cytoscape/enum_network_sources.py
  ··►  json, yaml, requests, logging [stdlib/external]

cytoscape/enum_network_sources.py
  ══►  cytoscape/Data/Apps_details.yaml        (loaded via yaml.safe_load at runtime)
  ══►  cytoscape/Data/properties_2_keep.yaml   (loaded via yaml.safe_load at runtime)
  ··►  os, enum [stdlib]
  ··►  yaml

cytoscape/element.py
  (no imports of internal modules)

database_analysis/sql_operations.py
  ──►  database_analysis/logs.py   (from logs import logger  OR  from logger import logger)
  ··►  mysql.connector
  ··►  pandas

database_analysis/logs.py
  ··►  logging [stdlib]
  ··►  logger (external package)

common_tools/common_tools.py
  ··►  csv [stdlib]
  ··►  bios
  ··►  requests
  ··►  beautifulsoup4 (bs4)

Constants.py
  (no imports — pure data/constants file)

ncbi/eutilities.py
  ··►  eutils
  ··►  lxml
  ··►  xml.etree.ElementTree [stdlib]
```

---

## Layered dependency diagram

The modules form four clear layers:

```
┌──────────────────────────────────────────────────────────────────────┐
│  LAYER 4 — Orchestration / CLI                                        │
│                                                                        │
│   network/main_pipeline.py                                             │
└─────────────────────┬──────────────┬───────────────────────────────── ┘
                      │              │
         ┌────────────▼──────────────▼──────────────────────────────────┐
         │  LAYER 3 — Domain Logic                                        │
         │                                                                │
         │   network/network_processing.py   network/node_evaluation.py  │
         │   network/walking_network.py                                   │
         └────────────┬──────────────┬──────────────────────────────────┘
                      │              │
         ┌────────────▼──────────────▼──────────────────────────────────┐
         │  LAYER 2 — I/O & Data Access                                   │
         │                                                                │
         │   cytoscape/cytoscape.py          (graph I/O)                 │
         │   cytoscape/element.py            (data model)                │
         │   cytoscape/enum_network_sources.py (source config)           │
         │   database_analysis/sql_operations.py (DB access)             │
         └────────────┬──────────────┬──────────────────────────────────┘
                      │              │
         ┌────────────▼──────────────▼──────────────────────────────────┐
         │  LAYER 1 — Shared Utilities & Config                           │
         │                                                                │
         │   common_tools/common_tools.py                                │
         │   database_analysis/logs.py                                   │
         │   Constants.py                                                 │
         │   cytoscape/Data/Apps_details.yaml  (runtime config)          │
         │   cytoscape/Data/properties_2_keep.yaml (runtime config)      │
         └────────────────────────────────────────────────────────────── ┘
```

---

## Key observations and migration notes

### 1. Naming collision in `node_evaluation.py`
`node_evaluation.py` contains:
```python
import network_processing as nx
```
This **shadows** the standard `networkx as nx` alias used everywhere else.  
Both `networkx` (external) and `network_processing` (internal) are used in that file.  
**Action:** In the migrated codebase, rename the alias (e.g., `import network_processing as ntp`) to avoid confusion.

### 2. `cytoscape/` is a critical shared dependency
`cytoscape/` is imported by **three** layers: main_pipeline, network_processing, and all network tests.  
It must be kept together as an intact sub-package during migration.  
**Target path:** `src/mirkat/io/cytoscape/`

### 3. `database_analysis/sql_operations.py` is the sole DB boundary
All remote MySQL access flows through a single module.  
The DB config (host, credentials) is hardcoded — this **must** be externalised to environment variables or a config file before the v1 release.  
**Action:** Introduce `configs/default.yml` and load credentials from environment.

### 4. `paper_mining/` is an isolated subgraph
`paper_mining/` has its own copies of `common_tools.py` and `eutilities.py`.  
It does **not** import any `network/` or `cytoscape/` modules.  
It can be migrated independently or omitted from v1 without breaking the core pipeline.

### 5. `ncbi/eutilities.py` and `paper_mining/eutilities.py` are duplicates
Both wrap the `eutils` package.  
**Action:** Consolidate into `src/mirkat/io/ncbi.py` and update all callers.

### 6. `network/jupyter_functions.py` partially duplicates `walking_network.py`
Functions like `register_path`, `visit_all_neighbours`, `start_mir_path` appear in both files.  
**Action:** Audit for differences; keep the version in `walking_network.py` as canonical.

---

## External package dependency summary

| Package | Version (requirements.txt) | Used by |
|---------|---------------------------|---------|
| `networkx` | 2.6.3 | `network_processing`, `node_evaluation`, `walking_network` |
| `pandas` | 2.2.2 | `network_processing`, `sql_operations`, `main_pipeline` |
| `numpy` | 2.0.0 | `network_processing`, `node_evaluation`, `walking_network` |
| `py4cytoscape` | 1.5.0 | `main_pipeline` (open Cytoscape sessions) |
| `mysql-connector-python` | 8.0.33 | `sql_operations` |
| `yaml` (PyYAML) | — (not pinned) | `enum_network_sources`, `cytoscape.py` |
| `requests` | 2.27.1 | `common_tools`, `cytoscape.py` |
| `beautifulsoup4` | 4.10.0 | `common_tools` |
| `bios` | 0.1.2 | `common_tools` |
| `eutils` | ~0.6.0 | `ncbi/eutilities.py`, `paper_mining/eutilities.py` |
| `lxml` | — (not pinned) | `ncbi/eutilities.py` |
| `logger` | ~1.4 | `sql_operations`, `logs.py` |
| `pytest` | ~7.1.2 | All test modules |
| `scikit-learn` | 1.5.0 | `network_processing` (SpectralClustering) |
| `scipy` | 1.14.0 | `network_processing` (pdist, squareform) |
| `matplotlib` | 3.9.0 | `network_processing` (draw_graph) |
| `dash` | ~2.5.1 | (referenced in requirements but not found in core imports) |

> **Note:** `PyYAML` is used but not pinned in `requirements.txt`. Add an explicit pin (e.g., `PyYAML>=6.0`) to prevent silent breakage.
