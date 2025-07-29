from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.v0040_assoc_flags_item import V0040AssocFlagsItem
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_assoc_accounting import V0040AssocAccounting
    from ..models.v0040_assoc_default import V0040AssocDefault
    from ..models.v0040_assoc_id import V0040AssocId
    from ..models.v0040_assoc_max import V0040AssocMax
    from ..models.v0040_assoc_min import V0040AssocMin
    from ..models.v0040_assoc_priority import V0040AssocPriority
    from ..models.v0040_assoc_qos import V0040AssocQos


T = TypeVar("T", bound="V0040Assoc")


@_attrs_define
class V0040Assoc:
    """
    Attributes:
        user (str):
        accounting (Union[Unset, V0040AssocAccounting]):
        account (Union[Unset, str]):
        cluster (Union[Unset, str]):
        comment (Union[Unset, str]): comment for the association
        default (Union[Unset, V0040AssocDefault]):
        flags (Union[Unset, list[V0040AssocFlagsItem]]):
        max_ (Union[Unset, V0040AssocMax]):
        id (Union[Unset, V0040AssocId]):
        is_default (Union[Unset, bool]):
        lineage (Union[Unset, str]): Complete path up the hierarchy to the root association
        min_ (Union[Unset, V0040AssocMin]):
        parent_account (Union[Unset, str]):
        partition (Union[Unset, str]):
        priority (Union[Unset, V0040AssocPriority]):
        qos (Union[Unset, V0040AssocQos]):
        shares_raw (Union[Unset, int]):
    """

    user: str
    accounting: Union[Unset, "V0040AssocAccounting"] = UNSET
    account: Union[Unset, str] = UNSET
    cluster: Union[Unset, str] = UNSET
    comment: Union[Unset, str] = UNSET
    default: Union[Unset, "V0040AssocDefault"] = UNSET
    flags: Union[Unset, list[V0040AssocFlagsItem]] = UNSET
    max_: Union[Unset, "V0040AssocMax"] = UNSET
    id: Union[Unset, "V0040AssocId"] = UNSET
    is_default: Union[Unset, bool] = UNSET
    lineage: Union[Unset, str] = UNSET
    min_: Union[Unset, "V0040AssocMin"] = UNSET
    parent_account: Union[Unset, str] = UNSET
    partition: Union[Unset, str] = UNSET
    priority: Union[Unset, "V0040AssocPriority"] = UNSET
    qos: Union[Unset, "V0040AssocQos"] = UNSET
    shares_raw: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        user = self.user

        accounting: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.accounting, Unset):
            accounting = self.accounting.to_dict()

        account = self.account

        cluster = self.cluster

        comment = self.comment

        default: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.default, Unset):
            default = self.default.to_dict()

        flags: Union[Unset, list[str]] = UNSET
        if not isinstance(self.flags, Unset):
            flags = []
            for flags_item_data in self.flags:
                flags_item = flags_item_data.value
                flags.append(flags_item)

        max_: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.max_, Unset):
            max_ = self.max_.to_dict()

        id: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.id, Unset):
            id = self.id.to_dict()

        is_default = self.is_default

        lineage = self.lineage

        min_: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.min_, Unset):
            min_ = self.min_.to_dict()

        parent_account = self.parent_account

        partition = self.partition

        priority: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.priority, Unset):
            priority = self.priority.to_dict()

        qos: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.qos, Unset):
            qos = self.qos.to_dict()

        shares_raw = self.shares_raw

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "user": user,
            }
        )
        if accounting is not UNSET:
            field_dict["accounting"] = accounting
        if account is not UNSET:
            field_dict["account"] = account
        if cluster is not UNSET:
            field_dict["cluster"] = cluster
        if comment is not UNSET:
            field_dict["comment"] = comment
        if default is not UNSET:
            field_dict["default"] = default
        if flags is not UNSET:
            field_dict["flags"] = flags
        if max_ is not UNSET:
            field_dict["max"] = max_
        if id is not UNSET:
            field_dict["id"] = id
        if is_default is not UNSET:
            field_dict["is_default"] = is_default
        if lineage is not UNSET:
            field_dict["lineage"] = lineage
        if min_ is not UNSET:
            field_dict["min"] = min_
        if parent_account is not UNSET:
            field_dict["parent_account"] = parent_account
        if partition is not UNSET:
            field_dict["partition"] = partition
        if priority is not UNSET:
            field_dict["priority"] = priority
        if qos is not UNSET:
            field_dict["qos"] = qos
        if shares_raw is not UNSET:
            field_dict["shares_raw"] = shares_raw

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0040_assoc_accounting import V0040AssocAccounting
        from ..models.v0040_assoc_default import V0040AssocDefault
        from ..models.v0040_assoc_id import V0040AssocId
        from ..models.v0040_assoc_max import V0040AssocMax
        from ..models.v0040_assoc_min import V0040AssocMin
        from ..models.v0040_assoc_priority import V0040AssocPriority
        from ..models.v0040_assoc_qos import V0040AssocQos

        d = dict(src_dict)
        user = d.pop("user")

        _accounting = d.pop("accounting", UNSET)
        accounting: Union[Unset, V0040AssocAccounting]
        if isinstance(_accounting, Unset):
            accounting = UNSET
        else:
            accounting = V0040AssocAccounting.from_dict(_accounting)

        account = d.pop("account", UNSET)

        cluster = d.pop("cluster", UNSET)

        comment = d.pop("comment", UNSET)

        _default = d.pop("default", UNSET)
        default: Union[Unset, V0040AssocDefault]
        if isinstance(_default, Unset):
            default = UNSET
        else:
            default = V0040AssocDefault.from_dict(_default)

        flags = []
        _flags = d.pop("flags", UNSET)
        for flags_item_data in _flags or []:
            flags_item = V0040AssocFlagsItem(flags_item_data)

            flags.append(flags_item)

        _max_ = d.pop("max", UNSET)
        max_: Union[Unset, V0040AssocMax]
        if isinstance(_max_, Unset):
            max_ = UNSET
        else:
            max_ = V0040AssocMax.from_dict(_max_)

        _id = d.pop("id", UNSET)
        id: Union[Unset, V0040AssocId]
        if isinstance(_id, Unset):
            id = UNSET
        else:
            id = V0040AssocId.from_dict(_id)

        is_default = d.pop("is_default", UNSET)

        lineage = d.pop("lineage", UNSET)

        _min_ = d.pop("min", UNSET)
        min_: Union[Unset, V0040AssocMin]
        if isinstance(_min_, Unset):
            min_ = UNSET
        else:
            min_ = V0040AssocMin.from_dict(_min_)

        parent_account = d.pop("parent_account", UNSET)

        partition = d.pop("partition", UNSET)

        _priority = d.pop("priority", UNSET)
        priority: Union[Unset, V0040AssocPriority]
        if isinstance(_priority, Unset):
            priority = UNSET
        else:
            priority = V0040AssocPriority.from_dict(_priority)

        _qos = d.pop("qos", UNSET)
        qos: Union[Unset, V0040AssocQos]
        if isinstance(_qos, Unset):
            qos = UNSET
        else:
            qos = V0040AssocQos.from_dict(_qos)

        shares_raw = d.pop("shares_raw", UNSET)

        v0040_assoc = cls(
            user=user,
            accounting=accounting,
            account=account,
            cluster=cluster,
            comment=comment,
            default=default,
            flags=flags,
            max_=max_,
            id=id,
            is_default=is_default,
            lineage=lineage,
            min_=min_,
            parent_account=parent_account,
            partition=partition,
            priority=priority,
            qos=qos,
            shares_raw=shares_raw,
        )

        v0040_assoc.additional_properties = d
        return v0040_assoc

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
