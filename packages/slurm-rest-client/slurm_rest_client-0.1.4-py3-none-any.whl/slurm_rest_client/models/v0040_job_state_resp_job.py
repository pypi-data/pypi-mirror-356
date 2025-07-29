from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.v0040_job_state_resp_job_state_item import V0040JobStateRespJobStateItem

T = TypeVar("T", bound="V0040JobStateRespJob")


@_attrs_define
class V0040JobStateRespJob:
    """
    Attributes:
        job_id (str): JobId
        state (list[V0040JobStateRespJobStateItem]): Job state
    """

    job_id: str
    state: list[V0040JobStateRespJobStateItem]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        job_id = self.job_id

        state = []
        for state_item_data in self.state:
            state_item = state_item_data.value
            state.append(state_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "job_id": job_id,
                "state": state,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        job_id = d.pop("job_id")

        state = []
        _state = d.pop("state")
        for state_item_data in _state:
            state_item = V0040JobStateRespJobStateItem(state_item_data)

            state.append(state_item)

        v0040_job_state_resp_job = cls(
            job_id=job_id,
            state=state,
        )

        v0040_job_state_resp_job.additional_properties = d
        return v0040_job_state_resp_job

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
