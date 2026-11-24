"""Dependency-free assertion tests; run: python test_catalog_pipeline.py"""

import copy
from catalog_pipeline import PRODUCTS, normalize_name, process_catalog, validate_product


def test_validation():
    assert validate_product({"id": 1, "name": "Laptop"}) is True
    assert validate_product({"id": 6, "name": "   "}) is False
    assert validate_product({"id": 7, "name": None}) is False
    assert validate_product({"id": 8}) is False
    assert validate_product({}) is False
    assert validate_product("not a dictionary") is False
    assert validate_product({"name": "Laptop"}) is False


def test_normalization():
    assert normalize_name("  APPLE__IPHONE--16  ") == "apple iphone 16"
    assert normalize_name("Samsung-Galaxy-S24") == "samsung galaxy s24"
    assert normalize_name("  a   b  ") == "a b"


def test_pipeline():
    original_products = copy.deepcopy(PRODUCTS)
    report = process_catalog(PRODUCTS)

    # Six final project checks
    assert report["total_clean"] == 4
    assert report["total_invalid"] == 2
    assert report["total_duplicates"] == 3
    assert report["duplicate_ids"] == [2, 4, 9]
    assert report["clean_products"][0]["name"] == "apple iphone 16 pro"
    assert PRODUCTS == original_products

    # Structure, order and source records
    assert report["clean_products"] == [
        {"id": 1, "name": "apple iphone 16 pro"},
        {"id": 3, "name": "samsung galaxy s24"},
        {"id": 5, "name": "lenovo thinkpad x1"},
        {"id": 8, "name": "dyson vacuum cleaner"},
    ]
    assert report["invalid_products"] == [
        {"id": 6, "name": "   "},
        {"id": 7, "name": None},
    ]
    assert process_catalog([]) == {
        "clean_products": [], "invalid_products": [], "duplicate_ids": [],
        "total_clean": 0, "total_invalid": 0, "total_duplicates": 0,
    }


if __name__ == "__main__":
    test_validation()
    test_normalization()
    test_pipeline()
    print("All tests passed: validation, normalization, pipeline, and input immutability.")
