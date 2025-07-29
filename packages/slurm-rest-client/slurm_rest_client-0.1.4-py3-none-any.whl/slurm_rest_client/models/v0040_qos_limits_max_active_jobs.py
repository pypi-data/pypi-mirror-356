from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="V0040QosLimitsMaxActiveJobs")


@_attrs_define
class V0040QosLimitsMaxActiveJobs:
    """
    Attributes:
        accruing (Union[Unset, int]):
        count (Union[Unset, int]):
    """

    accruing: Union[Unset, int] = UNSET
    count: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        accruing = self.accruing

        count = self.count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if accruing is not UNSET:
            field_dict["accruing"] = accruing
        if count is not UNSET:
            field_dict["count"] = count

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        accruing = d.pop("accruing", UNSET)

        count = d.pop("count", UNSET)

        v0040_qos_limits_max_active_jobs = cls(
            accruing=accruing,
            count=count,
        )

        v0040_qos_limits_max_active_jobs.additional_properties = d
        return v0040_qos_limits_max_active_jobs

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
