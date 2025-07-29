from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_stats_rec_rollups import V0040StatsRecRollups
    from ..models.v0040_stats_rec_rp_cs import V0040StatsRecRPCs
    from ..models.v0040_stats_rec_users import V0040StatsRecUsers


T = TypeVar("T", bound="V0040StatsRec")


@_attrs_define
class V0040StatsRec:
    """
    Attributes:
        time_start (Union[Unset, int]):
        rollups (Union[Unset, V0040StatsRecRollups]):
        rp_cs (Union[Unset, V0040StatsRecRPCs]):
        users (Union[Unset, V0040StatsRecUsers]):
    """

    time_start: Union[Unset, int] = UNSET
    rollups: Union[Unset, "V0040StatsRecRollups"] = UNSET
    rp_cs: Union[Unset, "V0040StatsRecRPCs"] = UNSET
    users: Union[Unset, "V0040StatsRecUsers"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        time_start = self.time_start

        rollups: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.rollups, Unset):
            rollups = self.rollups.to_dict()

        rp_cs: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.rp_cs, Unset):
            rp_cs = self.rp_cs.to_dict()

        users: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.users, Unset):
            users = self.users.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if time_start is not UNSET:
            field_dict["time_start"] = time_start
        if rollups is not UNSET:
            field_dict["rollups"] = rollups
        if rp_cs is not UNSET:
            field_dict["RPCs"] = rp_cs
        if users is not UNSET:
            field_dict["users"] = users

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0040_stats_rec_rollups import V0040StatsRecRollups
        from ..models.v0040_stats_rec_rp_cs import V0040StatsRecRPCs
        from ..models.v0040_stats_rec_users import V0040StatsRecUsers

        d = dict(src_dict)
        time_start = d.pop("time_start", UNSET)

        _rollups = d.pop("rollups", UNSET)
        rollups: Union[Unset, V0040StatsRecRollups]
        if isinstance(_rollups, Unset):
            rollups = UNSET
        else:
            rollups = V0040StatsRecRollups.from_dict(_rollups)

        _rp_cs = d.pop("RPCs", UNSET)
        rp_cs: Union[Unset, V0040StatsRecRPCs]
        if isinstance(_rp_cs, Unset):
            rp_cs = UNSET
        else:
            rp_cs = V0040StatsRecRPCs.from_dict(_rp_cs)

        _users = d.pop("users", UNSET)
        users: Union[Unset, V0040StatsRecUsers]
        if isinstance(_users, Unset):
            users = UNSET
        else:
            users = V0040StatsRecUsers.from_dict(_users)

        v0040_stats_rec = cls(
            time_start=time_start,
            rollups=rollups,
            rp_cs=rp_cs,
            users=users,
        )

        v0040_stats_rec.additional_properties = d
        return v0040_stats_rec

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
