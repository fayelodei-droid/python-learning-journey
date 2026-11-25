"""Validate, parse, and summarize HTTP API traffic logs.

A learning project for Python Core: string parsing and data quality.
"""

def validate_log(log):
    """Return True for a log with four valid fields."""
    http_methods = ["GET", "POST", "PUT", "DELETE", "PATCH"]
    clean_log = log.split()
    if len(clean_log) == 4:
        if clean_log[0] in http_methods:
            if clean_log[1].startswith("/api/"):
                if clean_log[2].isdigit() and clean_log[3].isdigit():
                    clean_log[2] = int(clean_log[2])
                    clean_log[3] = int(clean_log[3])
                    if 100 <= clean_log[2] <= 599 and clean_log[3] >= 0:
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


def parse_log(log):
    """Parse a previously validated log into typed fields."""
    log = log.split()
    log_dict = {
        "method": log[0],
        "endpoint": log[1],
        "status": int(log[2]),
        "response_time": int(log[3]),
    }
    return log_dict


def analyze_api_logs(logs):
    """Separate valid/invalid entries and calculate API quality metrics."""
    valid_logs = []
    invalid_logs = []
    server_errors = 0
    total_time = 0
    for log in logs:
        valid_log = validate_log(log)
        if not valid_log:
            invalid_logs.append(log)
            continue
        else:
            clean_dict = parse_log(log)
            valid_logs.append(clean_dict)
            total_time += int(clean_dict["response_time"])
            if 500 <= clean_dict["status"] <= 599:
                server_errors += 1

    if valid_logs:
        average_response_time = total_time / len(valid_logs)
    else:
        average_response_time = 0
    log_report = {
        "valid_logs": valid_logs,
        "invalid_logs": invalid_logs,
        "total_requests": len(valid_logs),
        "total_invalid": len(invalid_logs),
        "server_errors": server_errors,
        "average_response_time": average_response_time,
    }
    return log_report
