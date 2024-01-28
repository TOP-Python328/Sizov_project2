__all__ = [
    'Backup',
]

import pickle

from pathlib import Path
from tamagotchi import utils
from tamagotchi.app.model import *


class Backup:
    """Для работы с сохранением и загрузкой состояния существа."""
    
    def __init__(
            self,
            creature: Creature,
    ):
        self.creature = creature

    def save(self) -> None:
        """Сохраняет текущее состояние питомца в файл."""
        with open(utils.SAVE_DIR / 'data.pickle', 'wb') as f:
            pickle.dump(self.creature, f)

    def load(self) -> Creature | None:
        """Загружает последнее состояние питомца из файла или None если файла нет."""
        with open(utils.SAVE_DIR / 'data.pickle', 'rb') as f:
            creature = pickle.load(f)
            #print(creature)
            return creature



