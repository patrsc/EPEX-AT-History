"""Check if no gaps exist in data."""
import os
import json

from validation import ResponseData
from download import from_unix_timestamp


def main():
    """Check data completeness."""
    start_timestamp = None
    prev_timestamp = None
    folder = "data"
    n = 0
    for year in list_dir(folder):
        year_dir = os.path.join(folder, year)
        for month in list_dir(year_dir):
            month_dir = os.path.join(year_dir, month)
            for day in list_dir(month_dir):
                file = os.path.join(month_dir, day)
                with open(file, 'r', encoding='utf8') as f:
                    data = json.load(f)
                    d = ResponseData.model_validate(data)
                    for item in d.data:
                        start = item.start_timestamp
                        end = item.end_timestamp
                        n += 1
                        if prev_timestamp is None:
                            start_timestamp = start
                            prev_timestamp = start
                        if not start == prev_timestamp:
                            raise ValueError(f"Gap found in file: {file}")
                        prev_timestamp = end
    end_timestamp = prev_timestamp
    start_time = from_unix_timestamp(start_timestamp).strftime("%Y-%m-%d %H:%M:%S")
    end_time = from_unix_timestamp(end_timestamp).strftime("%Y-%m-%d %H:%M:%S")
    print(f"Data complete. No gaps found from {start_time} to {end_time}. Checked {n} datasets.")


def list_dir(folder):
    """List directory, ignoring dot files."""
    items = os.listdir(folder)
    return sorted([item for item in items if not item.startswith('.')])


if __name__ == "__main__":
    main()
