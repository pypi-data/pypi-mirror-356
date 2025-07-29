from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="V0040AssocShort")


@_attrs_define
class V0040AssocShort:
    """
    Attributes:
        user (str): Assocation user (if assigned)
        account (Union[Unset, str]): Association account (if assigned)
        cluster (Union[Unset, str]): Association cluster (if assigned)
        partition (Union[Unset, str]): Association partition (if assigned)
        id (Union[Unset, int]): Numeric Association ID (if known)
    """

    user: str
    account: Union[Unset, str] = UNSET
    cluster: Union[Unset, str] = UNSET
    partition: Union[Unset, str] = UNSET
    id: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        user = self.user

        account = self.account

        cluster = self.cluster

        partition = self.partition

        id = self.id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "user": user,
            }
        )
        if account is not UNSET:
            field_dict["account"] = account
        if cluster is not UNSET:
            field_dict["cluster"] = cluster
        if partition is not UNSET:
            field_dict["partition"] = partition
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        user = d.pop("user")

        account = d.pop("account", UNSET)

        cluster = d.pop("cluster", UNSET)

        partition = d.pop("partition", UNSET)

        id = d.pop("id", UNSET)

        v0040_assoc_short = cls(
            user=user,
            account=account,
            cluster=cluster,
            partition=partition,
            id=id,
        )

        v0040_assoc_short.additional_properties = d
        return v0040_assoc_short

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
