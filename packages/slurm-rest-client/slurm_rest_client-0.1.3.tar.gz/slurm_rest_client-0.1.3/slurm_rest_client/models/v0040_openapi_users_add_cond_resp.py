from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_openapi_users_add_cond_resp_association_condition import (
        V0040OpenapiUsersAddCondRespAssociationCondition,
    )
    from ..models.v0040_openapi_users_add_cond_resp_errors import V0040OpenapiUsersAddCondRespErrors
    from ..models.v0040_openapi_users_add_cond_resp_meta import V0040OpenapiUsersAddCondRespMeta
    from ..models.v0040_openapi_users_add_cond_resp_user import V0040OpenapiUsersAddCondRespUser
    from ..models.v0040_openapi_users_add_cond_resp_warnings import V0040OpenapiUsersAddCondRespWarnings


T = TypeVar("T", bound="V0040OpenapiUsersAddCondResp")


@_attrs_define
class V0040OpenapiUsersAddCondResp:
    """
    Attributes:
        association_condition (V0040OpenapiUsersAddCondRespAssociationCondition):
        user (V0040OpenapiUsersAddCondRespUser):
        meta (Union[Unset, V0040OpenapiUsersAddCondRespMeta]):
        errors (Union[Unset, V0040OpenapiUsersAddCondRespErrors]):
        warnings (Union[Unset, V0040OpenapiUsersAddCondRespWarnings]):
    """

    association_condition: "V0040OpenapiUsersAddCondRespAssociationCondition"
    user: "V0040OpenapiUsersAddCondRespUser"
    meta: Union[Unset, "V0040OpenapiUsersAddCondRespMeta"] = UNSET
    errors: Union[Unset, "V0040OpenapiUsersAddCondRespErrors"] = UNSET
    warnings: Union[Unset, "V0040OpenapiUsersAddCondRespWarnings"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        association_condition = self.association_condition.to_dict()

        user = self.user.to_dict()

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
                "association_condition": association_condition,
                "user": user,
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
        from ..models.v0040_openapi_users_add_cond_resp_association_condition import (
            V0040OpenapiUsersAddCondRespAssociationCondition,
        )
        from ..models.v0040_openapi_users_add_cond_resp_errors import V0040OpenapiUsersAddCondRespErrors
        from ..models.v0040_openapi_users_add_cond_resp_meta import V0040OpenapiUsersAddCondRespMeta
        from ..models.v0040_openapi_users_add_cond_resp_user import V0040OpenapiUsersAddCondRespUser
        from ..models.v0040_openapi_users_add_cond_resp_warnings import V0040OpenapiUsersAddCondRespWarnings

        d = dict(src_dict)
        association_condition = V0040OpenapiUsersAddCondRespAssociationCondition.from_dict(
            d.pop("association_condition")
        )

        user = V0040OpenapiUsersAddCondRespUser.from_dict(d.pop("user"))

        _meta = d.pop("meta", UNSET)
        meta: Union[Unset, V0040OpenapiUsersAddCondRespMeta]
        if isinstance(_meta, Unset):
            meta = UNSET
        else:
            meta = V0040OpenapiUsersAddCondRespMeta.from_dict(_meta)

        _errors = d.pop("errors", UNSET)
        errors: Union[Unset, V0040OpenapiUsersAddCondRespErrors]
        if isinstance(_errors, Unset):
            errors = UNSET
        else:
            errors = V0040OpenapiUsersAddCondRespErrors.from_dict(_errors)

        _warnings = d.pop("warnings", UNSET)
        warnings: Union[Unset, V0040OpenapiUsersAddCondRespWarnings]
        if isinstance(_warnings, Unset):
            warnings = UNSET
        else:
            warnings = V0040OpenapiUsersAddCondRespWarnings.from_dict(_warnings)

        v0040_openapi_users_add_cond_resp = cls(
            association_condition=association_condition,
            user=user,
            meta=meta,
            errors=errors,
            warnings=warnings,
        )

        v0040_openapi_users_add_cond_resp.additional_properties = d
        return v0040_openapi_users_add_cond_resp

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
