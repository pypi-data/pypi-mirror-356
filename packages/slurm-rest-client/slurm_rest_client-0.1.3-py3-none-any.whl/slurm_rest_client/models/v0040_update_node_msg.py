from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.v0040_update_node_msg_state_item import V0040UpdateNodeMsgStateItem
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_update_node_msg_address import V0040UpdateNodeMsgAddress
    from ..models.v0040_update_node_msg_features import V0040UpdateNodeMsgFeatures
    from ..models.v0040_update_node_msg_features_act import V0040UpdateNodeMsgFeaturesAct
    from ..models.v0040_update_node_msg_hostname import V0040UpdateNodeMsgHostname
    from ..models.v0040_update_node_msg_name import V0040UpdateNodeMsgName
    from ..models.v0040_update_node_msg_resume_after import V0040UpdateNodeMsgResumeAfter
    from ..models.v0040_update_node_msg_weight import V0040UpdateNodeMsgWeight


T = TypeVar("T", bound="V0040UpdateNodeMsg")


@_attrs_define
class V0040UpdateNodeMsg:
    """
    Attributes:
        comment (Union[Unset, str]): arbitrary comment
        cpu_bind (Union[Unset, int]): default CPU binding type
        extra (Union[Unset, str]): arbitrary string
        features (Union[Unset, V0040UpdateNodeMsgFeatures]):
        features_act (Union[Unset, V0040UpdateNodeMsgFeaturesAct]):
        gres (Union[Unset, str]): new generic resources for node
        address (Union[Unset, V0040UpdateNodeMsgAddress]):
        hostname (Union[Unset, V0040UpdateNodeMsgHostname]):
        name (Union[Unset, V0040UpdateNodeMsgName]):
        state (Union[Unset, list[V0040UpdateNodeMsgStateItem]]): assign new node state
        reason (Union[Unset, str]): reason for node being DOWN or DRAINING
        reason_uid (Union[Unset, str]): user ID of sending (needed if user root is sending message)
        resume_after (Union[Unset, V0040UpdateNodeMsgResumeAfter]):
        weight (Union[Unset, V0040UpdateNodeMsgWeight]):
    """

    comment: Union[Unset, str] = UNSET
    cpu_bind: Union[Unset, int] = UNSET
    extra: Union[Unset, str] = UNSET
    features: Union[Unset, "V0040UpdateNodeMsgFeatures"] = UNSET
    features_act: Union[Unset, "V0040UpdateNodeMsgFeaturesAct"] = UNSET
    gres: Union[Unset, str] = UNSET
    address: Union[Unset, "V0040UpdateNodeMsgAddress"] = UNSET
    hostname: Union[Unset, "V0040UpdateNodeMsgHostname"] = UNSET
    name: Union[Unset, "V0040UpdateNodeMsgName"] = UNSET
    state: Union[Unset, list[V0040UpdateNodeMsgStateItem]] = UNSET
    reason: Union[Unset, str] = UNSET
    reason_uid: Union[Unset, str] = UNSET
    resume_after: Union[Unset, "V0040UpdateNodeMsgResumeAfter"] = UNSET
    weight: Union[Unset, "V0040UpdateNodeMsgWeight"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        comment = self.comment

        cpu_bind = self.cpu_bind

        extra = self.extra

        features: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.features, Unset):
            features = self.features.to_dict()

        features_act: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.features_act, Unset):
            features_act = self.features_act.to_dict()

        gres = self.gres

        address: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.address, Unset):
            address = self.address.to_dict()

        hostname: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.hostname, Unset):
            hostname = self.hostname.to_dict()

        name: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.name, Unset):
            name = self.name.to_dict()

        state: Union[Unset, list[str]] = UNSET
        if not isinstance(self.state, Unset):
            state = []
            for state_item_data in self.state:
                state_item = state_item_data.value
                state.append(state_item)

        reason = self.reason

        reason_uid = self.reason_uid

        resume_after: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.resume_after, Unset):
            resume_after = self.resume_after.to_dict()

        weight: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.weight, Unset):
            weight = self.weight.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if comment is not UNSET:
            field_dict["comment"] = comment
        if cpu_bind is not UNSET:
            field_dict["cpu_bind"] = cpu_bind
        if extra is not UNSET:
            field_dict["extra"] = extra
        if features is not UNSET:
            field_dict["features"] = features
        if features_act is not UNSET:
            field_dict["features_act"] = features_act
        if gres is not UNSET:
            field_dict["gres"] = gres
        if address is not UNSET:
            field_dict["address"] = address
        if hostname is not UNSET:
            field_dict["hostname"] = hostname
        if name is not UNSET:
            field_dict["name"] = name
        if state is not UNSET:
            field_dict["state"] = state
        if reason is not UNSET:
            field_dict["reason"] = reason
        if reason_uid is not UNSET:
            field_dict["reason_uid"] = reason_uid
        if resume_after is not UNSET:
            field_dict["resume_after"] = resume_after
        if weight is not UNSET:
            field_dict["weight"] = weight

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0040_update_node_msg_address import V0040UpdateNodeMsgAddress
        from ..models.v0040_update_node_msg_features import V0040UpdateNodeMsgFeatures
        from ..models.v0040_update_node_msg_features_act import V0040UpdateNodeMsgFeaturesAct
        from ..models.v0040_update_node_msg_hostname import V0040UpdateNodeMsgHostname
        from ..models.v0040_update_node_msg_name import V0040UpdateNodeMsgName
        from ..models.v0040_update_node_msg_resume_after import V0040UpdateNodeMsgResumeAfter
        from ..models.v0040_update_node_msg_weight import V0040UpdateNodeMsgWeight

        d = dict(src_dict)
        comment = d.pop("comment", UNSET)

        cpu_bind = d.pop("cpu_bind", UNSET)

        extra = d.pop("extra", UNSET)

        _features = d.pop("features", UNSET)
        features: Union[Unset, V0040UpdateNodeMsgFeatures]
        if isinstance(_features, Unset):
            features = UNSET
        else:
            features = V0040UpdateNodeMsgFeatures.from_dict(_features)

        _features_act = d.pop("features_act", UNSET)
        features_act: Union[Unset, V0040UpdateNodeMsgFeaturesAct]
        if isinstance(_features_act, Unset):
            features_act = UNSET
        else:
            features_act = V0040UpdateNodeMsgFeaturesAct.from_dict(_features_act)

        gres = d.pop("gres", UNSET)

        _address = d.pop("address", UNSET)
        address: Union[Unset, V0040UpdateNodeMsgAddress]
        if isinstance(_address, Unset):
            address = UNSET
        else:
            address = V0040UpdateNodeMsgAddress.from_dict(_address)

        _hostname = d.pop("hostname", UNSET)
        hostname: Union[Unset, V0040UpdateNodeMsgHostname]
        if isinstance(_hostname, Unset):
            hostname = UNSET
        else:
            hostname = V0040UpdateNodeMsgHostname.from_dict(_hostname)

        _name = d.pop("name", UNSET)
        name: Union[Unset, V0040UpdateNodeMsgName]
        if isinstance(_name, Unset):
            name = UNSET
        else:
            name = V0040UpdateNodeMsgName.from_dict(_name)

        state = []
        _state = d.pop("state", UNSET)
        for state_item_data in _state or []:
            state_item = V0040UpdateNodeMsgStateItem(state_item_data)

            state.append(state_item)

        reason = d.pop("reason", UNSET)

        reason_uid = d.pop("reason_uid", UNSET)

        _resume_after = d.pop("resume_after", UNSET)
        resume_after: Union[Unset, V0040UpdateNodeMsgResumeAfter]
        if isinstance(_resume_after, Unset):
            resume_after = UNSET
        else:
            resume_after = V0040UpdateNodeMsgResumeAfter.from_dict(_resume_after)

        _weight = d.pop("weight", UNSET)
        weight: Union[Unset, V0040UpdateNodeMsgWeight]
        if isinstance(_weight, Unset):
            weight = UNSET
        else:
            weight = V0040UpdateNodeMsgWeight.from_dict(_weight)

        v0040_update_node_msg = cls(
            comment=comment,
            cpu_bind=cpu_bind,
            extra=extra,
            features=features,
            features_act=features_act,
            gres=gres,
            address=address,
            hostname=hostname,
            name=name,
            state=state,
            reason=reason,
            reason_uid=reason_uid,
            resume_after=resume_after,
            weight=weight,
        )

        v0040_update_node_msg.additional_properties = d
        return v0040_update_node_msg

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
