from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="V0040JobHet")


@_attrs_define
class V0040JobHet:
    """
    Attributes:
        job_id (Union[Unset, int]):
        job_offset (Union[Unset, int]):
    """

    job_id: Union[Unset, int] = UNSET
    job_offset: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        job_id = self.job_id

        job_offset = self.job_offset

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if job_id is not UNSET:
            field_dict["job_id"] = job_id
        if job_offset is not UNSET:
            field_dict["job_offset"] = job_offset

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        job_id = d.pop("job_id", UNSET)

        job_offset = d.pop("job_offset", UNSET)

        v0040_job_het = cls(
            job_id=job_id,
            job_offset=job_offset,
        )

        v0040_job_het.additional_properties = d
        return v0040_job_het

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
