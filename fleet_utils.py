# fleet_utils.py
# Helpers for Vossberg Mobility's KM-Waechter service.

KM_PER_MILE = 1.609344          # ISO 31-1: 1 international mile = 1.609344 km (exact)
MILES_PER_KM = 1.0 / KM_PER_MILE   # ≈ 0.62137 miles per km


def km_to_miles(km: float) -> float:
    """Convert kilometres to miles. Used by the nightly UK partner report."""
    return km * MILES_PER_KM


def format_number(value: float) -> str:
    """Format a float to one decimal place."""
    return f"{value:.1f}"


def format_percent(value: float) -> str:
    """Format a float as a whole-number percentage string."""
    return f"{int(value)}%"
