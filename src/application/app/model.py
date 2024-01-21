"""
Модель (MVC) приложения.
"""

 
from application import utils

from abc import ABC, abstractmethod
from collections.abc import Iterable
from dataclasses import dataclass 
from enum import Enum
from functools import cached_property
from pathlib import Path
from random import choice, sample
from typing import Type

 
@dataclass
class KindParameter:
    """Описывает параметр вида для фазы зрелости вида."""
    name: str
    initial: float
    min: float
    max: float

    def __hash__(self):
        return hash(self.name)


class CreatureParameter(ABC):
    """Описывает параметры существа - активные параметры."""
    name: str

    def __init__(
                self,
                initial: float,
                left: float,
                right: float,
                creature: 'Creature',
    ):
        self.__value = initial
        self._min = left
        self._max = right
        self.creature = creature

    @property
    def value(self) -> float:
        return self.__value

    @cached_property
    def range(self) -> tuple[float, float]:
        return self._min, self._max

    @value.setter
    def value(self, new_value: float):
#        if isinstance(new_value, float):
            if new_value <= self._min:
                self.__value = self._min 
            elif new_value >= self._max:
                self.__value = self._max
            else:
                self.__value = new_value
#        else:
#            raise TypeError

    @abstractmethod
    def update(self) -> None:
        pass


class Health(CreatureParameter):
    """Описывает параметр здоровье."""
    name = 'здоровье'
    
    def update(self) -> None:
        """Обновляет параметр."""
        satiety = self.creature.params[Satiety]
        critical = sum(satiety.range) / 4
        if 0 < satiety.value < critical:
            self.value -= 0.5
        elif satiety.value == 0:
            self.value -= 1


class Satiety(CreatureParameter):
    """Описывает параметр сытость."""
    name = 'сытость'
    
    def update(self) -> None:
        """Обновляет параметр."""
        self.value -= 1


class Mood(CreatureParameter):
    name = 'настроение'
    
    def update(self) -> None:
        satiety = self.creature.params[Satiety]
        critical = sum(satiety.range) / 4
        if 0 < satiety.value < critical:
            self.value -= 0.2
        elif satiety.value == 0:
            self.value -= 0.5
        satiety = self.creature.params[Health]
        critical = sum(satiety.range) / 4
        if 0 < satiety.value < critical:
            self.value -= 0.3
        elif satiety.value == 0:
            self.value -= 0.7
        else:
            self.value += 0.1


Parameters = Enum(
    """Перечислитель параметров."""
    'Parameters',
    {
        cls.__name__:cls
        for cls in CreatureParameter.__subclasses__()
    }    
)
   

class Action(ABC):
    name: str

    def __init__(self, creature: 'Creature' = None):
        self.creature = creature

    def __hash__(self):
        return hash(self.name)

    @abstractmethod
    def do(self) -> None:
        pass


class PlayerAction(Action):
    """Описывает действия игрока."""
    image: Path
    state = 'normal'


class Feed(PlayerAction):
    """Описывает действие игрока покормить питомца."""
    name = 'покормить'
    image = DATA_DIR / 'images/btn1.png'   
    
    def __init__(
            self,
            amount: float,
            creature: 'Creature' = None,            
    ):
        self.amount = amount
        super().__init__(creature)

    def do(self) -> str:
        self.creature.params[Satiety].value += self.amount
        return f'вы покормили питомца на {self.amount} ед.'


class TeaseHead(PlayerAction):
    """Описывает действие игрока чесать голову питомцу."""
    name = 'почесать голову'
    image = DATA_DIR / 'images/btn3.png'
    
    def do(self) -> str:
        return 'вы почесали голову питомцу'


class Play(PlayerAction):
    name = 'поиграть с питомцем'
    image = DATA_DIR / 'images/btn2.png'
    
    def __init__(
            self, 
            amount1: float,
            amount2: float,
            creature: 'Creature' = None, 
    ):
        self.amount1 = amount1
        self.amount2 = amount2
        super().__init__(creature)
    
    def do(self) -> str:
        self.creature.params[Mood].value += self.amount1
        self.creature.params[Satiety].value -= self.amount2
        return f'вы поиграли с питомцем'


