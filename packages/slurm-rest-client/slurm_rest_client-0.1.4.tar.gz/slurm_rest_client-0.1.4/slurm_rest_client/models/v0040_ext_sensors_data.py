from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="V0040ExtSensorsData")


@_attrs_define
class V0040ExtSensorsData:
    """
    Attributes:
        consumed_energy (Union[Unset, int]):
        temperature (Union[Unset, int]):
        energy_update_time (Union[Unset, int]):
        current_watts (Union[Unset, int]):
    """

    consumed_energy: Union[Unset, int] = UNSET
    temperature: Union[Unset, int] = UNSET
    energy_update_time: Union[Unset, int] = UNSET
    current_watts: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        consumed_energy = self.consumed_energy

        temperature = self.temperature

        energy_update_time = self.energy_update_time

        current_watts = self.current_watts

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if consumed_energy is not UNSET:
            field_dict["consumed_energy"] = consumed_energy
        if temperature is not UNSET:
            field_dict["temperature"] = temperature
        if energy_update_time is not UNSET:
            field_dict["energy_update_time"] = energy_update_time
        if current_watts is not UNSET:
            field_dict["current_watts"] = current_watts

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        consumed_energy = d.pop("consumed_energy", UNSET)

        temperature = d.pop("temperature", UNSET)

        energy_update_time = d.pop("energy_update_time", UNSET)

        current_watts = d.pop("current_watts", UNSET)

        v0040_ext_sensors_data = cls(
            consumed_energy=consumed_energy,
            temperature=temperature,
            energy_update_time=energy_update_time,
            current_watts=current_watts,
        )

        v0040_ext_sensors_data.additional_properties = d
        return v0040_ext_sensors_data

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
