from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_openapi_partition_resp_errors import V0040OpenapiPartitionRespErrors
    from ..models.v0040_openapi_partition_resp_last_update import V0040OpenapiPartitionRespLastUpdate
    from ..models.v0040_openapi_partition_resp_meta import V0040OpenapiPartitionRespMeta
    from ..models.v0040_openapi_partition_resp_partitions import V0040OpenapiPartitionRespPartitions
    from ..models.v0040_openapi_partition_resp_warnings import V0040OpenapiPartitionRespWarnings


T = TypeVar("T", bound="V0040OpenapiPartitionResp")


@_attrs_define
class V0040OpenapiPartitionResp:
    """
    Attributes:
        partitions (V0040OpenapiPartitionRespPartitions):
        last_update (V0040OpenapiPartitionRespLastUpdate):
        meta (Union[Unset, V0040OpenapiPartitionRespMeta]):
        errors (Union[Unset, V0040OpenapiPartitionRespErrors]):
        warnings (Union[Unset, V0040OpenapiPartitionRespWarnings]):
    """

    partitions: "V0040OpenapiPartitionRespPartitions"
    last_update: "V0040OpenapiPartitionRespLastUpdate"
    meta: Union[Unset, "V0040OpenapiPartitionRespMeta"] = UNSET
    errors: Union[Unset, "V0040OpenapiPartitionRespErrors"] = UNSET
    warnings: Union[Unset, "V0040OpenapiPartitionRespWarnings"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        partitions = self.partitions.to_dict()

        last_update = self.last_update.to_dict()

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
                "partitions": partitions,
                "last_update": last_update,
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
        from ..models.v0040_openapi_partition_resp_errors import V0040OpenapiPartitionRespErrors
        from ..models.v0040_openapi_partition_resp_last_update import V0040OpenapiPartitionRespLastUpdate
        from ..models.v0040_openapi_partition_resp_meta import V0040OpenapiPartitionRespMeta
        from ..models.v0040_openapi_partition_resp_partitions import V0040OpenapiPartitionRespPartitions
        from ..models.v0040_openapi_partition_resp_warnings import V0040OpenapiPartitionRespWarnings

        d = dict(src_dict)
        partitions = V0040OpenapiPartitionRespPartitions.from_dict(d.pop("partitions"))

        last_update = V0040OpenapiPartitionRespLastUpdate.from_dict(d.pop("last_update"))

        _meta = d.pop("meta", UNSET)
        meta: Union[Unset, V0040OpenapiPartitionRespMeta]
        if isinstance(_meta, Unset):
            meta = UNSET
        else:
            meta = V0040OpenapiPartitionRespMeta.from_dict(_meta)

        _errors = d.pop("errors", UNSET)
        errors: Union[Unset, V0040OpenapiPartitionRespErrors]
        if isinstance(_errors, Unset):
            errors = UNSET
        else:
            errors = V0040OpenapiPartitionRespErrors.from_dict(_errors)

        _warnings = d.pop("warnings", UNSET)
        warnings: Union[Unset, V0040OpenapiPartitionRespWarnings]
        if isinstance(_warnings, Unset):
            warnings = UNSET
        else:
            warnings = V0040OpenapiPartitionRespWarnings.from_dict(_warnings)

        v0040_openapi_partition_resp = cls(
            partitions=partitions,
            last_update=last_update,
            meta=meta,
            errors=errors,
            warnings=warnings,
        )

        v0040_openapi_partition_resp.additional_properties = d
        return v0040_openapi_partition_resp

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
