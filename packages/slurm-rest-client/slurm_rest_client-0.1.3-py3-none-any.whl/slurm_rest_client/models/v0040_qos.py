from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.v0040_qos_flags_item import V0040QosFlagsItem
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_qos_limits import V0040QosLimits
    from ..models.v0040_qos_preempt import V0040QosPreempt
    from ..models.v0040_qos_priority import V0040QosPriority
    from ..models.v0040_qos_usage_factor import V0040QosUsageFactor
    from ..models.v0040_qos_usage_threshold import V0040QosUsageThreshold


T = TypeVar("T", bound="V0040Qos")


@_attrs_define
class V0040Qos:
    """
    Attributes:
        description (Union[Unset, str]):
        flags (Union[Unset, list[V0040QosFlagsItem]]):
        id (Union[Unset, int]):
        limits (Union[Unset, V0040QosLimits]):
        name (Union[Unset, str]):
        preempt (Union[Unset, V0040QosPreempt]):
        priority (Union[Unset, V0040QosPriority]):
        usage_factor (Union[Unset, V0040QosUsageFactor]):
        usage_threshold (Union[Unset, V0040QosUsageThreshold]):
    """

    description: Union[Unset, str] = UNSET
    flags: Union[Unset, list[V0040QosFlagsItem]] = UNSET
    id: Union[Unset, int] = UNSET
    limits: Union[Unset, "V0040QosLimits"] = UNSET
    name: Union[Unset, str] = UNSET
    preempt: Union[Unset, "V0040QosPreempt"] = UNSET
    priority: Union[Unset, "V0040QosPriority"] = UNSET
    usage_factor: Union[Unset, "V0040QosUsageFactor"] = UNSET
    usage_threshold: Union[Unset, "V0040QosUsageThreshold"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        description = self.description

        flags: Union[Unset, list[str]] = UNSET
        if not isinstance(self.flags, Unset):
            flags = []
            for flags_item_data in self.flags:
                flags_item = flags_item_data.value
                flags.append(flags_item)

        id = self.id

        limits: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.limits, Unset):
            limits = self.limits.to_dict()

        name = self.name

        preempt: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.preempt, Unset):
            preempt = self.preempt.to_dict()

        priority: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.priority, Unset):
            priority = self.priority.to_dict()

        usage_factor: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.usage_factor, Unset):
            usage_factor = self.usage_factor.to_dict()

        usage_threshold: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.usage_threshold, Unset):
            usage_threshold = self.usage_threshold.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if description is not UNSET:
            field_dict["description"] = description
        if flags is not UNSET:
            field_dict["flags"] = flags
        if id is not UNSET:
            field_dict["id"] = id
        if limits is not UNSET:
            field_dict["limits"] = limits
        if name is not UNSET:
            field_dict["name"] = name
        if preempt is not UNSET:
            field_dict["preempt"] = preempt
        if priority is not UNSET:
            field_dict["priority"] = priority
        if usage_factor is not UNSET:
            field_dict["usage_factor"] = usage_factor
        if usage_threshold is not UNSET:
            field_dict["usage_threshold"] = usage_threshold

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0040_qos_limits import V0040QosLimits
        from ..models.v0040_qos_preempt import V0040QosPreempt
        from ..models.v0040_qos_priority import V0040QosPriority
        from ..models.v0040_qos_usage_factor import V0040QosUsageFactor
        from ..models.v0040_qos_usage_threshold import V0040QosUsageThreshold

        d = dict(src_dict)
        description = d.pop("description", UNSET)

        flags = []
        _flags = d.pop("flags", UNSET)
        for flags_item_data in _flags or []:
            flags_item = V0040QosFlagsItem(flags_item_data)

            flags.append(flags_item)

        id = d.pop("id", UNSET)

        _limits = d.pop("limits", UNSET)
        limits: Union[Unset, V0040QosLimits]
        if isinstance(_limits, Unset):
            limits = UNSET
        else:
            limits = V0040QosLimits.from_dict(_limits)

        name = d.pop("name", UNSET)

        _preempt = d.pop("preempt", UNSET)
        preempt: Union[Unset, V0040QosPreempt]
        if isinstance(_preempt, Unset):
            preempt = UNSET
        else:
            preempt = V0040QosPreempt.from_dict(_preempt)

        _priority = d.pop("priority", UNSET)
        priority: Union[Unset, V0040QosPriority]
        if isinstance(_priority, Unset):
            priority = UNSET
        else:
            priority = V0040QosPriority.from_dict(_priority)

        _usage_factor = d.pop("usage_factor", UNSET)
        usage_factor: Union[Unset, V0040QosUsageFactor]
        if isinstance(_usage_factor, Unset):
            usage_factor = UNSET
        else:
            usage_factor = V0040QosUsageFactor.from_dict(_usage_factor)

        _usage_threshold = d.pop("usage_threshold", UNSET)
        usage_threshold: Union[Unset, V0040QosUsageThreshold]
        if isinstance(_usage_threshold, Unset):
            usage_threshold = UNSET
        else:
            usage_threshold = V0040QosUsageThreshold.from_dict(_usage_threshold)

        v0040_qos = cls(
            description=description,
            flags=flags,
            id=id,
            limits=limits,
            name=name,
            preempt=preempt,
            priority=priority,
            usage_factor=usage_factor,
            usage_threshold=usage_threshold,
        )

        v0040_qos.additional_properties = d
        return v0040_qos

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
