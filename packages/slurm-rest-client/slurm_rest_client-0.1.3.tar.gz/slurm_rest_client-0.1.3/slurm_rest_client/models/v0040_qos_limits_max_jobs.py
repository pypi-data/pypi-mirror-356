from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_qos_limits_max_jobs_active_jobs import V0040QosLimitsMaxJobsActiveJobs
    from ..models.v0040_qos_limits_max_jobs_per import V0040QosLimitsMaxJobsPer


T = TypeVar("T", bound="V0040QosLimitsMaxJobs")


@_attrs_define
class V0040QosLimitsMaxJobs:
    """
    Attributes:
        active_jobs (Union[Unset, V0040QosLimitsMaxJobsActiveJobs]):
        per (Union[Unset, V0040QosLimitsMaxJobsPer]):
    """

    active_jobs: Union[Unset, "V0040QosLimitsMaxJobsActiveJobs"] = UNSET
    per: Union[Unset, "V0040QosLimitsMaxJobsPer"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        active_jobs: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.active_jobs, Unset):
            active_jobs = self.active_jobs.to_dict()

        per: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.per, Unset):
            per = self.per.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if active_jobs is not UNSET:
            field_dict["active_jobs"] = active_jobs
        if per is not UNSET:
            field_dict["per"] = per

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0040_qos_limits_max_jobs_active_jobs import V0040QosLimitsMaxJobsActiveJobs
        from ..models.v0040_qos_limits_max_jobs_per import V0040QosLimitsMaxJobsPer

        d = dict(src_dict)
        _active_jobs = d.pop("active_jobs", UNSET)
        active_jobs: Union[Unset, V0040QosLimitsMaxJobsActiveJobs]
        if isinstance(_active_jobs, Unset):
            active_jobs = UNSET
        else:
            active_jobs = V0040QosLimitsMaxJobsActiveJobs.from_dict(_active_jobs)

        _per = d.pop("per", UNSET)
        per: Union[Unset, V0040QosLimitsMaxJobsPer]
        if isinstance(_per, Unset):
            per = UNSET
        else:
            per = V0040QosLimitsMaxJobsPer.from_dict(_per)

        v0040_qos_limits_max_jobs = cls(
            active_jobs=active_jobs,
            per=per,
        )

        v0040_qos_limits_max_jobs.additional_properties = d
        return v0040_qos_limits_max_jobs

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
