from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_openapi_job_submit_response_errors import V0040OpenapiJobSubmitResponseErrors
    from ..models.v0040_openapi_job_submit_response_meta import V0040OpenapiJobSubmitResponseMeta
    from ..models.v0040_openapi_job_submit_response_result import V0040OpenapiJobSubmitResponseResult
    from ..models.v0040_openapi_job_submit_response_warnings import V0040OpenapiJobSubmitResponseWarnings


T = TypeVar("T", bound="V0040OpenapiJobSubmitResponse")


@_attrs_define
class V0040OpenapiJobSubmitResponse:
    """
    Attributes:
        result (Union[Unset, V0040OpenapiJobSubmitResponseResult]):
        job_id (Union[Unset, int]): submited JobId
        step_id (Union[Unset, str]): submited StepID
        job_submit_user_msg (Union[Unset, str]): job submision user message
        meta (Union[Unset, V0040OpenapiJobSubmitResponseMeta]):
        errors (Union[Unset, V0040OpenapiJobSubmitResponseErrors]):
        warnings (Union[Unset, V0040OpenapiJobSubmitResponseWarnings]):
    """

    result: Union[Unset, "V0040OpenapiJobSubmitResponseResult"] = UNSET
    job_id: Union[Unset, int] = UNSET
    step_id: Union[Unset, str] = UNSET
    job_submit_user_msg: Union[Unset, str] = UNSET
    meta: Union[Unset, "V0040OpenapiJobSubmitResponseMeta"] = UNSET
    errors: Union[Unset, "V0040OpenapiJobSubmitResponseErrors"] = UNSET
    warnings: Union[Unset, "V0040OpenapiJobSubmitResponseWarnings"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        result: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.result, Unset):
            result = self.result.to_dict()

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
        if result is not UNSET:
            field_dict["result"] = result
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
        from ..models.v0040_openapi_job_submit_response_errors import V0040OpenapiJobSubmitResponseErrors
        from ..models.v0040_openapi_job_submit_response_meta import V0040OpenapiJobSubmitResponseMeta
        from ..models.v0040_openapi_job_submit_response_result import V0040OpenapiJobSubmitResponseResult
        from ..models.v0040_openapi_job_submit_response_warnings import V0040OpenapiJobSubmitResponseWarnings

        d = dict(src_dict)
        _result = d.pop("result", UNSET)
        result: Union[Unset, V0040OpenapiJobSubmitResponseResult]
        if isinstance(_result, Unset):
            result = UNSET
        else:
            result = V0040OpenapiJobSubmitResponseResult.from_dict(_result)

        job_id = d.pop("job_id", UNSET)

        step_id = d.pop("step_id", UNSET)

        job_submit_user_msg = d.pop("job_submit_user_msg", UNSET)

        _meta = d.pop("meta", UNSET)
        meta: Union[Unset, V0040OpenapiJobSubmitResponseMeta]
        if isinstance(_meta, Unset):
            meta = UNSET
        else:
            meta = V0040OpenapiJobSubmitResponseMeta.from_dict(_meta)

        _errors = d.pop("errors", UNSET)
        errors: Union[Unset, V0040OpenapiJobSubmitResponseErrors]
        if isinstance(_errors, Unset):
            errors = UNSET
        else:
            errors = V0040OpenapiJobSubmitResponseErrors.from_dict(_errors)

        _warnings = d.pop("warnings", UNSET)
        warnings: Union[Unset, V0040OpenapiJobSubmitResponseWarnings]
        if isinstance(_warnings, Unset):
            warnings = UNSET
        else:
            warnings = V0040OpenapiJobSubmitResponseWarnings.from_dict(_warnings)

        v0040_openapi_job_submit_response = cls(
            result=result,
            job_id=job_id,
            step_id=step_id,
            job_submit_user_msg=job_submit_user_msg,
            meta=meta,
            errors=errors,
            warnings=warnings,
        )

        v0040_openapi_job_submit_response.additional_properties = d
        return v0040_openapi_job_submit_response

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
