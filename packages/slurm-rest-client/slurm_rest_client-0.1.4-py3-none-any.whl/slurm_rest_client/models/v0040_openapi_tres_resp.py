from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_openapi_error import V0040OpenapiError
    from ..models.v0040_openapi_meta import V0040OpenapiMeta
    from ..models.v0040_openapi_warning import V0040OpenapiWarning
    from ..models.v0040_tres import V0040Tres


T = TypeVar("T", bound="V0040OpenapiTresResp")


@_attrs_define
class V0040OpenapiTresResp:
    """
    Attributes:
        tres (list['V0040Tres']):
        meta (Union[Unset, V0040OpenapiMeta]):
        errors (Union[Unset, list['V0040OpenapiError']]):
        warnings (Union[Unset, list['V0040OpenapiWarning']]):
    """

    tres: list["V0040Tres"]
    meta: Union[Unset, "V0040OpenapiMeta"] = UNSET
    errors: Union[Unset, list["V0040OpenapiError"]] = UNSET
    warnings: Union[Unset, list["V0040OpenapiWarning"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        tres = []
        for componentsschemasv0_0_40_tres_list_item_data in self.tres:
            componentsschemasv0_0_40_tres_list_item = componentsschemasv0_0_40_tres_list_item_data.to_dict()
            tres.append(componentsschemasv0_0_40_tres_list_item)

        meta: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.meta, Unset):
            meta = self.meta.to_dict()

        errors: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.errors, Unset):
            errors = []
            for componentsschemasv0_0_40_openapi_errors_item_data in self.errors:
                componentsschemasv0_0_40_openapi_errors_item = (
                    componentsschemasv0_0_40_openapi_errors_item_data.to_dict()
                )
                errors.append(componentsschemasv0_0_40_openapi_errors_item)

        warnings: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.warnings, Unset):
            warnings = []
            for componentsschemasv0_0_40_openapi_warnings_item_data in self.warnings:
                componentsschemasv0_0_40_openapi_warnings_item = (
                    componentsschemasv0_0_40_openapi_warnings_item_data.to_dict()
                )
                warnings.append(componentsschemasv0_0_40_openapi_warnings_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "TRES": tres,
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
        from ..models.v0040_openapi_error import V0040OpenapiError
        from ..models.v0040_openapi_meta import V0040OpenapiMeta
        from ..models.v0040_openapi_warning import V0040OpenapiWarning
        from ..models.v0040_tres import V0040Tres

        d = dict(src_dict)
        tres = []
        _tres = d.pop("TRES")
        for componentsschemasv0_0_40_tres_list_item_data in _tres:
            componentsschemasv0_0_40_tres_list_item = V0040Tres.from_dict(componentsschemasv0_0_40_tres_list_item_data)

            tres.append(componentsschemasv0_0_40_tres_list_item)

        _meta = d.pop("meta", UNSET)
        meta: Union[Unset, V0040OpenapiMeta]
        if isinstance(_meta, Unset):
            meta = UNSET
        else:
            meta = V0040OpenapiMeta.from_dict(_meta)

        errors = []
        _errors = d.pop("errors", UNSET)
        for componentsschemasv0_0_40_openapi_errors_item_data in _errors or []:
            componentsschemasv0_0_40_openapi_errors_item = V0040OpenapiError.from_dict(
                componentsschemasv0_0_40_openapi_errors_item_data
            )

            errors.append(componentsschemasv0_0_40_openapi_errors_item)

        warnings = []
        _warnings = d.pop("warnings", UNSET)
        for componentsschemasv0_0_40_openapi_warnings_item_data in _warnings or []:
            componentsschemasv0_0_40_openapi_warnings_item = V0040OpenapiWarning.from_dict(
                componentsschemasv0_0_40_openapi_warnings_item_data
            )

            warnings.append(componentsschemasv0_0_40_openapi_warnings_item)

        v0040_openapi_tres_resp = cls(
            tres=tres,
            meta=meta,
            errors=errors,
            warnings=warnings,
        )

        v0040_openapi_tres_resp.additional_properties = d
        return v0040_openapi_tres_resp

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
