# File Inventory — Muscle_wasting Repository

> Generated: 2026-04-09  
> Branch: `GuerreroVazquez-master`  
> Decision key: **KEEP** = required for core pipeline / tests; **DROP** = exploratory, generated, or redundant; **ARCHIVE** = potentially useful but not core runtime; **EXTERNAL** = large data that should live in a data repository or LFS.

---

## Classification decision tree applied

1. Imported by an essential module → **KEEP**
2. Required by a public CLI workflow documented in README → **KEEP**
3. Test/fixture data needed for reproducibility → **KEEP** (minimal subset)
4. Exploratory artifact (notebook, pickle, log, IDE metadata) → **DROP / ARCHIVE**
5. Large binary/data file → **EXTERNAL**

---

## Root-level files

| Path | Owner | Purpose | Decision | Rationale |
|------|-------|---------|----------|-----------|
| `__init__.py` | Karen GV | Package marker for root module | KEEP | Required for relative imports |
| `Constants.py` | Karen GV | Shared test fixtures and constant data (small cytoscape JSON samples) | KEEP | Imported by `network/test_*.py`, `cytoscape/test_cytoscape.py`; needed for unit tests |
| `main.py` | Karen GV | **Stub only** – prints "Hi PyCharm"; not the actual pipeline entry-point | DROP | Contains no pipeline logic; README references functions that do not exist here; safe to delete or replace with real CLI entry |
| `requirements.txt` | Karen GV | Python dependency list (pinned versions) | KEEP | Required for reproducible installs |
| `README.md` | Karen GV | Project overview and quickstart | KEEP | User-facing documentation; needs rewrite for v1 migration |
| `DE_genes.ods` | Karen GV | Example spreadsheet of differentially expressed genes | ARCHIVE | Binary spreadsheet; useful as reference data but not imported by code; move to `data/` or docs |
| `Untitled.ipynb` | Karen GV | Blank / scratch Jupyter notebook | DROP | No content; pure exploratory artifact |
| `.gitignore` | Karen GV | Git ignore rules | KEEP | Necessary for version control hygiene |

---

## `.idea/` — IDE configuration

| Path | Owner | Purpose | Decision | Rationale |
|------|-------|---------|----------|-----------|
| `.idea/` (all files) | Karen GV | PyCharm project metadata | DROP | IDE-specific; not portable; should be in `.gitignore` |

---

## `common_tools/`

| Path | Owner | Purpose | Decision | Rationale |
|------|-------|---------|----------|-----------|
| `common_tools/__init__.py` | Karen GV | Package marker | KEEP | Required for module resolution |
| `common_tools/common_tools.py` | Karen GV | Shared file I/O and CSV helpers; imports `bios`, `requests`, `BeautifulSoup` | KEEP | Imported by `Tests/test_common_tools.py`; provides reusable utilities |

---

## `Constants.py` (see root-level above)

---

## `cytoscape/`

| Path | Owner | Purpose | Decision | Rationale |
|------|-------|---------|----------|-----------|
| `cytoscape/__init__.py` | Karen GV | Package marker; re-exports `read_cytoscape_json`, `format_cytoscape_json`, `create_cytoscape_node`, `create_cytoscape_edge`, `protein_name` | KEEP | Imported by `network/network_processing.py`, `network/main_pipeline.py`, all network tests |
| `cytoscape/cytoscape.py` | Karen GV | Core I/O: reads/writes Cytoscape JSON (`.cyjs`), formats graph data, creates node/edge objects | KEEP | Primary I/O layer for the network pipeline |
| `cytoscape/element.py` | Karen GV | Data class for Cytoscape element (data + position + selected) | KEEP | Used internally by `cytoscape.py` |
| `cytoscape/enum_network_sources.py` | Karen GV | `NetworkSource` enum mapping source names (STRING, GeneMANIA, INTACT, TF) to YAML-configured key sets | KEEP | Imported by `network/network_processing.py` and tests; controls how each network source is parsed |
| `cytoscape/Data/Apps_details.json` | Karen GV | JSON copy of network source app details | ARCHIVE | Superseded by the YAML version; not imported directly |
| `cytoscape/Data/Apps_details.yaml` | Karen GV | YAML config loaded by `NetworkSource._load_keys()` at runtime | KEEP | Required at runtime by `enum_network_sources.py` |
| `cytoscape/Data/properties_2_keep.yaml` | Karen GV | YAML config listing node/edge properties to retain per source | KEEP | Required at runtime by `NetworkSource._load_desired_data()` |
| `cytoscape/Diff_express_genes.cyjs` | Karen GV | Large example Cytoscape network export (16 MB) | EXTERNAL | Binary-like JSON; 16 MB; not referenced by tests; move to external data store or Git LFS |
| `cytoscape/graph1_Analysis_Sarcopenia.cyjs.png` | Karen GV | Screenshot of a network analysis | DROP | Image artifact; not imported or tested |
| `cytoscape/test.cyjs` | Karen GV | Small test Cytoscape fixture | KEEP | Used as fixture in `test_cytoscape.py` |
| `cytoscape/test_cytoscape.py` | Karen GV | Unit tests for cytoscape I/O functions | KEEP | Core test coverage for the I/O layer |
| `cytoscape/Cytoscape_trials.ipynb` | Karen GV | Exploratory notebook for Cytoscape API experiments | DROP | Notebook; exploratory; not reproducible without live Cytoscape desktop |
| `cytoscape/.ipynb_checkpoints/` | Karen GV | Jupyter checkpoint for `Cytoscape_trials.ipynb` | DROP | Auto-generated; should be in `.gitignore` |

