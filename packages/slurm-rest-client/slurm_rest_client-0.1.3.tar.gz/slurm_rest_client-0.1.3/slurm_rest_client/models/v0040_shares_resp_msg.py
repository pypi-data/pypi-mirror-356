from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_shares_resp_msg_shares import V0040SharesRespMsgShares


T = TypeVar("T", bound="V0040SharesRespMsg")


@_attrs_define
class V0040SharesRespMsg:
    """
    Attributes:
        shares (Union[Unset, V0040SharesRespMsgShares]):
        total_shares (Union[Unset, int]): Total number of shares
    """

    shares: Union[Unset, "V0040SharesRespMsgShares"] = UNSET
    total_shares: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        shares: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.shares, Unset):
            shares = self.shares.to_dict()

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
        from ..models.v0040_shares_resp_msg_shares import V0040SharesRespMsgShares

        d = dict(src_dict)
        _shares = d.pop("shares", UNSET)
        shares: Union[Unset, V0040SharesRespMsgShares]
        if isinstance(_shares, Unset):
            shares = UNSET
        else:
            shares = V0040SharesRespMsgShares.from_dict(_shares)

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
