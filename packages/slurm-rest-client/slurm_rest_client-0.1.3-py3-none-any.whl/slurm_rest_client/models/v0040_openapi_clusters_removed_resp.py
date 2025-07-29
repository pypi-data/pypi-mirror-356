from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_openapi_clusters_removed_resp_deleted_clusters import (
        V0040OpenapiClustersRemovedRespDeletedClusters,
    )
    from ..models.v0040_openapi_clusters_removed_resp_errors import V0040OpenapiClustersRemovedRespErrors
    from ..models.v0040_openapi_clusters_removed_resp_meta import V0040OpenapiClustersRemovedRespMeta
    from ..models.v0040_openapi_clusters_removed_resp_warnings import V0040OpenapiClustersRemovedRespWarnings


T = TypeVar("T", bound="V0040OpenapiClustersRemovedResp")


@_attrs_define
class V0040OpenapiClustersRemovedResp:
    """
    Attributes:
        deleted_clusters (V0040OpenapiClustersRemovedRespDeletedClusters):
        meta (Union[Unset, V0040OpenapiClustersRemovedRespMeta]):
        errors (Union[Unset, V0040OpenapiClustersRemovedRespErrors]):
        warnings (Union[Unset, V0040OpenapiClustersRemovedRespWarnings]):
    """

    deleted_clusters: "V0040OpenapiClustersRemovedRespDeletedClusters"
    meta: Union[Unset, "V0040OpenapiClustersRemovedRespMeta"] = UNSET
    errors: Union[Unset, "V0040OpenapiClustersRemovedRespErrors"] = UNSET
    warnings: Union[Unset, "V0040OpenapiClustersRemovedRespWarnings"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        deleted_clusters = self.deleted_clusters.to_dict()

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
                "deleted_clusters": deleted_clusters,
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
        from ..models.v0040_openapi_clusters_removed_resp_deleted_clusters import (
            V0040OpenapiClustersRemovedRespDeletedClusters,
        )
        from ..models.v0040_openapi_clusters_removed_resp_errors import V0040OpenapiClustersRemovedRespErrors
        from ..models.v0040_openapi_clusters_removed_resp_meta import V0040OpenapiClustersRemovedRespMeta
        from ..models.v0040_openapi_clusters_removed_resp_warnings import V0040OpenapiClustersRemovedRespWarnings

        d = dict(src_dict)
        deleted_clusters = V0040OpenapiClustersRemovedRespDeletedClusters.from_dict(d.pop("deleted_clusters"))

        _meta = d.pop("meta", UNSET)
        meta: Union[Unset, V0040OpenapiClustersRemovedRespMeta]
        if isinstance(_meta, Unset):
            meta = UNSET
        else:
            meta = V0040OpenapiClustersRemovedRespMeta.from_dict(_meta)

        _errors = d.pop("errors", UNSET)
        errors: Union[Unset, V0040OpenapiClustersRemovedRespErrors]
        if isinstance(_errors, Unset):
            errors = UNSET
        else:
            errors = V0040OpenapiClustersRemovedRespErrors.from_dict(_errors)

        _warnings = d.pop("warnings", UNSET)
        warnings: Union[Unset, V0040OpenapiClustersRemovedRespWarnings]
        if isinstance(_warnings, Unset):
            warnings = UNSET
        else:
            warnings = V0040OpenapiClustersRemovedRespWarnings.from_dict(_warnings)

        v0040_openapi_clusters_removed_resp = cls(
            deleted_clusters=deleted_clusters,
            meta=meta,
            errors=errors,
            warnings=warnings,
        )

        v0040_openapi_clusters_removed_resp.additional_properties = d
        return v0040_openapi_clusters_removed_resp

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
