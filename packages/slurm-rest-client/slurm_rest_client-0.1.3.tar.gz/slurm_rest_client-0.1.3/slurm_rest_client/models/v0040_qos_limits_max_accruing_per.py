from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_qos_limits_max_accruing_per_account import V0040QosLimitsMaxAccruingPerAccount
    from ..models.v0040_qos_limits_max_accruing_per_user import V0040QosLimitsMaxAccruingPerUser


T = TypeVar("T", bound="V0040QosLimitsMaxAccruingPer")


@_attrs_define
class V0040QosLimitsMaxAccruingPer:
    """
    Attributes:
        account (Union[Unset, V0040QosLimitsMaxAccruingPerAccount]):
        user (Union[Unset, V0040QosLimitsMaxAccruingPerUser]):
    """

    account: Union[Unset, "V0040QosLimitsMaxAccruingPerAccount"] = UNSET
    user: Union[Unset, "V0040QosLimitsMaxAccruingPerUser"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        account: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.account, Unset):
            account = self.account.to_dict()

        user: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.user, Unset):
            user = self.user.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if account is not UNSET:
            field_dict["account"] = account
        if user is not UNSET:
            field_dict["user"] = user

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0040_qos_limits_max_accruing_per_account import V0040QosLimitsMaxAccruingPerAccount
        from ..models.v0040_qos_limits_max_accruing_per_user import V0040QosLimitsMaxAccruingPerUser

        d = dict(src_dict)
        _account = d.pop("account", UNSET)
        account: Union[Unset, V0040QosLimitsMaxAccruingPerAccount]
        if isinstance(_account, Unset):
            account = UNSET
        else:
            account = V0040QosLimitsMaxAccruingPerAccount.from_dict(_account)

        _user = d.pop("user", UNSET)
        user: Union[Unset, V0040QosLimitsMaxAccruingPerUser]
        if isinstance(_user, Unset):
            user = UNSET
        else:
            user = V0040QosLimitsMaxAccruingPerUser.from_dict(_user)

        v0040_qos_limits_max_accruing_per = cls(
            account=account,
            user=user,
        )

        v0040_qos_limits_max_accruing_per.additional_properties = d
        return v0040_qos_limits_max_accruing_per

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
