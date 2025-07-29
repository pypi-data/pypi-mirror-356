from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.v0040_user_administrator_level_item import V0040UserAdministratorLevelItem
from ..models.v0040_user_flags_item import V0040UserFlagsItem
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_user_associations import V0040UserAssociations
    from ..models.v0040_user_coordinators import V0040UserCoordinators
    from ..models.v0040_user_default import V0040UserDefault
    from ..models.v0040_user_wckeys import V0040UserWckeys


T = TypeVar("T", bound="V0040User")


@_attrs_define
class V0040User:
    """
    Attributes:
        name (str):
        administrator_level (Union[Unset, list[V0040UserAdministratorLevelItem]]):
        associations (Union[Unset, V0040UserAssociations]):
        coordinators (Union[Unset, V0040UserCoordinators]):
        default (Union[Unset, V0040UserDefault]):
        flags (Union[Unset, list[V0040UserFlagsItem]]):
        old_name (Union[Unset, str]):
        wckeys (Union[Unset, V0040UserWckeys]):
    """

    name: str
    administrator_level: Union[Unset, list[V0040UserAdministratorLevelItem]] = UNSET
    associations: Union[Unset, "V0040UserAssociations"] = UNSET
    coordinators: Union[Unset, "V0040UserCoordinators"] = UNSET
    default: Union[Unset, "V0040UserDefault"] = UNSET
    flags: Union[Unset, list[V0040UserFlagsItem]] = UNSET
    old_name: Union[Unset, str] = UNSET
    wckeys: Union[Unset, "V0040UserWckeys"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        administrator_level: Union[Unset, list[str]] = UNSET
        if not isinstance(self.administrator_level, Unset):
            administrator_level = []
            for administrator_level_item_data in self.administrator_level:
                administrator_level_item = administrator_level_item_data.value
                administrator_level.append(administrator_level_item)

        associations: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.associations, Unset):
            associations = self.associations.to_dict()

        coordinators: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.coordinators, Unset):
            coordinators = self.coordinators.to_dict()

        default: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.default, Unset):
            default = self.default.to_dict()

        flags: Union[Unset, list[str]] = UNSET
        if not isinstance(self.flags, Unset):
            flags = []
            for flags_item_data in self.flags:
                flags_item = flags_item_data.value
                flags.append(flags_item)

        old_name = self.old_name

        wckeys: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.wckeys, Unset):
            wckeys = self.wckeys.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if administrator_level is not UNSET:
            field_dict["administrator_level"] = administrator_level
        if associations is not UNSET:
            field_dict["associations"] = associations
        if coordinators is not UNSET:
            field_dict["coordinators"] = coordinators
        if default is not UNSET:
            field_dict["default"] = default
        if flags is not UNSET:
            field_dict["flags"] = flags
        if old_name is not UNSET:
            field_dict["old_name"] = old_name
        if wckeys is not UNSET:
            field_dict["wckeys"] = wckeys

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0040_user_associations import V0040UserAssociations
        from ..models.v0040_user_coordinators import V0040UserCoordinators
        from ..models.v0040_user_default import V0040UserDefault
        from ..models.v0040_user_wckeys import V0040UserWckeys

        d = dict(src_dict)
        name = d.pop("name")

        administrator_level = []
        _administrator_level = d.pop("administrator_level", UNSET)
        for administrator_level_item_data in _administrator_level or []:
            administrator_level_item = V0040UserAdministratorLevelItem(administrator_level_item_data)

            administrator_level.append(administrator_level_item)

        _associations = d.pop("associations", UNSET)
        associations: Union[Unset, V0040UserAssociations]
        if isinstance(_associations, Unset):
            associations = UNSET
        else:
            associations = V0040UserAssociations.from_dict(_associations)

        _coordinators = d.pop("coordinators", UNSET)
        coordinators: Union[Unset, V0040UserCoordinators]
        if isinstance(_coordinators, Unset):
            coordinators = UNSET
        else:
            coordinators = V0040UserCoordinators.from_dict(_coordinators)

        _default = d.pop("default", UNSET)
        default: Union[Unset, V0040UserDefault]
        if isinstance(_default, Unset):
            default = UNSET
        else:
            default = V0040UserDefault.from_dict(_default)

        flags = []
        _flags = d.pop("flags", UNSET)
        for flags_item_data in _flags or []:
            flags_item = V0040UserFlagsItem(flags_item_data)

            flags.append(flags_item)

        old_name = d.pop("old_name", UNSET)

        _wckeys = d.pop("wckeys", UNSET)
        wckeys: Union[Unset, V0040UserWckeys]
        if isinstance(_wckeys, Unset):
            wckeys = UNSET
        else:
            wckeys = V0040UserWckeys.from_dict(_wckeys)

        v0040_user = cls(
            name=name,
            administrator_level=administrator_level,
            associations=associations,
            coordinators=coordinators,
            default=default,
            flags=flags,
            old_name=old_name,
            wckeys=wckeys,
        )

        v0040_user.additional_properties = d
        return v0040_user

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
