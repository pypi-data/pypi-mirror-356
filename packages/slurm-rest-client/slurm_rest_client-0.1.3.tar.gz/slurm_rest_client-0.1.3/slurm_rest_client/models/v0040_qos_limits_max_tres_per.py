from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_qos_limits_max_tres_per_account import V0040QosLimitsMaxTresPerAccount
    from ..models.v0040_qos_limits_max_tres_per_job import V0040QosLimitsMaxTresPerJob
    from ..models.v0040_qos_limits_max_tres_per_node import V0040QosLimitsMaxTresPerNode
    from ..models.v0040_qos_limits_max_tres_per_user import V0040QosLimitsMaxTresPerUser


T = TypeVar("T", bound="V0040QosLimitsMaxTresPer")


@_attrs_define
class V0040QosLimitsMaxTresPer:
    """
    Attributes:
        account (Union[Unset, V0040QosLimitsMaxTresPerAccount]):
        job (Union[Unset, V0040QosLimitsMaxTresPerJob]):
        node (Union[Unset, V0040QosLimitsMaxTresPerNode]):
        user (Union[Unset, V0040QosLimitsMaxTresPerUser]):
    """

    account: Union[Unset, "V0040QosLimitsMaxTresPerAccount"] = UNSET
    job: Union[Unset, "V0040QosLimitsMaxTresPerJob"] = UNSET
    node: Union[Unset, "V0040QosLimitsMaxTresPerNode"] = UNSET
    user: Union[Unset, "V0040QosLimitsMaxTresPerUser"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        account: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.account, Unset):
            account = self.account.to_dict()

        job: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.job, Unset):
            job = self.job.to_dict()

        node: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.node, Unset):
            node = self.node.to_dict()

        user: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.user, Unset):
            user = self.user.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if account is not UNSET:
            field_dict["account"] = account
        if job is not UNSET:
            field_dict["job"] = job
        if node is not UNSET:
            field_dict["node"] = node
        if user is not UNSET:
            field_dict["user"] = user

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0040_qos_limits_max_tres_per_account import V0040QosLimitsMaxTresPerAccount
        from ..models.v0040_qos_limits_max_tres_per_job import V0040QosLimitsMaxTresPerJob
        from ..models.v0040_qos_limits_max_tres_per_node import V0040QosLimitsMaxTresPerNode
        from ..models.v0040_qos_limits_max_tres_per_user import V0040QosLimitsMaxTresPerUser

        d = dict(src_dict)
        _account = d.pop("account", UNSET)
        account: Union[Unset, V0040QosLimitsMaxTresPerAccount]
        if isinstance(_account, Unset):
            account = UNSET
        else:
            account = V0040QosLimitsMaxTresPerAccount.from_dict(_account)

        _job = d.pop("job", UNSET)
        job: Union[Unset, V0040QosLimitsMaxTresPerJob]
        if isinstance(_job, Unset):
            job = UNSET
        else:
            job = V0040QosLimitsMaxTresPerJob.from_dict(_job)

        _node = d.pop("node", UNSET)
        node: Union[Unset, V0040QosLimitsMaxTresPerNode]
        if isinstance(_node, Unset):
            node = UNSET
        else:
            node = V0040QosLimitsMaxTresPerNode.from_dict(_node)

        _user = d.pop("user", UNSET)
        user: Union[Unset, V0040QosLimitsMaxTresPerUser]
        if isinstance(_user, Unset):
            user = UNSET
        else:
            user = V0040QosLimitsMaxTresPerUser.from_dict(_user)

        v0040_qos_limits_max_tres_per = cls(
            account=account,
            job=job,
            node=node,
            user=user,
        )

        v0040_qos_limits_max_tres_per.additional_properties = d
        return v0040_qos_limits_max_tres_per

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
