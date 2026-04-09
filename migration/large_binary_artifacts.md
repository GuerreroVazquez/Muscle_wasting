# Large & Binary Artifacts — External Storage Manifest

> Generated: 2026-04-09  
> Threshold for "large": > 500 KB  
> Binary types flagged regardless of size: `.pkl`, `.cys`, `.fa`, `.fa.gz`, `.ods`, `.xlsx`, `.png`, `.html` (generated), `.ipynb` (with outputs)

All items in this table should be **removed from the Git repository** and stored externally.  
Recommended storage options are listed per item.

---

## Recommended external storage options

| Option | Best for | Notes |
|--------|----------|-------|
| **Git LFS** | Files that must stay co-located with the repo; ≤ 2 GB | Transparent to `git clone`; requires LFS support on host |
| **Zenodo / Figshare** | Published datasets; immutable reference data | Assigns DOI; good for paper reproducibility |
| **AWS S3 / GCS bucket** | Large operational data; frequently updated | Use presigned URLs or a download script |
| **DVC (Data Version Control)** | Data tied to specific code commits | Works with S3, GCS, Azure, SSH; integrates with Git |
| **Separate `data-artifacts` GitHub repo** | Binary outputs tied to analysis runs | Can be a submodule or referenced by SHA |

---

## File manifest

### Binary pickle / serialised graphs

| File | Size | Type | Recommended storage | Notes |
|------|------|------|---------------------|-------|
| `network/big_graph.pkl` | 4.9 MB | Python pickle (NetworkX DiGraph) | DVC or S3 | Regenerable by running `main_pipeline.py`; include in baseline run manifest |
| `network/small_graph.pkl` | ~50 KB | Python pickle (NetworkX graph) | DVC or S3 | Smaller but same reasoning; regenerable |
| `network/high_degree.pkl` | 1.0 MB | Python pickle (node list) | DVC or S3 | Regenerable from `big_graph.pkl` + `network_processing.py` |

**Action:** Add to `.gitignore`:
```
network/*.pkl
```
Provide a regeneration script in `scripts/regenerate_graphs.py`.

---

### Cytoscape session / style files

| File | Size | Type | Recommended storage | Notes |
|------|------|------|---------------------|-------|
| `network/Young_to_old.cys` | 1.1 MB | Binary Cytoscape session | Git LFS | Cannot be diffed; contains embedded graphs + styles |
| `cytoscape/Diff_express_genes.cyjs` | 16 MB | Cytoscape JSON (large) | Git LFS or S3 | Largest `.cyjs` in repo; used as example but not in tests |

---

### miRBase database dumps

| File | Size | Type | Recommended storage | Notes |
|------|------|------|---------------------|-------|
| `Databases/miRBase/miRNA.dat` | 44 MB | miRBase flat-file annotation | Zenodo + Git LFS | Largest file in repo; version: miRBase r22.1 (verify); immutable reference |
| `Databases/miRBase/mirna.txt` | 6.9 MB | miRBase tabular dump | Zenodo + Git LFS | DB export; immutable |
| `Databases/miRBase/mirna_mature.txt` | 3.2 MB | miRBase mature miRNA table | Zenodo + Git LFS | DB export |
| `Databases/miRBase/mature.fa` | 3.7 MB | miRBase mature sequences (FASTA) | Zenodo + Git LFS | Standard reference file |
| `Databases/miRBase/mature.fa.gz` | 788 KB | Compressed FASTA | Zenodo + Git LFS | Duplicate of `mature.fa`; consider deduplicate and store only one form |
| `Databases/miRBase/confidence.txt` | 1.6 MB | miRBase confidence scores | Zenodo + Git LFS | |
| `Databases/miRBase/mirna_context.txt` | 1.3 MB | Context annotations | Zenodo + Git LFS | |
| `Databases/miRBase/mirna_context (1).txt` | 1.3 MB | Duplicate context file | **DROP** | Exact duplicate with space in filename; delete before migration |
| `Databases/miRBase/mirna_chromosome_build.txt` | 1.2 MB | Chromosome build mapping | Zenodo + Git LFS | |
| `Databases/miRBase/mirna_pre_mature.txt` | 976 KB | Pre-miRNA to mature mapping | Zenodo + Git LFS | |
| `Databases/miRBase/mature_database_links.txt` | 992 KB | DB cross-reference links | Zenodo + Git LFS | |
| `Databases/miRBase/mirna_database_links.txt` | 436 KB | DB cross-reference links | Zenodo + Git LFS | |
| `Databases/miRBase/mirna_literature_references.txt` | 688 KB | Literature reference dump | Zenodo + Git LFS | |

---

### External expression databases

| File | Size | Type | Recommended storage | Notes |
|------|------|------|---------------------|-------|
| `Databases/diana_miTed/miTED-Log2RPM.tsv` | 21 MB | DIANA miTED tissue expression | Zenodo + DVC | Largest TSV; required at runtime by `network_processing.py`; must be accessible |
| `Databases/HMDD/target.txt` | 2.1 MB | HMDD miRNA–disease targets | Zenodo + DVC | Reference DB dump |
| `Databases/HMDD/tissue_expression.txt` | 1.9 MB | HMDD tissue expression | Zenodo + DVC | Reference DB dump |
| `Databases/miRNATissueAtlas2/miRNATissueAtlas2.txt` | — | miRNA Tissue Atlas v2 | Zenodo + DVC | Large; external reference |
| `Databases/targetscan/seeds.txt` | 312 KB | TargetScan seed sequences | Zenodo + DVC | Reference data |
| `Databases/dunhill/dunhill abundances.xlsx` | 612 KB | Binary Excel abundances | Zenodo + DVC | Binary; convert to TSV/CSV for version control friendliness |
| `Databases/dunhill/dunhillAbundances.txt` | — | Text version of Dunhill data | DVC | Operational input data |

