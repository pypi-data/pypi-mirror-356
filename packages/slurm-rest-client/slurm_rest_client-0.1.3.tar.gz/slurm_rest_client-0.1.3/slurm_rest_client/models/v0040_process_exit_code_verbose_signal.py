from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_process_exit_code_verbose_signal_id import V0040ProcessExitCodeVerboseSignalId


T = TypeVar("T", bound="V0040ProcessExitCodeVerboseSignal")


@_attrs_define
class V0040ProcessExitCodeVerboseSignal:
    """
    Attributes:
        id (Union[Unset, V0040ProcessExitCodeVerboseSignalId]):
        name (Union[Unset, str]): Signal sent to process
    """

    id: Union[Unset, "V0040ProcessExitCodeVerboseSignalId"] = UNSET
    name: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.id, Unset):
            id = self.id.to_dict()

        name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0040_process_exit_code_verbose_signal_id import V0040ProcessExitCodeVerboseSignalId

        d = dict(src_dict)
        _id = d.pop("id", UNSET)
        id: Union[Unset, V0040ProcessExitCodeVerboseSignalId]
        if isinstance(_id, Unset):
            id = UNSET
        else:
            id = V0040ProcessExitCodeVerboseSignalId.from_dict(_id)

        name = d.pop("name", UNSET)

        v0040_process_exit_code_verbose_signal = cls(
            id=id,
            name=name,
        )

        v0040_process_exit_code_verbose_signal.additional_properties = d
        return v0040_process_exit_code_verbose_signal

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
