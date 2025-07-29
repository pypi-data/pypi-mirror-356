from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.v0040_rollup_stats_item_type import V0040RollupStatsItemType
from ..types import UNSET, Unset

T = TypeVar("T", bound="V0040RollupStatsItem")


@_attrs_define
class V0040RollupStatsItem:
    """recorded rollup statistics

    Attributes:
        type_ (Union[Unset, V0040RollupStatsItemType]): type
        last_run (Union[Unset, int]): Last time rollup ran (UNIX timestamp)
        max_cycle (Union[Unset, int]): longest rollup time (seconds)
        total_time (Union[Unset, int]): total time spent doing rollups (seconds)
        total_cycles (Union[Unset, int]): number of rollups since last_run
        mean_cycles (Union[Unset, int]): average time for rollup (seconds)
    """

    type_: Union[Unset, V0040RollupStatsItemType] = UNSET
    last_run: Union[Unset, int] = UNSET
    max_cycle: Union[Unset, int] = UNSET
    total_time: Union[Unset, int] = UNSET
    total_cycles: Union[Unset, int] = UNSET
    mean_cycles: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_: Union[Unset, str] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        last_run = self.last_run

        max_cycle = self.max_cycle

        total_time = self.total_time

        total_cycles = self.total_cycles

        mean_cycles = self.mean_cycles

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type_ is not UNSET:
            field_dict["type"] = type_
        if last_run is not UNSET:
            field_dict["last run"] = last_run
        if max_cycle is not UNSET:
            field_dict["max_cycle"] = max_cycle
        if total_time is not UNSET:
            field_dict["total_time"] = total_time
        if total_cycles is not UNSET:
            field_dict["total_cycles"] = total_cycles
        if mean_cycles is not UNSET:
            field_dict["mean_cycles"] = mean_cycles

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _type_ = d.pop("type", UNSET)
        type_: Union[Unset, V0040RollupStatsItemType]
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = V0040RollupStatsItemType(_type_)

        last_run = d.pop("last run", UNSET)

        max_cycle = d.pop("max_cycle", UNSET)

        total_time = d.pop("total_time", UNSET)

        total_cycles = d.pop("total_cycles", UNSET)

        mean_cycles = d.pop("mean_cycles", UNSET)

        v0040_rollup_stats_item = cls(
            type_=type_,
            last_run=last_run,
            max_cycle=max_cycle,
            total_time=total_time,
            total_cycles=total_cycles,
            mean_cycles=mean_cycles,
        )

        v0040_rollup_stats_item.additional_properties = d
        return v0040_rollup_stats_item

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
