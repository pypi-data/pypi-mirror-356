from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_qos_limits_max_tres_minutes import V0040QosLimitsMaxTresMinutes
    from ..models.v0040_qos_limits_max_tres_per import V0040QosLimitsMaxTresPer
    from ..models.v0040_tres import V0040Tres


T = TypeVar("T", bound="V0040QosLimitsMaxTres")


@_attrs_define
class V0040QosLimitsMaxTres:
    """
    Attributes:
        total (Union[Unset, list['V0040Tres']]):
        minutes (Union[Unset, V0040QosLimitsMaxTresMinutes]):
        per (Union[Unset, V0040QosLimitsMaxTresPer]):
    """

    total: Union[Unset, list["V0040Tres"]] = UNSET
    minutes: Union[Unset, "V0040QosLimitsMaxTresMinutes"] = UNSET
    per: Union[Unset, "V0040QosLimitsMaxTresPer"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        total: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.total, Unset):
            total = []
            for componentsschemasv0_0_40_tres_list_item_data in self.total:
                componentsschemasv0_0_40_tres_list_item = componentsschemasv0_0_40_tres_list_item_data.to_dict()
                total.append(componentsschemasv0_0_40_tres_list_item)

        minutes: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.minutes, Unset):
            minutes = self.minutes.to_dict()

        per: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.per, Unset):
            per = self.per.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if total is not UNSET:
            field_dict["total"] = total
        if minutes is not UNSET:
            field_dict["minutes"] = minutes
        if per is not UNSET:
            field_dict["per"] = per

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0040_qos_limits_max_tres_minutes import V0040QosLimitsMaxTresMinutes
        from ..models.v0040_qos_limits_max_tres_per import V0040QosLimitsMaxTresPer
        from ..models.v0040_tres import V0040Tres

        d = dict(src_dict)
        total = []
        _total = d.pop("total", UNSET)
        for componentsschemasv0_0_40_tres_list_item_data in _total or []:
            componentsschemasv0_0_40_tres_list_item = V0040Tres.from_dict(componentsschemasv0_0_40_tres_list_item_data)

            total.append(componentsschemasv0_0_40_tres_list_item)

        _minutes = d.pop("minutes", UNSET)
        minutes: Union[Unset, V0040QosLimitsMaxTresMinutes]
        if isinstance(_minutes, Unset):
            minutes = UNSET
        else:
            minutes = V0040QosLimitsMaxTresMinutes.from_dict(_minutes)

        _per = d.pop("per", UNSET)
        per: Union[Unset, V0040QosLimitsMaxTresPer]
        if isinstance(_per, Unset):
            per = UNSET
        else:
            per = V0040QosLimitsMaxTresPer.from_dict(_per)

        v0040_qos_limits_max_tres = cls(
            total=total,
            minutes=minutes,
            per=per,
        )

        v0040_qos_limits_max_tres.additional_properties = d
        return v0040_qos_limits_max_tres

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
