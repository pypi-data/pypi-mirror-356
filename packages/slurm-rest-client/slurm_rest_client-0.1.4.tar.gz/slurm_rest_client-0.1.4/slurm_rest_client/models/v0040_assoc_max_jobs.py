from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_assoc_max_jobs_per import V0040AssocMaxJobsPer


T = TypeVar("T", bound="V0040AssocMaxJobs")


@_attrs_define
class V0040AssocMaxJobs:
    """
    Attributes:
        per (Union[Unset, V0040AssocMaxJobsPer]):
        active (Union[Unset, int]):
        accruing (Union[Unset, int]):
        total (Union[Unset, int]):
    """

    per: Union[Unset, "V0040AssocMaxJobsPer"] = UNSET
    active: Union[Unset, int] = UNSET
    accruing: Union[Unset, int] = UNSET
    total: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        per: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.per, Unset):
            per = self.per.to_dict()

        active = self.active

        accruing = self.accruing

        total = self.total

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if per is not UNSET:
            field_dict["per"] = per
        if active is not UNSET:
            field_dict["active"] = active
        if accruing is not UNSET:
            field_dict["accruing"] = accruing
        if total is not UNSET:
            field_dict["total"] = total

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0040_assoc_max_jobs_per import V0040AssocMaxJobsPer

        d = dict(src_dict)
        _per = d.pop("per", UNSET)
        per: Union[Unset, V0040AssocMaxJobsPer]
        if isinstance(_per, Unset):
            per = UNSET
        else:
            per = V0040AssocMaxJobsPer.from_dict(_per)

        active = d.pop("active", UNSET)

        accruing = d.pop("accruing", UNSET)

        total = d.pop("total", UNSET)

        v0040_assoc_max_jobs = cls(
            per=per,
            active=active,
            accruing=accruing,
            total=total,
        )

        v0040_assoc_max_jobs.additional_properties = d
        return v0040_assoc_max_jobs

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
