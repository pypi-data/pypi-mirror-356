from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_openapi_job_state_resp_errors import V0040OpenapiJobStateRespErrors
    from ..models.v0040_openapi_job_state_resp_jobs import V0040OpenapiJobStateRespJobs
    from ..models.v0040_openapi_job_state_resp_meta import V0040OpenapiJobStateRespMeta
    from ..models.v0040_openapi_job_state_resp_warnings import V0040OpenapiJobStateRespWarnings


T = TypeVar("T", bound="V0040OpenapiJobStateResp")


@_attrs_define
class V0040OpenapiJobStateResp:
    """
    Attributes:
        jobs (Union[Unset, V0040OpenapiJobStateRespJobs]):
        meta (Union[Unset, V0040OpenapiJobStateRespMeta]):
        errors (Union[Unset, V0040OpenapiJobStateRespErrors]):
        warnings (Union[Unset, V0040OpenapiJobStateRespWarnings]):
    """

    jobs: Union[Unset, "V0040OpenapiJobStateRespJobs"] = UNSET
    meta: Union[Unset, "V0040OpenapiJobStateRespMeta"] = UNSET
    errors: Union[Unset, "V0040OpenapiJobStateRespErrors"] = UNSET
    warnings: Union[Unset, "V0040OpenapiJobStateRespWarnings"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        jobs: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.jobs, Unset):
            jobs = self.jobs.to_dict()

        meta: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.meta, Unset):
            meta = self.meta.to_dict()

        errors: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.errors, Unset):
            errors = self.errors.to_dict()

        warnings: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.warnings, Unset):
            warnings = self.warnings.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if jobs is not UNSET:
            field_dict["jobs"] = jobs
        if meta is not UNSET:
            field_dict["meta"] = meta
        if errors is not UNSET:
            field_dict["errors"] = errors
        if warnings is not UNSET:
            field_dict["warnings"] = warnings

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0040_openapi_job_state_resp_errors import V0040OpenapiJobStateRespErrors
        from ..models.v0040_openapi_job_state_resp_jobs import V0040OpenapiJobStateRespJobs
        from ..models.v0040_openapi_job_state_resp_meta import V0040OpenapiJobStateRespMeta
        from ..models.v0040_openapi_job_state_resp_warnings import V0040OpenapiJobStateRespWarnings

        d = dict(src_dict)
        _jobs = d.pop("jobs", UNSET)
        jobs: Union[Unset, V0040OpenapiJobStateRespJobs]
        if isinstance(_jobs, Unset):
            jobs = UNSET
        else:
            jobs = V0040OpenapiJobStateRespJobs.from_dict(_jobs)

        _meta = d.pop("meta", UNSET)
        meta: Union[Unset, V0040OpenapiJobStateRespMeta]
        if isinstance(_meta, Unset):
            meta = UNSET
        else:
            meta = V0040OpenapiJobStateRespMeta.from_dict(_meta)

        _errors = d.pop("errors", UNSET)
        errors: Union[Unset, V0040OpenapiJobStateRespErrors]
        if isinstance(_errors, Unset):
            errors = UNSET
        else:
            errors = V0040OpenapiJobStateRespErrors.from_dict(_errors)

        _warnings = d.pop("warnings", UNSET)
        warnings: Union[Unset, V0040OpenapiJobStateRespWarnings]
        if isinstance(_warnings, Unset):
            warnings = UNSET
        else:
            warnings = V0040OpenapiJobStateRespWarnings.from_dict(_warnings)

        v0040_openapi_job_state_resp = cls(
            jobs=jobs,
            meta=meta,
            errors=errors,
            warnings=warnings,
        )

        v0040_openapi_job_state_resp.additional_properties = d
        return v0040_openapi_job_state_resp

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
