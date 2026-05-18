import os

def read_lines(file_path:str):
    """Reads lines from a file and returns them as a list."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, 'r', encoding='utf-8', errors="replace") as f:
        for line in f:
            line = line.strip()
            if line:
                yield line

def read_lines_as_list(file_path:str):
    """Reads lines from a file and returns them as a list."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        return [line.strip() for line in f if line.strip()]