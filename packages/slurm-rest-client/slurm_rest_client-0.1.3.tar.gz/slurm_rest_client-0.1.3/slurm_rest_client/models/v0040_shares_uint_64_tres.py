from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_shares_uint_64_tres_value import V0040SharesUint64TresValue


T = TypeVar("T", bound="V0040SharesUint64Tres")


@_attrs_define
class V0040SharesUint64Tres:
    """
    Attributes:
        name (Union[Unset, str]): TRES name
        value (Union[Unset, V0040SharesUint64TresValue]):
    """

    name: Union[Unset, str] = UNSET
    value: Union[Unset, "V0040SharesUint64TresValue"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        value: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.value, Unset):
            value = self.value.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0040_shares_uint_64_tres_value import V0040SharesUint64TresValue

        d = dict(src_dict)
        name = d.pop("name", UNSET)

        _value = d.pop("value", UNSET)
        value: Union[Unset, V0040SharesUint64TresValue]
        if isinstance(_value, Unset):
            value = UNSET
        else:
            value = V0040SharesUint64TresValue.from_dict(_value)

        v0040_shares_uint_64_tres = cls(
            name=name,
            value=value,
        )

        v0040_shares_uint_64_tres.additional_properties = d
        return v0040_shares_uint_64_tres

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
