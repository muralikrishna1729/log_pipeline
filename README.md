# Log File Pipeline

A memory-efficient generator pipeline for processing large log files (100MB+) in constant memory.

## Architecture

```
read_lines → filter_errors → parse_timestamps → group_by_hour → summary.json
```

Each stage is a Python generator — data flows one line at a time, never loading the full file into memory.

## Pipeline Stages

| Stage | Input | Output | Purpose |
|---|---|---|---|
| `read_lines` | file path | `str` per line | Lazy file iteration |
| `filter_errors` | `str` lines | filtered `str` | Keep ERROR/WARN lines only |
| `parse_timestamps` | filtered `str` | `dict` records | Extract timestamp + level + message |
| `group_by_hour` | `dict` records | `dict` summary | Aggregate counts per hour |

## Expected Log Format

```
2024-01-15 14:23:01,456 ERROR [auth] Login failed for user=john
2024-01-15 14:23:02,789 INFO  [api] GET /health 200
2024-01-15 14:23:03,123 WARN  [db] Slow query detected: 2300ms
```

## Output Format

```json
{
  "generated_at": "2024-01-15T18:00:00",
  "source_file": "app.log",
  "total_errors": 1523,
  "by_hour": {
    "2024-01-15T14": { "ERROR": 42, "WARN": 17, "total": 59 },
    "2024-01-15T15": { "ERROR": 88, "WARN": 31, "total": 119 }
  },
  "top_hours": [
    { "hour": "2024-01-15T15", "total": 119 }
  ]
}
```

## Project Structure

```
log_pipeline/
├── src/
│   └── pipeline/
│       ├── __init__.py
│       ├── readers.py        # read_lines generator
│       ├── filters.py        # filter_errors generator
│       ├── parsers.py        # parse_timestamps generator
│       ├── aggregators.py    # group_by_hour (consumes pipeline)
│       └── runner.py         # Wires stages together, writes JSON
├── tests/
│   ├── test_readers.py
│   ├── test_filters.py
│   ├── test_parsers.py
│   └── test_aggregators.py
├── data/
│   └── generate_sample.py    # Generates a 100MB sample log
├── output/                   # summary.json written here
├── main.py                   # CLI entrypoint
├── pyproject.toml
└── README.md
```

## Usage

```bash
# Install dependencies
pip install -e ".[dev]"

# Generate a 100MB sample log
python data/generate_sample.py

# Run the pipeline
python main.py --input data/sample.log --output output/summary.json

# Run with verbose progress
python main.py --input data/sample.log --output output/summary.json --verbose

# Run tests
pytest tests/ -v
```

## Memory Guarantee

The pipeline uses Python generators throughout. At any point, only **one log line** is held in memory (plus the running aggregation dict). Memory usage stays flat regardless of file size.

Verified with: `tracemalloc` + `memory_profiler` (see `tests/test_memory.py`).