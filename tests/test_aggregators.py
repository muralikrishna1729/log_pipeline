# test_aggregator.py
import json
import tracemalloc
from src.pipeline.readers      import read_lines
from src.pipeline.filters      import filter_errors
from src.pipeline.parsers      import parse_timestamps
from src.pipeline.aggregators  import group_by_hour, write_summary

LOGFILE = "data/Linux_2k.log"
OUTPUT  = "output/summary.json"

def build_pipeline():
    return parse_timestamps(
               filter_errors(
                   read_lines(LOGFILE)
               )
           )

# --- Test 1: run the full pipeline ---
print("=== Test 1: Full pipeline run ===")
summary = group_by_hour(build_pipeline())
print(f"Unique hours in summary : {len(summary)}")

# --- Test 2: inspect a few buckets ---
print("\n=== Test 2: Sample hourly buckets ===")
for i, (hour, counts) in enumerate(summary.items()):
    print(f"  {hour}  →  {counts}")
    if i == 4:
        print("  ...")
        break

# --- Test 3: find the busiest hour ---
print("\n=== Test 3: Busiest hour ===")
busiest = max(summary.items(), key=lambda x: x[1]["total"])
print(f"  Hour    : {busiest[0]}")
print(f"  Counts  : {busiest[1]}")

# --- Test 4: overall totals ---
print("\n=== Test 4: Overall totals ===")
totals = {"FAILURE": 0, "ALERT": 0, "ERROR": 0, "UNKNOWN": 0, "total": 0}
for counts in summary.values():
    for key in totals:
        totals[key] += counts[key]
for key, val in totals.items():
    print(f"  {key:10}: {val}")

# --- Test 5: memory check — the big one ---
print("\n=== Test 5: Peak memory across full pipeline ===")
tracemalloc.start()
_ = group_by_hour(build_pipeline())
current, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()
print(f"  Peak memory : {peak / 1024:.2f} KB")
print(f"  (file is 211 KB — peak should be far smaller)")

# --- Test 6: write the JSON output ---
print("\n=== Test 6: Write summary.json ===")
write_summary(summary, OUTPUT)

# Verify it roundtrips correctly
with open(OUTPUT) as f:
    loaded = json.load(f)
print(f"  JSON loads back correctly : {loaded == summary}")
print(f"\n  Preview of summary.json:")
print(json.dumps(dict(list(loaded.items())[:3]), indent=2))