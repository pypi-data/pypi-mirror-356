from enum import Enum


class _BaseHeleketEnum(str, Enum):

    def __str__(self) -> str:
        return self.value
    
    @classmethod
    def to_list(cls):
        return list(cls)