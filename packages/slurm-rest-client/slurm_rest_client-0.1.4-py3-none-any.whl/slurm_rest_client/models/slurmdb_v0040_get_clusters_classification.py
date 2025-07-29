from enum import Enum


class SlurmdbV0040GetClustersClassification(str, Enum):
    CAPABILITY = "CAPABILITY"
    CAPACITY = "CAPACITY"
    CAPAPACITY = "CAPAPACITY"
    UNCLASSIFIED = "UNCLASSIFIED"

    def __str__(self) -> str:
        return str(self.value)
