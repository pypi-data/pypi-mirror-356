from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="V0040StatsMsgRpcsByUserItem")


@_attrs_define
class V0040StatsMsgRpcsByUserItem:
    """user

    Attributes:
        user (Union[Unset, str]): user name
        user_id (Union[Unset, int]): user id (numeric)
        count (Union[Unset, int]): Number of RPCs received
        average_time (Union[Unset, int]): Average time spent processing RPC in seconds
        total_time (Union[Unset, int]): Total time spent processing RPC in seconds
    """

    user: Union[Unset, str] = UNSET
    user_id: Union[Unset, int] = UNSET
    count: Union[Unset, int] = UNSET
    average_time: Union[Unset, int] = UNSET
    total_time: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        user = self.user

        user_id = self.user_id

        count = self.count

        average_time = self.average_time

        total_time = self.total_time

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if user is not UNSET:
            field_dict["user"] = user
        if user_id is not UNSET:
            field_dict["user_id"] = user_id
        if count is not UNSET:
            field_dict["count"] = count
        if average_time is not UNSET:
            field_dict["average_time"] = average_time
        if total_time is not UNSET:
            field_dict["total_time"] = total_time

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        user = d.pop("user", UNSET)

        user_id = d.pop("user_id", UNSET)

        count = d.pop("count", UNSET)

        average_time = d.pop("average_time", UNSET)

        total_time = d.pop("total_time", UNSET)

        v0040_stats_msg_rpcs_by_user_item = cls(
            user=user,
            user_id=user_id,
            count=count,
            average_time=average_time,
            total_time=total_time,
        )

        v0040_stats_msg_rpcs_by_user_item.additional_properties = d
        return v0040_stats_msg_rpcs_by_user_item

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
