from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_openapi_accounts_resp_accounts import V0040OpenapiAccountsRespAccounts
    from ..models.v0040_openapi_accounts_resp_errors import V0040OpenapiAccountsRespErrors
    from ..models.v0040_openapi_accounts_resp_meta import V0040OpenapiAccountsRespMeta
    from ..models.v0040_openapi_accounts_resp_warnings import V0040OpenapiAccountsRespWarnings


T = TypeVar("T", bound="V0040OpenapiAccountsResp")


@_attrs_define
class V0040OpenapiAccountsResp:
    """
    Attributes:
        accounts (V0040OpenapiAccountsRespAccounts):
        meta (Union[Unset, V0040OpenapiAccountsRespMeta]):
        errors (Union[Unset, V0040OpenapiAccountsRespErrors]):
        warnings (Union[Unset, V0040OpenapiAccountsRespWarnings]):
    """

    accounts: "V0040OpenapiAccountsRespAccounts"
    meta: Union[Unset, "V0040OpenapiAccountsRespMeta"] = UNSET
    errors: Union[Unset, "V0040OpenapiAccountsRespErrors"] = UNSET
    warnings: Union[Unset, "V0040OpenapiAccountsRespWarnings"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        accounts = self.accounts.to_dict()

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
                "accounts": accounts,
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
        from ..models.v0040_openapi_accounts_resp_accounts import V0040OpenapiAccountsRespAccounts
        from ..models.v0040_openapi_accounts_resp_errors import V0040OpenapiAccountsRespErrors
        from ..models.v0040_openapi_accounts_resp_meta import V0040OpenapiAccountsRespMeta
        from ..models.v0040_openapi_accounts_resp_warnings import V0040OpenapiAccountsRespWarnings

        d = dict(src_dict)
        accounts = V0040OpenapiAccountsRespAccounts.from_dict(d.pop("accounts"))

        _meta = d.pop("meta", UNSET)
        meta: Union[Unset, V0040OpenapiAccountsRespMeta]
        if isinstance(_meta, Unset):
            meta = UNSET
        else:
            meta = V0040OpenapiAccountsRespMeta.from_dict(_meta)

        _errors = d.pop("errors", UNSET)
        errors: Union[Unset, V0040OpenapiAccountsRespErrors]
        if isinstance(_errors, Unset):
            errors = UNSET
        else:
            errors = V0040OpenapiAccountsRespErrors.from_dict(_errors)

        _warnings = d.pop("warnings", UNSET)
        warnings: Union[Unset, V0040OpenapiAccountsRespWarnings]
        if isinstance(_warnings, Unset):
            warnings = UNSET
        else:
            warnings = V0040OpenapiAccountsRespWarnings.from_dict(_warnings)

        v0040_openapi_accounts_resp = cls(
            accounts=accounts,
            meta=meta,
            errors=errors,
            warnings=warnings,
        )

        v0040_openapi_accounts_resp.additional_properties = d
        return v0040_openapi_accounts_resp

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
