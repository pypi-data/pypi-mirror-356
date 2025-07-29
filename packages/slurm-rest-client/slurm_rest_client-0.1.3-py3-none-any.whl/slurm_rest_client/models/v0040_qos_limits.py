from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_qos_limits_factor import V0040QosLimitsFactor
    from ..models.v0040_qos_limits_max import V0040QosLimitsMax
    from ..models.v0040_qos_limits_min import V0040QosLimitsMin


T = TypeVar("T", bound="V0040QosLimits")


@_attrs_define
class V0040QosLimits:
    """
    Attributes:
        grace_time (Union[Unset, int]):
        max_ (Union[Unset, V0040QosLimitsMax]):
        factor (Union[Unset, V0040QosLimitsFactor]):
        min_ (Union[Unset, V0040QosLimitsMin]):
    """

    grace_time: Union[Unset, int] = UNSET
    max_: Union[Unset, "V0040QosLimitsMax"] = UNSET
    factor: Union[Unset, "V0040QosLimitsFactor"] = UNSET
    min_: Union[Unset, "V0040QosLimitsMin"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        grace_time = self.grace_time

        max_: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.max_, Unset):
            max_ = self.max_.to_dict()

        factor: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.factor, Unset):
            factor = self.factor.to_dict()

        min_: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.min_, Unset):
            min_ = self.min_.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if grace_time is not UNSET:
            field_dict["grace_time"] = grace_time
        if max_ is not UNSET:
            field_dict["max"] = max_
        if factor is not UNSET:
            field_dict["factor"] = factor
        if min_ is not UNSET:
            field_dict["min"] = min_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0040_qos_limits_factor import V0040QosLimitsFactor
        from ..models.v0040_qos_limits_max import V0040QosLimitsMax
        from ..models.v0040_qos_limits_min import V0040QosLimitsMin

        d = dict(src_dict)
        grace_time = d.pop("grace_time", UNSET)

        _max_ = d.pop("max", UNSET)
        max_: Union[Unset, V0040QosLimitsMax]
        if isinstance(_max_, Unset):
            max_ = UNSET
        else:
            max_ = V0040QosLimitsMax.from_dict(_max_)

        _factor = d.pop("factor", UNSET)
        factor: Union[Unset, V0040QosLimitsFactor]
        if isinstance(_factor, Unset):
            factor = UNSET
        else:
            factor = V0040QosLimitsFactor.from_dict(_factor)

        _min_ = d.pop("min", UNSET)
        min_: Union[Unset, V0040QosLimitsMin]
        if isinstance(_min_, Unset):
            min_ = UNSET
        else:
            min_ = V0040QosLimitsMin.from_dict(_min_)

        v0040_qos_limits = cls(
            grace_time=grace_time,
            max_=max_,
            factor=factor,
            min_=min_,
        )

        v0040_qos_limits.additional_properties = d
        return v0040_qos_limits

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
