"""Normalize and deduplicate a small product catalog (Python Core lesson 4)."""

PRODUCTS = [
    {"id": 1, "name": "  APPLE_IPHONE_16_PRO  "},
    {"id": 2, "name": "apple  iphone  16  pro"},
    {"id": 3, "name": "Samsung-Galaxy-S24"},
    {"id": 4, "name": " samsung galaxy s24 "},
    {"id": 5, "name": "LENOVO__THINKPAD_X1"},
    {"id": 6, "name": "   "},
    {"id": 7, "name": None},
    {"id": 8, "name": "Dyson---Vacuum-Cleaner"},
    {"id": 9, "name": "Lenovo ThinkPad X1"},
]


def validate_product(product):
    """Check required keys and a non-blank string name."""
    if not isinstance(product, dict):
        return False
    if product:
        if "name" not in product or "id" not in product:
            return False
        if isinstance(product["name"], str):
            prd_name = product["name"].strip()
        else:
            return False
        if prd_name == "":
            return False
    else:
        return False
    return True


def normalize_name(name):
    """Normalize separators, whitespace and case of a product name."""
    clean_name = name.strip().replace("-", " ").replace("_", " ").casefold()
    clean_name = clean_name.split()
    clean_name = " ".join(clean_name)
    return clean_name


def process_catalog(products):
    """Return unique cleaned records, rejected records and quality counts."""
    clean_products = []
    invalid_products = []
    duplicate_ids = []
    seen_names = []

    for product in products:
        valid_name = validate_product(product)
        if valid_name:
            clean_name = normalize_name(product["name"])
        else:
            invalid_products.append(product)
            continue

        seen_products = {"id": product["id"], "name": clean_name}
        if clean_name not in seen_names:
            clean_products.append(seen_products)
            seen_names.append(clean_name)
        else:
            duplicate_ids.append(product["id"])
            continue

    summary_dict = {
        "clean_products": clean_products,
        "invalid_products": invalid_products,
        "duplicate_ids": duplicate_ids,
        "total_clean": len(clean_products),
        "total_invalid": len(invalid_products),
        "total_duplicates": len(duplicate_ids),
    }
    return summary_dict


if __name__ == "__main__":
    from pprint import pprint
    pprint(process_catalog(PRODUCTS))
