import csv
import json
from math import isfinite  # Added: reject non-finite numeric values


total_revenue = 0
average_revenue = 0
valid_row = 0
product_names = set()

with open("sales.csv", "r", encoding="utf-8", newline="") as file:
    reader = csv.DictReader(file)
    # Added: provide a clear error when expected columns are absent.
    required_columns = {"product", "price", "quantity"}
    if not required_columns.issubset(reader.fieldnames or []):
        raise ValueError("CSV must include product, price, and quantity columns")
    for row in reader:
        try:
            price = float(row['price'])
            quantity = int(row['quantity'])
            # Added: avoid counting non-finite values or unnamed products.
            if not isfinite(price) or not row['product'] or not row['product'].strip():
                continue
            if price <= 0 or quantity <= 0:
                continue
            revenue = price * quantity
            valid_row += 1
            total_revenue += revenue
            product_names.add(row['product'])
        except (ValueError, TypeError, ZeroDivisionError):
            continue

if valid_row > 0:
    average_revenue = total_revenue / valid_row

count_unique = len(product_names)

sales = {
    "total_revenue": total_revenue,
    "average_revenue": average_revenue,
    "unique_products": count_unique
}

with open("sales_report.json", "w", encoding="utf-8") as file:
    json.dump(sales, file, indent=4, ensure_ascii=False)
