from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_openapi_users_add_cond_resp_str_errors import V0040OpenapiUsersAddCondRespStrErrors
    from ..models.v0040_openapi_users_add_cond_resp_str_meta import V0040OpenapiUsersAddCondRespStrMeta
    from ..models.v0040_openapi_users_add_cond_resp_str_warnings import V0040OpenapiUsersAddCondRespStrWarnings


T = TypeVar("T", bound="V0040OpenapiUsersAddCondRespStr")


@_attrs_define
class V0040OpenapiUsersAddCondRespStr:
    """
    Attributes:
        added_users (str): added_users
        meta (Union[Unset, V0040OpenapiUsersAddCondRespStrMeta]):
        errors (Union[Unset, V0040OpenapiUsersAddCondRespStrErrors]):
        warnings (Union[Unset, V0040OpenapiUsersAddCondRespStrWarnings]):
    """

    added_users: str
    meta: Union[Unset, "V0040OpenapiUsersAddCondRespStrMeta"] = UNSET
    errors: Union[Unset, "V0040OpenapiUsersAddCondRespStrErrors"] = UNSET
    warnings: Union[Unset, "V0040OpenapiUsersAddCondRespStrWarnings"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        added_users = self.added_users

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
                "added_users": added_users,
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
        from ..models.v0040_openapi_users_add_cond_resp_str_errors import V0040OpenapiUsersAddCondRespStrErrors
        from ..models.v0040_openapi_users_add_cond_resp_str_meta import V0040OpenapiUsersAddCondRespStrMeta
        from ..models.v0040_openapi_users_add_cond_resp_str_warnings import V0040OpenapiUsersAddCondRespStrWarnings

        d = dict(src_dict)
        added_users = d.pop("added_users")

        _meta = d.pop("meta", UNSET)
        meta: Union[Unset, V0040OpenapiUsersAddCondRespStrMeta]
        if isinstance(_meta, Unset):
            meta = UNSET
        else:
            meta = V0040OpenapiUsersAddCondRespStrMeta.from_dict(_meta)

        _errors = d.pop("errors", UNSET)
        errors: Union[Unset, V0040OpenapiUsersAddCondRespStrErrors]
        if isinstance(_errors, Unset):
            errors = UNSET
        else:
            errors = V0040OpenapiUsersAddCondRespStrErrors.from_dict(_errors)

        _warnings = d.pop("warnings", UNSET)
        warnings: Union[Unset, V0040OpenapiUsersAddCondRespStrWarnings]
        if isinstance(_warnings, Unset):
            warnings = UNSET
        else:
            warnings = V0040OpenapiUsersAddCondRespStrWarnings.from_dict(_warnings)

        v0040_openapi_users_add_cond_resp_str = cls(
            added_users=added_users,
            meta=meta,
            errors=errors,
            warnings=warnings,
        )

        v0040_openapi_users_add_cond_resp_str.additional_properties = d
        return v0040_openapi_users_add_cond_resp_str

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
