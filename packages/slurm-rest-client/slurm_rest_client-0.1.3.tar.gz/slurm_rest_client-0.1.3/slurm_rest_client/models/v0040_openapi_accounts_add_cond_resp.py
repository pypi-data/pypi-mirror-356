from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_openapi_accounts_add_cond_resp_account import V0040OpenapiAccountsAddCondRespAccount
    from ..models.v0040_openapi_accounts_add_cond_resp_association_condition import (
        V0040OpenapiAccountsAddCondRespAssociationCondition,
    )
    from ..models.v0040_openapi_accounts_add_cond_resp_errors import V0040OpenapiAccountsAddCondRespErrors
    from ..models.v0040_openapi_accounts_add_cond_resp_meta import V0040OpenapiAccountsAddCondRespMeta
    from ..models.v0040_openapi_accounts_add_cond_resp_warnings import V0040OpenapiAccountsAddCondRespWarnings


T = TypeVar("T", bound="V0040OpenapiAccountsAddCondResp")


@_attrs_define
class V0040OpenapiAccountsAddCondResp:
    """
    Attributes:
        association_condition (Union[Unset, V0040OpenapiAccountsAddCondRespAssociationCondition]):
        account (Union[Unset, V0040OpenapiAccountsAddCondRespAccount]):
        meta (Union[Unset, V0040OpenapiAccountsAddCondRespMeta]):
        errors (Union[Unset, V0040OpenapiAccountsAddCondRespErrors]):
        warnings (Union[Unset, V0040OpenapiAccountsAddCondRespWarnings]):
    """

    association_condition: Union[Unset, "V0040OpenapiAccountsAddCondRespAssociationCondition"] = UNSET
    account: Union[Unset, "V0040OpenapiAccountsAddCondRespAccount"] = UNSET
    meta: Union[Unset, "V0040OpenapiAccountsAddCondRespMeta"] = UNSET
    errors: Union[Unset, "V0040OpenapiAccountsAddCondRespErrors"] = UNSET
    warnings: Union[Unset, "V0040OpenapiAccountsAddCondRespWarnings"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        association_condition: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.association_condition, Unset):
            association_condition = self.association_condition.to_dict()

        account: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.account, Unset):
            account = self.account.to_dict()

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
        field_dict.update({})
        if association_condition is not UNSET:
            field_dict["association_condition"] = association_condition
        if account is not UNSET:
            field_dict["account"] = account
        if meta is not UNSET:
            field_dict["meta"] = meta
        if errors is not UNSET:
            field_dict["errors"] = errors
        if warnings is not UNSET:
            field_dict["warnings"] = warnings

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0040_openapi_accounts_add_cond_resp_account import V0040OpenapiAccountsAddCondRespAccount
        from ..models.v0040_openapi_accounts_add_cond_resp_association_condition import (
            V0040OpenapiAccountsAddCondRespAssociationCondition,
        )
        from ..models.v0040_openapi_accounts_add_cond_resp_errors import V0040OpenapiAccountsAddCondRespErrors
        from ..models.v0040_openapi_accounts_add_cond_resp_meta import V0040OpenapiAccountsAddCondRespMeta
        from ..models.v0040_openapi_accounts_add_cond_resp_warnings import V0040OpenapiAccountsAddCondRespWarnings

        d = dict(src_dict)
        _association_condition = d.pop("association_condition", UNSET)
        association_condition: Union[Unset, V0040OpenapiAccountsAddCondRespAssociationCondition]
        if isinstance(_association_condition, Unset):
            association_condition = UNSET
        else:
            association_condition = V0040OpenapiAccountsAddCondRespAssociationCondition.from_dict(
                _association_condition
            )

        _account = d.pop("account", UNSET)
        account: Union[Unset, V0040OpenapiAccountsAddCondRespAccount]
        if isinstance(_account, Unset):
            account = UNSET
        else:
            account = V0040OpenapiAccountsAddCondRespAccount.from_dict(_account)

        _meta = d.pop("meta", UNSET)
        meta: Union[Unset, V0040OpenapiAccountsAddCondRespMeta]
        if isinstance(_meta, Unset):
            meta = UNSET
        else:
            meta = V0040OpenapiAccountsAddCondRespMeta.from_dict(_meta)

        _errors = d.pop("errors", UNSET)
        errors: Union[Unset, V0040OpenapiAccountsAddCondRespErrors]
        if isinstance(_errors, Unset):
            errors = UNSET
        else:
            errors = V0040OpenapiAccountsAddCondRespErrors.from_dict(_errors)

        _warnings = d.pop("warnings", UNSET)
        warnings: Union[Unset, V0040OpenapiAccountsAddCondRespWarnings]
        if isinstance(_warnings, Unset):
            warnings = UNSET
        else:
            warnings = V0040OpenapiAccountsAddCondRespWarnings.from_dict(_warnings)

        v0040_openapi_accounts_add_cond_resp = cls(
            association_condition=association_condition,
            account=account,
            meta=meta,
            errors=errors,
            warnings=warnings,
        )

        v0040_openapi_accounts_add_cond_resp.additional_properties = d
        return v0040_openapi_accounts_add_cond_resp

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
