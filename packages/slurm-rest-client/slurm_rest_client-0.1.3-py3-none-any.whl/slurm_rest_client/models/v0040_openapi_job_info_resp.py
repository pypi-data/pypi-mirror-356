from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_openapi_job_info_resp_errors import V0040OpenapiJobInfoRespErrors
    from ..models.v0040_openapi_job_info_resp_jobs import V0040OpenapiJobInfoRespJobs
    from ..models.v0040_openapi_job_info_resp_last_backfill import V0040OpenapiJobInfoRespLastBackfill
    from ..models.v0040_openapi_job_info_resp_last_update import V0040OpenapiJobInfoRespLastUpdate
    from ..models.v0040_openapi_job_info_resp_meta import V0040OpenapiJobInfoRespMeta
    from ..models.v0040_openapi_job_info_resp_warnings import V0040OpenapiJobInfoRespWarnings


T = TypeVar("T", bound="V0040OpenapiJobInfoResp")


@_attrs_define
class V0040OpenapiJobInfoResp:
    """
    Attributes:
        jobs (V0040OpenapiJobInfoRespJobs):
        last_backfill (V0040OpenapiJobInfoRespLastBackfill):
        last_update (V0040OpenapiJobInfoRespLastUpdate):
        meta (Union[Unset, V0040OpenapiJobInfoRespMeta]):
        errors (Union[Unset, V0040OpenapiJobInfoRespErrors]):
        warnings (Union[Unset, V0040OpenapiJobInfoRespWarnings]):
    """

    jobs: "V0040OpenapiJobInfoRespJobs"
    last_backfill: "V0040OpenapiJobInfoRespLastBackfill"
    last_update: "V0040OpenapiJobInfoRespLastUpdate"
    meta: Union[Unset, "V0040OpenapiJobInfoRespMeta"] = UNSET
    errors: Union[Unset, "V0040OpenapiJobInfoRespErrors"] = UNSET
    warnings: Union[Unset, "V0040OpenapiJobInfoRespWarnings"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        jobs = self.jobs.to_dict()

        last_backfill = self.last_backfill.to_dict()

        last_update = self.last_update.to_dict()

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
        field_dict.update(
            {
                "jobs": jobs,
                "last_backfill": last_backfill,
                "last_update": last_update,
            }
        )
        if meta is not UNSET:
            field_dict["meta"] = meta
        if errors is not UNSET:
            field_dict["errors"] = errors
        if warnings is not UNSET:
            field_dict["warnings"] = warnings

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0040_openapi_job_info_resp_errors import V0040OpenapiJobInfoRespErrors
        from ..models.v0040_openapi_job_info_resp_jobs import V0040OpenapiJobInfoRespJobs
        from ..models.v0040_openapi_job_info_resp_last_backfill import V0040OpenapiJobInfoRespLastBackfill
        from ..models.v0040_openapi_job_info_resp_last_update import V0040OpenapiJobInfoRespLastUpdate
        from ..models.v0040_openapi_job_info_resp_meta import V0040OpenapiJobInfoRespMeta
        from ..models.v0040_openapi_job_info_resp_warnings import V0040OpenapiJobInfoRespWarnings

        d = dict(src_dict)
        jobs = V0040OpenapiJobInfoRespJobs.from_dict(d.pop("jobs"))

        last_backfill = V0040OpenapiJobInfoRespLastBackfill.from_dict(d.pop("last_backfill"))

        last_update = V0040OpenapiJobInfoRespLastUpdate.from_dict(d.pop("last_update"))

        _meta = d.pop("meta", UNSET)
        meta: Union[Unset, V0040OpenapiJobInfoRespMeta]
        if isinstance(_meta, Unset):
            meta = UNSET
        else:
            meta = V0040OpenapiJobInfoRespMeta.from_dict(_meta)

        _errors = d.pop("errors", UNSET)
        errors: Union[Unset, V0040OpenapiJobInfoRespErrors]
        if isinstance(_errors, Unset):
            errors = UNSET
        else:
            errors = V0040OpenapiJobInfoRespErrors.from_dict(_errors)

        _warnings = d.pop("warnings", UNSET)
        warnings: Union[Unset, V0040OpenapiJobInfoRespWarnings]
        if isinstance(_warnings, Unset):
            warnings = UNSET
        else:
            warnings = V0040OpenapiJobInfoRespWarnings.from_dict(_warnings)

        v0040_openapi_job_info_resp = cls(
            jobs=jobs,
            last_backfill=last_backfill,
            last_update=last_update,
            meta=meta,
            errors=errors,
            warnings=warnings,
        )

        v0040_openapi_job_info_resp.additional_properties = d
        return v0040_openapi_job_info_resp

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
