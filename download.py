"""Download data of EPEX Spot AT."""
import os
import json
import sys
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import requests

from validation import validate

TIMEZONE = "Europe/Vienna"


def main():
    """Download single day data if not yet existing (next day if no YYYY-DD-MM date provided)."""
    if len(sys.argv) > 1:
        day_start = day_from_string(sys.argv[1])
    else:
        t = get_current_local_time()
        today_start = get_day_start(t)
        day_start = today_start + timedelta(days=1)

    download_day(day_start)


def download_day(day_start: datetime):
    """Download data of given day."""
    print(f"Target day: {day_start.strftime('%Y-%m-%d')}")
    day_end = day_start + timedelta(days=1)
    start_time = to_unix_timestamp(day_start)
    end_time = to_unix_timestamp(day_end)
    file = day_start.strftime("data/%Y/%m/%d.json")
    if not os.path.isfile(file):
        print(f"Downloading to {file}")
        content = download(start_time, end_time)
        save_file(file, content)
    else:
        print("Nothing to do.")
    print("Finished successfully.")


def download(start_time: int, end_time: int):
    """Download data from API server."""
    url = f"https://api.awattar.at/v1/marketdata?start={start_time}&end={end_time}"
    response = requests.get(url, timeout=15)
    if not response.ok:
        raise ValueError(f"Server returned status {response.status_code}")
    text = response.text
    data = json.loads(text)
    validate(data, start_time, end_time)
    return text


def save_file(file: str, text: str):
    """Save file, creating parent folders if they don't exist."""
    dir_path = os.path.dirname(file)
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)
    with open(file, 'w', encoding='utf8') as f:
        f.write(text)


def to_unix_timestamp(dt: datetime) -> int:
    """Return UNIX timestamp (int in milliseconds) of datetime."""
    return int(dt.timestamp() * 1000)


def from_unix_timestamp(n: int) -> datetime:
    """Return datetime (in TIMEZONE) from UNIX timestamp."""
    return datetime.fromtimestamp(n / 1000, tz=ZoneInfo(TIMEZONE))


def get_current_local_time() -> datetime:
    """Return datetime object with current local time in TIMEZONE."""
    return datetime.now(tz=ZoneInfo(TIMEZONE))


def get_day_start(dt: datetime) -> datetime:
    """Return start of the day of given datetime (00:00:00)."""
    return dt.replace(hour=0, minute=0, second=0, microsecond=0)


def day_from_string(date_str: str) -> datetime:
    """Return datetime from string in form YYYY-MM-DD (at 00:00:00 in TIMEZONE)."""
    dt = datetime.strptime(date_str, '%Y-%m-%d')
    dt.replace(tzinfo=ZoneInfo(TIMEZONE))
    return dt


if __name__ == "__main__":
    main()
