from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.v0040_job_info_power_flags_item import V0040JobInfoPowerFlagsItem
from ..types import UNSET, Unset

T = TypeVar("T", bound="V0040JobInfoPower")


@_attrs_define
class V0040JobInfoPower:
    """
    Attributes:
        flags (Union[Unset, list[V0040JobInfoPowerFlagsItem]]):
    """

    flags: Union[Unset, list[V0040JobInfoPowerFlagsItem]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        flags: Union[Unset, list[str]] = UNSET
        if not isinstance(self.flags, Unset):
            flags = []
            for flags_item_data in self.flags:
                flags_item = flags_item_data.value
                flags.append(flags_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if flags is not UNSET:
            field_dict["flags"] = flags

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        flags = []
        _flags = d.pop("flags", UNSET)
        for flags_item_data in _flags or []:
            flags_item = V0040JobInfoPowerFlagsItem(flags_item_data)

            flags.append(flags_item)

        v0040_job_info_power = cls(
            flags=flags,
        )

        v0040_job_info_power.additional_properties = d
        return v0040_job_info_power

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
