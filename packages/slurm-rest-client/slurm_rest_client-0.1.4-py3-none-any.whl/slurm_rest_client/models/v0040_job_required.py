from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="V0040JobRequired")


@_attrs_define
class V0040JobRequired:
    """
    Attributes:
        cp_us (Union[Unset, int]):
        memory_per_cpu (Union[Unset, int]):
        memory_per_node (Union[Unset, int]):
    """

    cp_us: Union[Unset, int] = UNSET
    memory_per_cpu: Union[Unset, int] = UNSET
    memory_per_node: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cp_us = self.cp_us

        memory_per_cpu = self.memory_per_cpu

        memory_per_node = self.memory_per_node

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if cp_us is not UNSET:
            field_dict["CPUs"] = cp_us
        if memory_per_cpu is not UNSET:
            field_dict["memory_per_cpu"] = memory_per_cpu
        if memory_per_node is not UNSET:
            field_dict["memory_per_node"] = memory_per_node

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        cp_us = d.pop("CPUs", UNSET)

        memory_per_cpu = d.pop("memory_per_cpu", UNSET)

        memory_per_node = d.pop("memory_per_node", UNSET)

        v0040_job_required = cls(
            cp_us=cp_us,
            memory_per_cpu=memory_per_cpu,
            memory_per_node=memory_per_node,
        )

        v0040_job_required.additional_properties = d
        return v0040_job_required

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
