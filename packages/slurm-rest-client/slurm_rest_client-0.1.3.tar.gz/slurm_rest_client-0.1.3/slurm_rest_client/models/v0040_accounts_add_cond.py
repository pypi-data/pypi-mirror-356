from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_accounts_add_cond_accounts import V0040AccountsAddCondAccounts
    from ..models.v0040_accounts_add_cond_association import V0040AccountsAddCondAssociation
    from ..models.v0040_accounts_add_cond_clusters import V0040AccountsAddCondClusters


T = TypeVar("T", bound="V0040AccountsAddCond")


@_attrs_define
class V0040AccountsAddCond:
    """
    Attributes:
        accounts (V0040AccountsAddCondAccounts):
        association (Union[Unset, V0040AccountsAddCondAssociation]):
        clusters (Union[Unset, V0040AccountsAddCondClusters]):
    """

    accounts: "V0040AccountsAddCondAccounts"
    association: Union[Unset, "V0040AccountsAddCondAssociation"] = UNSET
    clusters: Union[Unset, "V0040AccountsAddCondClusters"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        accounts = self.accounts.to_dict()

        association: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.association, Unset):
            association = self.association.to_dict()

        clusters: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.clusters, Unset):
            clusters = self.clusters.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "accounts": accounts,
            }
        )
        if association is not UNSET:
            field_dict["association"] = association
        if clusters is not UNSET:
            field_dict["clusters"] = clusters

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0040_accounts_add_cond_accounts import V0040AccountsAddCondAccounts
        from ..models.v0040_accounts_add_cond_association import V0040AccountsAddCondAssociation
        from ..models.v0040_accounts_add_cond_clusters import V0040AccountsAddCondClusters

        d = dict(src_dict)
        accounts = V0040AccountsAddCondAccounts.from_dict(d.pop("accounts"))

        _association = d.pop("association", UNSET)
        association: Union[Unset, V0040AccountsAddCondAssociation]
        if isinstance(_association, Unset):
            association = UNSET
        else:
            association = V0040AccountsAddCondAssociation.from_dict(_association)

        _clusters = d.pop("clusters", UNSET)
        clusters: Union[Unset, V0040AccountsAddCondClusters]
        if isinstance(_clusters, Unset):
            clusters = UNSET
        else:
            clusters = V0040AccountsAddCondClusters.from_dict(_clusters)

        v0040_accounts_add_cond = cls(
            accounts=accounts,
            association=association,
            clusters=clusters,
        )

        v0040_accounts_add_cond.additional_properties = d
        return v0040_accounts_add_cond

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