---

## `data/`

| Path | Owner | Purpose | Decision | Rationale |
|------|-------|---------|----------|-----------|
| `data/All_negative_slope.txt` | Karen GV | Gene list: all genes with negative age-slope | KEEP (minimal) | Small text fixture; may be needed for integration tests |
| `data/All_positive_slope.txt` | Karen GV | Gene list: all genes with positive age-slope | KEEP (minimal) | Small text fixture; may be needed for integration tests |
| `data/Middle_Old_negative.txt` | Karen GV | DEG list: Middle vs Old, down-regulated | KEEP (minimal) | Small fixture |
| `data/Middle_Old_positive.txt` | Karen GV | DEG list: Middle vs Old, up-regulated | KEEP (minimal) | Small fixture |
| `data/Young_Old_negative.txt` | Karen GV | DEG list: Young vs Old, down-regulated | KEEP (minimal) | Small fixture |
| `data/Young_Old_positive.txt` | Karen GV | DEG list: Young vs Old, up-regulated | KEEP (minimal) | Small fixture |

---

## `database_analysis/`

| Path | Owner | Purpose | Decision | Rationale |
|------|-------|---------|----------|-----------|
| `database_analysis/__init__.py` | Karen GV | Package marker | KEEP | Required for `from database_analysis import sql_operations` in `network_processing.py` |
| `database_analysis/sql_operations.py` | Karen GV | MySQL connector to remote miRNA DB; executes queries for miRNA–target relationships and tissue expression | KEEP | Imported by `network/network_processing.py`; central data access layer |
| `database_analysis/logs.py` | Karen GV | Logging setup (wraps `logger` package) | KEEP | Imported by `sql_operations.py` and other modules |
| `database_analysis/convert_gene_names.py` | Karen GV | Utility: converts gene identifiers via NCBI/Entrez | ARCHIVE | Not directly imported by core pipeline; useful but ancillary |
| `database_analysis/get_genes.py` | Karen GV | Fetches gene lists from DB | ARCHIVE | Not imported by core network pipeline; may be used in data prep |
| `database_analysis/remote_conection_test.py` | Karen GV | Ad hoc script to test remote DB connectivity | DROP | Diagnostic/dev script; not part of pipeline |
| `database_analysis/update_genes.sql` | Karen GV | 3.8 MB SQL script to populate gene table | EXTERNAL | Large SQL dump; belongs in DB migration tooling or external data store, not runtime repo |
| `database_analysis/test_convert_gene_names.py` | Karen GV | Tests for `convert_gene_names.py` | ARCHIVE | Keep if `convert_gene_names.py` is kept |
| `database_analysis/test_sql_connections.py` | Karen GV | Tests for DB connectivity (requires live DB) | ARCHIVE | Integration test needing live DB; move to `tests/integration/` |
| `database_analysis/__pycache__/` | auto | Python bytecode cache | DROP | Auto-generated; should be in `.gitignore` |

---

## `Databases/`

