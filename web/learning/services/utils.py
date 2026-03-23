def calculate_percentage(part: int, total: int) -> int:
    """
    Calculate percentage safely.

    Returns 0 if total is 0.
    """
    if not total:
        return 0

    return round((part / total) * 100)
