from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="V0040ControllerPing")


@_attrs_define
class V0040ControllerPing:
    """
    Attributes:
        hostname (Union[Unset, str]):
        pinged (Union[Unset, str]):
        latency (Union[Unset, int]):
        mode (Union[Unset, str]):
    """

    hostname: Union[Unset, str] = UNSET
    pinged: Union[Unset, str] = UNSET
    latency: Union[Unset, int] = UNSET
    mode: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        hostname = self.hostname

        pinged = self.pinged

        latency = self.latency

        mode = self.mode

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if hostname is not UNSET:
            field_dict["hostname"] = hostname
        if pinged is not UNSET:
            field_dict["pinged"] = pinged
        if latency is not UNSET:
            field_dict["latency"] = latency
        if mode is not UNSET:
            field_dict["mode"] = mode

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        hostname = d.pop("hostname", UNSET)

        pinged = d.pop("pinged", UNSET)

        latency = d.pop("latency", UNSET)

        mode = d.pop("mode", UNSET)

        v0040_controller_ping = cls(
            hostname=hostname,
            pinged=pinged,
            latency=latency,
            mode=mode,
        )

        v0040_controller_ping.additional_properties = d
        return v0040_controller_ping

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
