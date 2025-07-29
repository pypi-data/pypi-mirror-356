from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_assoc_shares_obj_wrap_tres_group_minutes import V0040AssocSharesObjWrapTresGroupMinutes
    from ..models.v0040_assoc_shares_obj_wrap_tres_run_seconds import V0040AssocSharesObjWrapTresRunSeconds
    from ..models.v0040_assoc_shares_obj_wrap_tres_usage import V0040AssocSharesObjWrapTresUsage


T = TypeVar("T", bound="V0040AssocSharesObjWrapTres")


@_attrs_define
class V0040AssocSharesObjWrapTres:
    """
    Attributes:
        run_seconds (Union[Unset, V0040AssocSharesObjWrapTresRunSeconds]):
        group_minutes (Union[Unset, V0040AssocSharesObjWrapTresGroupMinutes]):
        usage (Union[Unset, V0040AssocSharesObjWrapTresUsage]):
    """

    run_seconds: Union[Unset, "V0040AssocSharesObjWrapTresRunSeconds"] = UNSET
    group_minutes: Union[Unset, "V0040AssocSharesObjWrapTresGroupMinutes"] = UNSET
    usage: Union[Unset, "V0040AssocSharesObjWrapTresUsage"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        run_seconds: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.run_seconds, Unset):
            run_seconds = self.run_seconds.to_dict()

        group_minutes: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.group_minutes, Unset):
            group_minutes = self.group_minutes.to_dict()

        usage: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.usage, Unset):
            usage = self.usage.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if run_seconds is not UNSET:
            field_dict["run_seconds"] = run_seconds
        if group_minutes is not UNSET:
            field_dict["group_minutes"] = group_minutes
        if usage is not UNSET:
            field_dict["usage"] = usage

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0040_assoc_shares_obj_wrap_tres_group_minutes import V0040AssocSharesObjWrapTresGroupMinutes
        from ..models.v0040_assoc_shares_obj_wrap_tres_run_seconds import V0040AssocSharesObjWrapTresRunSeconds
        from ..models.v0040_assoc_shares_obj_wrap_tres_usage import V0040AssocSharesObjWrapTresUsage

        d = dict(src_dict)
        _run_seconds = d.pop("run_seconds", UNSET)
        run_seconds: Union[Unset, V0040AssocSharesObjWrapTresRunSeconds]
        if isinstance(_run_seconds, Unset):
            run_seconds = UNSET
        else:
            run_seconds = V0040AssocSharesObjWrapTresRunSeconds.from_dict(_run_seconds)

        _group_minutes = d.pop("group_minutes", UNSET)
        group_minutes: Union[Unset, V0040AssocSharesObjWrapTresGroupMinutes]
        if isinstance(_group_minutes, Unset):
            group_minutes = UNSET
        else:
            group_minutes = V0040AssocSharesObjWrapTresGroupMinutes.from_dict(_group_minutes)

        _usage = d.pop("usage", UNSET)
        usage: Union[Unset, V0040AssocSharesObjWrapTresUsage]
        if isinstance(_usage, Unset):
            usage = UNSET
        else:
            usage = V0040AssocSharesObjWrapTresUsage.from_dict(_usage)

        v0040_assoc_shares_obj_wrap_tres = cls(
            run_seconds=run_seconds,
            group_minutes=group_minutes,
            usage=usage,
        )

        v0040_assoc_shares_obj_wrap_tres.additional_properties = d
        return v0040_assoc_shares_obj_wrap_tres

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
