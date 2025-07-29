from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_step_tres_allocated import V0040StepTresAllocated
    from ..models.v0040_step_tres_consumed import V0040StepTresConsumed
    from ..models.v0040_step_tres_requested import V0040StepTresRequested


T = TypeVar("T", bound="V0040StepTres")


@_attrs_define
class V0040StepTres:
    """
    Attributes:
        requested (Union[Unset, V0040StepTresRequested]):
        consumed (Union[Unset, V0040StepTresConsumed]):
        allocated (Union[Unset, V0040StepTresAllocated]):
    """

    requested: Union[Unset, "V0040StepTresRequested"] = UNSET
    consumed: Union[Unset, "V0040StepTresConsumed"] = UNSET
    allocated: Union[Unset, "V0040StepTresAllocated"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        requested: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.requested, Unset):
            requested = self.requested.to_dict()

        consumed: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.consumed, Unset):
            consumed = self.consumed.to_dict()

        allocated: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.allocated, Unset):
            allocated = self.allocated.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if requested is not UNSET:
            field_dict["requested"] = requested
        if consumed is not UNSET:
            field_dict["consumed"] = consumed
        if allocated is not UNSET:
            field_dict["allocated"] = allocated

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0040_step_tres_allocated import V0040StepTresAllocated
        from ..models.v0040_step_tres_consumed import V0040StepTresConsumed
        from ..models.v0040_step_tres_requested import V0040StepTresRequested

        d = dict(src_dict)
        _requested = d.pop("requested", UNSET)
        requested: Union[Unset, V0040StepTresRequested]
        if isinstance(_requested, Unset):
            requested = UNSET
        else:
            requested = V0040StepTresRequested.from_dict(_requested)

        _consumed = d.pop("consumed", UNSET)
        consumed: Union[Unset, V0040StepTresConsumed]
        if isinstance(_consumed, Unset):
            consumed = UNSET
        else:
            consumed = V0040StepTresConsumed.from_dict(_consumed)

        _allocated = d.pop("allocated", UNSET)
        allocated: Union[Unset, V0040StepTresAllocated]
        if isinstance(_allocated, Unset):
            allocated = UNSET
        else:
            allocated = V0040StepTresAllocated.from_dict(_allocated)

        v0040_step_tres = cls(
            requested=requested,
            consumed=consumed,
            allocated=allocated,
        )

        v0040_step_tres.additional_properties = d
        return v0040_step_tres

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
