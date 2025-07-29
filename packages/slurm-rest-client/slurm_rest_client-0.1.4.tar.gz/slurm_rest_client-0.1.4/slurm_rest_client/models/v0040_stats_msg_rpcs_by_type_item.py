from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="V0040StatsMsgRpcsByTypeItem")


@_attrs_define
class V0040StatsMsgRpcsByTypeItem:
    """RPC

    Attributes:
        message_type (Union[Unset, str]): Message type as string
        type_id (Union[Unset, int]): Message type as integer
        count (Union[Unset, int]): Number of RPCs received
        average_time (Union[Unset, int]): Average time spent processing RPC in seconds
        total_time (Union[Unset, int]): Total time spent processing RPC in seconds
    """

    message_type: Union[Unset, str] = UNSET
    type_id: Union[Unset, int] = UNSET
    count: Union[Unset, int] = UNSET
    average_time: Union[Unset, int] = UNSET
    total_time: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        message_type = self.message_type

        type_id = self.type_id

        count = self.count

        average_time = self.average_time

        total_time = self.total_time

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if message_type is not UNSET:
            field_dict["message_type"] = message_type
        if type_id is not UNSET:
            field_dict["type_id"] = type_id
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
        message_type = d.pop("message_type", UNSET)

        type_id = d.pop("type_id", UNSET)

        count = d.pop("count", UNSET)

        average_time = d.pop("average_time", UNSET)

        total_time = d.pop("total_time", UNSET)

        v0040_stats_msg_rpcs_by_type_item = cls(
            message_type=message_type,
            type_id=type_id,
            count=count,
            average_time=average_time,
            total_time=total_time,
        )

        v0040_stats_msg_rpcs_by_type_item.additional_properties = d
        return v0040_stats_msg_rpcs_by_type_item

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
