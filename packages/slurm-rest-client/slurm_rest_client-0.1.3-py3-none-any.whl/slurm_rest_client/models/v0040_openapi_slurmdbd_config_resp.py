from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_openapi_slurmdbd_config_resp_accounts import V0040OpenapiSlurmdbdConfigRespAccounts
    from ..models.v0040_openapi_slurmdbd_config_resp_associations import V0040OpenapiSlurmdbdConfigRespAssociations
    from ..models.v0040_openapi_slurmdbd_config_resp_clusters import V0040OpenapiSlurmdbdConfigRespClusters
    from ..models.v0040_openapi_slurmdbd_config_resp_errors import V0040OpenapiSlurmdbdConfigRespErrors
    from ..models.v0040_openapi_slurmdbd_config_resp_instances import V0040OpenapiSlurmdbdConfigRespInstances
    from ..models.v0040_openapi_slurmdbd_config_resp_meta import V0040OpenapiSlurmdbdConfigRespMeta
    from ..models.v0040_openapi_slurmdbd_config_resp_qos import V0040OpenapiSlurmdbdConfigRespQos
    from ..models.v0040_openapi_slurmdbd_config_resp_tres import V0040OpenapiSlurmdbdConfigRespTres
    from ..models.v0040_openapi_slurmdbd_config_resp_users import V0040OpenapiSlurmdbdConfigRespUsers
    from ..models.v0040_openapi_slurmdbd_config_resp_warnings import V0040OpenapiSlurmdbdConfigRespWarnings
    from ..models.v0040_openapi_slurmdbd_config_resp_wckeys import V0040OpenapiSlurmdbdConfigRespWckeys


T = TypeVar("T", bound="V0040OpenapiSlurmdbdConfigResp")


