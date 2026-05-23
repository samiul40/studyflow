from django import template

register = template.Library()


@register.filter
def format_duration(minutes):
    """Convert a total-minutes integer to a human-readable string.

    Examples: 0 → "0m", 45 → "45m", 90 → "1h 30m", 120 → "2h"
    """
    if not minutes:
        return "0m"
    hours, mins = divmod(int(minutes), 60)
    if hours and mins:
        return f"{hours}h {mins}m"
    if hours:
        return f"{hours}h"
    return f"{mins}m"
