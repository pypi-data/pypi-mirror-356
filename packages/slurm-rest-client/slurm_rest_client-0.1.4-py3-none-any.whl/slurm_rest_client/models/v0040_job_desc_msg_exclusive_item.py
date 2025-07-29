from enum import Enum


class V0040JobDescMsgExclusiveItem(str, Enum):
    FALSE = "false"
    MCS = "mcs"
    TRUE = "true"
    USER = "user"

    def __str__(self) -> str:
        return str(self.value)
