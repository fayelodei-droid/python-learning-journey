# API Traffic Quality Monitoring Pipeline

A beginner-friendly Python project that validates HTTP API logs, converts valid records into structured data, and calculates traffic-quality metrics. Built as part of **Python Core — String Methods** practice, with an emphasis on real-world data-quality problems for Data Science and Software Engineering.

## What it does

- Validates HTTP method, endpoint prefix, status code, and non-negative response time.
- Separates valid and invalid records while preserving the original invalid text and input order.
- Converts valid records to dictionaries with integer status codes and response times.
- Calculates total valid requests, total invalid records, number of HTTP 5xx errors, and mean response time in milliseconds.
- Handles empty input without dividing by zero.
- Does not modify the input list.

## Project structure

```text
api-traffic-quality-monitoring/
├── api_monitor.py          # Three core functions
├── main.py                 # Run the sample report
├── data/
│   └── api_logs.txt        # Sample input (12 records)
├── tests/
│   └── test_api_monitor.py # Automated unit tests
├── README.md
└── .gitignore
```

## Requirements

Python 3.9+; **no third-party dependencies**.

## Quick start

Run from the project directory:

```bash
python3 main.py
```

Run the tests:

```bash
python3 -m unittest discover -s tests -v
```

## Sample output

For the included 12 log lines:

| Metric | Value |
|---|---:|
| Valid requests | 7 |
| Invalid records | 5 |
| Server errors (HTTP 500–599) | 2 |
| Average response time | 451.43 ms |

The average is computed only from valid entries: `3160 / 7 = 451.428571... ms`.

## Log format and validation rules

Each line contains exactly four whitespace-separated fields:

```text
METHOD ENDPOINT STATUS RESPONSE_TIME
GET /api/users 200 120
```

- Methods: `GET`, `POST`, `PUT`, `PATCH`, `DELETE`.
- Endpoint must begin with `/api/`.
- HTTP status: integer from 100 through 599, inclusive.
- Response time: non-negative integer (milliseconds).
- Invalid records are preserved as their original strings.

## Design

The pipeline separates three responsibilities:

1. `validate_log(log)` returns a boolean indicating whether the record meets the specification.
2. `parse_log(log)` transforms an already-validated record into a typed dictionary.
3. `analyze_api_logs(logs)` orchestrates validation, parsing, and metric calculation.

**Scope:** This is a learning project, not a full HTTP log parser. It assumes simple whitespace-delimited logs, a fixed API prefix, and integer millisecond response times. It intentionally uses Python's standard library and basic control flow.

## Tests

The standard-library `unittest` suite tests valid/invalid records, boundary status codes (100 and 599), zero response time, negative values, allowed methods, typed parsing, expected metrics, ordering, empty input, and immutability.

## Possible next steps

Add CSV/JSON exports, structured logging, and integration into a reproducible data preprocessing pipeline.
