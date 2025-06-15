import os
import zipfile


def compress(filepath):
    """
    Compress a JSON file into a ZIP archive and delete the original JSON file.
    Example: 'a.json' -> 'a.zip'
    """
    if not filepath.endswith('.json'):
        raise ValueError("Expected a .json file")

    zip_path = filepath[:-5] + '.zip'
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as f:
        f.write(filepath, arcname=os.path.basename(filepath))

    os.remove(filepath)
    return zip_path


def decompress(filepath):
    """
    Decompress a ZIP archive containing a JSON file and delete the ZIP file.
    Example: 'a.zip' -> 'a.json'
    """
    if not filepath.endswith('.zip'):
        raise ValueError("Expected a .zip file")

    with zipfile.ZipFile(filepath, 'r') as f:
        f.extractall(path=os.path.dirname(filepath))

    os.remove(filepath)

    # Return path to extracted .json file
    for name in f.namelist():
        if name.endswith('.json'):
            return os.path.join(os.path.dirname(filepath), name)
    raise FileNotFoundError("No .json file found in the ZIP archive")
