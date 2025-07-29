from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="V0040JobArrayResponseMsgEntry")


@_attrs_define
class V0040JobArrayResponseMsgEntry:
    """
    Attributes:
        job_id (Union[Unset, int]): JobId for updated Job
        step_id (Union[Unset, str]): StepId for updated Job
        error (Union[Unset, str]): Verbose update status or error
        error_code (Union[Unset, int]): Verbose update status or error
        why (Union[Unset, str]): Update response message
    """

    job_id: Union[Unset, int] = UNSET
    step_id: Union[Unset, str] = UNSET
    error: Union[Unset, str] = UNSET
    error_code: Union[Unset, int] = UNSET
    why: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        job_id = self.job_id

        step_id = self.step_id

        error = self.error

        error_code = self.error_code

        why = self.why

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if job_id is not UNSET:
            field_dict["job_id"] = job_id
        if step_id is not UNSET:
            field_dict["step_id"] = step_id
        if error is not UNSET:
            field_dict["error"] = error
        if error_code is not UNSET:
            field_dict["error_code"] = error_code
        if why is not UNSET:
            field_dict["why"] = why

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        job_id = d.pop("job_id", UNSET)

        step_id = d.pop("step_id", UNSET)

        error = d.pop("error", UNSET)

        error_code = d.pop("error_code", UNSET)

        why = d.pop("why", UNSET)

        v0040_job_array_response_msg_entry = cls(
            job_id=job_id,
            step_id=step_id,
            error=error,
            error_code=error_code,
            why=why,
        )

        v0040_job_array_response_msg_entry.additional_properties = d
        return v0040_job_array_response_msg_entry

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