---

### Exploratory notebook outputs

The following notebooks contain embedded output cells (images, DataFrames, HTML) that inflate file sizes significantly. Strip outputs before committing or exclude entirely.

| File | Size | Decision | Notes |
|------|------|----------|-------|
| `network/mirnas_influence_more_mirnas.ipynb` | 1.8 MB | DROP / ARCHIVE | Exploratory; 1.8 MB with embedded outputs |
| `network/mirnas_influence_04.ipynb` | 10 MB | DROP / ARCHIVE | 10 MB; strip outputs or archive in `data-artifacts` repo |
| `network/.ipynb_checkpoints/mirnas_influence_more_mirnas-checkpoint.ipynb` | 14 MB | DROP | Auto-generated checkpoint; 14 MB |
| `network/.ipynb_checkpoints/mirnas_influence_04-checkpoint.ipynb` | 10 MB | DROP | Checkpoint; 10 MB |
| `network/.ipynb_checkpoints/mirnas_influence_REPORT-checkpoint.ipynb` | 9.8 MB | DROP | Checkpoint |
| `network/mirnas_influence_tissue.ipynb` | 1.6 MB | DROP / ARCHIVE | Exploratory |
| `network/Pathways_in_nodes.ipynb` | 548 KB | DROP / ARCHIVE | Exploratory |
| `network/mirnas_influence_03_90.ipynb` | 488 KB | DROP / ARCHIVE | Exploratory |

---

### Generated HTML reports

| File | Size | Decision | Notes |
|------|------|----------|-------|
| `network/mirnas_influence_REPORT.html` | 11 MB | DROP | Generated from notebook; store in separate results/outputs repo |
| `network/.ipynb_checkpoints/mirnas_influence_REPORT-checkpoint.html` | 11 MB | DROP | Checkpoint copy of above |

---

### Binary spreadsheets / documents

| File | Size | Decision | Notes |
|------|------|----------|-------|
| `DE_genes.ods` | 28 KB | ARCHIVE | ODS spreadsheet; not version-diff-friendly; convert to CSV or move to `data/` |
| `Databases/sources.ods` | — | ARCHIVE | Documentation spreadsheet; move to `docs/` as Markdown or PDF |

---

### Images

| File | Size | Decision | Notes |
|------|------|----------|-------|
| `cytoscape/graph1_Analysis_Sarcopenia.cyjs.png` | — | DROP | Generated figure; not imported |
| `network/hsa-miR-34a-5p.png` | — | DROP | Generated figure; not imported |

---

### SQL data dumps

| File | Size | Decision | Notes |
|------|------|----------|-------|
| `database_analysis/update_genes.sql` | 3.8 MB | EXTERNAL | Large SQL data dump; belongs in DB migration tooling (e.g., Flyway/Alembic scripts), not runtime repo |

---

## `.gitignore` additions recommended for new repo

```gitignore
# Binary artifacts
*.pkl
*.cys
*.pyc
__pycache__/

# Jupyter
.ipynb_checkpoints/
.virtual_documents/

# IDE
.idea/
*.iml

# Logs and outputs
*.log
*.html   # if generated reports

# Large data (handled via DVC or LFS)
Databases/
data/*.csv
data/*.tsv
```

---

## Git LFS setup (if using LFS)

```bash
# Install LFS
git lfs install

# Track large file types
git lfs track "*.pkl"
git lfs track "*.cys"
git lfs track "*.fa"
git lfs track "*.fa.gz"
git lfs track "*.dat"
git lfs track "Databases/**"

git add .gitattributes
git commit -m "chore: configure Git LFS for large data files"
```

---

## DVC setup (if using DVC for data versioning)

```bash
pip install dvc dvc-s3  # or dvc-gs / dvc-azure

dvc init
dvc remote add -d myremote s3://my-bucket/mirkat-data

# Track large files
dvc add Databases/diana_miTed/miTED-Log2RPM.tsv
dvc add Databases/HMDD/
dvc add network/big_graph.pkl
dvc add network/small_graph.pkl
dvc add network/high_degree.pkl

git add *.dvc .dvcignore
git commit -m "chore: add DVC tracking for large data files"
dvc push
```

---

## Total size summary

| Category | Approx. total size | Recommended storage |
|----------|--------------------|---------------------|
| miRBase dumps | ~70 MB | Zenodo + Git LFS |
| DIANA miTED | 21 MB | DVC / S3 |
| HMDD | ~4 MB | DVC / S3 |
| Notebook outputs | ~50 MB | DROP (regenerate) |
| Pickle graphs | ~6 MB | DVC / S3 |
| Cytoscape files | ~18 MB | Git LFS |
| SQL dumps | ~4 MB | DB migration tooling |
| **Total to externalise** | **~173 MB** | |

Removing these artifacts would bring the working tree from **~210 MB** down to approximately **~37 MB** (primarily source code, small fixtures, and config).
