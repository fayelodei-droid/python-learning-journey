from datetime import datetime
from zoneinfo import ZoneInfo


events = [
    {"id": 1, "timestamp": "2026-07-15T12:00:00+00:00", "value": 120},
    {"id": 2, "timestamp": "invalid-date", "value": 75},
    {"id": 3, "timestamp": "2026-10-25T01:30:00+00:00", "value": 200},
    {"id": 4, "timestamp": None, "value": 90},
    {"id": 5, "timestamp": "2026-11-16T07:00:00+00:00", "value": 150}
]


def validate_event(event):
    # 1. Check dictionary and required keys
    key_list = ["id", "timestamp", "value"]
    if not isinstance(event, dict):
        return False
    for key in key_list:
        if key not in event:
            return False

    # 2. Validate id and value types
    if isinstance(event["id"], bool) or isinstance(event["value"], bool):
        return False
    event_id = isinstance(event["id"], int)
    value = isinstance(event["value"], (int, float))
    if event_id is False or value is False:
        return False

    try:
        timestamp = datetime.fromisoformat(event["timestamp"])
        utc_offset = timestamp.utcoffset()
        if utc_offset is None:
            return False
    except (ValueError, TypeError, OverflowError, OSError):
        return False

    return True


def extract_features(event):
    # 1. Parse ISO timestamp
    parsed = datetime.fromisoformat(event["timestamp"])
    # 2. Convert to Europe/Kyiv
    kyiv_time = parsed.astimezone(ZoneInfo("Europe/Kyiv"))
    # 3. Extract hour, weekday, fold
    hour = kyiv_time.hour
    weekday = kyiv_time.weekday()
    fold = kyiv_time.fold
    # 4. Determine is_weekend
    is_weekend = 0
    if weekday == 5 or weekday == 6:
        is_weekend = 1
    feature_dict = {
        "id": event["id"],
        "value": event["value"],
        "local_hour": hour,
        "weekday": weekday,
        "is_weekend": is_weekend,
        "fold": fold
    }
    # 5. Return feature dictionary
    return feature_dict


def process_events(events):
    clean_events = []
    invalid_events = []
    total_value = 0

    # 1. Loop through events
    for event in events:
        # 2. Validate each event
        is_validate = validate_event(event)
        # 3. Extract features for valid events
        if is_validate is True:
            result = extract_features(event)
            clean_events.append(result)
            total_value += event["value"]
        # 4. Collect invalid events
        else:
            invalid_events.append(event)
    # 5. Calculate average_value safely
    if clean_events:
        average_value = total_value / len(clean_events)
    else:
        average_value = 0.0
    # 6. Return summary report
    summary_report = {
        "clean_events": clean_events,
        "invalid_events": invalid_events,
        "total_clean": len(clean_events),
        "total_invalid": len(invalid_events),
        "average_value": average_value
    }
    return summary_report


if __name__ == "__main__":
    report = process_events(events)
    print(report)
