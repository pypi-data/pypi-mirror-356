from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="V0040PartitionInfoTimeouts")


@_attrs_define
class V0040PartitionInfoTimeouts:
    """
    Attributes:
        resume (Union[Unset, int]):
        suspend (Union[Unset, int]):
    """

    resume: Union[Unset, int] = UNSET
    suspend: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        resume = self.resume

        suspend = self.suspend

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if resume is not UNSET:
            field_dict["resume"] = resume
        if suspend is not UNSET:
            field_dict["suspend"] = suspend

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        resume = d.pop("resume", UNSET)

        suspend = d.pop("suspend", UNSET)

        v0040_partition_info_timeouts = cls(
            resume=resume,
            suspend=suspend,
        )

        v0040_partition_info_timeouts.additional_properties = d
        return v0040_partition_info_timeouts

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
