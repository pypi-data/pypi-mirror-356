from enum import Enum


class V0040AccountFlagsItem(str, Enum):
    DELETED = "DELETED"

    def __str__(self) -> str:
        return str(self.value)