class CreatureAction(Action):
    """Описывает действие питомца."""
    def __init__(
            self,
            rand_coeff: float,
            creature: 'Creature' = None,
    ):
        self.rand_coeff = rand_coeff
        super().__init__(creature)


class ChaseTail(CreatureAction):
    """Описывает действие питомца гоняться за своим хвостом."""
    name = 'гоняться за своим хвостом'
    
    def do(self) -> None:
        print('бегает за своим хвостом')


class Sleep(CreatureAction):
    name = 'спать'
    
    def do(self) -> None:
        print('спит')


class NoAction(Action):
    """Описывает бездействие питомца."""
    name = 'бездействие'
    
    def do(self) -> None:
        print('бездействует')


class MaturePhase:
    """Описывает фазу взросления.
   Содержит:
    - колличество игровых дней на фазе зрелости,
    - список параметров,
    - список действий игрока,
    - список активностей существа.
    """
    def __init__(
                self,
                days: int,
                *parameters: KindParameter,
                player_actions = Iterable[PlayerAction],
                creature_actions = Iterable[CreatureAction],
    ):
        self.days = days
        self.params = set(parameters)
        self.player_actions = set(player_actions)
        self.creature_actions = set(creature_actions)


class Kind(utils.DictOfRange):
    """Описывает вид как словарь диапазонов, где ключи это игровые дни (возраст существа), а значения - фазы взросления."""
    def __init__(
                self, 
                name: str, 
                *mature_phases: MaturePhase
    ):
        self.name = name
        
        phases = {}
        left = 0
        for phase in mature_phases:
            key = left, left + phase.days  - 1
            phases[key] = phase
            left = left + phase.days
        super().__init__(phases)


@dataclass
class State:
    age: int
    
    def __repr__(self):
        return '/'.join(v for v in self.__dict__.values())


class History(list):
    """Описывает историю состояний."""
    def get_param(self, param: Type) -> list[float]:
        return [
            getattr(state, param.__name__)
            for state in self 
        ]


class Creature:
    """Описывает существо."""
    def __init__(
            self,
            kind: Kind,
            name: str,
    ):
        self.kind = kind
        self.name = name
        self.__age: int = 0
        self.params: dict[Type, CreatureParameter] = {}
        for param in kind[0].params:
            cls = Parameters[param.name].value
            self.params[cls] = cls(
                initial = param.initial,
                left = param.min,
                right = param.max,
                creature = self,
            )
        self.player_actions: set[PlayerAction]
        self.creature_actions: set[CreatureAction]
        self.__set_actions()
        self.history: History = History()

    def __repr__(self):
        title = f'({self.kind.name}) {self.name}: {self.age} ИД'
        params = '\n'.join(
            f'{p.name}: {p.value:.1f}'
            for p in self.params.values()
        )
        return f'{title}\n{params}'

    def __set_actions(self) -> None:
        self.player_actions = {
            action.__class__(**{**action.__dict__, 'creature': self})
            for action in self.kind[self.age].player_actions
        }
        self.creature_actions = {
            action.__class__(**{**action.__dict__, 'creature': self})
            for action in self.kind[self.age].creature_actions
        }

    def update(self) -> None:
        """Обновляет параметры существа."""
        for param in self.params.values():
            param.update()
        self.save()

    @property
    def age(self) -> int:
        return self.__age
    
    @age.setter
    def age(self, new_value: int):
    
        old_phase = self.kind.get_range(self.__age)
        old_phase = self.kind.get_range(new_value)
        self.__age = new_value
        if old_phase != new_value:
            self._grow_up()
    
    def _grow_up(self) -> None:
        for param in self.kind[self.age].params:
            cls = Parameters[param.name].value
            initial = param.initial or self.params[cls].value 
            self.params[cls] = cls(
                initial = initial,
                left = param.min,
                right = param.max,
                creature = self,
            )
        self.__set_actions()

    def random_action(self) -> None:
        """вызывает случайное действие."""
        action = choice(tuple(self.creature_actions))
        no_action = NoAction()
        prob = int(action.rand_coeff*100)
        choice(sample([action, no_action], counts=[prob, 100-prob], k = 100)).do()

    def save(self) -> State:
        state = State(self.age)
        for cls, param in self.params.items():
            setattr(state, cls.__name__, param.value)
        self.history.append(state)
        return state