| Path | Owner | Purpose | Decision | Rationale |
|------|-------|---------|----------|-----------|
| `Databases/HMDD/target.txt` (2.1 MB) | External | HMDD miRNA–disease association targets | EXTERNAL | Large external database dump; not imported directly; should live in data registry or LFS |
| `Databases/HMDD/tissue_expression.txt` (1.9 MB) | External | HMDD tissue expression data | EXTERNAL | Large external DB dump; same reasoning |
| `Databases/diana_miTed/miTED-Log2RPM.tsv` (21 MB) | External | DIANA miTED miRNA tissue expression (Log2 RPM) | EXTERNAL | 21 MB; largest single file; required by `network_processing.py` at runtime; move to Git LFS or object storage |
| `Databases/dunhill/dunhill abundances.xlsx` (612 KB) | External | Dunhill abundance measurements | EXTERNAL | Binary Excel file; reference data; move to LFS |
| `Databases/dunhill/dunhillAbundances.txt` | External | Text version of Dunhill abundances | EXTERNAL | Reference data; not imported by tests; move to LFS |
| `Databases/dunhill/experiments.txt` | External | Dunhill experiment metadata | EXTERNAL | Reference data |
| `Databases/miRBase/miRNA.dat` (44 MB) | External | miRBase full annotation flat file | EXTERNAL | 44 MB; largest file in repo; must be in Git LFS or separate data repo |
| `Databases/miRBase/mature.fa` (3.7 MB) | External | miRBase mature miRNA sequences (FASTA) | EXTERNAL | Binary-like; move to LFS |
| `Databases/miRBase/mature.fa.gz` (788 KB) | External | Compressed FASTA | EXTERNAL | Duplicate compressed copy; move to LFS or deduplicate |
| `Databases/miRBase/mirna.txt` (6.9 MB) | External | miRBase tabular dump | EXTERNAL | Large DB dump; LFS |
| `Databases/miRBase/mirna_mature.txt` (3.2 MB) | External | miRBase mature miRNA dump | EXTERNAL | Large; LFS |
| `Databases/miRBase/mirna_context.txt` (1.3 MB) | External | miRBase context annotations | EXTERNAL | LFS |
| `Databases/miRBase/mirna_context (1).txt` (1.3 MB) | External | Duplicate of `mirna_context.txt` | DROP | Exact duplicate with space in filename; remove |
| `Databases/miRBase/mirna_chromosome_build.txt` (1.2 MB) | External | Chromosome build mapping | EXTERNAL | LFS |
| `Databases/miRBase/confidence.txt` (1.6 MB) | External | miRBase confidence scores | EXTERNAL | LFS |
| `Databases/miRBase/confidence_score.txt` | External | miRBase confidence scores (alt format) | EXTERNAL | Potentially duplicate; evaluate against `confidence.txt` |
| `Databases/miRBase/dead_mirna.txt` | External | Deprecated/dead miRNA IDs | KEEP (small) | Small; referenced by pipeline to filter obsolete IDs |
| `Databases/miRBase/mature_database_links.txt` (992 KB) | External | DB cross-reference links | EXTERNAL | LFS |
| `Databases/miRBase/mature_database_url.txt` | External | DB URL list | EXTERNAL | Small but reference-only |
| `Databases/miRBase/mirna_database_links.txt` (436 KB) | External | DB cross-reference links | EXTERNAL | LFS |
| `Databases/miRBase/mirna_database_url.txt` | External | DB URL list | EXTERNAL | Reference-only |
| `Databases/miRBase/mirna_literature_references.txt` (688 KB) | External | Literature references | EXTERNAL | LFS |
| `Databases/miRBase/literature_references.txt` | External | Literature references | EXTERNAL | Possibly duplicate; evaluate |
| `Databases/miRBase/mirna_2_prefam.txt` | External | miRNA-to-precursor-family mapping | EXTERNAL | DB dump |
| `Databases/miRBase/mirna_pre_mature.txt` (976 KB) | External | Pre-miRNA to mature mapping | EXTERNAL | LFS |
| `Databases/miRBase/mirna_prefam.txt` | External | Precursor family table | EXTERNAL | DB dump |
| `Databases/miRBase/mirna_species.txt` | External | Species table | EXTERNAL | DB dump |
| `Databases/miRBase/mirna_seeds_table.sql` | External | SQL for seeds table | EXTERNAL | SQL schema/data; belongs in DB migration scripts |
| `Databases/miRBase/organisms.txt` | External | Organism listing | EXTERNAL | Reference data |
| `Databases/miRBase/*.sql` (All_tables, Analyze_querys, Gibran_query, etc.) | Karen GV | SQL analysis queries and schema scripts | ARCHIVE | Dev/research scripts; move to `docs/migration/` or a `scripts/db/` folder |
| `Databases/miRNATissueAtlas2/miRNATissueAtlas2.txt` | External | miRNA Tissue Atlas v2 expression data | EXTERNAL | Reference DB dump; LFS |
| `Databases/mini_test/mirTarBase/miRTarBase_Target.txt` | External | Small miRTarBase fixture for testing | KEEP (minimal) | Test fixture; small; keep for contract tests |
| `Databases/mini_test/parsed/mirTarBase_miRTarBase_Target.txt` | External | Parsed version of mini_test fixture | KEEP (minimal) | Test fixture |
| `Databases/organs.txt` | External | Organ/tissue list used in network annotation | KEEP (small) | Referenced by `network_processing.add_organ_system_relationship()` |
| `Databases/parsed/genes.txt` | External | Pre-parsed gene list | KEEP (small) | Referenced by network processing as input |
| `Databases/targetscan/seeds.txt` (312 KB) | External | TargetScan seed sequences | EXTERNAL | Reference data; moderate size; LFS or external store |
| `Databases/sources.ods` | Karen GV | Spreadsheet listing data sources | ARCHIVE | Documentation artifact; not imported by code; move to `docs/` |

