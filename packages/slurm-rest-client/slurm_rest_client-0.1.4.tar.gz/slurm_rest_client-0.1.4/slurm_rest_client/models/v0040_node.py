from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.v0040_node_next_state_after_reboot_item import V0040NodeNextStateAfterRebootItem
from ..models.v0040_node_state_item import V0040NodeStateItem
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_acct_gather_energy import V0040AcctGatherEnergy
    from ..models.v0040_ext_sensors_data import V0040ExtSensorsData
    from ..models.v0040_power_mgmt_data import V0040PowerMgmtData


T = TypeVar("T", bound="V0040Node")


@_attrs_define
class V0040Node:
    """
    Attributes:
        architecture (Union[Unset, str]):
        burstbuffer_network_address (Union[Unset, str]):
        boards (Union[Unset, int]):
        boot_time (Union[Unset, int]):
        cluster_name (Union[Unset, str]):
        cores (Union[Unset, int]):
        specialized_cores (Union[Unset, int]):
        cpu_binding (Union[Unset, int]):
        cpu_load (Union[Unset, int]):
        free_mem (Union[Unset, int]):
        cpus (Union[Unset, int]):
        effective_cpus (Union[Unset, int]):
        specialized_cpus (Union[Unset, str]):
        energy (Union[Unset, V0040AcctGatherEnergy]):
        external_sensors (Union[Unset, V0040ExtSensorsData]):
        extra (Union[Unset, str]):
        power (Union[Unset, V0040PowerMgmtData]):
        features (Union[Unset, list[str]]):
        active_features (Union[Unset, list[str]]):
        gres (Union[Unset, str]):
        gres_drained (Union[Unset, str]):
        gres_used (Union[Unset, str]):
        instance_id (Union[Unset, str]):
        instance_type (Union[Unset, str]):
        last_busy (Union[Unset, int]):
        mcs_label (Union[Unset, str]):
        specialized_memory (Union[Unset, int]):
        name (Union[Unset, str]):
        next_state_after_reboot (Union[Unset, list[V0040NodeNextStateAfterRebootItem]]):
        address (Union[Unset, str]):
        hostname (Union[Unset, str]):
        state (Union[Unset, list[V0040NodeStateItem]]):
        operating_system (Union[Unset, str]):
        owner (Union[Unset, str]):
        partitions (Union[Unset, list[str]]):
        port (Union[Unset, int]):
        real_memory (Union[Unset, int]):
        comment (Union[Unset, str]):
        reason (Union[Unset, str]):
        reason_changed_at (Union[Unset, int]):
        reason_set_by_user (Union[Unset, str]):
        resume_after (Union[Unset, int]):
        reservation (Union[Unset, str]):
        alloc_memory (Union[Unset, int]):
        alloc_cpus (Union[Unset, int]):
        alloc_idle_cpus (Union[Unset, int]):
        tres_used (Union[Unset, str]):
        tres_weighted (Union[Unset, float]):
        slurmd_start_time (Union[Unset, int]):
        sockets (Union[Unset, int]):
        threads (Union[Unset, int]):
        temporary_disk (Union[Unset, int]):
        weight (Union[Unset, int]):
        tres (Union[Unset, str]):
        version (Union[Unset, str]):
    """

    architecture: Union[Unset, str] = UNSET
    burstbuffer_network_address: Union[Unset, str] = UNSET
    boards: Union[Unset, int] = UNSET
    boot_time: Union[Unset, int] = UNSET
    cluster_name: Union[Unset, str] = UNSET
    cores: Union[Unset, int] = UNSET
    specialized_cores: Union[Unset, int] = UNSET
    cpu_binding: Union[Unset, int] = UNSET
    cpu_load: Union[Unset, int] = UNSET
    free_mem: Union[Unset, int] = UNSET
    cpus: Union[Unset, int] = UNSET
    effective_cpus: Union[Unset, int] = UNSET
    specialized_cpus: Union[Unset, str] = UNSET
    energy: Union[Unset, "V0040AcctGatherEnergy"] = UNSET
    external_sensors: Union[Unset, "V0040ExtSensorsData"] = UNSET
    extra: Union[Unset, str] = UNSET
    power: Union[Unset, "V0040PowerMgmtData"] = UNSET
    features: Union[Unset, list[str]] = UNSET
    active_features: Union[Unset, list[str]] = UNSET
    gres: Union[Unset, str] = UNSET
    gres_drained: Union[Unset, str] = UNSET
    gres_used: Union[Unset, str] = UNSET
    instance_id: Union[Unset, str] = UNSET
    instance_type: Union[Unset, str] = UNSET
    last_busy: Union[Unset, int] = UNSET
    mcs_label: Union[Unset, str] = UNSET
    specialized_memory: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    next_state_after_reboot: Union[Unset, list[V0040NodeNextStateAfterRebootItem]] = UNSET
    address: Union[Unset, str] = UNSET
    hostname: Union[Unset, str] = UNSET
    state: Union[Unset, list[V0040NodeStateItem]] = UNSET
    operating_system: Union[Unset, str] = UNSET
    owner: Union[Unset, str] = UNSET
    partitions: Union[Unset, list[str]] = UNSET
    port: Union[Unset, int] = UNSET
    real_memory: Union[Unset, int] = UNSET
    comment: Union[Unset, str] = UNSET
    reason: Union[Unset, str] = UNSET
    reason_changed_at: Union[Unset, int] = UNSET
    reason_set_by_user: Union[Unset, str] = UNSET
    resume_after: Union[Unset, int] = UNSET
    reservation: Union[Unset, str] = UNSET
    alloc_memory: Union[Unset, int] = UNSET
    alloc_cpus: Union[Unset, int] = UNSET
    alloc_idle_cpus: Union[Unset, int] = UNSET
    tres_used: Union[Unset, str] = UNSET
    tres_weighted: Union[Unset, float] = UNSET
    slurmd_start_time: Union[Unset, int] = UNSET
    sockets: Union[Unset, int] = UNSET
    threads: Union[Unset, int] = UNSET
    temporary_disk: Union[Unset, int] = UNSET
    weight: Union[Unset, int] = UNSET
    tres: Union[Unset, str] = UNSET
    version: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        architecture = self.architecture

        burstbuffer_network_address = self.burstbuffer_network_address

        boards = self.boards

        boot_time = self.boot_time

        cluster_name = self.cluster_name

        cores = self.cores

        specialized_cores = self.specialized_cores

        cpu_binding = self.cpu_binding

        cpu_load = self.cpu_load

        free_mem = self.free_mem

        cpus = self.cpus

        effective_cpus = self.effective_cpus

        specialized_cpus = self.specialized_cpus

        energy: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.energy, Unset):
            energy = self.energy.to_dict()

        external_sensors: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.external_sensors, Unset):
            external_sensors = self.external_sensors.to_dict()

        extra = self.extra

        power: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.power, Unset):
            power = self.power.to_dict()

        features: Union[Unset, list[str]] = UNSET
        if not isinstance(self.features, Unset):
            features = self.features

        active_features: Union[Unset, list[str]] = UNSET
        if not isinstance(self.active_features, Unset):
            active_features = self.active_features

        gres = self.gres

        gres_drained = self.gres_drained

        gres_used = self.gres_used

        instance_id = self.instance_id

        instance_type = self.instance_type

        last_busy = self.last_busy

        mcs_label = self.mcs_label

        specialized_memory = self.specialized_memory

        name = self.name

        next_state_after_reboot: Union[Unset, list[str]] = UNSET
        if not isinstance(self.next_state_after_reboot, Unset):
            next_state_after_reboot = []
            for next_state_after_reboot_item_data in self.next_state_after_reboot:
                next_state_after_reboot_item = next_state_after_reboot_item_data.value
                next_state_after_reboot.append(next_state_after_reboot_item)

        address = self.address

        hostname = self.hostname

        state: Union[Unset, list[str]] = UNSET
        if not isinstance(self.state, Unset):
            state = []
            for state_item_data in self.state:
                state_item = state_item_data.value
                state.append(state_item)

        operating_system = self.operating_system

        owner = self.owner

        partitions: Union[Unset, list[str]] = UNSET
        if not isinstance(self.partitions, Unset):
            partitions = self.partitions

        port = self.port

        real_memory = self.real_memory

        comment = self.comment

        reason = self.reason

        reason_changed_at = self.reason_changed_at

        reason_set_by_user = self.reason_set_by_user

        resume_after = self.resume_after

        reservation = self.reservation

        alloc_memory = self.alloc_memory

        alloc_cpus = self.alloc_cpus

        alloc_idle_cpus = self.alloc_idle_cpus

        tres_used = self.tres_used

        tres_weighted = self.tres_weighted

        slurmd_start_time = self.slurmd_start_time

        sockets = self.sockets

        threads = self.threads

        temporary_disk = self.temporary_disk

        weight = self.weight

        tres = self.tres

        version = self.version

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if architecture is not UNSET:
            field_dict["architecture"] = architecture
        if burstbuffer_network_address is not UNSET:
            field_dict["burstbuffer_network_address"] = burstbuffer_network_address
        if boards is not UNSET:
            field_dict["boards"] = boards
        if boot_time is not UNSET:
            field_dict["boot_time"] = boot_time
        if cluster_name is not UNSET:
            field_dict["cluster_name"] = cluster_name
        if cores is not UNSET:
            field_dict["cores"] = cores
        if specialized_cores is not UNSET:
            field_dict["specialized_cores"] = specialized_cores
        if cpu_binding is not UNSET:
            field_dict["cpu_binding"] = cpu_binding
        if cpu_load is not UNSET:
            field_dict["cpu_load"] = cpu_load
        if free_mem is not UNSET:
            field_dict["free_mem"] = free_mem
        if cpus is not UNSET:
            field_dict["cpus"] = cpus
        if effective_cpus is not UNSET:
            field_dict["effective_cpus"] = effective_cpus
        if specialized_cpus is not UNSET:
            field_dict["specialized_cpus"] = specialized_cpus
        if energy is not UNSET:
            field_dict["energy"] = energy
        if external_sensors is not UNSET:
            field_dict["external_sensors"] = external_sensors
        if extra is not UNSET:
            field_dict["extra"] = extra
        if power is not UNSET:
            field_dict["power"] = power
        if features is not UNSET:
            field_dict["features"] = features
        if active_features is not UNSET:
            field_dict["active_features"] = active_features
        if gres is not UNSET:
            field_dict["gres"] = gres
        if gres_drained is not UNSET:
            field_dict["gres_drained"] = gres_drained
        if gres_used is not UNSET:
            field_dict["gres_used"] = gres_used
        if instance_id is not UNSET:
            field_dict["instance_id"] = instance_id
        if instance_type is not UNSET:
            field_dict["instance_type"] = instance_type
        if last_busy is not UNSET:
            field_dict["last_busy"] = last_busy
        if mcs_label is not UNSET:
            field_dict["mcs_label"] = mcs_label
        if specialized_memory is not UNSET:
            field_dict["specialized_memory"] = specialized_memory
        if name is not UNSET:
            field_dict["name"] = name
        if next_state_after_reboot is not UNSET:
            field_dict["next_state_after_reboot"] = next_state_after_reboot
        if address is not UNSET:
            field_dict["address"] = address
        if hostname is not UNSET:
            field_dict["hostname"] = hostname
        if state is not UNSET:
            field_dict["state"] = state
        if operating_system is not UNSET:
            field_dict["operating_system"] = operating_system
        if owner is not UNSET:
            field_dict["owner"] = owner
        if partitions is not UNSET:
            field_dict["partitions"] = partitions
        if port is not UNSET:
            field_dict["port"] = port
        if real_memory is not UNSET:
            field_dict["real_memory"] = real_memory
        if comment is not UNSET:
            field_dict["comment"] = comment
        if reason is not UNSET:
            field_dict["reason"] = reason
        if reason_changed_at is not UNSET:
            field_dict["reason_changed_at"] = reason_changed_at
        if reason_set_by_user is not UNSET:
            field_dict["reason_set_by_user"] = reason_set_by_user
        if resume_after is not UNSET:
            field_dict["resume_after"] = resume_after
        if reservation is not UNSET:
            field_dict["reservation"] = reservation
        if alloc_memory is not UNSET:
            field_dict["alloc_memory"] = alloc_memory
        if alloc_cpus is not UNSET:
            field_dict["alloc_cpus"] = alloc_cpus
        if alloc_idle_cpus is not UNSET:
            field_dict["alloc_idle_cpus"] = alloc_idle_cpus
        if tres_used is not UNSET:
            field_dict["tres_used"] = tres_used
        if tres_weighted is not UNSET:
            field_dict["tres_weighted"] = tres_weighted
        if slurmd_start_time is not UNSET:
            field_dict["slurmd_start_time"] = slurmd_start_time
        if sockets is not UNSET:
            field_dict["sockets"] = sockets
        if threads is not UNSET:
            field_dict["threads"] = threads
        if temporary_disk is not UNSET:
            field_dict["temporary_disk"] = temporary_disk
        if weight is not UNSET:
            field_dict["weight"] = weight
        if tres is not UNSET:
            field_dict["tres"] = tres
        if version is not UNSET:
            field_dict["version"] = version

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0040_acct_gather_energy import V0040AcctGatherEnergy
        from ..models.v0040_ext_sensors_data import V0040ExtSensorsData
        from ..models.v0040_power_mgmt_data import V0040PowerMgmtData

        d = dict(src_dict)
        architecture = d.pop("architecture", UNSET)

        burstbuffer_network_address = d.pop("burstbuffer_network_address", UNSET)

        boards = d.pop("boards", UNSET)

        boot_time = d.pop("boot_time", UNSET)

        cluster_name = d.pop("cluster_name", UNSET)

        cores = d.pop("cores", UNSET)

        specialized_cores = d.pop("specialized_cores", UNSET)

        cpu_binding = d.pop("cpu_binding", UNSET)

        cpu_load = d.pop("cpu_load", UNSET)

        free_mem = d.pop("free_mem", UNSET)

        cpus = d.pop("cpus", UNSET)

        effective_cpus = d.pop("effective_cpus", UNSET)

        specialized_cpus = d.pop("specialized_cpus", UNSET)

        _energy = d.pop("energy", UNSET)
        energy: Union[Unset, V0040AcctGatherEnergy]
        if isinstance(_energy, Unset):
            energy = UNSET
        else:
            energy = V0040AcctGatherEnergy.from_dict(_energy)

        _external_sensors = d.pop("external_sensors", UNSET)
        external_sensors: Union[Unset, V0040ExtSensorsData]
        if isinstance(_external_sensors, Unset):
            external_sensors = UNSET
        else:
            external_sensors = V0040ExtSensorsData.from_dict(_external_sensors)

        extra = d.pop("extra", UNSET)

        _power = d.pop("power", UNSET)
        power: Union[Unset, V0040PowerMgmtData]
        if isinstance(_power, Unset):
            power = UNSET
        else:
            power = V0040PowerMgmtData.from_dict(_power)

        features = cast(list[str], d.pop("features", UNSET))

        active_features = cast(list[str], d.pop("active_features", UNSET))

        gres = d.pop("gres", UNSET)

        gres_drained = d.pop("gres_drained", UNSET)

        gres_used = d.pop("gres_used", UNSET)

        instance_id = d.pop("instance_id", UNSET)

        instance_type = d.pop("instance_type", UNSET)

        last_busy = d.pop("last_busy", UNSET)

        mcs_label = d.pop("mcs_label", UNSET)

        specialized_memory = d.pop("specialized_memory", UNSET)

        name = d.pop("name", UNSET)

        next_state_after_reboot = []
        _next_state_after_reboot = d.pop("next_state_after_reboot", UNSET)
        for next_state_after_reboot_item_data in _next_state_after_reboot or []:
            next_state_after_reboot_item = V0040NodeNextStateAfterRebootItem(next_state_after_reboot_item_data)

            next_state_after_reboot.append(next_state_after_reboot_item)

        address = d.pop("address", UNSET)

        hostname = d.pop("hostname", UNSET)

        state = []
        _state = d.pop("state", UNSET)
        for state_item_data in _state or []:
            state_item = V0040NodeStateItem(state_item_data)

            state.append(state_item)

        operating_system = d.pop("operating_system", UNSET)

        owner = d.pop("owner", UNSET)

        partitions = cast(list[str], d.pop("partitions", UNSET))

        port = d.pop("port", UNSET)

        real_memory = d.pop("real_memory", UNSET)

        comment = d.pop("comment", UNSET)

        reason = d.pop("reason", UNSET)

        reason_changed_at = d.pop("reason_changed_at", UNSET)

        reason_set_by_user = d.pop("reason_set_by_user", UNSET)

        resume_after = d.pop("resume_after", UNSET)

        reservation = d.pop("reservation", UNSET)

        alloc_memory = d.pop("alloc_memory", UNSET)

        alloc_cpus = d.pop("alloc_cpus", UNSET)

        alloc_idle_cpus = d.pop("alloc_idle_cpus", UNSET)

        tres_used = d.pop("tres_used", UNSET)

        tres_weighted = d.pop("tres_weighted", UNSET)

        slurmd_start_time = d.pop("slurmd_start_time", UNSET)

        sockets = d.pop("sockets", UNSET)

        threads = d.pop("threads", UNSET)

        temporary_disk = d.pop("temporary_disk", UNSET)

        weight = d.pop("weight", UNSET)

        tres = d.pop("tres", UNSET)

        version = d.pop("version", UNSET)

        v0040_node = cls(
            architecture=architecture,
            burstbuffer_network_address=burstbuffer_network_address,
            boards=boards,
            boot_time=boot_time,
            cluster_name=cluster_name,
            cores=cores,
            specialized_cores=specialized_cores,
            cpu_binding=cpu_binding,
            cpu_load=cpu_load,
            free_mem=free_mem,
            cpus=cpus,
            effective_cpus=effective_cpus,
            specialized_cpus=specialized_cpus,
            energy=energy,
            external_sensors=external_sensors,
            extra=extra,
            power=power,
            features=features,
            active_features=active_features,
            gres=gres,
            gres_drained=gres_drained,
            gres_used=gres_used,
            instance_id=instance_id,
            instance_type=instance_type,
            last_busy=last_busy,
            mcs_label=mcs_label,
            specialized_memory=specialized_memory,
            name=name,
            next_state_after_reboot=next_state_after_reboot,
            address=address,
            hostname=hostname,
            state=state,
            operating_system=operating_system,
            owner=owner,
            partitions=partitions,
            port=port,
            real_memory=real_memory,
            comment=comment,
            reason=reason,
            reason_changed_at=reason_changed_at,
            reason_set_by_user=reason_set_by_user,
            resume_after=resume_after,
            reservation=reservation,
            alloc_memory=alloc_memory,
            alloc_cpus=alloc_cpus,
            alloc_idle_cpus=alloc_idle_cpus,
            tres_used=tres_used,
            tres_weighted=tres_weighted,
            slurmd_start_time=slurmd_start_time,
            sockets=sockets,
            threads=threads,
            temporary_disk=temporary_disk,
            weight=weight,
            tres=tres,
            version=version,
        )

        v0040_node.additional_properties = d
        return v0040_node

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
