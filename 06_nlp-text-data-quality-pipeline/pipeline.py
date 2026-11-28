reviews = [
    {"id": 1, "text": "VERY-GOOD product!!!"},
    {"id": 2, "text": "very_good product."},
    {"id": 3, "text": "I can't recommend it."},
    {"id": 4, "text": "The product isn't working."},
    {"id": 5, "text": "Fast-delivery; great service!"},
    {"id": 6, "text": "   "},
    {"id": 7, "text": None},
    {"id": 8, "text": "AMAZING-quality!!!"},
    {"id": 9, "text": "Amazing_quality."},
    {"id": 10, "text": "Poor customer-support???"},
    {"id": 11, "text": 12345},
    {"id": 12, "text": "Not_bad, but expensive."}
]


def validate_review(review):
    # Validate dictionary, id and text
    if isinstance(review, dict):
        if "id" in review and "text" in review:
            if isinstance(review["id"], int) and not isinstance(review["id"], bool) and review["id"] > 0:
                if isinstance(review["text"],str):
                    strip_row = review["text"].strip()
                    if strip_row != "":
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False


def normalize_text(text):
    # Normalize separators and case
    # Expand contractions
    # Remove punctuation
    # Normalize whitespace
    trans_table = str.maketrans({
        "!": None,
        "?": None,
        ".": None,
        ",": None,
        ";": None
    })
    clean_text = text.casefold()
    clean_text = clean_text.replace("-", " ").replace("_", " ").replace("can't","cannot").replace("isn't", "is not")
    clean_text = clean_text.translate(trans_table).strip()
    clean_text = clean_text.split()
    clean_text = " ".join(clean_text)
    return clean_text


def process_reviews(reviews):
    clean_reviews = []
    invalid_reviews = []
    duplicate_ids = []
    seen = set()
    total_records = 0

    # Validate each review
    for review in reviews:
    # Normalize valid text
        valid_text = validate_review(review)
        if valid_text:
            clean_text = normalize_text(review["text"])
            if clean_text not in seen:
                key_dict = {
                    "id": review["id"],
                    "text": clean_text
                }
                seen.add(clean_text)
                clean_reviews.append(key_dict)
            else:
                duplicate_ids.append(review["id"])
        else:
            invalid_reviews.append(review)
        total_records += 1
    # Build the final report
    final_report = {
        "clean_reviews": clean_reviews,
        "invalid_reviews": invalid_reviews,
        "duplicate_ids": duplicate_ids,
        "total_records": total_records,
        "total_clean": len(clean_reviews),
        "total_invalid": len(invalid_reviews),
        "total_duplicates": len(duplicate_ids)
    }
    return final_report


if __name__ == '__main__':
    report = process_reviews(reviews)
    print(report)
