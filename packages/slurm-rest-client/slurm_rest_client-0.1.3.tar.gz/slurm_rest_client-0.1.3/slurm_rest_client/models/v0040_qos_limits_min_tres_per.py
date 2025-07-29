from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_qos_limits_min_tres_per_job import V0040QosLimitsMinTresPerJob


T = TypeVar("T", bound="V0040QosLimitsMinTresPer")


@_attrs_define
class V0040QosLimitsMinTresPer:
    """
    Attributes:
        job (Union[Unset, V0040QosLimitsMinTresPerJob]):
    """

    job: Union[Unset, "V0040QosLimitsMinTresPerJob"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        job: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.job, Unset):
            job = self.job.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if job is not UNSET:
            field_dict["job"] = job

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0040_qos_limits_min_tres_per_job import V0040QosLimitsMinTresPerJob

        d = dict(src_dict)
        _job = d.pop("job", UNSET)
        job: Union[Unset, V0040QosLimitsMinTresPerJob]
        if isinstance(_job, Unset):
            job = UNSET
        else:
            job = V0040QosLimitsMinTresPerJob.from_dict(_job)

        v0040_qos_limits_min_tres_per = cls(
            job=job,
        )

        v0040_qos_limits_min_tres_per.additional_properties = d
        return v0040_qos_limits_min_tres_per

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
