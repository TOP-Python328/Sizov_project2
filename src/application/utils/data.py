__all__ = [
    'ROOT_DIR',
    'DATA_DIR',
]


from pathlib import Path
from sys import path


ROOT_DIR = Path(path[0]).parent.parent
DATA_DIR = ROOT_DIR / 'data'