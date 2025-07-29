from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_openapi_meta_client import V0040OpenapiMetaClient
    from ..models.v0040_openapi_meta_command import V0040OpenapiMetaCommand
    from ..models.v0040_openapi_meta_plugin import V0040OpenapiMetaPlugin
    from ..models.v0040_openapi_meta_slurm import V0040OpenapiMetaSlurm


T = TypeVar("T", bound="V0040OpenapiMeta")


@_attrs_define
class V0040OpenapiMeta:
    """
    Attributes:
        plugin (Union[Unset, V0040OpenapiMetaPlugin]):
        client (Union[Unset, V0040OpenapiMetaClient]):
        command (Union[Unset, V0040OpenapiMetaCommand]):
        slurm (Union[Unset, V0040OpenapiMetaSlurm]):
    """

    plugin: Union[Unset, "V0040OpenapiMetaPlugin"] = UNSET
    client: Union[Unset, "V0040OpenapiMetaClient"] = UNSET
    command: Union[Unset, "V0040OpenapiMetaCommand"] = UNSET
    slurm: Union[Unset, "V0040OpenapiMetaSlurm"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        plugin: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.plugin, Unset):
            plugin = self.plugin.to_dict()

        client: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.client, Unset):
            client = self.client.to_dict()

        command: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.command, Unset):
            command = self.command.to_dict()

        slurm: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.slurm, Unset):
            slurm = self.slurm.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if plugin is not UNSET:
            field_dict["plugin"] = plugin
        if client is not UNSET:
            field_dict["client"] = client
        if command is not UNSET:
            field_dict["command"] = command
        if slurm is not UNSET:
            field_dict["slurm"] = slurm

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0040_openapi_meta_client import V0040OpenapiMetaClient
        from ..models.v0040_openapi_meta_command import V0040OpenapiMetaCommand
        from ..models.v0040_openapi_meta_plugin import V0040OpenapiMetaPlugin
        from ..models.v0040_openapi_meta_slurm import V0040OpenapiMetaSlurm

        d = dict(src_dict)
        _plugin = d.pop("plugin", UNSET)
        plugin: Union[Unset, V0040OpenapiMetaPlugin]
        if isinstance(_plugin, Unset):
            plugin = UNSET
        else:
            plugin = V0040OpenapiMetaPlugin.from_dict(_plugin)

        _client = d.pop("client", UNSET)
        client: Union[Unset, V0040OpenapiMetaClient]
        if isinstance(_client, Unset):
            client = UNSET
        else:
            client = V0040OpenapiMetaClient.from_dict(_client)

        _command = d.pop("command", UNSET)
        command: Union[Unset, V0040OpenapiMetaCommand]
        if isinstance(_command, Unset):
            command = UNSET
        else:
            command = V0040OpenapiMetaCommand.from_dict(_command)

        _slurm = d.pop("slurm", UNSET)
        slurm: Union[Unset, V0040OpenapiMetaSlurm]
        if isinstance(_slurm, Unset):
            slurm = UNSET
        else:
            slurm = V0040OpenapiMetaSlurm.from_dict(_slurm)

        v0040_openapi_meta = cls(
            plugin=plugin,
            client=client,
            command=command,
            slurm=slurm,
        )

        v0040_openapi_meta.additional_properties = d
        return v0040_openapi_meta

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
