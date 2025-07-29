from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_partition_info_maximums_cpus_per_node import V0040PartitionInfoMaximumsCpusPerNode
    from ..models.v0040_partition_info_maximums_cpus_per_socket import V0040PartitionInfoMaximumsCpusPerSocket
    from ..models.v0040_partition_info_maximums_nodes import V0040PartitionInfoMaximumsNodes
    from ..models.v0040_partition_info_maximums_over_time_limit import V0040PartitionInfoMaximumsOverTimeLimit
    from ..models.v0040_partition_info_maximums_oversubscribe import V0040PartitionInfoMaximumsOversubscribe
    from ..models.v0040_partition_info_maximums_partition_memory_per_cpu import (
        V0040PartitionInfoMaximumsPartitionMemoryPerCpu,
    )
    from ..models.v0040_partition_info_maximums_partition_memory_per_node import (
        V0040PartitionInfoMaximumsPartitionMemoryPerNode,
    )
    from ..models.v0040_partition_info_maximums_time import V0040PartitionInfoMaximumsTime


T = TypeVar("T", bound="V0040PartitionInfoMaximums")


@_attrs_define
class V0040PartitionInfoMaximums:
    """
    Attributes:
        cpus_per_node (Union[Unset, V0040PartitionInfoMaximumsCpusPerNode]):
        cpus_per_socket (Union[Unset, V0040PartitionInfoMaximumsCpusPerSocket]):
        memory_per_cpu (Union[Unset, int]):
        partition_memory_per_cpu (Union[Unset, V0040PartitionInfoMaximumsPartitionMemoryPerCpu]):
        partition_memory_per_node (Union[Unset, V0040PartitionInfoMaximumsPartitionMemoryPerNode]):
        nodes (Union[Unset, V0040PartitionInfoMaximumsNodes]):
        shares (Union[Unset, int]):
        oversubscribe (Union[Unset, V0040PartitionInfoMaximumsOversubscribe]):
        time (Union[Unset, V0040PartitionInfoMaximumsTime]):
        over_time_limit (Union[Unset, V0040PartitionInfoMaximumsOverTimeLimit]):
    """

    cpus_per_node: Union[Unset, "V0040PartitionInfoMaximumsCpusPerNode"] = UNSET
    cpus_per_socket: Union[Unset, "V0040PartitionInfoMaximumsCpusPerSocket"] = UNSET
    memory_per_cpu: Union[Unset, int] = UNSET
    partition_memory_per_cpu: Union[Unset, "V0040PartitionInfoMaximumsPartitionMemoryPerCpu"] = UNSET
    partition_memory_per_node: Union[Unset, "V0040PartitionInfoMaximumsPartitionMemoryPerNode"] = UNSET
    nodes: Union[Unset, "V0040PartitionInfoMaximumsNodes"] = UNSET
    shares: Union[Unset, int] = UNSET
    oversubscribe: Union[Unset, "V0040PartitionInfoMaximumsOversubscribe"] = UNSET
    time: Union[Unset, "V0040PartitionInfoMaximumsTime"] = UNSET
    over_time_limit: Union[Unset, "V0040PartitionInfoMaximumsOverTimeLimit"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cpus_per_node: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.cpus_per_node, Unset):
            cpus_per_node = self.cpus_per_node.to_dict()

        cpus_per_socket: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.cpus_per_socket, Unset):
            cpus_per_socket = self.cpus_per_socket.to_dict()

        memory_per_cpu = self.memory_per_cpu

        partition_memory_per_cpu: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.partition_memory_per_cpu, Unset):
            partition_memory_per_cpu = self.partition_memory_per_cpu.to_dict()

        partition_memory_per_node: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.partition_memory_per_node, Unset):
            partition_memory_per_node = self.partition_memory_per_node.to_dict()

        nodes: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.nodes, Unset):
            nodes = self.nodes.to_dict()

        shares = self.shares

        oversubscribe: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.oversubscribe, Unset):
            oversubscribe = self.oversubscribe.to_dict()

        time: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.time, Unset):
            time = self.time.to_dict()

        over_time_limit: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.over_time_limit, Unset):
            over_time_limit = self.over_time_limit.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if cpus_per_node is not UNSET:
            field_dict["cpus_per_node"] = cpus_per_node
        if cpus_per_socket is not UNSET:
            field_dict["cpus_per_socket"] = cpus_per_socket
        if memory_per_cpu is not UNSET:
            field_dict["memory_per_cpu"] = memory_per_cpu
        if partition_memory_per_cpu is not UNSET:
            field_dict["partition_memory_per_cpu"] = partition_memory_per_cpu
        if partition_memory_per_node is not UNSET:
            field_dict["partition_memory_per_node"] = partition_memory_per_node
        if nodes is not UNSET:
            field_dict["nodes"] = nodes
        if shares is not UNSET:
            field_dict["shares"] = shares
        if oversubscribe is not UNSET:
            field_dict["oversubscribe"] = oversubscribe
        if time is not UNSET:
            field_dict["time"] = time
        if over_time_limit is not UNSET:
            field_dict["over_time_limit"] = over_time_limit

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0040_partition_info_maximums_cpus_per_node import V0040PartitionInfoMaximumsCpusPerNode
        from ..models.v0040_partition_info_maximums_cpus_per_socket import V0040PartitionInfoMaximumsCpusPerSocket
        from ..models.v0040_partition_info_maximums_nodes import V0040PartitionInfoMaximumsNodes
        from ..models.v0040_partition_info_maximums_over_time_limit import V0040PartitionInfoMaximumsOverTimeLimit
        from ..models.v0040_partition_info_maximums_oversubscribe import V0040PartitionInfoMaximumsOversubscribe
        from ..models.v0040_partition_info_maximums_partition_memory_per_cpu import (
            V0040PartitionInfoMaximumsPartitionMemoryPerCpu,
        )
        from ..models.v0040_partition_info_maximums_partition_memory_per_node import (
            V0040PartitionInfoMaximumsPartitionMemoryPerNode,
        )
        from ..models.v0040_partition_info_maximums_time import V0040PartitionInfoMaximumsTime

        d = dict(src_dict)
        _cpus_per_node = d.pop("cpus_per_node", UNSET)
        cpus_per_node: Union[Unset, V0040PartitionInfoMaximumsCpusPerNode]
        if isinstance(_cpus_per_node, Unset):
            cpus_per_node = UNSET
        else:
            cpus_per_node = V0040PartitionInfoMaximumsCpusPerNode.from_dict(_cpus_per_node)

        _cpus_per_socket = d.pop("cpus_per_socket", UNSET)
        cpus_per_socket: Union[Unset, V0040PartitionInfoMaximumsCpusPerSocket]
        if isinstance(_cpus_per_socket, Unset):
            cpus_per_socket = UNSET
        else:
            cpus_per_socket = V0040PartitionInfoMaximumsCpusPerSocket.from_dict(_cpus_per_socket)

        memory_per_cpu = d.pop("memory_per_cpu", UNSET)

        _partition_memory_per_cpu = d.pop("partition_memory_per_cpu", UNSET)
        partition_memory_per_cpu: Union[Unset, V0040PartitionInfoMaximumsPartitionMemoryPerCpu]
        if isinstance(_partition_memory_per_cpu, Unset):
            partition_memory_per_cpu = UNSET
        else:
            partition_memory_per_cpu = V0040PartitionInfoMaximumsPartitionMemoryPerCpu.from_dict(
                _partition_memory_per_cpu
            )

        _partition_memory_per_node = d.pop("partition_memory_per_node", UNSET)
        partition_memory_per_node: Union[Unset, V0040PartitionInfoMaximumsPartitionMemoryPerNode]
        if isinstance(_partition_memory_per_node, Unset):
            partition_memory_per_node = UNSET
        else:
            partition_memory_per_node = V0040PartitionInfoMaximumsPartitionMemoryPerNode.from_dict(
                _partition_memory_per_node
            )

        _nodes = d.pop("nodes", UNSET)
        nodes: Union[Unset, V0040PartitionInfoMaximumsNodes]
        if isinstance(_nodes, Unset):
            nodes = UNSET
        else:
            nodes = V0040PartitionInfoMaximumsNodes.from_dict(_nodes)

        shares = d.pop("shares", UNSET)

        _oversubscribe = d.pop("oversubscribe", UNSET)
        oversubscribe: Union[Unset, V0040PartitionInfoMaximumsOversubscribe]
        if isinstance(_oversubscribe, Unset):
            oversubscribe = UNSET
        else:
            oversubscribe = V0040PartitionInfoMaximumsOversubscribe.from_dict(_oversubscribe)

        _time = d.pop("time", UNSET)
        time: Union[Unset, V0040PartitionInfoMaximumsTime]
        if isinstance(_time, Unset):
            time = UNSET
        else:
            time = V0040PartitionInfoMaximumsTime.from_dict(_time)

        _over_time_limit = d.pop("over_time_limit", UNSET)
        over_time_limit: Union[Unset, V0040PartitionInfoMaximumsOverTimeLimit]
        if isinstance(_over_time_limit, Unset):
            over_time_limit = UNSET
        else:
            over_time_limit = V0040PartitionInfoMaximumsOverTimeLimit.from_dict(_over_time_limit)

        v0040_partition_info_maximums = cls(
            cpus_per_node=cpus_per_node,
            cpus_per_socket=cpus_per_socket,
            memory_per_cpu=memory_per_cpu,
            partition_memory_per_cpu=partition_memory_per_cpu,
            partition_memory_per_node=partition_memory_per_node,
            nodes=nodes,
            shares=shares,
            oversubscribe=oversubscribe,
            time=time,
            over_time_limit=over_time_limit,
        )

        v0040_partition_info_maximums.additional_properties = d
        return v0040_partition_info_maximums

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
