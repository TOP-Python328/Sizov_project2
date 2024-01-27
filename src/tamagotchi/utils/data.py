__all__ = [
    'ROOT_DIR',
    'DATA_DIR',
    'SAVE_DIR',
    'KINDS_DIR',
    'DictOfRanges',
]


from pathlib import Path
from sys import path


ROOT_DIR = Path(path[0]).parent
DATA_DIR = ROOT_DIR / 'data'
SAVE_DIR = ROOT_DIR / 'data' / 'save'
KINDS_DIR = DATA_DIR / 'kinds'

class DictOfRanges(dict):
    """Описывает словарь диапазонов."""
    def __init__(self, mappable: dict):
        for key in mappable:
            if (
                    not isinstance(key, tuple)
                or len(key) != 2
                or not isinstance(key[0], int)
                or not isinstance(key[1], int)                    
            ):
                raise ValueError('...')
        super().__init__(mappable)

    def __getitem__(self, key: int):
        if isinstance(key, int):
            for left, right in self:
                if left <= key <= right:
                    return super().__getitem__((left, right))
        else:
            return super().__getitem__(key)

    def get_range(self, key: int) -> tuple[int, int]:
        if isinstance(key, int):
            for left, right in self:
                if left <= key <= right:
                    return left, right
        else:
            raise TypeError