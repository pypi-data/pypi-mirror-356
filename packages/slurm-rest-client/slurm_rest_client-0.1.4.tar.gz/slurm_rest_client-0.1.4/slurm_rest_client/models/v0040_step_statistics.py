from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_step_statistics_cpu import V0040StepStatisticsCPU
    from ..models.v0040_step_statistics_energy import V0040StepStatisticsEnergy


T = TypeVar("T", bound="V0040StepStatistics")


@_attrs_define
class V0040StepStatistics:
    """
    Attributes:
        cpu (Union[Unset, V0040StepStatisticsCPU]):
        energy (Union[Unset, V0040StepStatisticsEnergy]):
    """

    cpu: Union[Unset, "V0040StepStatisticsCPU"] = UNSET
    energy: Union[Unset, "V0040StepStatisticsEnergy"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cpu: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.cpu, Unset):
            cpu = self.cpu.to_dict()

        energy: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.energy, Unset):
            energy = self.energy.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if cpu is not UNSET:
            field_dict["CPU"] = cpu
        if energy is not UNSET:
            field_dict["energy"] = energy

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0040_step_statistics_cpu import V0040StepStatisticsCPU
        from ..models.v0040_step_statistics_energy import V0040StepStatisticsEnergy

        d = dict(src_dict)
        _cpu = d.pop("CPU", UNSET)
        cpu: Union[Unset, V0040StepStatisticsCPU]
        if isinstance(_cpu, Unset):
            cpu = UNSET
        else:
            cpu = V0040StepStatisticsCPU.from_dict(_cpu)

        _energy = d.pop("energy", UNSET)
        energy: Union[Unset, V0040StepStatisticsEnergy]
        if isinstance(_energy, Unset):
            energy = UNSET
        else:
            energy = V0040StepStatisticsEnergy.from_dict(_energy)

        v0040_step_statistics = cls(
            cpu=cpu,
            energy=energy,
        )

        v0040_step_statistics.additional_properties = d
        return v0040_step_statistics

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
