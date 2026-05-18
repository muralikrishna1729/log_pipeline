# test_parser.py
from src.pipeline.readers import read_lines
from src.pipeline.filters import filter_errors
from src.pipeline.parsers import parse_timestamps

LOGFILE = "data/Linux_2k.log"

def build_pipeline():
    lines   = read_lines(LOGFILE)
    errors  = filter_errors(lines)
    records = parse_timestamps(errors)
    return records

# --- Test 1: inspect parsed dicts ---
print("=== Test 1: First 3 parsed records ===")
for i, record in enumerate(build_pipeline()):
    print(f"\nRecord {i}:")
    for key, val in record.items():
        print(f"  {key:12}: {val}")
    if i == 2:
        break

# --- Test 2: count successfully parsed records ---
print("\n=== Test 2: Parse success rate ===")
from src.pipeline.filters import filter_errors as fe
total_filtered = sum(1 for _ in filter_errors(read_lines(LOGFILE)))
total_parsed   = sum(1 for _ in build_pipeline())
print(f"Filtered lines : {total_filtered}")
print(f"Parsed records : {total_parsed}")
print(f"Parse failures : {total_filtered - total_parsed}")

# --- Test 3: level distribution ---
print("\n=== Test 3: Level distribution ===")
from collections import Counter
levels = Counter(r["level"] for r in build_pipeline())
for level, count in levels.most_common():
    print(f"  {level:10}: {count}")

# --- Test 4: unique processes seen ---
print("\n=== Test 4: Unique processes ===")
processes = set(r["process"] for r in build_pipeline())
for p in sorted(processes):
    print(f"  {p}")

# --- Test 5: timestamp sanity check ---
print("\n=== Test 5: Date range in file ===")
timestamps = [r["timestamp"] for r in build_pipeline()]
print(f"  Earliest : {min(timestamps)}")
print(f"  Latest   : {max(timestamps)}")
print(f"  Span     : {max(timestamps) - min(timestamps)}")