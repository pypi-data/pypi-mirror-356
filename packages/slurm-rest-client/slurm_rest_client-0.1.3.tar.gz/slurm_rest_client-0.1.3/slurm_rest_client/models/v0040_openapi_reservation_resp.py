from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_openapi_reservation_resp_errors import V0040OpenapiReservationRespErrors
    from ..models.v0040_openapi_reservation_resp_last_update import V0040OpenapiReservationRespLastUpdate
    from ..models.v0040_openapi_reservation_resp_meta import V0040OpenapiReservationRespMeta
    from ..models.v0040_openapi_reservation_resp_reservations import V0040OpenapiReservationRespReservations
    from ..models.v0040_openapi_reservation_resp_warnings import V0040OpenapiReservationRespWarnings


T = TypeVar("T", bound="V0040OpenapiReservationResp")


@_attrs_define
class V0040OpenapiReservationResp:
    """
    Attributes:
        reservations (V0040OpenapiReservationRespReservations):
        last_update (V0040OpenapiReservationRespLastUpdate):
        meta (Union[Unset, V0040OpenapiReservationRespMeta]):
        errors (Union[Unset, V0040OpenapiReservationRespErrors]):
        warnings (Union[Unset, V0040OpenapiReservationRespWarnings]):
    """

    reservations: "V0040OpenapiReservationRespReservations"
    last_update: "V0040OpenapiReservationRespLastUpdate"
    meta: Union[Unset, "V0040OpenapiReservationRespMeta"] = UNSET
    errors: Union[Unset, "V0040OpenapiReservationRespErrors"] = UNSET
    warnings: Union[Unset, "V0040OpenapiReservationRespWarnings"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        reservations = self.reservations.to_dict()

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
                "reservations": reservations,
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
        from ..models.v0040_openapi_reservation_resp_errors import V0040OpenapiReservationRespErrors
        from ..models.v0040_openapi_reservation_resp_last_update import V0040OpenapiReservationRespLastUpdate
        from ..models.v0040_openapi_reservation_resp_meta import V0040OpenapiReservationRespMeta
        from ..models.v0040_openapi_reservation_resp_reservations import V0040OpenapiReservationRespReservations
        from ..models.v0040_openapi_reservation_resp_warnings import V0040OpenapiReservationRespWarnings

        d = dict(src_dict)
        reservations = V0040OpenapiReservationRespReservations.from_dict(d.pop("reservations"))

        last_update = V0040OpenapiReservationRespLastUpdate.from_dict(d.pop("last_update"))

        _meta = d.pop("meta", UNSET)
        meta: Union[Unset, V0040OpenapiReservationRespMeta]
        if isinstance(_meta, Unset):
            meta = UNSET
        else:
            meta = V0040OpenapiReservationRespMeta.from_dict(_meta)

        _errors = d.pop("errors", UNSET)
        errors: Union[Unset, V0040OpenapiReservationRespErrors]
        if isinstance(_errors, Unset):
            errors = UNSET
        else:
            errors = V0040OpenapiReservationRespErrors.from_dict(_errors)

        _warnings = d.pop("warnings", UNSET)
        warnings: Union[Unset, V0040OpenapiReservationRespWarnings]
        if isinstance(_warnings, Unset):
            warnings = UNSET
        else:
            warnings = V0040OpenapiReservationRespWarnings.from_dict(_warnings)

        v0040_openapi_reservation_resp = cls(
            reservations=reservations,
            last_update=last_update,
            meta=meta,
            errors=errors,
            warnings=warnings,
        )

        v0040_openapi_reservation_resp.additional_properties = d
        return v0040_openapi_reservation_resp

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
