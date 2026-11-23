# Sales Data Pipeline

A Python coursework mini-project for reading sales records, filtering invalid values, calculating business metrics, and saving a JSON report.

**Status:** Documentation scaffold. The original Python implementation and `sales.csv` input file still need to be added; this folder does not claim to contain a working pipeline yet.

## Intended workflow

1. Read `sales.csv` using `csv.DictReader`.
2. Exclude records with non-positive prices or quantities.
3. Calculate total revenue from accepted rows.
4. Calculate average revenue per valid row (not necessarily average order value).
5. Count unique product names using a set.
6. Write the report to `sales_report.json`.

## Planned files

```text
02_sales_data_pipeline/
├── README.md
├── sales_pipeline.py       # Add original solution
└── sales.csv               # Add original coursework data
```

The generated `sales_report.json` can be included after running and reviewing the original script.

## Python concepts

CSV reading, dictionaries, loops, numeric validation, sets, aggregation, and JSON export.

## Questions to explore during improvement

- What happens when a price or quantity is missing or cannot be converted to a number?
- How should the program handle a CSV file containing only invalid rows?
- Are product names that differ only by spaces or capitalization counted as different products?
- Should the report include the count of rejected rows?

## Learning note

This documentation is based on the completed coursework exercise. It will be updated once my original code is added and reviewed.
