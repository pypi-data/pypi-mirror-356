from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_step_tres_consumed import V0040StepTresConsumed
    from ..models.v0040_step_tres_requested import V0040StepTresRequested
    from ..models.v0040_tres import V0040Tres


T = TypeVar("T", bound="V0040StepTres")


@_attrs_define
class V0040StepTres:
    """
    Attributes:
        requested (Union[Unset, V0040StepTresRequested]):
        consumed (Union[Unset, V0040StepTresConsumed]):
        allocated (Union[Unset, list['V0040Tres']]):
    """

    requested: Union[Unset, "V0040StepTresRequested"] = UNSET
    consumed: Union[Unset, "V0040StepTresConsumed"] = UNSET
    allocated: Union[Unset, list["V0040Tres"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        requested: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.requested, Unset):
            requested = self.requested.to_dict()

        consumed: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.consumed, Unset):
            consumed = self.consumed.to_dict()

        allocated: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.allocated, Unset):
            allocated = []
            for componentsschemasv0_0_40_tres_list_item_data in self.allocated:
                componentsschemasv0_0_40_tres_list_item = componentsschemasv0_0_40_tres_list_item_data.to_dict()
                allocated.append(componentsschemasv0_0_40_tres_list_item)

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
        from ..models.v0040_step_tres_consumed import V0040StepTresConsumed
        from ..models.v0040_step_tres_requested import V0040StepTresRequested
        from ..models.v0040_tres import V0040Tres

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

        allocated = []
        _allocated = d.pop("allocated", UNSET)
        for componentsschemasv0_0_40_tres_list_item_data in _allocated or []:
            componentsschemasv0_0_40_tres_list_item = V0040Tres.from_dict(componentsschemasv0_0_40_tres_list_item_data)

            allocated.append(componentsschemasv0_0_40_tres_list_item)

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
