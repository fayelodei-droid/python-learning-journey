def summarize_data(*args, **kwargs):
    metric = kwargs.get("metric", "mean")
    round_digits = kwargs.get("round_digits", 2)

    if not args:
        return None

    # Added validation: keep unsupported metrics from silently returning zero.
    if metric not in ("sum", "mean"):
        raise ValueError("metric must be 'sum' or 'mean'")

    # Added validation: only finite real numbers are supported.
    from math import isfinite
    from numbers import Real

    if any(isinstance(value, bool) or not isinstance(value, Real) or not isfinite(value) for value in args):
        raise ValueError("all values must be finite real numbers")

    # Added validation for rounding precision.
    if isinstance(round_digits, bool) or not isinstance(round_digits, int):
        raise ValueError("round_digits must be an integer")

    result = 0

    if metric == "sum":
        result = sum(args)
    elif metric == "mean":
        result = sum(args) / len(args)

    return round(result, round_digits)
