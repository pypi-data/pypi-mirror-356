from enum import Enum


class V0040PartitionInfoMaximumsOversubscribeFlagsItem(str, Enum):
    FORCE = "force"

    def __str__(self) -> str:
        return str(self.value)
