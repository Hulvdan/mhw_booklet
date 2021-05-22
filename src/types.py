
from typing import Tuple, TypedDict, Union

ElementWeakness = Union[Tuple[int, int], int]


class MonsterData(TypedDict):
    name: str
    attack: str
    weakness: Tuple[ElementWeakness]
    ailments: Tuple[int, int, int, int, int]
    color: str
