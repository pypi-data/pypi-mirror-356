from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_partition_info_maximums_oversubscribe import V0040PartitionInfoMaximumsOversubscribe


T = TypeVar("T", bound="V0040PartitionInfoMaximums")


@_attrs_define
class V0040PartitionInfoMaximums:
    """
    Attributes:
        cpus_per_node (Union[Unset, int]):
        cpus_per_socket (Union[Unset, int]):
        memory_per_cpu (Union[Unset, int]):
        partition_memory_per_cpu (Union[Unset, int]):
        partition_memory_per_node (Union[Unset, int]):
        nodes (Union[Unset, int]):
        shares (Union[Unset, int]):
        oversubscribe (Union[Unset, V0040PartitionInfoMaximumsOversubscribe]):
        time (Union[Unset, int]):
        over_time_limit (Union[Unset, int]):
    """

    cpus_per_node: Union[Unset, int] = UNSET
    cpus_per_socket: Union[Unset, int] = UNSET
    memory_per_cpu: Union[Unset, int] = UNSET
    partition_memory_per_cpu: Union[Unset, int] = UNSET
    partition_memory_per_node: Union[Unset, int] = UNSET
    nodes: Union[Unset, int] = UNSET
    shares: Union[Unset, int] = UNSET
    oversubscribe: Union[Unset, "V0040PartitionInfoMaximumsOversubscribe"] = UNSET
    time: Union[Unset, int] = UNSET
    over_time_limit: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cpus_per_node = self.cpus_per_node

        cpus_per_socket = self.cpus_per_socket

        memory_per_cpu = self.memory_per_cpu

        partition_memory_per_cpu = self.partition_memory_per_cpu

        partition_memory_per_node = self.partition_memory_per_node

        nodes = self.nodes

        shares = self.shares

        oversubscribe: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.oversubscribe, Unset):
            oversubscribe = self.oversubscribe.to_dict()

        time = self.time

        over_time_limit = self.over_time_limit

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
        from ..models.v0040_partition_info_maximums_oversubscribe import V0040PartitionInfoMaximumsOversubscribe

        d = dict(src_dict)
        cpus_per_node = d.pop("cpus_per_node", UNSET)

        cpus_per_socket = d.pop("cpus_per_socket", UNSET)

        memory_per_cpu = d.pop("memory_per_cpu", UNSET)

        partition_memory_per_cpu = d.pop("partition_memory_per_cpu", UNSET)

        partition_memory_per_node = d.pop("partition_memory_per_node", UNSET)

        nodes = d.pop("nodes", UNSET)

        shares = d.pop("shares", UNSET)

        _oversubscribe = d.pop("oversubscribe", UNSET)
        oversubscribe: Union[Unset, V0040PartitionInfoMaximumsOversubscribe]
        if isinstance(_oversubscribe, Unset):
            oversubscribe = UNSET
        else:
            oversubscribe = V0040PartitionInfoMaximumsOversubscribe.from_dict(_oversubscribe)

        time = d.pop("time", UNSET)

        over_time_limit = d.pop("over_time_limit", UNSET)

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
