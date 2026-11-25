# NLP Text Data Quality Pipeline

A beginner-friendly Python pipeline for validating, cleaning, and deduplicating customer reviews before basic NLP / sentiment-analysis workflows.

## Features
- Validates review records (`id` must be a positive integer, not `bool`; `text` must be a non-empty string).
- Normalizes case with Unicode-aware `casefold()`.
- Replaces hyphens and underscores with spaces.
- Expands `can't` and `isn't` while preserving negation.
- Removes selected punctuation and normalizes whitespace.
- Deduplicates by normalized text, retaining the first occurrence.
- Produces a data-quality summary and does not mutate source data.

## Project structure
```text
nlp_text_data_quality_pipeline/
├── pipeline.py       # Original learner implementation
├── test_pipeline.py  # Automated unittest suite (21 tests)
└── README.md
```

## Run
```bash
python pipeline.py
python -m unittest -v test_pipeline.py
```

## Example quality report
| Metric | Count |
|---|---:|
| Input records | 12 |
| Unique clean reviews | 7 |
| Invalid records | 3 |
| Duplicate records | 2 |

Duplicate IDs: `2`, `9`. Invalid record IDs: `6`, `7`, `11`.

## Scope and limitations
This pipeline deliberately uses basic Python string methods and no third-party NLP dependencies. It removes only five punctuation characters (`! ? . , ;`) and expands only two English contractions (`can't`, `isn't`). It is a learning project, not a language-independent production tokenizer. Further improvements may include tests for semantic edge cases, configurable normalization, logging, and a CLI/API.
