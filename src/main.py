from os import path
from compat.osCompat import escapeFilePaths

with open(path.dirname(path.abspath(__file__)) + escapeFilePaths(['ui', 'interface.py'])) as f:
    exec(f.read())