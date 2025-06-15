"""Download data of a whole year and store in archive as ZIP file."""
import os
import sys
from download import download, to_unix_timestamp, save_file, day_from_string
from archive import compress

def main():
    year = int(sys.argv[1])
    day_start = day_from_string(f"{year}-01-01")
    day_end = day_from_string(f"{year + 1}-01-01")

    start_time = to_unix_timestamp(day_start)
    end_time = to_unix_timestamp(day_end)
    file = f"archive/{year}.json"
    target = f"archive/{year}.zip"
    print(target)
    if not os.path.isfile(target):
        print(f"Downloading to {file}")
        content = download(start_time, end_time)
        save_file(file, content)
        compress(file)


if __name__ == "__main__":
    main()
