# BioMed-Enriched

Populate paragraph text into BioMed-Enriched Non-Commercial split.

## Install
```bash
pip install biomed-enriched
```
Requires **Python ≥ 3.10**.  No extra setup needed for end-users.

## Quick start (Python)
```python
from biomed_enriched import populate

DATASET_DIR = "/path/to/biomed-enriched"  # input dataset
PMC_XML_ROOT = "/path/to/pmc/xml"          # PMC XML dump
OUTPUT_DIR = "/path/to/populated-biomed-enriched"  # drop arg to overwrite in-place

populate(DATASET_DIR, PMC_XML_ROOT, output_path=OUTPUT_DIR, splits="non-comm", num_proc=1)
```
The call overwrites the dataset in-place, adding a new `text` column as the third column (after `article_id`, `path`).

## Quick start (CLI)
```bash
biomed-enriched \
  --input pubmed_sample \
  --xml-root /path/to/pmc/xml/root \
  --num-proc 8
```
Add `--output DIR` if you prefer writing to a new directory instead of overwriting.