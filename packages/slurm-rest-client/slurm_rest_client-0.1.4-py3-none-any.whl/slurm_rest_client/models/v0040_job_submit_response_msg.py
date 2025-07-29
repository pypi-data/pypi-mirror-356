from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="V0040JobSubmitResponseMsg")


@_attrs_define
class V0040JobSubmitResponseMsg:
    """
    Attributes:
        job_id (Union[Unset, int]):
        step_id (Union[Unset, str]):
        error_code (Union[Unset, int]):
        error (Union[Unset, str]):
        job_submit_user_msg (Union[Unset, str]):
    """

    job_id: Union[Unset, int] = UNSET
    step_id: Union[Unset, str] = UNSET
    error_code: Union[Unset, int] = UNSET
    error: Union[Unset, str] = UNSET
    job_submit_user_msg: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        job_id = self.job_id

        step_id = self.step_id

        error_code = self.error_code

        error = self.error

        job_submit_user_msg = self.job_submit_user_msg

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if job_id is not UNSET:
            field_dict["job_id"] = job_id
        if step_id is not UNSET:
            field_dict["step_id"] = step_id
        if error_code is not UNSET:
            field_dict["error_code"] = error_code
        if error is not UNSET:
            field_dict["error"] = error
        if job_submit_user_msg is not UNSET:
            field_dict["job_submit_user_msg"] = job_submit_user_msg

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        job_id = d.pop("job_id", UNSET)

        step_id = d.pop("step_id", UNSET)

        error_code = d.pop("error_code", UNSET)

        error = d.pop("error", UNSET)

        job_submit_user_msg = d.pop("job_submit_user_msg", UNSET)

        v0040_job_submit_response_msg = cls(
            job_id=job_id,
            step_id=step_id,
            error_code=error_code,
            error=error,
            job_submit_user_msg=job_submit_user_msg,
        )

        v0040_job_submit_response_msg.additional_properties = d
        return v0040_job_submit_response_msg

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
