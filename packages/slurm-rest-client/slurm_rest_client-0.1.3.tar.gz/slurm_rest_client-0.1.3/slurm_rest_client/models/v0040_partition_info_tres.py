from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="V0040PartitionInfoTres")


@_attrs_define
class V0040PartitionInfoTres:
    """
    Attributes:
        billing_weights (Union[Unset, str]):
        configured (Union[Unset, str]):
    """

    billing_weights: Union[Unset, str] = UNSET
    configured: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        billing_weights = self.billing_weights

        configured = self.configured

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if billing_weights is not UNSET:
            field_dict["billing_weights"] = billing_weights
        if configured is not UNSET:
            field_dict["configured"] = configured

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        billing_weights = d.pop("billing_weights", UNSET)

        configured = d.pop("configured", UNSET)

        v0040_partition_info_tres = cls(
            billing_weights=billing_weights,
            configured=configured,
        )

        v0040_partition_info_tres.additional_properties = d
        return v0040_partition_info_tres

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
