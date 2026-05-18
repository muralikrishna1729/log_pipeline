from collections import defaultdict
from datetime import datetime



def group_by_hour(records):
    counts = defaultdict(lambda: {
        "FAILURE": 0,
        "ALERT"  : 0,
        "ERROR"  : 0,
        "UNKNOWN": 0,
        "total"  : 0,
    })

    for record in records:
        hour = record["timestamp"].replace(minute=0, second=0, microsecond=0)
        level = record["level"]
        hour_key = hour.strftime("%Y-%m-%d %H:00")

        counts[hour_key][level] += 1
        counts[hour_key]["total"] += 1
    return dict(sorted(counts.items()))

def write_summary(summary:dict , output_path:str):
    import os 
    import json
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Summary written → {output_path}")
    print(f"  Hours tracked : {len(summary)}")
    print(f"  Total events  : {sum(v['total'] for v in summary.values())}")