@_attrs_define
class V0040OpenapiSlurmdbdConfigResp:
    """
    Attributes:
        clusters (Union[Unset, V0040OpenapiSlurmdbdConfigRespClusters]):
        tres (Union[Unset, V0040OpenapiSlurmdbdConfigRespTres]):
        accounts (Union[Unset, V0040OpenapiSlurmdbdConfigRespAccounts]):
        users (Union[Unset, V0040OpenapiSlurmdbdConfigRespUsers]):
        qos (Union[Unset, V0040OpenapiSlurmdbdConfigRespQos]):
        wckeys (Union[Unset, V0040OpenapiSlurmdbdConfigRespWckeys]):
        associations (Union[Unset, V0040OpenapiSlurmdbdConfigRespAssociations]):
        instances (Union[Unset, V0040OpenapiSlurmdbdConfigRespInstances]):
        meta (Union[Unset, V0040OpenapiSlurmdbdConfigRespMeta]):
        errors (Union[Unset, V0040OpenapiSlurmdbdConfigRespErrors]):
        warnings (Union[Unset, V0040OpenapiSlurmdbdConfigRespWarnings]):
    """

    clusters: Union[Unset, "V0040OpenapiSlurmdbdConfigRespClusters"] = UNSET
    tres: Union[Unset, "V0040OpenapiSlurmdbdConfigRespTres"] = UNSET
    accounts: Union[Unset, "V0040OpenapiSlurmdbdConfigRespAccounts"] = UNSET
    users: Union[Unset, "V0040OpenapiSlurmdbdConfigRespUsers"] = UNSET
    qos: Union[Unset, "V0040OpenapiSlurmdbdConfigRespQos"] = UNSET
    wckeys: Union[Unset, "V0040OpenapiSlurmdbdConfigRespWckeys"] = UNSET
    associations: Union[Unset, "V0040OpenapiSlurmdbdConfigRespAssociations"] = UNSET
    instances: Union[Unset, "V0040OpenapiSlurmdbdConfigRespInstances"] = UNSET
    meta: Union[Unset, "V0040OpenapiSlurmdbdConfigRespMeta"] = UNSET
    errors: Union[Unset, "V0040OpenapiSlurmdbdConfigRespErrors"] = UNSET
    warnings: Union[Unset, "V0040OpenapiSlurmdbdConfigRespWarnings"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        clusters: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.clusters, Unset):
            clusters = self.clusters.to_dict()

        tres: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.tres, Unset):
            tres = self.tres.to_dict()

        accounts: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.accounts, Unset):
            accounts = self.accounts.to_dict()

        users: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.users, Unset):
            users = self.users.to_dict()

        qos: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.qos, Unset):
            qos = self.qos.to_dict()

        wckeys: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.wckeys, Unset):
            wckeys = self.wckeys.to_dict()

        associations: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.associations, Unset):
            associations = self.associations.to_dict()

        instances: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.instances, Unset):
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
        field_dict.update({})
        if clusters is not UNSET:
            field_dict["clusters"] = clusters
        if tres is not UNSET:
            field_dict["tres"] = tres
        if accounts is not UNSET:
            field_dict["accounts"] = accounts
        if users is not UNSET:
            field_dict["users"] = users
        if qos is not UNSET:
            field_dict["qos"] = qos
        if wckeys is not UNSET:
            field_dict["wckeys"] = wckeys
        if associations is not UNSET:
            field_dict["associations"] = associations
        if instances is not UNSET:
            field_dict["instances"] = instances
        if meta is not UNSET:
            field_dict["meta"] = meta
        if errors is not UNSET:
            field_dict["errors"] = errors
        if warnings is not UNSET:
            field_dict["warnings"] = warnings

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0040_openapi_slurmdbd_config_resp_accounts import V0040OpenapiSlurmdbdConfigRespAccounts
        from ..models.v0040_openapi_slurmdbd_config_resp_associations import V0040OpenapiSlurmdbdConfigRespAssociations
        from ..models.v0040_openapi_slurmdbd_config_resp_clusters import V0040OpenapiSlurmdbdConfigRespClusters
        from ..models.v0040_openapi_slurmdbd_config_resp_errors import V0040OpenapiSlurmdbdConfigRespErrors
        from ..models.v0040_openapi_slurmdbd_config_resp_instances import V0040OpenapiSlurmdbdConfigRespInstances
        from ..models.v0040_openapi_slurmdbd_config_resp_meta import V0040OpenapiSlurmdbdConfigRespMeta
        from ..models.v0040_openapi_slurmdbd_config_resp_qos import V0040OpenapiSlurmdbdConfigRespQos
        from ..models.v0040_openapi_slurmdbd_config_resp_tres import V0040OpenapiSlurmdbdConfigRespTres
        from ..models.v0040_openapi_slurmdbd_config_resp_users import V0040OpenapiSlurmdbdConfigRespUsers
        from ..models.v0040_openapi_slurmdbd_config_resp_warnings import V0040OpenapiSlurmdbdConfigRespWarnings
        from ..models.v0040_openapi_slurmdbd_config_resp_wckeys import V0040OpenapiSlurmdbdConfigRespWckeys

        d = dict(src_dict)
        _clusters = d.pop("clusters", UNSET)
        clusters: Union[Unset, V0040OpenapiSlurmdbdConfigRespClusters]
        if isinstance(_clusters, Unset):
            clusters = UNSET
        else:
            clusters = V0040OpenapiSlurmdbdConfigRespClusters.from_dict(_clusters)

        _tres = d.pop("tres", UNSET)
        tres: Union[Unset, V0040OpenapiSlurmdbdConfigRespTres]
        if isinstance(_tres, Unset):
            tres = UNSET
        else:
            tres = V0040OpenapiSlurmdbdConfigRespTres.from_dict(_tres)

        _accounts = d.pop("accounts", UNSET)
        accounts: Union[Unset, V0040OpenapiSlurmdbdConfigRespAccounts]
        if isinstance(_accounts, Unset):
            accounts = UNSET
        else:
            accounts = V0040OpenapiSlurmdbdConfigRespAccounts.from_dict(_accounts)

        _users = d.pop("users", UNSET)
        users: Union[Unset, V0040OpenapiSlurmdbdConfigRespUsers]
        if isinstance(_users, Unset):
            users = UNSET
        else:
            users = V0040OpenapiSlurmdbdConfigRespUsers.from_dict(_users)

        _qos = d.pop("qos", UNSET)
        qos: Union[Unset, V0040OpenapiSlurmdbdConfigRespQos]
        if isinstance(_qos, Unset):
            qos = UNSET
        else:
            qos = V0040OpenapiSlurmdbdConfigRespQos.from_dict(_qos)

        _wckeys = d.pop("wckeys", UNSET)
        wckeys: Union[Unset, V0040OpenapiSlurmdbdConfigRespWckeys]
        if isinstance(_wckeys, Unset):
            wckeys = UNSET
        else:
            wckeys = V0040OpenapiSlurmdbdConfigRespWckeys.from_dict(_wckeys)

        _associations = d.pop("associations", UNSET)
        associations: Union[Unset, V0040OpenapiSlurmdbdConfigRespAssociations]
        if isinstance(_associations, Unset):
            associations = UNSET
        else:
            associations = V0040OpenapiSlurmdbdConfigRespAssociations.from_dict(_associations)

        _instances = d.pop("instances", UNSET)
        instances: Union[Unset, V0040OpenapiSlurmdbdConfigRespInstances]
        if isinstance(_instances, Unset):
            instances = UNSET
        else:
            instances = V0040OpenapiSlurmdbdConfigRespInstances.from_dict(_instances)

        _meta = d.pop("meta", UNSET)
        meta: Union[Unset, V0040OpenapiSlurmdbdConfigRespMeta]
        if isinstance(_meta, Unset):
            meta = UNSET
        else:
            meta = V0040OpenapiSlurmdbdConfigRespMeta.from_dict(_meta)

        _errors = d.pop("errors", UNSET)
        errors: Union[Unset, V0040OpenapiSlurmdbdConfigRespErrors]
        if isinstance(_errors, Unset):
            errors = UNSET
        else:
            errors = V0040OpenapiSlurmdbdConfigRespErrors.from_dict(_errors)

        _warnings = d.pop("warnings", UNSET)
        warnings: Union[Unset, V0040OpenapiSlurmdbdConfigRespWarnings]
        if isinstance(_warnings, Unset):
            warnings = UNSET
        else:
            warnings = V0040OpenapiSlurmdbdConfigRespWarnings.from_dict(_warnings)

        v0040_openapi_slurmdbd_config_resp = cls(
            clusters=clusters,
            tres=tres,
            accounts=accounts,
            users=users,
            qos=qos,
            wckeys=wckeys,
            associations=associations,
            instances=instances,
            meta=meta,
            errors=errors,
            warnings=warnings,
        )

        v0040_openapi_slurmdbd_config_resp.additional_properties = d
        return v0040_openapi_slurmdbd_config_resp

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
