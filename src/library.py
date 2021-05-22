from functools import lru_cache
from typing import List, Tuple, TypedDict

import commentjson

from .config import LIBRARY_DATA_PATH, logger
from .types import MonsterData


class Library:
    @classmethod
    @lru_cache(1)
    def get_instance(cls) -> List[MonsterData]:
        logger.info('Loading library "%s"...' % LIBRARY_DATA_PATH)
        with open(str(LIBRARY_DATA_PATH)) as data_file:
            return commentjson.load(data_file)
