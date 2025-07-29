from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="V0040AssocMaxJobsPer")


@_attrs_define
class V0040AssocMaxJobsPer:
    """
    Attributes:
        count (Union[Unset, int]):
        accruing (Union[Unset, int]):
        submitted (Union[Unset, int]):
        wall_clock (Union[Unset, int]):
    """

    count: Union[Unset, int] = UNSET
    accruing: Union[Unset, int] = UNSET
    submitted: Union[Unset, int] = UNSET
    wall_clock: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        count = self.count

        accruing = self.accruing

        submitted = self.submitted

        wall_clock = self.wall_clock

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if count is not UNSET:
            field_dict["count"] = count
        if accruing is not UNSET:
            field_dict["accruing"] = accruing
        if submitted is not UNSET:
            field_dict["submitted"] = submitted
        if wall_clock is not UNSET:
            field_dict["wall_clock"] = wall_clock

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        count = d.pop("count", UNSET)

        accruing = d.pop("accruing", UNSET)

        submitted = d.pop("submitted", UNSET)

        wall_clock = d.pop("wall_clock", UNSET)

        v0040_assoc_max_jobs_per = cls(
            count=count,
            accruing=accruing,
            submitted=submitted,
            wall_clock=wall_clock,
        )

        v0040_assoc_max_jobs_per.additional_properties = d
        return v0040_assoc_max_jobs_per

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
