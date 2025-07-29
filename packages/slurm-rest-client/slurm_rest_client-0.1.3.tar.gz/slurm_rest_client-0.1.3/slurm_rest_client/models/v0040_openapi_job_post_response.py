from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_openapi_job_post_response_errors import V0040OpenapiJobPostResponseErrors
    from ..models.v0040_openapi_job_post_response_meta import V0040OpenapiJobPostResponseMeta
    from ..models.v0040_openapi_job_post_response_results import V0040OpenapiJobPostResponseResults
    from ..models.v0040_openapi_job_post_response_warnings import V0040OpenapiJobPostResponseWarnings


T = TypeVar("T", bound="V0040OpenapiJobPostResponse")


@_attrs_define
class V0040OpenapiJobPostResponse:
    """
    Attributes:
        results (Union[Unset, V0040OpenapiJobPostResponseResults]):
        job_id (Union[Unset, str]): First updated JobId - Use results instead
        step_id (Union[Unset, str]): First updated StepID - Use results instead
        job_submit_user_msg (Union[Unset, str]): First updated Job submision user message - Use results instead
        meta (Union[Unset, V0040OpenapiJobPostResponseMeta]):
        errors (Union[Unset, V0040OpenapiJobPostResponseErrors]):
        warnings (Union[Unset, V0040OpenapiJobPostResponseWarnings]):
    """

    results: Union[Unset, "V0040OpenapiJobPostResponseResults"] = UNSET
    job_id: Union[Unset, str] = UNSET
    step_id: Union[Unset, str] = UNSET
    job_submit_user_msg: Union[Unset, str] = UNSET
    meta: Union[Unset, "V0040OpenapiJobPostResponseMeta"] = UNSET
    errors: Union[Unset, "V0040OpenapiJobPostResponseErrors"] = UNSET
    warnings: Union[Unset, "V0040OpenapiJobPostResponseWarnings"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        results: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.results, Unset):
            results = self.results.to_dict()

        job_id = self.job_id

        step_id = self.step_id

        job_submit_user_msg = self.job_submit_user_msg

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
        if results is not UNSET:
            field_dict["results"] = results
        if job_id is not UNSET:
            field_dict["job_id"] = job_id
        if step_id is not UNSET:
            field_dict["step_id"] = step_id
        if job_submit_user_msg is not UNSET:
            field_dict["job_submit_user_msg"] = job_submit_user_msg
        if meta is not UNSET:
            field_dict["meta"] = meta
        if errors is not UNSET:
            field_dict["errors"] = errors
        if warnings is not UNSET:
            field_dict["warnings"] = warnings

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0040_openapi_job_post_response_errors import V0040OpenapiJobPostResponseErrors
        from ..models.v0040_openapi_job_post_response_meta import V0040OpenapiJobPostResponseMeta
        from ..models.v0040_openapi_job_post_response_results import V0040OpenapiJobPostResponseResults
        from ..models.v0040_openapi_job_post_response_warnings import V0040OpenapiJobPostResponseWarnings

        d = dict(src_dict)
        _results = d.pop("results", UNSET)
        results: Union[Unset, V0040OpenapiJobPostResponseResults]
        if isinstance(_results, Unset):
            results = UNSET
        else:
            results = V0040OpenapiJobPostResponseResults.from_dict(_results)

        job_id = d.pop("job_id", UNSET)

        step_id = d.pop("step_id", UNSET)

        job_submit_user_msg = d.pop("job_submit_user_msg", UNSET)

        _meta = d.pop("meta", UNSET)
        meta: Union[Unset, V0040OpenapiJobPostResponseMeta]
        if isinstance(_meta, Unset):
            meta = UNSET
        else:
            meta = V0040OpenapiJobPostResponseMeta.from_dict(_meta)

        _errors = d.pop("errors", UNSET)
        errors: Union[Unset, V0040OpenapiJobPostResponseErrors]
        if isinstance(_errors, Unset):
            errors = UNSET
        else:
            errors = V0040OpenapiJobPostResponseErrors.from_dict(_errors)

        _warnings = d.pop("warnings", UNSET)
        warnings: Union[Unset, V0040OpenapiJobPostResponseWarnings]
        if isinstance(_warnings, Unset):
            warnings = UNSET
        else:
            warnings = V0040OpenapiJobPostResponseWarnings.from_dict(_warnings)

        v0040_openapi_job_post_response = cls(
            results=results,
            job_id=job_id,
            step_id=step_id,
            job_submit_user_msg=job_submit_user_msg,
            meta=meta,
            errors=errors,
            warnings=warnings,
        )

        v0040_openapi_job_post_response.additional_properties = d
        return v0040_openapi_job_post_response

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
