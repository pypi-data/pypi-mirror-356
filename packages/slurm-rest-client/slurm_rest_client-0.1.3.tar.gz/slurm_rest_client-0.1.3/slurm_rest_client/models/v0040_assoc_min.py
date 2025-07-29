from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_assoc_min_priority_threshold import V0040AssocMinPriorityThreshold


T = TypeVar("T", bound="V0040AssocMin")


@_attrs_define
class V0040AssocMin:
    """
    Attributes:
        priority_threshold (Union[Unset, V0040AssocMinPriorityThreshold]):
    """

    priority_threshold: Union[Unset, "V0040AssocMinPriorityThreshold"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        priority_threshold: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.priority_threshold, Unset):
            priority_threshold = self.priority_threshold.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if priority_threshold is not UNSET:
            field_dict["priority_threshold"] = priority_threshold

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0040_assoc_min_priority_threshold import V0040AssocMinPriorityThreshold

        d = dict(src_dict)
        _priority_threshold = d.pop("priority_threshold", UNSET)
        priority_threshold: Union[Unset, V0040AssocMinPriorityThreshold]
        if isinstance(_priority_threshold, Unset):
            priority_threshold = UNSET
        else:
            priority_threshold = V0040AssocMinPriorityThreshold.from_dict(_priority_threshold)

        v0040_assoc_min = cls(
            priority_threshold=priority_threshold,
        )

        v0040_assoc_min.additional_properties = d
        return v0040_assoc_min

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
