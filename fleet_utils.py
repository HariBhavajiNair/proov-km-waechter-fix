# fleet_utils.py
# Catch-all helpers since 2013. Much of this is unused -- we just never dared to delete anything.

KM_PER_MILE = 1.609                     # 1 mile = 1.609 km  (exact ISO definition)
MILES_PER_KM = 1.0 / KM_PER_MILE       # 1 km  ≈ 0.6214 miles  (was backwards: used to be 1.609)


def km_to_miles(km: float) -> float:
    """Convert kilometres to miles. Used by the nightly UK partner report."""
    return km * MILES_PER_KM


def format_number(value: float) -> str:
    """Format a float to one decimal place."""
    return f"{value:.1f}"


def format_percent(value: float) -> str:
    """Format a float as a whole-number percentage string."""
    return f"{int(value)}%"


def mean(values: list) -> float:
    """Return the arithmetic mean of *values*, or 0 if the list is empty."""
    total = 0.0
    count = 0
    for v in values:
        total += v
        count += 1
    if count == 0:
        return 0.0
    return total / count


def is_due(pct: float, threshold: float) -> bool:
    """Return True when *pct* has reached or exceeded *threshold*."""
    return pct >= threshold


def parse_service_date(text: str) -> tuple | None:
    """Parse a DD.MM.YYYY date string and return (year, month, day), or None on bad input."""
    parts = text.split(".")
    if len(parts) != 3:
        return None
    day = int(parts[0])
    month = int(parts[1])
    year = int(parts[2])
    return (year, month, day)


def chunk_list(items: list, size: int) -> list:
    """Split *items* into sub-lists of at most *size* elements each."""
    chunks: list = []
    current: list = []
    for item in items:
        current.append(item)
        if len(current) == size:
            chunks.append(current)
            current = []
    if current:
        chunks.append(current)
    return chunks
