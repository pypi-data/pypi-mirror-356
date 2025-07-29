from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_step_tres_consumed_average import V0040StepTresConsumedAverage
    from ..models.v0040_step_tres_consumed_max import V0040StepTresConsumedMax
    from ..models.v0040_step_tres_consumed_min import V0040StepTresConsumedMin
    from ..models.v0040_step_tres_consumed_total import V0040StepTresConsumedTotal


T = TypeVar("T", bound="V0040StepTresConsumed")


@_attrs_define
class V0040StepTresConsumed:
    """
    Attributes:
        max_ (Union[Unset, V0040StepTresConsumedMax]):
        min_ (Union[Unset, V0040StepTresConsumedMin]):
        average (Union[Unset, V0040StepTresConsumedAverage]):
        total (Union[Unset, V0040StepTresConsumedTotal]):
    """

    max_: Union[Unset, "V0040StepTresConsumedMax"] = UNSET
    min_: Union[Unset, "V0040StepTresConsumedMin"] = UNSET
    average: Union[Unset, "V0040StepTresConsumedAverage"] = UNSET
    total: Union[Unset, "V0040StepTresConsumedTotal"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        max_: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.max_, Unset):
            max_ = self.max_.to_dict()

        min_: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.min_, Unset):
            min_ = self.min_.to_dict()

        average: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.average, Unset):
            average = self.average.to_dict()

        total: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.total, Unset):
            total = self.total.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if max_ is not UNSET:
            field_dict["max"] = max_
        if min_ is not UNSET:
            field_dict["min"] = min_
        if average is not UNSET:
            field_dict["average"] = average
        if total is not UNSET:
            field_dict["total"] = total

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0040_step_tres_consumed_average import V0040StepTresConsumedAverage
        from ..models.v0040_step_tres_consumed_max import V0040StepTresConsumedMax
        from ..models.v0040_step_tres_consumed_min import V0040StepTresConsumedMin
        from ..models.v0040_step_tres_consumed_total import V0040StepTresConsumedTotal

        d = dict(src_dict)
        _max_ = d.pop("max", UNSET)
        max_: Union[Unset, V0040StepTresConsumedMax]
        if isinstance(_max_, Unset):
            max_ = UNSET
        else:
            max_ = V0040StepTresConsumedMax.from_dict(_max_)

        _min_ = d.pop("min", UNSET)
        min_: Union[Unset, V0040StepTresConsumedMin]
        if isinstance(_min_, Unset):
            min_ = UNSET
        else:
            min_ = V0040StepTresConsumedMin.from_dict(_min_)

        _average = d.pop("average", UNSET)
        average: Union[Unset, V0040StepTresConsumedAverage]
        if isinstance(_average, Unset):
            average = UNSET
        else:
            average = V0040StepTresConsumedAverage.from_dict(_average)

        _total = d.pop("total", UNSET)
        total: Union[Unset, V0040StepTresConsumedTotal]
        if isinstance(_total, Unset):
            total = UNSET
        else:
            total = V0040StepTresConsumedTotal.from_dict(_total)

        v0040_step_tres_consumed = cls(
            max_=max_,
            min_=min_,
            average=average,
            total=total,
        )

        v0040_step_tres_consumed.additional_properties = d
        return v0040_step_tres_consumed

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
