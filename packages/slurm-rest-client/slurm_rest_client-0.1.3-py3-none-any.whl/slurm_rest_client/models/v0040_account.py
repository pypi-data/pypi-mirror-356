from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.v0040_account_flags_item import V0040AccountFlagsItem
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_account_associations import V0040AccountAssociations
    from ..models.v0040_account_coordinators import V0040AccountCoordinators


T = TypeVar("T", bound="V0040Account")


@_attrs_define
class V0040Account:
    """
    Attributes:
        description (str):
        name (str):
        organization (str):
        associations (Union[Unset, V0040AccountAssociations]):
        coordinators (Union[Unset, V0040AccountCoordinators]):
        flags (Union[Unset, list[V0040AccountFlagsItem]]):
    """

    description: str
    name: str
    organization: str
    associations: Union[Unset, "V0040AccountAssociations"] = UNSET
    coordinators: Union[Unset, "V0040AccountCoordinators"] = UNSET
    flags: Union[Unset, list[V0040AccountFlagsItem]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        description = self.description

        name = self.name

        organization = self.organization

        associations: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.associations, Unset):
            associations = self.associations.to_dict()

        coordinators: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.coordinators, Unset):
            coordinators = self.coordinators.to_dict()

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
        from ..models.v0040_account_associations import V0040AccountAssociations
        from ..models.v0040_account_coordinators import V0040AccountCoordinators

        d = dict(src_dict)
        description = d.pop("description")

        name = d.pop("name")

        organization = d.pop("organization")

        _associations = d.pop("associations", UNSET)
        associations: Union[Unset, V0040AccountAssociations]
        if isinstance(_associations, Unset):
            associations = UNSET
        else:
            associations = V0040AccountAssociations.from_dict(_associations)

        _coordinators = d.pop("coordinators", UNSET)
        coordinators: Union[Unset, V0040AccountCoordinators]
        if isinstance(_coordinators, Unset):
            coordinators = UNSET
        else:
            coordinators = V0040AccountCoordinators.from_dict(_coordinators)

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
