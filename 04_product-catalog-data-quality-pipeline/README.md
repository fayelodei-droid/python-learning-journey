# Product Catalog Data Quality Pipeline

## Problem

Product names are often inconsistently formatted (`APPLE_IPHONE_16_PRO` vs. `apple  iphone  16  pro`). Without normalization, equivalent products may be counted separately. Blank or missing names also require validation.

## Pipeline

1. `validate_product(product)` checks that a record is a dict with `id` and a nonblank string `name`.
2. `normalize_name(name)` uses `strip`, `replace`, `casefold`, `split`, and `join` to standardize names.
3. `process_catalog(products)` keeps the **first** record for each normalized name, collects invalid records and duplicate IDs, and returns summary counts.

Input records are not mutated. Order of first appearance is retained.

## Project structure

```text
product-catalog-data-quality-pipeline/
├── catalog_pipeline.py
├── test_catalog_pipeline.py
├── README.md
└── .gitignore
```

## Run

Requires **Python 3.9+**; no third-party packages.

```bash
python3 catalog_pipeline.py
python3 test_catalog_pipeline.py
```

## Expected outcome (example data)

| Metric | Result |
| --- | ---: |
| Unique products | 4 |
| Invalid records | 2 |
| Duplicate records | 3 |

- Kept product IDs: `1, 3, 5, 8`
- Invalid product IDs: `6, 7`
- Duplicate IDs: `2, 4, 9`

## Tests

The test script uses built-in `assert` statements and covers valid/invalid entries, edge cases, normalization, totals, duplicate IDs, product ordering, exact result structure and input immutability (using `copy.deepcopy`).

## Current scope / possible improvements

- Designed for in-memory lists of dicts, not very large datasets. Duplicate lookup in `seen_names` is linear; future versions could use a `set`.
- Normalization treats hyphens and underscores as separators; this is a domain choice, not universally correct for product names.
- `id` is required to be present, but its type/uniqueness is not validated.
- A production pipeline should define a stronger schema, configurable text rules, logging and file ingestion.

## Skills practiced

Python functions, string methods, dictionaries, loops, type checks, `continue`, deduplication, reproducible tests, data quality reporting.