---

## `ncbi/`

| Path | Owner | Purpose | Decision | Rationale |
|------|-------|---------|----------|-----------|
| `ncbi/__init__.py` | Karen GV | Package marker | KEEP | Required for `from ncbi import eutilities` in `Tests/test_ncbi.py` |
| `ncbi/eutilities.py` | Karen GV | Wrapper around `eutils` for NCBI Entrez queries (gene → PubMed, gene details) | KEEP | Imported by `Tests/test_ncbi.py`; utility for literature evidence |
| `ncbi/main.py` | Karen GV | NCBI CLI entry-point / demo script | ARCHIVE | Not imported by core pipeline; candidate for `examples/` |
| `ncbi/__pycache__/` | auto | Bytecode cache | DROP | Auto-generated |

---

## `network/`

| Path | Owner | Purpose | Decision | Rationale |
|------|-------|---------|----------|-----------|
| `network/__init__.py` | Karen GV | Package marker | KEEP | Required for `from network import network_processing` in tests |
| `network/main_pipeline.py` | Karen GV | Core orchestration: load network → add miRNAs → filter by centrality → save `.cyjs` | KEEP | **Primary pipeline module**; imported by integration tests |
| `network/network_processing.py` | Karen GV | Graph construction, miRNA/tissue/organ/TF annotation, centrality filtering, JSON conversion | KEEP | **Core logic module**; most heavily imported file in repo |
| `network/node_evaluation.py` | Karen GV | Eigenvector centrality, shortest-path scoring, Pareto-front selection for miRNA nodes | KEEP | Imported by `main_pipeline.py` |
| `network/walking_network.py` | Karen GV | Influence propagation, DFS traversal, pathway/DE evaluation along network paths | KEEP | Contains core miRNA scoring logic; imported by `test_walking_network.py` |
| `network/jupyter_functions.py` | Karen GV | Helper functions developed in notebook context (path registration, influence traversal) | ARCHIVE | Partially overlaps with `walking_network.py`; not imported by core modules; review before migrating |
| `network/temp_network_processing.py` | Karen GV | Temporary/draft version of network processing | DROP | Filename indicates it's a scratch file; verify no unique logic before deletion |
| `network/settings/metadata.yml` | Karen GV | Metadata config (comparisons, analysis names) | KEEP | Referenced by `network_processing.py` for comparison labels |
| `network/test_integration.py` | Karen GV | Integration tests: end-to-end network load → format → graph creation | KEEP | Covers critical cross-module flow |
| `network/test_network.py` | Karen GV | Unit tests for network module public API | KEEP | Core test coverage |
| `network/test_network_processing.py` | Karen GV | Unit tests for `network_processing.py` functions | KEEP | Core test coverage |
| `network/test_node_evaluation.py` | Karen GV | Unit tests for `node_evaluation.py` | KEEP | Core test coverage |
| `network/test_walking_network.py` | Karen GV | Unit tests for `walking_network.py` | KEEP | Core test coverage |
| `network/test.cyjs` | Karen GV | Small Cytoscape JSON fixture | KEEP | Used as test fixture |
| `network/big_graph.pkl` (4.9 MB) | Karen GV | Serialised NetworkX graph (large) | EXTERNAL | Binary pickle; not version-controllable; 4.9 MB; move to artifact store |
| `network/small_graph.pkl` | Karen GV | Serialised NetworkX graph (small) | EXTERNAL | Binary pickle; move to artifact store or regenerate from fixture |
| `network/high_degree.pkl` (1 MB) | Karen GV | Serialised high-degree node list | EXTERNAL | Binary pickle; 1 MB; regenerable from pipeline run |
| `network/Young_to_old.cys` (1.1 MB) | Karen GV | Cytoscape session file (binary) | EXTERNAL | Binary Cytoscape session; not parseable by code; move to LFS |
| `network/hsa-miR-34a-5p.png` | Karen GV | Network visualisation PNG | DROP | Generated image artifact; not imported |
| `network/mirnas_influence_REPORT.html` (11 MB) | Karen GV | Generated HTML report | DROP | 11 MB generated output; not source; move to separate outputs repo or regenerate |
| `network/Styles/directed_tf.json` | Karen GV | Cytoscape visual style definition | ARCHIVE | May be needed for reproducing published figures; move to `configs/` |
| `network/Styles/styles.xml` | Karen GV | Cytoscape style XML | ARCHIVE | Same as above |
| `network/Styles/.Rhistory` | Karen GV | R session history | DROP | Stale IDE artifact |
| `network/*.ipynb` (all notebooks) | Karen GV | Exploratory analyses: Tissue-DE-Network series, mirnas_influence series, normalizeDDS, Pathways_in_nodes, etc. | DROP / ARCHIVE | Exploratory; large (up to 14 MB); not reproducible without data; archive separately |
| `network/.ipynb_checkpoints/` | auto | Jupyter checkpoints | DROP | Auto-generated; should be in `.gitignore` |
| `network/.virtual_documents/` | auto | Jupyter virtual documents | DROP | IDE artifact |

