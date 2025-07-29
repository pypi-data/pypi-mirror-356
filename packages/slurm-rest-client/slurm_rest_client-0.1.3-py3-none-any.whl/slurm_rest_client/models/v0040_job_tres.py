from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_job_tres_allocated import V0040JobTresAllocated
    from ..models.v0040_job_tres_requested import V0040JobTresRequested


T = TypeVar("T", bound="V0040JobTres")


@_attrs_define
class V0040JobTres:
    """
    Attributes:
        allocated (Union[Unset, V0040JobTresAllocated]):
        requested (Union[Unset, V0040JobTresRequested]):
    """

    allocated: Union[Unset, "V0040JobTresAllocated"] = UNSET
    requested: Union[Unset, "V0040JobTresRequested"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        allocated: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.allocated, Unset):
            allocated = self.allocated.to_dict()

        requested: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.requested, Unset):
            requested = self.requested.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if allocated is not UNSET:
            field_dict["allocated"] = allocated
        if requested is not UNSET:
            field_dict["requested"] = requested

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0040_job_tres_allocated import V0040JobTresAllocated
        from ..models.v0040_job_tres_requested import V0040JobTresRequested

        d = dict(src_dict)
        _allocated = d.pop("allocated", UNSET)
        allocated: Union[Unset, V0040JobTresAllocated]
        if isinstance(_allocated, Unset):
            allocated = UNSET
        else:
            allocated = V0040JobTresAllocated.from_dict(_allocated)

        _requested = d.pop("requested", UNSET)
        requested: Union[Unset, V0040JobTresRequested]
        if isinstance(_requested, Unset):
            requested = UNSET
        else:
            requested = V0040JobTresRequested.from_dict(_requested)

        v0040_job_tres = cls(
            allocated=allocated,
            requested=requested,
        )

        v0040_job_tres.additional_properties = d
        return v0040_job_tres

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
