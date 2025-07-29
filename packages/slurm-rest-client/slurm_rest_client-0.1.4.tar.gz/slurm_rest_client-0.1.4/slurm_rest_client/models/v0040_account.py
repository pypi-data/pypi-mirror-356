from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.v0040_account_flags_item import V0040AccountFlagsItem
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_assoc_short import V0040AssocShort
    from ..models.v0040_coord import V0040Coord


T = TypeVar("T", bound="V0040Account")


@_attrs_define
class V0040Account:
    """
    Attributes:
        description (str):
        name (str):
        organization (str):
        associations (Union[Unset, list['V0040AssocShort']]):
        coordinators (Union[Unset, list['V0040Coord']]):
        flags (Union[Unset, list[V0040AccountFlagsItem]]):
    """

    description: str
    name: str
    organization: str
    associations: Union[Unset, list["V0040AssocShort"]] = UNSET
    coordinators: Union[Unset, list["V0040Coord"]] = UNSET
    flags: Union[Unset, list[V0040AccountFlagsItem]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        description = self.description

        name = self.name

        organization = self.organization

        associations: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.associations, Unset):
            associations = []
            for componentsschemasv0_0_40_assoc_short_list_item_data in self.associations:
                componentsschemasv0_0_40_assoc_short_list_item = (
                    componentsschemasv0_0_40_assoc_short_list_item_data.to_dict()
                )
                associations.append(componentsschemasv0_0_40_assoc_short_list_item)

        coordinators: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.coordinators, Unset):
            coordinators = []
            for componentsschemasv0_0_40_coord_list_item_data in self.coordinators:
                componentsschemasv0_0_40_coord_list_item = componentsschemasv0_0_40_coord_list_item_data.to_dict()
                coordinators.append(componentsschemasv0_0_40_coord_list_item)

        flags: Union[Unset, list[str]] = UNSET
        if not isinstance(self.flags, Unset):
            flags = []
            for flags_item_data in self.flags:
                flags_item = flags_item_data.value
                flags.append(flags_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "description": description,
                "name": name,
                "organization": organization,
            }
        )
        if associations is not UNSET:
            field_dict["associations"] = associations
        if coordinators is not UNSET:
            field_dict["coordinators"] = coordinators
        if flags is not UNSET:
            field_dict["flags"] = flags

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0040_assoc_short import V0040AssocShort
        from ..models.v0040_coord import V0040Coord

        d = dict(src_dict)
        description = d.pop("description")

        name = d.pop("name")

        organization = d.pop("organization")

        associations = []
        _associations = d.pop("associations", UNSET)
        for componentsschemasv0_0_40_assoc_short_list_item_data in _associations or []:
            componentsschemasv0_0_40_assoc_short_list_item = V0040AssocShort.from_dict(
                componentsschemasv0_0_40_assoc_short_list_item_data
            )

            associations.append(componentsschemasv0_0_40_assoc_short_list_item)

        coordinators = []
        _coordinators = d.pop("coordinators", UNSET)
        for componentsschemasv0_0_40_coord_list_item_data in _coordinators or []:
            componentsschemasv0_0_40_coord_list_item = V0040Coord.from_dict(
                componentsschemasv0_0_40_coord_list_item_data
            )

            coordinators.append(componentsschemasv0_0_40_coord_list_item)

        flags = []
        _flags = d.pop("flags", UNSET)
        for flags_item_data in _flags or []:
            flags_item = V0040AccountFlagsItem(flags_item_data)

            flags.append(flags_item)

        v0040_account = cls(
            description=description,
            name=name,
            organization=organization,
            associations=associations,
            coordinators=coordinators,
            flags=flags,
        )

        v0040_account.additional_properties = d
        return v0040_account

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
