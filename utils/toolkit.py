# Format bytes to human-readable format
def format_bytes(value):
    """Convert bytes to a human-readable format."""
    if value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.2f} GB"
    else:
        return f"{value / 1_000_000:.2f} MB"