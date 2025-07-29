from enum import Enum


class V0040JobInfoPowerFlagsItem(str, Enum):
    EQUAL_POWER = "EQUAL_POWER"

    def __str__(self) -> str:
        return str(self.value)
