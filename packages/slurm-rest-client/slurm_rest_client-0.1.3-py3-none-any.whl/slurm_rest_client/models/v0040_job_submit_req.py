from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_job_submit_req_job import V0040JobSubmitReqJob
    from ..models.v0040_job_submit_req_jobs import V0040JobSubmitReqJobs


T = TypeVar("T", bound="V0040JobSubmitReq")


@_attrs_define
class V0040JobSubmitReq:
    """
    Attributes:
        script (Union[Unset, str]): Batch job script. Batch script must be specified in first component of jobs or in
            job if this field is not populated.
        jobs (Union[Unset, V0040JobSubmitReqJobs]):
        job (Union[Unset, V0040JobSubmitReqJob]):
    """

    script: Union[Unset, str] = UNSET
    jobs: Union[Unset, "V0040JobSubmitReqJobs"] = UNSET
    job: Union[Unset, "V0040JobSubmitReqJob"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        script = self.script

        jobs: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.jobs, Unset):
            jobs = self.jobs.to_dict()

        job: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.job, Unset):
            job = self.job.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if script is not UNSET:
            field_dict["script"] = script
        if jobs is not UNSET:
            field_dict["jobs"] = jobs
        if job is not UNSET:
            field_dict["job"] = job

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0040_job_submit_req_job import V0040JobSubmitReqJob
        from ..models.v0040_job_submit_req_jobs import V0040JobSubmitReqJobs

        d = dict(src_dict)
        script = d.pop("script", UNSET)

        _jobs = d.pop("jobs", UNSET)
        jobs: Union[Unset, V0040JobSubmitReqJobs]
        if isinstance(_jobs, Unset):
            jobs = UNSET
        else:
            jobs = V0040JobSubmitReqJobs.from_dict(_jobs)

        _job = d.pop("job", UNSET)
        job: Union[Unset, V0040JobSubmitReqJob]
        if isinstance(_job, Unset):
            job = UNSET
        else:
            job = V0040JobSubmitReqJob.from_dict(_job)

        v0040_job_submit_req = cls(
            script=script,
            jobs=jobs,
            job=job,
        )

        v0040_job_submit_req.additional_properties = d
        return v0040_job_submit_req

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
