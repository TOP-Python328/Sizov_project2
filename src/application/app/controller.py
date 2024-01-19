"""
Controller (MVC): управляющий модуль.
"""

from application import utils

#import model
#import view
from pathlib import Path
#from sys import path

from .model import *

#ROOT_DIR = Path(path[0]).parent.parent
#DATA_DIR = ROOT_DIR / 'data'

class KindLoader:
    default_path: Path = utils.DATA_DIR / 'kinds'
    
    @classmethod
    def _get_files(cls) -> list[Path]:
        return list(cls.default_path.glob('*.kind'))

    @classmethod 
    def load(cls) -> list[Kind]:
        kinds = []
        for file in cls._get_files():
            source = file.read_text(encoding='utf-8')
            # вычисление выражения в строке с исходным кодом - функция eval() возвращает объект, полученный в результате вычисления выражения
            kind = eval(source)
            kinds.append(kind)
        return kinds


kinds = KindLoader.load()

jack = Creature(kinds[0], 'Джек')