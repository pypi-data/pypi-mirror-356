from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_assoc_shares_obj_wrap import V0040AssocSharesObjWrap


T = TypeVar("T", bound="V0040SharesRespMsg")


@_attrs_define
class V0040SharesRespMsg:
    """
    Attributes:
        shares (Union[Unset, list['V0040AssocSharesObjWrap']]):
        total_shares (Union[Unset, int]): Total number of shares
    """

    shares: Union[Unset, list["V0040AssocSharesObjWrap"]] = UNSET
    total_shares: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        shares: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.shares, Unset):
            shares = []
            for componentsschemasv0_0_40_assoc_shares_obj_list_item_data in self.shares:
                componentsschemasv0_0_40_assoc_shares_obj_list_item = (
                    componentsschemasv0_0_40_assoc_shares_obj_list_item_data.to_dict()
                )
                shares.append(componentsschemasv0_0_40_assoc_shares_obj_list_item)

        total_shares = self.total_shares

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if shares is not UNSET:
            field_dict["shares"] = shares
        if total_shares is not UNSET:
            field_dict["total_shares"] = total_shares

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0040_assoc_shares_obj_wrap import V0040AssocSharesObjWrap

        d = dict(src_dict)
        shares = []
        _shares = d.pop("shares", UNSET)
        for componentsschemasv0_0_40_assoc_shares_obj_list_item_data in _shares or []:
            componentsschemasv0_0_40_assoc_shares_obj_list_item = V0040AssocSharesObjWrap.from_dict(
                componentsschemasv0_0_40_assoc_shares_obj_list_item_data
            )

            shares.append(componentsschemasv0_0_40_assoc_shares_obj_list_item)

        total_shares = d.pop("total_shares", UNSET)

        v0040_shares_resp_msg = cls(
            shares=shares,
            total_shares=total_shares,
        )

        v0040_shares_resp_msg.additional_properties = d
        return v0040_shares_resp_msg

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
