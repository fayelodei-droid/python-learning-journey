# DST-Aware Event Data Pipeline

A beginner-friendly Python data-processing project that validates event records, converts ISO 8601 timestamps to the **Europe/Kyiv** timezone, derives time-based features, and returns a summary of valid/invalid events. Built as a Python Core learning project.

## Features

- Validates required fields (`id`, `timestamp`, `value`) and data types, rejecting booleans in numeric fields.
- Rejects invalid, missing, or timezone-naive timestamps.
- Extracts local hour, weekday, weekend indicator and DST `fold` from valid records.
- Separates valid and invalid records; computes counts and the average `value` of valid records.
- Handles empty input and does not mutate source records.
- Includes standard-library unit tests; the GitHub Actions workflow is at the repository root.

## Project structure

```text
python-core/dst-event-pipeline/
├── main.py                  # Original functions and sample data (minimal refactoring)
├── tests/
│   └── test_pipeline.py     # Automated tests (unittest)
├── .gitignore
└── README.md
```

## Requirements

- Python 3.9+ (recommended: Python 3.12)
- IANA timezone data available to `zoneinfo` (built into most macOS/Linux systems)
- No third-party Python packages required for typical macOS/Linux installations.

On Windows, if your system has no IANA timezone database, run `python -m pip install tzdata`.

## Run

From `python-core/dst-event-pipeline/`:

```bash
python main.py
```

## Run tests

```bash
python -m unittest discover -s tests -v
```

## Example output

For the five sample events in `main.py`:

| Metric | Result |
| --- | ---: |
| Valid events | 3 |
| Invalid events | 2 |
| Average value of valid events | 156.6667 (approx.) |

Valid IDs: `1, 3, 5`; invalid IDs: `2, 4`.

Time features of valid events:

| ID | local_hour | weekday | is_weekend | fold |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 15 | 2 | 0 | 0 |
| 3 | 3 | 6 | 1 | 1 |
| 5 | 9 | 0 | 0 | 0 |

`fold=1` represents the second occurrence of a repeated local clock time during the autumn DST transition.

## Functions

- `validate_event(event)`: Returns `True` for an accepted event and `False` otherwise.
- `extract_features(event)`: Returns features for an **already validated** event.
- `process_events(events)`: Validates each record, extracts features, and returns a summary dictionary.

## Notes / scope

This is an educational portfolio project, not a production deployment. The supplied timestamps use explicit UTC offsets. The `value` field is an integer or float; timestamps must include a timezone offset. The code follows the original course solution, with only minimal adjustments to remove repeated validation, correctly handle missing keys, and safely import it for testing.

## Suggested future improvements

- Read events from JSON/CSV.
- Add type hints and structured logging.
- Add further timezone cases and input-schema tests.
- Use pytest and a larger realistic dataset.

## Location in learning journey

This project is part of the `python-learning-journey` repository at `python-core/dst-event-pipeline/`. The dedicated CI workflow lives at `.github/workflows/dst-event-pipeline-tests.yml` in the repository root.
