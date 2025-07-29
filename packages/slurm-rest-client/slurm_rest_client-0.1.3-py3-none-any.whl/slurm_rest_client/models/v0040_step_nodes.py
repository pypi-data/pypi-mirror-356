from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_step_nodes_list import V0040StepNodesList


T = TypeVar("T", bound="V0040StepNodes")


@_attrs_define
class V0040StepNodes:
    """
    Attributes:
        count (Union[Unset, int]):
        range_ (Union[Unset, str]):
        list_ (Union[Unset, V0040StepNodesList]):
    """

    count: Union[Unset, int] = UNSET
    range_: Union[Unset, str] = UNSET
    list_: Union[Unset, "V0040StepNodesList"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        count = self.count

        range_ = self.range_

        list_: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.list_, Unset):
            list_ = self.list_.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if count is not UNSET:
            field_dict["count"] = count
        if range_ is not UNSET:
            field_dict["range"] = range_
        if list_ is not UNSET:
            field_dict["list"] = list_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0040_step_nodes_list import V0040StepNodesList

        d = dict(src_dict)
        count = d.pop("count", UNSET)

        range_ = d.pop("range", UNSET)

        _list_ = d.pop("list", UNSET)
        list_: Union[Unset, V0040StepNodesList]
        if isinstance(_list_, Unset):
            list_ = UNSET
        else:
            list_ = V0040StepNodesList.from_dict(_list_)

        v0040_step_nodes = cls(
            count=count,
            range_=range_,
            list_=list_,
        )

        v0040_step_nodes.additional_properties = d
        return v0040_step_nodes

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
