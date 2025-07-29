from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_power_mgmt_data_maximum_watts import V0040PowerMgmtDataMaximumWatts
    from ..models.v0040_power_mgmt_data_new_job_time import V0040PowerMgmtDataNewJobTime


T = TypeVar("T", bound="V0040PowerMgmtData")


@_attrs_define
class V0040PowerMgmtData:
    """
    Attributes:
        maximum_watts (Union[Unset, V0040PowerMgmtDataMaximumWatts]):
        current_watts (Union[Unset, int]):
        total_energy (Union[Unset, int]):
        new_maximum_watts (Union[Unset, int]):
        peak_watts (Union[Unset, int]):
        lowest_watts (Union[Unset, int]):
        new_job_time (Union[Unset, V0040PowerMgmtDataNewJobTime]):
        state (Union[Unset, int]):
        time_start_day (Union[Unset, int]):
    """

    maximum_watts: Union[Unset, "V0040PowerMgmtDataMaximumWatts"] = UNSET
    current_watts: Union[Unset, int] = UNSET
    total_energy: Union[Unset, int] = UNSET
    new_maximum_watts: Union[Unset, int] = UNSET
    peak_watts: Union[Unset, int] = UNSET
    lowest_watts: Union[Unset, int] = UNSET
    new_job_time: Union[Unset, "V0040PowerMgmtDataNewJobTime"] = UNSET
    state: Union[Unset, int] = UNSET
    time_start_day: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        maximum_watts: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.maximum_watts, Unset):
            maximum_watts = self.maximum_watts.to_dict()

        current_watts = self.current_watts

        total_energy = self.total_energy

        new_maximum_watts = self.new_maximum_watts

        peak_watts = self.peak_watts

        lowest_watts = self.lowest_watts

        new_job_time: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.new_job_time, Unset):
            new_job_time = self.new_job_time.to_dict()

        state = self.state

        time_start_day = self.time_start_day

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if maximum_watts is not UNSET:
            field_dict["maximum_watts"] = maximum_watts
        if current_watts is not UNSET:
            field_dict["current_watts"] = current_watts
        if total_energy is not UNSET:
            field_dict["total_energy"] = total_energy
        if new_maximum_watts is not UNSET:
            field_dict["new_maximum_watts"] = new_maximum_watts
        if peak_watts is not UNSET:
            field_dict["peak_watts"] = peak_watts
        if lowest_watts is not UNSET:
            field_dict["lowest_watts"] = lowest_watts
        if new_job_time is not UNSET:
            field_dict["new_job_time"] = new_job_time
        if state is not UNSET:
            field_dict["state"] = state
        if time_start_day is not UNSET:
            field_dict["time_start_day"] = time_start_day

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0040_power_mgmt_data_maximum_watts import V0040PowerMgmtDataMaximumWatts
        from ..models.v0040_power_mgmt_data_new_job_time import V0040PowerMgmtDataNewJobTime

        d = dict(src_dict)
        _maximum_watts = d.pop("maximum_watts", UNSET)
        maximum_watts: Union[Unset, V0040PowerMgmtDataMaximumWatts]
        if isinstance(_maximum_watts, Unset):
            maximum_watts = UNSET
        else:
            maximum_watts = V0040PowerMgmtDataMaximumWatts.from_dict(_maximum_watts)

        current_watts = d.pop("current_watts", UNSET)

        total_energy = d.pop("total_energy", UNSET)

        new_maximum_watts = d.pop("new_maximum_watts", UNSET)

        peak_watts = d.pop("peak_watts", UNSET)

        lowest_watts = d.pop("lowest_watts", UNSET)

        _new_job_time = d.pop("new_job_time", UNSET)
        new_job_time: Union[Unset, V0040PowerMgmtDataNewJobTime]
        if isinstance(_new_job_time, Unset):
            new_job_time = UNSET
        else:
            new_job_time = V0040PowerMgmtDataNewJobTime.from_dict(_new_job_time)

        state = d.pop("state", UNSET)

        time_start_day = d.pop("time_start_day", UNSET)

        v0040_power_mgmt_data = cls(
            maximum_watts=maximum_watts,
            current_watts=current_watts,
            total_energy=total_energy,
            new_maximum_watts=new_maximum_watts,
            peak_watts=peak_watts,
            lowest_watts=lowest_watts,
            new_job_time=new_job_time,
            state=state,
            time_start_day=time_start_day,
        )

        v0040_power_mgmt_data.additional_properties = d
        return v0040_power_mgmt_data

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
