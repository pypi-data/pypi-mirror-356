from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_openapi_instances_resp_errors import V0040OpenapiInstancesRespErrors
    from ..models.v0040_openapi_instances_resp_instances import V0040OpenapiInstancesRespInstances
    from ..models.v0040_openapi_instances_resp_meta import V0040OpenapiInstancesRespMeta
    from ..models.v0040_openapi_instances_resp_warnings import V0040OpenapiInstancesRespWarnings


T = TypeVar("T", bound="V0040OpenapiInstancesResp")


@_attrs_define
class V0040OpenapiInstancesResp:
    """
    Attributes:
        instances (V0040OpenapiInstancesRespInstances):
        meta (Union[Unset, V0040OpenapiInstancesRespMeta]):
        errors (Union[Unset, V0040OpenapiInstancesRespErrors]):
        warnings (Union[Unset, V0040OpenapiInstancesRespWarnings]):
    """

    instances: "V0040OpenapiInstancesRespInstances"
    meta: Union[Unset, "V0040OpenapiInstancesRespMeta"] = UNSET
    errors: Union[Unset, "V0040OpenapiInstancesRespErrors"] = UNSET
    warnings: Union[Unset, "V0040OpenapiInstancesRespWarnings"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        instances = self.instances.to_dict()

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
                "instances": instances,
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
        from ..models.v0040_openapi_instances_resp_errors import V0040OpenapiInstancesRespErrors
        from ..models.v0040_openapi_instances_resp_instances import V0040OpenapiInstancesRespInstances
        from ..models.v0040_openapi_instances_resp_meta import V0040OpenapiInstancesRespMeta
        from ..models.v0040_openapi_instances_resp_warnings import V0040OpenapiInstancesRespWarnings

        d = dict(src_dict)
        instances = V0040OpenapiInstancesRespInstances.from_dict(d.pop("instances"))

        _meta = d.pop("meta", UNSET)
        meta: Union[Unset, V0040OpenapiInstancesRespMeta]
        if isinstance(_meta, Unset):
            meta = UNSET
        else:
            meta = V0040OpenapiInstancesRespMeta.from_dict(_meta)

        _errors = d.pop("errors", UNSET)
        errors: Union[Unset, V0040OpenapiInstancesRespErrors]
        if isinstance(_errors, Unset):
            errors = UNSET
        else:
            errors = V0040OpenapiInstancesRespErrors.from_dict(_errors)

        _warnings = d.pop("warnings", UNSET)
        warnings: Union[Unset, V0040OpenapiInstancesRespWarnings]
        if isinstance(_warnings, Unset):
            warnings = UNSET
        else:
            warnings = V0040OpenapiInstancesRespWarnings.from_dict(_warnings)

        v0040_openapi_instances_resp = cls(
            instances=instances,
            meta=meta,
            errors=errors,
            warnings=warnings,
        )

        v0040_openapi_instances_resp.additional_properties = d
        return v0040_openapi_instances_resp

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
