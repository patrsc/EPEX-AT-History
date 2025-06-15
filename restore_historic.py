"""Restore data from archive and put them into data."""
import os
import json
from datetime import datetime
from shutil import copyfile
from archive import decompress

from download import from_unix_timestamp, save_file


def main():
    archive_dir = 'archive'
    for file in os.listdir(archive_dir):
        if file.endswith('.zip'):
            restore(os.path.join(archive_dir, file))


def restore(zip_file):
    dst = f'data/{os.path.basename(zip_file)}'
    file = dst.replace('.zip', '.json')
    copyfile(zip_file, dst)
    decompress(dst)
    split_days(file)


def split_days(file):
    with open(file, 'r', encoding='utf8') as f:
        data = json.load(f)
    values = data['data']
    day_data = {}
    for value in values:
        start_time = from_unix_timestamp(value['start_timestamp'])
        day_str = datetime.strftime(start_time, '%Y-%m-%d')
        if day_str not in day_data:
            day_data[day_str] = []
        day_data[day_str].append(value)
    for day_str, values in day_data.items():
        out_file = f"data/{day_str.replace('-', '/')}.json"
        d = {
            "object": data["object"],
            "data": values,
            "url": data["url"]
        }
        text = json.dumps(d, indent=2)
        save_file(out_file, text)
    os.remove(file)


if __name__ == "__main__":
    main()
