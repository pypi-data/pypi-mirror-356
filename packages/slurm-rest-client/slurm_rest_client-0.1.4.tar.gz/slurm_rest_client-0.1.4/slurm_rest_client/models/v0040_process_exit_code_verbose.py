from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.v0040_process_exit_code_verbose_status_item import V0040ProcessExitCodeVerboseStatusItem
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_process_exit_code_verbose_signal import V0040ProcessExitCodeVerboseSignal


T = TypeVar("T", bound="V0040ProcessExitCodeVerbose")


@_attrs_define
class V0040ProcessExitCodeVerbose:
    """
    Attributes:
        status (Union[Unset, list[V0040ProcessExitCodeVerboseStatusItem]]): Status given by return code
        return_code (Union[Unset, int]):
        signal (Union[Unset, V0040ProcessExitCodeVerboseSignal]):
    """

    status: Union[Unset, list[V0040ProcessExitCodeVerboseStatusItem]] = UNSET
    return_code: Union[Unset, int] = UNSET
    signal: Union[Unset, "V0040ProcessExitCodeVerboseSignal"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        status: Union[Unset, list[str]] = UNSET
        if not isinstance(self.status, Unset):
            status = []
            for status_item_data in self.status:
                status_item = status_item_data.value
                status.append(status_item)

        return_code = self.return_code

        signal: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.signal, Unset):
            signal = self.signal.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if status is not UNSET:
            field_dict["status"] = status
        if return_code is not UNSET:
            field_dict["return_code"] = return_code
        if signal is not UNSET:
            field_dict["signal"] = signal

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0040_process_exit_code_verbose_signal import V0040ProcessExitCodeVerboseSignal

        d = dict(src_dict)
        status = []
        _status = d.pop("status", UNSET)
        for status_item_data in _status or []:
            status_item = V0040ProcessExitCodeVerboseStatusItem(status_item_data)

            status.append(status_item)

        return_code = d.pop("return_code", UNSET)

        _signal = d.pop("signal", UNSET)
        signal: Union[Unset, V0040ProcessExitCodeVerboseSignal]
        if isinstance(_signal, Unset):
            signal = UNSET
        else:
            signal = V0040ProcessExitCodeVerboseSignal.from_dict(_signal)

        v0040_process_exit_code_verbose = cls(
            status=status,
            return_code=return_code,
            signal=signal,
        )

        v0040_process_exit_code_verbose.additional_properties = d
        return v0040_process_exit_code_verbose

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
