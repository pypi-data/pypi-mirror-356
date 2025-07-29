from enum import Enum


class V0040ClusterRecFlagsItem(str, Enum):
    CRAY_NATIVE = "CRAY_NATIVE"
    EXTERNAL = "EXTERNAL"
    FEDERATION = "FEDERATION"
    FRONT_END = "FRONT_END"
    MULTIPLE_SLURMD = "MULTIPLE_SLURMD"
    REGISTERING = "REGISTERING"

    def __str__(self) -> str:
        return str(self.value)
