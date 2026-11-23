# Data Summary Function

A beginner-friendly Python mini-project that calculates a summary metric for a variable number of numeric inputs.

## What it does

- Accepts a variable number of positional arguments with `*args`.
- Supports `mean` (default) and `sum` metrics selected via `**kwargs`.
- Rounds results to two decimal places by default, or to a specified number of decimal places.
- Returns `None` when no values are provided.
- Raises `ValueError` for unsupported metric names, non-finite/non-numeric values, and invalid rounding precision.

## Run locally

Requires Python 3 and no third-party packages.

```bash
python3
```

Then in the Python REPL:

```python
from summarize_data import summarize_data

print(summarize_data(10, 20, 30))
print(summarize_data(10, 20, 30, metric="sum"))
print(summarize_data(10, 20, 30, round_digits=1))
print(summarize_data())
```

Run these commands from the `01_data_summary_function` directory.

## Python concepts

Functions, `*args`, `**kwargs`, default values, conditional logic, built-in aggregation, and rounding.

## Run tests

From the `01_data_summary_function` directory:

```bash
python3 -m unittest -v
```

## Limitations / future improvements

- The function supports only `mean` and `sum`.
- Boolean and non-finite values are rejected.
- More summary metrics and broader numeric types could be added later.

## Learning note

The original learning implementation is preserved line-for-line. Validation checks and unit tests were added without removing or changing the original statements.
