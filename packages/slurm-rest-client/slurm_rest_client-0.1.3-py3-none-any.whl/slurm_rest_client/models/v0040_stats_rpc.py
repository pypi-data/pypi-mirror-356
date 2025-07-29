from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_stats_rpc_time import V0040StatsRpcTime


T = TypeVar("T", bound="V0040StatsRpc")


@_attrs_define
class V0040StatsRpc:
    """
    Attributes:
        rpc (Union[Unset, str]):
        count (Union[Unset, int]):
        time (Union[Unset, V0040StatsRpcTime]):
    """

    rpc: Union[Unset, str] = UNSET
    count: Union[Unset, int] = UNSET
    time: Union[Unset, "V0040StatsRpcTime"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        rpc = self.rpc

        count = self.count

        time: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.time, Unset):
            time = self.time.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if rpc is not UNSET:
            field_dict["rpc"] = rpc
        if count is not UNSET:
            field_dict["count"] = count
        if time is not UNSET:
            field_dict["time"] = time

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0040_stats_rpc_time import V0040StatsRpcTime

        d = dict(src_dict)
        rpc = d.pop("rpc", UNSET)

        count = d.pop("count", UNSET)

        _time = d.pop("time", UNSET)
        time: Union[Unset, V0040StatsRpcTime]
        if isinstance(_time, Unset):
            time = UNSET
        else:
            time = V0040StatsRpcTime.from_dict(_time)

        v0040_stats_rpc = cls(
            rpc=rpc,
            count=count,
            time=time,
        )

        v0040_stats_rpc.additional_properties = d
        return v0040_stats_rpc

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
