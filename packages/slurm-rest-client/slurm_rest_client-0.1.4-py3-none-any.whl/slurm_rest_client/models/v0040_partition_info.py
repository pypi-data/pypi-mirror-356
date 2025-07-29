from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_partition_info_accounts import V0040PartitionInfoAccounts
    from ..models.v0040_partition_info_cpus import V0040PartitionInfoCpus
    from ..models.v0040_partition_info_defaults import V0040PartitionInfoDefaults
    from ..models.v0040_partition_info_groups import V0040PartitionInfoGroups
    from ..models.v0040_partition_info_maximums import V0040PartitionInfoMaximums
    from ..models.v0040_partition_info_minimums import V0040PartitionInfoMinimums
    from ..models.v0040_partition_info_nodes import V0040PartitionInfoNodes
    from ..models.v0040_partition_info_partition import V0040PartitionInfoPartition
    from ..models.v0040_partition_info_priority import V0040PartitionInfoPriority
    from ..models.v0040_partition_info_qos import V0040PartitionInfoQos
    from ..models.v0040_partition_info_timeouts import V0040PartitionInfoTimeouts
    from ..models.v0040_partition_info_tres import V0040PartitionInfoTres


T = TypeVar("T", bound="V0040PartitionInfo")


@_attrs_define
class V0040PartitionInfo:
    """
    Attributes:
        nodes (Union[Unset, V0040PartitionInfoNodes]):
        accounts (Union[Unset, V0040PartitionInfoAccounts]):
        groups (Union[Unset, V0040PartitionInfoGroups]):
        qos (Union[Unset, V0040PartitionInfoQos]):
        alternate (Union[Unset, str]):
        tres (Union[Unset, V0040PartitionInfoTres]):
        cluster (Union[Unset, str]):
        cpus (Union[Unset, V0040PartitionInfoCpus]):
        defaults (Union[Unset, V0040PartitionInfoDefaults]):
        grace_time (Union[Unset, int]):
        maximums (Union[Unset, V0040PartitionInfoMaximums]):
        minimums (Union[Unset, V0040PartitionInfoMinimums]):
        name (Union[Unset, str]):
        node_sets (Union[Unset, str]):
        priority (Union[Unset, V0040PartitionInfoPriority]):
        timeouts (Union[Unset, V0040PartitionInfoTimeouts]):
        partition (Union[Unset, V0040PartitionInfoPartition]):
        suspend_time (Union[Unset, int]):
    """

    nodes: Union[Unset, "V0040PartitionInfoNodes"] = UNSET
    accounts: Union[Unset, "V0040PartitionInfoAccounts"] = UNSET
    groups: Union[Unset, "V0040PartitionInfoGroups"] = UNSET
    qos: Union[Unset, "V0040PartitionInfoQos"] = UNSET
    alternate: Union[Unset, str] = UNSET
    tres: Union[Unset, "V0040PartitionInfoTres"] = UNSET
    cluster: Union[Unset, str] = UNSET
    cpus: Union[Unset, "V0040PartitionInfoCpus"] = UNSET
    defaults: Union[Unset, "V0040PartitionInfoDefaults"] = UNSET
    grace_time: Union[Unset, int] = UNSET
    maximums: Union[Unset, "V0040PartitionInfoMaximums"] = UNSET
    minimums: Union[Unset, "V0040PartitionInfoMinimums"] = UNSET
    name: Union[Unset, str] = UNSET
    node_sets: Union[Unset, str] = UNSET
    priority: Union[Unset, "V0040PartitionInfoPriority"] = UNSET
    timeouts: Union[Unset, "V0040PartitionInfoTimeouts"] = UNSET
    partition: Union[Unset, "V0040PartitionInfoPartition"] = UNSET
    suspend_time: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        nodes: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.nodes, Unset):
            nodes = self.nodes.to_dict()

        accounts: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.accounts, Unset):
            accounts = self.accounts.to_dict()

        groups: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.groups, Unset):
            groups = self.groups.to_dict()

        qos: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.qos, Unset):
            qos = self.qos.to_dict()

        alternate = self.alternate

        tres: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.tres, Unset):
            tres = self.tres.to_dict()

        cluster = self.cluster

        cpus: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.cpus, Unset):
            cpus = self.cpus.to_dict()

        defaults: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.defaults, Unset):
            defaults = self.defaults.to_dict()

        grace_time = self.grace_time

        maximums: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.maximums, Unset):
            maximums = self.maximums.to_dict()

        minimums: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.minimums, Unset):
            minimums = self.minimums.to_dict()

        name = self.name

        node_sets = self.node_sets

        priority: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.priority, Unset):
            priority = self.priority.to_dict()

        timeouts: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.timeouts, Unset):
            timeouts = self.timeouts.to_dict()

        partition: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.partition, Unset):
            partition = self.partition.to_dict()

        suspend_time = self.suspend_time

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if nodes is not UNSET:
            field_dict["nodes"] = nodes
        if accounts is not UNSET:
            field_dict["accounts"] = accounts
        if groups is not UNSET:
            field_dict["groups"] = groups
        if qos is not UNSET:
            field_dict["qos"] = qos
        if alternate is not UNSET:
            field_dict["alternate"] = alternate
        if tres is not UNSET:
            field_dict["tres"] = tres
        if cluster is not UNSET:
            field_dict["cluster"] = cluster
        if cpus is not UNSET:
            field_dict["cpus"] = cpus
        if defaults is not UNSET:
            field_dict["defaults"] = defaults
        if grace_time is not UNSET:
            field_dict["grace_time"] = grace_time
        if maximums is not UNSET:
            field_dict["maximums"] = maximums
        if minimums is not UNSET:
            field_dict["minimums"] = minimums
        if name is not UNSET:
            field_dict["name"] = name
        if node_sets is not UNSET:
            field_dict["node_sets"] = node_sets
        if priority is not UNSET:
            field_dict["priority"] = priority
        if timeouts is not UNSET:
            field_dict["timeouts"] = timeouts
        if partition is not UNSET:
            field_dict["partition"] = partition
        if suspend_time is not UNSET:
            field_dict["suspend_time"] = suspend_time

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0040_partition_info_accounts import V0040PartitionInfoAccounts
        from ..models.v0040_partition_info_cpus import V0040PartitionInfoCpus
        from ..models.v0040_partition_info_defaults import V0040PartitionInfoDefaults
        from ..models.v0040_partition_info_groups import V0040PartitionInfoGroups
        from ..models.v0040_partition_info_maximums import V0040PartitionInfoMaximums
        from ..models.v0040_partition_info_minimums import V0040PartitionInfoMinimums
        from ..models.v0040_partition_info_nodes import V0040PartitionInfoNodes
        from ..models.v0040_partition_info_partition import V0040PartitionInfoPartition
        from ..models.v0040_partition_info_priority import V0040PartitionInfoPriority
        from ..models.v0040_partition_info_qos import V0040PartitionInfoQos
        from ..models.v0040_partition_info_timeouts import V0040PartitionInfoTimeouts
        from ..models.v0040_partition_info_tres import V0040PartitionInfoTres

        d = dict(src_dict)
        _nodes = d.pop("nodes", UNSET)
        nodes: Union[Unset, V0040PartitionInfoNodes]
        if isinstance(_nodes, Unset):
            nodes = UNSET
        else:
            nodes = V0040PartitionInfoNodes.from_dict(_nodes)

        _accounts = d.pop("accounts", UNSET)
        accounts: Union[Unset, V0040PartitionInfoAccounts]
        if isinstance(_accounts, Unset):
            accounts = UNSET
        else:
            accounts = V0040PartitionInfoAccounts.from_dict(_accounts)

        _groups = d.pop("groups", UNSET)
        groups: Union[Unset, V0040PartitionInfoGroups]
        if isinstance(_groups, Unset):
            groups = UNSET
        else:
            groups = V0040PartitionInfoGroups.from_dict(_groups)

        _qos = d.pop("qos", UNSET)
        qos: Union[Unset, V0040PartitionInfoQos]
        if isinstance(_qos, Unset):
            qos = UNSET
        else:
            qos = V0040PartitionInfoQos.from_dict(_qos)

        alternate = d.pop("alternate", UNSET)

        _tres = d.pop("tres", UNSET)
        tres: Union[Unset, V0040PartitionInfoTres]
        if isinstance(_tres, Unset):
            tres = UNSET
        else:
            tres = V0040PartitionInfoTres.from_dict(_tres)

        cluster = d.pop("cluster", UNSET)

        _cpus = d.pop("cpus", UNSET)
        cpus: Union[Unset, V0040PartitionInfoCpus]
        if isinstance(_cpus, Unset):
            cpus = UNSET
        else:
            cpus = V0040PartitionInfoCpus.from_dict(_cpus)

        _defaults = d.pop("defaults", UNSET)
        defaults: Union[Unset, V0040PartitionInfoDefaults]
        if isinstance(_defaults, Unset):
            defaults = UNSET
        else:
            defaults = V0040PartitionInfoDefaults.from_dict(_defaults)

        grace_time = d.pop("grace_time", UNSET)

        _maximums = d.pop("maximums", UNSET)
        maximums: Union[Unset, V0040PartitionInfoMaximums]
        if isinstance(_maximums, Unset):
            maximums = UNSET
        else:
            maximums = V0040PartitionInfoMaximums.from_dict(_maximums)

        _minimums = d.pop("minimums", UNSET)
        minimums: Union[Unset, V0040PartitionInfoMinimums]
        if isinstance(_minimums, Unset):
            minimums = UNSET
        else:
            minimums = V0040PartitionInfoMinimums.from_dict(_minimums)

        name = d.pop("name", UNSET)

        node_sets = d.pop("node_sets", UNSET)

        _priority = d.pop("priority", UNSET)
        priority: Union[Unset, V0040PartitionInfoPriority]
        if isinstance(_priority, Unset):
            priority = UNSET
        else:
            priority = V0040PartitionInfoPriority.from_dict(_priority)

        _timeouts = d.pop("timeouts", UNSET)
        timeouts: Union[Unset, V0040PartitionInfoTimeouts]
        if isinstance(_timeouts, Unset):
            timeouts = UNSET
        else:
            timeouts = V0040PartitionInfoTimeouts.from_dict(_timeouts)

        _partition = d.pop("partition", UNSET)
        partition: Union[Unset, V0040PartitionInfoPartition]
        if isinstance(_partition, Unset):
            partition = UNSET
        else:
            partition = V0040PartitionInfoPartition.from_dict(_partition)

        suspend_time = d.pop("suspend_time", UNSET)

        v0040_partition_info = cls(
            nodes=nodes,
            accounts=accounts,
            groups=groups,
            qos=qos,
            alternate=alternate,
            tres=tres,
            cluster=cluster,
            cpus=cpus,
            defaults=defaults,
            grace_time=grace_time,
            maximums=maximums,
            minimums=minimums,
            name=name,
            node_sets=node_sets,
            priority=priority,
            timeouts=timeouts,
            partition=partition,
            suspend_time=suspend_time,
        )

        v0040_partition_info.additional_properties = d
        return v0040_partition_info

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
