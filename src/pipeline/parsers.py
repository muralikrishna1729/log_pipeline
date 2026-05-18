import re
from datetime import datetime

# Syslog format: "Jun 15 04:06:20 combo process[pid]: message"
LOG_PATTERN = re.compile(
    r'^(\w{3})\s+(\d{1,2})\s+(\d{2}:\d{2}:\d{2})\s+(\S+)\s+(.+)$'
)

CURRENT_YEAR = datetime.now().year
def classify_level(message: str) -> str:
    msg_lower = message.lower()
    if "alert" in msg_lower:
        return "ALERT"
    if "authentication failure" in msg_lower or "check pass" in msg_lower:
        return "FAILURE"
    if "error" in msg_lower:
        return "ERROR"
    return "UNKNOWN"

def parse_timestamps(lines):
    for line in lines:
        match = LOG_PATTERN.match(line)
        if not match:
            continue
        month_str, day_str, time_str, host, message = match.groups()
        raw_dt_str = f"{CURRENT_YEAR} {month_str} {day_str} {time_str}"
        try:
            timestamp = datetime.strptime(raw_dt_str, "%Y %b %d %H:%M:%S")
        except ValueError:
            continue
        yield {
            "timestamp" : timestamp,
            "level"     : classify_level(message),
            "host"      : host,
            "process"   : message.split("[")[0].split(":")[0].strip(),
            "message"   : message,
        }
            