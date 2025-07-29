from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_assoc_max_tres_minutes_per_job import V0040AssocMaxTresMinutesPerJob


T = TypeVar("T", bound="V0040AssocMaxTresMinutesPer")


@_attrs_define
class V0040AssocMaxTresMinutesPer:
    """
    Attributes:
        job (Union[Unset, V0040AssocMaxTresMinutesPerJob]):
    """

    job: Union[Unset, "V0040AssocMaxTresMinutesPerJob"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        job: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.job, Unset):
            job = self.job.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if job is not UNSET:
            field_dict["job"] = job

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0040_assoc_max_tres_minutes_per_job import V0040AssocMaxTresMinutesPerJob

        d = dict(src_dict)
        _job = d.pop("job", UNSET)
        job: Union[Unset, V0040AssocMaxTresMinutesPerJob]
        if isinstance(_job, Unset):
            job = UNSET
        else:
            job = V0040AssocMaxTresMinutesPerJob.from_dict(_job)

        v0040_assoc_max_tres_minutes_per = cls(
            job=job,
        )

        v0040_assoc_max_tres_minutes_per.additional_properties = d
        return v0040_assoc_max_tres_minutes_per

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
