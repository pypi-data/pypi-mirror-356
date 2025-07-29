from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.v0040_qos_preempt_mode_item import V0040QosPreemptModeItem
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_qos_preempt_exempt_time import V0040QosPreemptExemptTime
    from ..models.v0040_qos_preempt_list import V0040QosPreemptList


T = TypeVar("T", bound="V0040QosPreempt")


@_attrs_define
class V0040QosPreempt:
    """
    Attributes:
        list_ (Union[Unset, V0040QosPreemptList]):
        mode (Union[Unset, list[V0040QosPreemptModeItem]]):
        exempt_time (Union[Unset, V0040QosPreemptExemptTime]):
    """

    list_: Union[Unset, "V0040QosPreemptList"] = UNSET
    mode: Union[Unset, list[V0040QosPreemptModeItem]] = UNSET
    exempt_time: Union[Unset, "V0040QosPreemptExemptTime"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        list_: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.list_, Unset):
            list_ = self.list_.to_dict()

        mode: Union[Unset, list[str]] = UNSET
        if not isinstance(self.mode, Unset):
            mode = []
            for mode_item_data in self.mode:
                mode_item = mode_item_data.value
                mode.append(mode_item)

        exempt_time: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.exempt_time, Unset):
            exempt_time = self.exempt_time.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if list_ is not UNSET:
            field_dict["list"] = list_
        if mode is not UNSET:
            field_dict["mode"] = mode
        if exempt_time is not UNSET:
            field_dict["exempt_time"] = exempt_time

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0040_qos_preempt_exempt_time import V0040QosPreemptExemptTime
        from ..models.v0040_qos_preempt_list import V0040QosPreemptList

        d = dict(src_dict)
        _list_ = d.pop("list", UNSET)
        list_: Union[Unset, V0040QosPreemptList]
        if isinstance(_list_, Unset):
            list_ = UNSET
        else:
            list_ = V0040QosPreemptList.from_dict(_list_)

        mode = []
        _mode = d.pop("mode", UNSET)
        for mode_item_data in _mode or []:
            mode_item = V0040QosPreemptModeItem(mode_item_data)

            mode.append(mode_item)

        _exempt_time = d.pop("exempt_time", UNSET)
        exempt_time: Union[Unset, V0040QosPreemptExemptTime]
        if isinstance(_exempt_time, Unset):
            exempt_time = UNSET
        else:
            exempt_time = V0040QosPreemptExemptTime.from_dict(_exempt_time)

        v0040_qos_preempt = cls(
            list_=list_,
            mode=mode,
            exempt_time=exempt_time,
        )

        v0040_qos_preempt.additional_properties = d
        return v0040_qos_preempt

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
