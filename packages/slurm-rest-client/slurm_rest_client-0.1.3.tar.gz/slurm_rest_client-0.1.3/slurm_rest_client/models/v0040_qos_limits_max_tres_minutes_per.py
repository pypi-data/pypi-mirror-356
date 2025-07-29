from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_qos_limits_max_tres_minutes_per_account import V0040QosLimitsMaxTresMinutesPerAccount
    from ..models.v0040_qos_limits_max_tres_minutes_per_job import V0040QosLimitsMaxTresMinutesPerJob
    from ..models.v0040_qos_limits_max_tres_minutes_per_qos import V0040QosLimitsMaxTresMinutesPerQos
    from ..models.v0040_qos_limits_max_tres_minutes_per_user import V0040QosLimitsMaxTresMinutesPerUser


T = TypeVar("T", bound="V0040QosLimitsMaxTresMinutesPer")


@_attrs_define
class V0040QosLimitsMaxTresMinutesPer:
    """
    Attributes:
        qos (Union[Unset, V0040QosLimitsMaxTresMinutesPerQos]):
        job (Union[Unset, V0040QosLimitsMaxTresMinutesPerJob]):
        account (Union[Unset, V0040QosLimitsMaxTresMinutesPerAccount]):
        user (Union[Unset, V0040QosLimitsMaxTresMinutesPerUser]):
    """

    qos: Union[Unset, "V0040QosLimitsMaxTresMinutesPerQos"] = UNSET
    job: Union[Unset, "V0040QosLimitsMaxTresMinutesPerJob"] = UNSET
    account: Union[Unset, "V0040QosLimitsMaxTresMinutesPerAccount"] = UNSET
    user: Union[Unset, "V0040QosLimitsMaxTresMinutesPerUser"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        qos: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.qos, Unset):
            qos = self.qos.to_dict()

        job: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.job, Unset):
            job = self.job.to_dict()

        account: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.account, Unset):
            account = self.account.to_dict()

        user: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.user, Unset):
            user = self.user.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if qos is not UNSET:
            field_dict["qos"] = qos
        if job is not UNSET:
            field_dict["job"] = job
        if account is not UNSET:
            field_dict["account"] = account
        if user is not UNSET:
            field_dict["user"] = user

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0040_qos_limits_max_tres_minutes_per_account import V0040QosLimitsMaxTresMinutesPerAccount
        from ..models.v0040_qos_limits_max_tres_minutes_per_job import V0040QosLimitsMaxTresMinutesPerJob
        from ..models.v0040_qos_limits_max_tres_minutes_per_qos import V0040QosLimitsMaxTresMinutesPerQos
        from ..models.v0040_qos_limits_max_tres_minutes_per_user import V0040QosLimitsMaxTresMinutesPerUser

        d = dict(src_dict)
        _qos = d.pop("qos", UNSET)
        qos: Union[Unset, V0040QosLimitsMaxTresMinutesPerQos]
        if isinstance(_qos, Unset):
            qos = UNSET
        else:
            qos = V0040QosLimitsMaxTresMinutesPerQos.from_dict(_qos)

        _job = d.pop("job", UNSET)
        job: Union[Unset, V0040QosLimitsMaxTresMinutesPerJob]
        if isinstance(_job, Unset):
            job = UNSET
        else:
            job = V0040QosLimitsMaxTresMinutesPerJob.from_dict(_job)

        _account = d.pop("account", UNSET)
        account: Union[Unset, V0040QosLimitsMaxTresMinutesPerAccount]
        if isinstance(_account, Unset):
            account = UNSET
        else:
            account = V0040QosLimitsMaxTresMinutesPerAccount.from_dict(_account)

        _user = d.pop("user", UNSET)
        user: Union[Unset, V0040QosLimitsMaxTresMinutesPerUser]
        if isinstance(_user, Unset):
            user = UNSET
        else:
            user = V0040QosLimitsMaxTresMinutesPerUser.from_dict(_user)

        v0040_qos_limits_max_tres_minutes_per = cls(
            qos=qos,
            job=job,
            account=account,
            user=user,
        )

        v0040_qos_limits_max_tres_minutes_per.additional_properties = d
        return v0040_qos_limits_max_tres_minutes_per

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
