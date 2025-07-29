from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_job_array_limits import V0040JobArrayLimits


T = TypeVar("T", bound="V0040JobArray")


@_attrs_define
class V0040JobArray:
    """
    Attributes:
        job_id (Union[Unset, int]):
        limits (Union[Unset, V0040JobArrayLimits]):
        task_id (Union[Unset, int]):
        task (Union[Unset, str]):
    """

    job_id: Union[Unset, int] = UNSET
    limits: Union[Unset, "V0040JobArrayLimits"] = UNSET
    task_id: Union[Unset, int] = UNSET
    task: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        job_id = self.job_id

        limits: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.limits, Unset):
            limits = self.limits.to_dict()

        task_id = self.task_id

        task = self.task

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if job_id is not UNSET:
            field_dict["job_id"] = job_id
        if limits is not UNSET:
            field_dict["limits"] = limits
        if task_id is not UNSET:
            field_dict["task_id"] = task_id
        if task is not UNSET:
            field_dict["task"] = task

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0040_job_array_limits import V0040JobArrayLimits

        d = dict(src_dict)
        job_id = d.pop("job_id", UNSET)

        _limits = d.pop("limits", UNSET)
        limits: Union[Unset, V0040JobArrayLimits]
        if isinstance(_limits, Unset):
            limits = UNSET
        else:
            limits = V0040JobArrayLimits.from_dict(_limits)

        task_id = d.pop("task_id", UNSET)

        task = d.pop("task", UNSET)

        v0040_job_array = cls(
            job_id=job_id,
            limits=limits,
            task_id=task_id,
            task=task,
        )

        v0040_job_array.additional_properties = d
        return v0040_job_array

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
