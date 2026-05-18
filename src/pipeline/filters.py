
ERROR_KEYWORDS = (
    "authentication failure",
    "check pass; user unknown",
    "alert",
    "error",
)
def filter_errors(lines):
    """Filters lines that contain any of the specified error keywords."""
    for line in lines:
        line_lower = line.lower()
        if any(keyword in line_lower for keyword in ERROR_KEYWORDS):
            yield line
