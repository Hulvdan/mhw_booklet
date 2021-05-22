from functools import lru_cache
from typing import List, Tuple, TypedDict

import commentjson

from .config import LIBRARY_DATA_PATH, logger
from .monster_card import ElementWeakness


class MonsterData(TypedDict):
    name: str
    attack: str
    weakness: Tuple[ElementWeakness]
    ailments: Tuple[int, int, int, int, int]
    color: str


class Library:
    @classmethod
    @lru_cache(1)
    def get_instance(cls) -> List[MonsterData]:
        logger.info('Loading library "%s"...' % LIBRARY_DATA_PATH)
        with open(str(LIBRARY_DATA_PATH)) as data_file:
            return commentjson.load(data_file)
