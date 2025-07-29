from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_openapi_accounts_add_cond_resp_str_errors import V0040OpenapiAccountsAddCondRespStrErrors
    from ..models.v0040_openapi_accounts_add_cond_resp_str_meta import V0040OpenapiAccountsAddCondRespStrMeta
    from ..models.v0040_openapi_accounts_add_cond_resp_str_warnings import V0040OpenapiAccountsAddCondRespStrWarnings


T = TypeVar("T", bound="V0040OpenapiAccountsAddCondRespStr")


@_attrs_define
class V0040OpenapiAccountsAddCondRespStr:
    """
    Attributes:
        added_accounts (str): added_accounts
        meta (Union[Unset, V0040OpenapiAccountsAddCondRespStrMeta]):
        errors (Union[Unset, V0040OpenapiAccountsAddCondRespStrErrors]):
        warnings (Union[Unset, V0040OpenapiAccountsAddCondRespStrWarnings]):
    """

    added_accounts: str
    meta: Union[Unset, "V0040OpenapiAccountsAddCondRespStrMeta"] = UNSET
    errors: Union[Unset, "V0040OpenapiAccountsAddCondRespStrErrors"] = UNSET
    warnings: Union[Unset, "V0040OpenapiAccountsAddCondRespStrWarnings"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        added_accounts = self.added_accounts

        meta: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.meta, Unset):
            meta = self.meta.to_dict()

        errors: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.errors, Unset):
            errors = self.errors.to_dict()

        warnings: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.warnings, Unset):
            warnings = self.warnings.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "added_accounts": added_accounts,
            }
        )
        if meta is not UNSET:
            field_dict["meta"] = meta
        if errors is not UNSET:
            field_dict["errors"] = errors
        if warnings is not UNSET:
            field_dict["warnings"] = warnings

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0040_openapi_accounts_add_cond_resp_str_errors import V0040OpenapiAccountsAddCondRespStrErrors
        from ..models.v0040_openapi_accounts_add_cond_resp_str_meta import V0040OpenapiAccountsAddCondRespStrMeta
        from ..models.v0040_openapi_accounts_add_cond_resp_str_warnings import (
            V0040OpenapiAccountsAddCondRespStrWarnings,
        )

        d = dict(src_dict)
        added_accounts = d.pop("added_accounts")

        _meta = d.pop("meta", UNSET)
        meta: Union[Unset, V0040OpenapiAccountsAddCondRespStrMeta]
        if isinstance(_meta, Unset):
            meta = UNSET
        else:
            meta = V0040OpenapiAccountsAddCondRespStrMeta.from_dict(_meta)

        _errors = d.pop("errors", UNSET)
        errors: Union[Unset, V0040OpenapiAccountsAddCondRespStrErrors]
        if isinstance(_errors, Unset):
            errors = UNSET
        else:
            errors = V0040OpenapiAccountsAddCondRespStrErrors.from_dict(_errors)

        _warnings = d.pop("warnings", UNSET)
        warnings: Union[Unset, V0040OpenapiAccountsAddCondRespStrWarnings]
        if isinstance(_warnings, Unset):
            warnings = UNSET
        else:
            warnings = V0040OpenapiAccountsAddCondRespStrWarnings.from_dict(_warnings)

        v0040_openapi_accounts_add_cond_resp_str = cls(
            added_accounts=added_accounts,
            meta=meta,
            errors=errors,
            warnings=warnings,
        )

        v0040_openapi_accounts_add_cond_resp_str.additional_properties = d
        return v0040_openapi_accounts_add_cond_resp_str

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