---

## `paper_mining/`

| Path | Owner | Purpose | Decision | Rationale |
|------|-------|---------|----------|-----------|
| `paper_mining/__init__.py` | Karen GV | Package marker | ARCHIVE | Only needed if `paper_mining` is kept |
| `paper_mining/paper_miner.py` | Karen GV | PubMed search and article retrieval via Entrez | ARCHIVE | Not part of core miRNA/network pipeline; useful for literature evidence augmentation; keep as optional module |
| `paper_mining/paper_info.py` | Karen GV | Data class for paper metadata | ARCHIVE | Supporting class for `paper_miner.py` |
| `paper_mining/paper_optimization.py` | Karen GV | `EvaluatePapers` class: ranks/filters papers by relevance metrics | ARCHIVE | Imported by `Tests/test_paper_miner.py` |
| `paper_mining/eutilities.py` | Karen GV | Local copy of NCBI eutils wrapper | ARCHIVE | Duplicates `ncbi/eutilities.py`; consolidate in migration |
| `paper_mining/common_tools.py` | Karen GV | Local copy of common utilities | ARCHIVE | Duplicates `common_tools/common_tools.py`; consolidate in migration |
| `paper_mining/requirements.txt` | Karen GV | Separate dependency list for paper_mining | ARCHIVE | Merge into top-level `requirements.txt` |
| `paper_mining/paper_miner_output.csv` | Karen GV | Sample CSV output from paper miner | DROP | Generated output artifact |
| `paper_mining/paper_mining.log` | Karen GV | Log file from a paper mining run | DROP | Runtime log; not source |
| `paper_mining/.idea/` | Karen GV | Nested PyCharm project config | DROP | IDE artifact |

---

## `Tests/`

| Path | Owner | Purpose | Decision | Rationale |
|------|-------|---------|----------|-----------|
| `Tests/__init__.py` | Karen GV | Package marker | KEEP | Required for test discovery |
| `Tests/test_common_tools.py` | Karen GV | Unit tests for `common_tools/common_tools.py` | KEEP | Core test coverage |
| `Tests/test_ncbi.py` | Karen GV | Unit tests for `ncbi/eutilities.py` | KEEP | Covers NCBI query utility |
| `Tests/test_paper_miner.py` | Karen GV | Unit tests for `paper_mining/paper_miner.py` | ARCHIVE | Keep only if `paper_mining` is migrated |
| `Tests/test.tsv` | Karen GV | TSV fixture file for tests | KEEP | Small fixture used by `test_common_tools.py` |

---

## Summary counts

| Decision | Count |
|----------|-------|
| KEEP | 46 |
| DROP | 28 |
| ARCHIVE | 20 |
| EXTERNAL | 27 |

> **KEEP** = copy to new `mirkat-studio/` repo verbatim  
> **DROP** = delete; do not migrate  
> **ARCHIVE** = move to `archive/` branch or separate archival repo  
> **EXTERNAL** = store in Git LFS, Zenodo, S3, or equivalent data registry; reference via URL/manifest in new repo
