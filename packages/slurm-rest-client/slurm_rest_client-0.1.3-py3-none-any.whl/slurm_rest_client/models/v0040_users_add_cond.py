from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_users_add_cond_accounts import V0040UsersAddCondAccounts
    from ..models.v0040_users_add_cond_association import V0040UsersAddCondAssociation
    from ..models.v0040_users_add_cond_clusters import V0040UsersAddCondClusters
    from ..models.v0040_users_add_cond_partitions import V0040UsersAddCondPartitions
    from ..models.v0040_users_add_cond_users import V0040UsersAddCondUsers
    from ..models.v0040_users_add_cond_wckeys import V0040UsersAddCondWckeys


T = TypeVar("T", bound="V0040UsersAddCond")


@_attrs_define
class V0040UsersAddCond:
    """
    Attributes:
        users (V0040UsersAddCondUsers):
        accounts (Union[Unset, V0040UsersAddCondAccounts]):
        association (Union[Unset, V0040UsersAddCondAssociation]):
        clusters (Union[Unset, V0040UsersAddCondClusters]):
        partitions (Union[Unset, V0040UsersAddCondPartitions]):
        wckeys (Union[Unset, V0040UsersAddCondWckeys]):
    """

    users: "V0040UsersAddCondUsers"
    accounts: Union[Unset, "V0040UsersAddCondAccounts"] = UNSET
    association: Union[Unset, "V0040UsersAddCondAssociation"] = UNSET
    clusters: Union[Unset, "V0040UsersAddCondClusters"] = UNSET
    partitions: Union[Unset, "V0040UsersAddCondPartitions"] = UNSET
    wckeys: Union[Unset, "V0040UsersAddCondWckeys"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        users = self.users.to_dict()

        accounts: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.accounts, Unset):
            accounts = self.accounts.to_dict()

        association: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.association, Unset):
            association = self.association.to_dict()

        clusters: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.clusters, Unset):
            clusters = self.clusters.to_dict()

        partitions: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.partitions, Unset):
            partitions = self.partitions.to_dict()

        wckeys: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.wckeys, Unset):
            wckeys = self.wckeys.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "users": users,
            }
        )
        if accounts is not UNSET:
            field_dict["accounts"] = accounts
        if association is not UNSET:
            field_dict["association"] = association
        if clusters is not UNSET:
            field_dict["clusters"] = clusters
        if partitions is not UNSET:
            field_dict["partitions"] = partitions
        if wckeys is not UNSET:
            field_dict["wckeys"] = wckeys

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0040_users_add_cond_accounts import V0040UsersAddCondAccounts
        from ..models.v0040_users_add_cond_association import V0040UsersAddCondAssociation
        from ..models.v0040_users_add_cond_clusters import V0040UsersAddCondClusters
        from ..models.v0040_users_add_cond_partitions import V0040UsersAddCondPartitions
        from ..models.v0040_users_add_cond_users import V0040UsersAddCondUsers
        from ..models.v0040_users_add_cond_wckeys import V0040UsersAddCondWckeys

        d = dict(src_dict)
        users = V0040UsersAddCondUsers.from_dict(d.pop("users"))

        _accounts = d.pop("accounts", UNSET)
        accounts: Union[Unset, V0040UsersAddCondAccounts]
        if isinstance(_accounts, Unset):
            accounts = UNSET
        else:
            accounts = V0040UsersAddCondAccounts.from_dict(_accounts)

        _association = d.pop("association", UNSET)
        association: Union[Unset, V0040UsersAddCondAssociation]
        if isinstance(_association, Unset):
            association = UNSET
        else:
            association = V0040UsersAddCondAssociation.from_dict(_association)

        _clusters = d.pop("clusters", UNSET)
        clusters: Union[Unset, V0040UsersAddCondClusters]
        if isinstance(_clusters, Unset):
            clusters = UNSET
        else:
            clusters = V0040UsersAddCondClusters.from_dict(_clusters)

        _partitions = d.pop("partitions", UNSET)
        partitions: Union[Unset, V0040UsersAddCondPartitions]
        if isinstance(_partitions, Unset):
            partitions = UNSET
        else:
            partitions = V0040UsersAddCondPartitions.from_dict(_partitions)

        _wckeys = d.pop("wckeys", UNSET)
        wckeys: Union[Unset, V0040UsersAddCondWckeys]
        if isinstance(_wckeys, Unset):
            wckeys = UNSET
        else:
            wckeys = V0040UsersAddCondWckeys.from_dict(_wckeys)

        v0040_users_add_cond = cls(
            users=users,
            accounts=accounts,
            association=association,
            clusters=clusters,
            partitions=partitions,
            wckeys=wckeys,
        )

        v0040_users_add_cond.additional_properties = d
        return v0040_users_add_cond

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
