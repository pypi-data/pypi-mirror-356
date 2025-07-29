from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_assoc_max_tres_group_active import V0040AssocMaxTresGroupActive
    from ..models.v0040_assoc_max_tres_group_minutes import V0040AssocMaxTresGroupMinutes


T = TypeVar("T", bound="V0040AssocMaxTresGroup")


@_attrs_define
class V0040AssocMaxTresGroup:
    """
    Attributes:
        minutes (Union[Unset, V0040AssocMaxTresGroupMinutes]):
        active (Union[Unset, V0040AssocMaxTresGroupActive]):
    """

    minutes: Union[Unset, "V0040AssocMaxTresGroupMinutes"] = UNSET
    active: Union[Unset, "V0040AssocMaxTresGroupActive"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        minutes: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.minutes, Unset):
            minutes = self.minutes.to_dict()

        active: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.active, Unset):
            active = self.active.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if minutes is not UNSET:
            field_dict["minutes"] = minutes
        if active is not UNSET:
            field_dict["active"] = active

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0040_assoc_max_tres_group_active import V0040AssocMaxTresGroupActive
        from ..models.v0040_assoc_max_tres_group_minutes import V0040AssocMaxTresGroupMinutes

        d = dict(src_dict)
        _minutes = d.pop("minutes", UNSET)
        minutes: Union[Unset, V0040AssocMaxTresGroupMinutes]
        if isinstance(_minutes, Unset):
            minutes = UNSET
        else:
            minutes = V0040AssocMaxTresGroupMinutes.from_dict(_minutes)

        _active = d.pop("active", UNSET)
        active: Union[Unset, V0040AssocMaxTresGroupActive]
        if isinstance(_active, Unset):
            active = UNSET
        else:
            active = V0040AssocMaxTresGroupActive.from_dict(_active)

        v0040_assoc_max_tres_group = cls(
            minutes=minutes,
            active=active,
        )

        v0040_assoc_max_tres_group.additional_properties = d
        return v0040_assoc_max_tres_group

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
