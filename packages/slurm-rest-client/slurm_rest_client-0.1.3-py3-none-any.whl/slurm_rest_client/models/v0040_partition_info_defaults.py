from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_partition_info_defaults_partition_memory_per_cpu import (
        V0040PartitionInfoDefaultsPartitionMemoryPerCpu,
    )
    from ..models.v0040_partition_info_defaults_partition_memory_per_node import (
        V0040PartitionInfoDefaultsPartitionMemoryPerNode,
    )
    from ..models.v0040_partition_info_defaults_time import V0040PartitionInfoDefaultsTime


T = TypeVar("T", bound="V0040PartitionInfoDefaults")


@_attrs_define
class V0040PartitionInfoDefaults:
    """
    Attributes:
        memory_per_cpu (Union[Unset, int]):
        partition_memory_per_cpu (Union[Unset, V0040PartitionInfoDefaultsPartitionMemoryPerCpu]):
        partition_memory_per_node (Union[Unset, V0040PartitionInfoDefaultsPartitionMemoryPerNode]):
        time (Union[Unset, V0040PartitionInfoDefaultsTime]):
        job (Union[Unset, str]):
    """

    memory_per_cpu: Union[Unset, int] = UNSET
    partition_memory_per_cpu: Union[Unset, "V0040PartitionInfoDefaultsPartitionMemoryPerCpu"] = UNSET
    partition_memory_per_node: Union[Unset, "V0040PartitionInfoDefaultsPartitionMemoryPerNode"] = UNSET
    time: Union[Unset, "V0040PartitionInfoDefaultsTime"] = UNSET
    job: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        memory_per_cpu = self.memory_per_cpu

        partition_memory_per_cpu: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.partition_memory_per_cpu, Unset):
            partition_memory_per_cpu = self.partition_memory_per_cpu.to_dict()

        partition_memory_per_node: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.partition_memory_per_node, Unset):
            partition_memory_per_node = self.partition_memory_per_node.to_dict()

        time: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.time, Unset):
            time = self.time.to_dict()

        job = self.job

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if memory_per_cpu is not UNSET:
            field_dict["memory_per_cpu"] = memory_per_cpu
        if partition_memory_per_cpu is not UNSET:
            field_dict["partition_memory_per_cpu"] = partition_memory_per_cpu
        if partition_memory_per_node is not UNSET:
            field_dict["partition_memory_per_node"] = partition_memory_per_node
        if time is not UNSET:
            field_dict["time"] = time
        if job is not UNSET:
            field_dict["job"] = job

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0040_partition_info_defaults_partition_memory_per_cpu import (
            V0040PartitionInfoDefaultsPartitionMemoryPerCpu,
        )
        from ..models.v0040_partition_info_defaults_partition_memory_per_node import (
            V0040PartitionInfoDefaultsPartitionMemoryPerNode,
        )
        from ..models.v0040_partition_info_defaults_time import V0040PartitionInfoDefaultsTime

        d = dict(src_dict)
        memory_per_cpu = d.pop("memory_per_cpu", UNSET)

        _partition_memory_per_cpu = d.pop("partition_memory_per_cpu", UNSET)
        partition_memory_per_cpu: Union[Unset, V0040PartitionInfoDefaultsPartitionMemoryPerCpu]
        if isinstance(_partition_memory_per_cpu, Unset):
            partition_memory_per_cpu = UNSET
        else:
            partition_memory_per_cpu = V0040PartitionInfoDefaultsPartitionMemoryPerCpu.from_dict(
                _partition_memory_per_cpu
            )

        _partition_memory_per_node = d.pop("partition_memory_per_node", UNSET)
        partition_memory_per_node: Union[Unset, V0040PartitionInfoDefaultsPartitionMemoryPerNode]
        if isinstance(_partition_memory_per_node, Unset):
            partition_memory_per_node = UNSET
        else:
            partition_memory_per_node = V0040PartitionInfoDefaultsPartitionMemoryPerNode.from_dict(
                _partition_memory_per_node
            )

        _time = d.pop("time", UNSET)
        time: Union[Unset, V0040PartitionInfoDefaultsTime]
        if isinstance(_time, Unset):
            time = UNSET
        else:
            time = V0040PartitionInfoDefaultsTime.from_dict(_time)

        job = d.pop("job", UNSET)

        v0040_partition_info_defaults = cls(
            memory_per_cpu=memory_per_cpu,
            partition_memory_per_cpu=partition_memory_per_cpu,
            partition_memory_per_node=partition_memory_per_node,
            time=time,
            job=job,
        )

        v0040_partition_info_defaults.additional_properties = d
        return v0040_partition_info_defaults

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
