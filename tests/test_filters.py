from src.pipeline.filters import ERROR_KEYWORDS, filter_errors
from src.pipeline.readers import read_lines

LOGFILE = "data/Linux_2k.log"

# --- Test 1: see what gets through ---
print("=== Test 1: First 5 filtered lines ===")
lines   = read_lines(LOGFILE)
errors  = filter_errors(lines)

for i, line in enumerate(errors):
    print(f"[{i}] {line}")
    if i == 4:
        break

print("\n=== Test 3: Hits per keyword ===")
lines   = read_lines(LOGFILE)
for kw in ERROR_KEYWORDS:
    count = sum(1 for line in filter_errors(lines) if kw in line.lower())
    print(f"{kw}: {count} hits")