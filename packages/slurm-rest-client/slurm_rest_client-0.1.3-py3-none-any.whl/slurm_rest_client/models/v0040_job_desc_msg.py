from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.v0040_job_desc_msg_cpu_binding_flags_item import V0040JobDescMsgCpuBindingFlagsItem
from ..models.v0040_job_desc_msg_exclusive_item import V0040JobDescMsgExclusiveItem
from ..models.v0040_job_desc_msg_flags_item import V0040JobDescMsgFlagsItem
from ..models.v0040_job_desc_msg_kill_warning_flags_item import V0040JobDescMsgKillWarningFlagsItem
from ..models.v0040_job_desc_msg_mail_type_item import V0040JobDescMsgMailTypeItem
from ..models.v0040_job_desc_msg_memory_binding_type_item import V0040JobDescMsgMemoryBindingTypeItem
from ..models.v0040_job_desc_msg_open_mode_item import V0040JobDescMsgOpenModeItem
from ..models.v0040_job_desc_msg_power_flags_item import V0040JobDescMsgPowerFlagsItem
from ..models.v0040_job_desc_msg_profile_item import V0040JobDescMsgProfileItem
from ..models.v0040_job_desc_msg_shared_item import V0040JobDescMsgSharedItem
from ..models.v0040_job_desc_msg_x11_item import V0040JobDescMsgX11Item
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_job_desc_msg_argv import V0040JobDescMsgArgv
    from ..models.v0040_job_desc_msg_begin_time import V0040JobDescMsgBeginTime
    from ..models.v0040_job_desc_msg_crontab import V0040JobDescMsgCrontab
    from ..models.v0040_job_desc_msg_environment import V0040JobDescMsgEnvironment
    from ..models.v0040_job_desc_msg_excluded_nodes import V0040JobDescMsgExcludedNodes
    from ..models.v0040_job_desc_msg_kill_warning_delay import V0040JobDescMsgKillWarningDelay
    from ..models.v0040_job_desc_msg_memory_per_cpu import V0040JobDescMsgMemoryPerCpu
    from ..models.v0040_job_desc_msg_memory_per_node import V0040JobDescMsgMemoryPerNode
    from ..models.v0040_job_desc_msg_priority import V0040JobDescMsgPriority
    from ..models.v0040_job_desc_msg_required_nodes import V0040JobDescMsgRequiredNodes
    from ..models.v0040_job_desc_msg_required_switches import V0040JobDescMsgRequiredSwitches
    from ..models.v0040_job_desc_msg_rlimits import V0040JobDescMsgRlimits
    from ..models.v0040_job_desc_msg_spank_environment import V0040JobDescMsgSpankEnvironment
    from ..models.v0040_job_desc_msg_time_limit import V0040JobDescMsgTimeLimit
    from ..models.v0040_job_desc_msg_time_minimum import V0040JobDescMsgTimeMinimum


T = TypeVar("T", bound="V0040JobDescMsg")


@_attrs_define
class V0040JobDescMsg:
    """
    Attributes:
        account (Union[Unset, str]):
        account_gather_frequency (Union[Unset, str]):
        admin_comment (Union[Unset, str]):
        allocation_node_list (Union[Unset, str]):
        allocation_node_port (Union[Unset, int]):
        argv (Union[Unset, V0040JobDescMsgArgv]):
        array (Union[Unset, str]):
        batch_features (Union[Unset, str]):
        begin_time (Union[Unset, V0040JobDescMsgBeginTime]):
        flags (Union[Unset, list[V0040JobDescMsgFlagsItem]]):
        burst_buffer (Union[Unset, str]):
        clusters (Union[Unset, str]):
        cluster_constraint (Union[Unset, str]):
        comment (Union[Unset, str]):
        contiguous (Union[Unset, bool]):
        container (Union[Unset, str]):
        container_id (Union[Unset, str]):
        cores_per_socket (Union[Unset, int]):
        core_specification (Union[Unset, int]):
        thread_specification (Union[Unset, int]):
        cpu_binding (Union[Unset, str]):
        cpu_binding_flags (Union[Unset, list[V0040JobDescMsgCpuBindingFlagsItem]]):
        cpu_frequency (Union[Unset, str]):
        cpus_per_tres (Union[Unset, str]):
        crontab (Union[Unset, V0040JobDescMsgCrontab]):
        deadline (Union[Unset, int]):
        delay_boot (Union[Unset, int]):
        dependency (Union[Unset, str]):
        end_time (Union[Unset, int]):
        environment (Union[Unset, V0040JobDescMsgEnvironment]):
        rlimits (Union[Unset, V0040JobDescMsgRlimits]):
        excluded_nodes (Union[Unset, V0040JobDescMsgExcludedNodes]):
        extra (Union[Unset, str]):
        constraints (Union[Unset, str]):
        group_id (Union[Unset, str]):
        hetjob_group (Union[Unset, int]):
        immediate (Union[Unset, bool]):
        job_id (Union[Unset, int]):
        kill_on_node_fail (Union[Unset, bool]):
        licenses (Union[Unset, str]):
        mail_type (Union[Unset, list[V0040JobDescMsgMailTypeItem]]):
        mail_user (Union[Unset, str]):
        mcs_label (Union[Unset, str]):
        memory_binding (Union[Unset, str]):
        memory_binding_type (Union[Unset, list[V0040JobDescMsgMemoryBindingTypeItem]]):
        memory_per_tres (Union[Unset, str]):
        name (Union[Unset, str]):
        network (Union[Unset, str]):
        nice (Union[Unset, int]):
        tasks (Union[Unset, int]):
        open_mode (Union[Unset, list[V0040JobDescMsgOpenModeItem]]):
        reserve_ports (Union[Unset, int]):
        overcommit (Union[Unset, bool]):
        partition (Union[Unset, str]):
        distribution_plane_size (Union[Unset, int]):
        power_flags (Union[Unset, list[V0040JobDescMsgPowerFlagsItem]]):
        prefer (Union[Unset, str]):
        hold (Union[Unset, bool]): Job held
        priority (Union[Unset, V0040JobDescMsgPriority]):
        profile (Union[Unset, list[V0040JobDescMsgProfileItem]]):
        qos (Union[Unset, str]):
        reboot (Union[Unset, bool]):
        required_nodes (Union[Unset, V0040JobDescMsgRequiredNodes]):
        requeue (Union[Unset, bool]):
        reservation (Union[Unset, str]):
        script (Union[Unset, str]): Job batch script. Only first component in a HetJob is populated or honored.
        shared (Union[Unset, list[V0040JobDescMsgSharedItem]]):
        exclusive (Union[Unset, list[V0040JobDescMsgExclusiveItem]]):
        oversubscribe (Union[Unset, bool]):
        site_factor (Union[Unset, int]):
        spank_environment (Union[Unset, V0040JobDescMsgSpankEnvironment]):
        distribution (Union[Unset, str]):
        time_limit (Union[Unset, V0040JobDescMsgTimeLimit]):
        time_minimum (Union[Unset, V0040JobDescMsgTimeMinimum]):
        tres_bind (Union[Unset, str]):
        tres_freq (Union[Unset, str]):
        tres_per_job (Union[Unset, str]):
        tres_per_node (Union[Unset, str]):
        tres_per_socket (Union[Unset, str]):
        tres_per_task (Union[Unset, str]):
        user_id (Union[Unset, str]):
        wait_all_nodes (Union[Unset, bool]):
        kill_warning_flags (Union[Unset, list[V0040JobDescMsgKillWarningFlagsItem]]):
        kill_warning_signal (Union[Unset, str]):
        kill_warning_delay (Union[Unset, V0040JobDescMsgKillWarningDelay]):
        current_working_directory (Union[Unset, str]):
        cpus_per_task (Union[Unset, int]):
        minimum_cpus (Union[Unset, int]):
        maximum_cpus (Union[Unset, int]):
        nodes (Union[Unset, str]):
        minimum_nodes (Union[Unset, int]):
        maximum_nodes (Union[Unset, int]):
        minimum_boards_per_node (Union[Unset, int]):
        minimum_sockets_per_board (Union[Unset, int]):
        sockets_per_node (Union[Unset, int]):
        threads_per_core (Union[Unset, int]):
        tasks_per_node (Union[Unset, int]):
        tasks_per_socket (Union[Unset, int]):
        tasks_per_core (Union[Unset, int]):
        tasks_per_board (Union[Unset, int]):
        ntasks_per_tres (Union[Unset, int]):
        minimum_cpus_per_node (Union[Unset, int]):
        memory_per_cpu (Union[Unset, V0040JobDescMsgMemoryPerCpu]):
        memory_per_node (Union[Unset, V0040JobDescMsgMemoryPerNode]):
        temporary_disk_per_node (Union[Unset, int]):
        selinux_context (Union[Unset, str]):
        required_switches (Union[Unset, V0040JobDescMsgRequiredSwitches]):
        standard_error (Union[Unset, str]):
        standard_input (Union[Unset, str]):
        standard_output (Union[Unset, str]):
        wait_for_switch (Union[Unset, int]):
        wckey (Union[Unset, str]):
        x11 (Union[Unset, list[V0040JobDescMsgX11Item]]):
        x11_magic_cookie (Union[Unset, str]):
        x11_target_host (Union[Unset, str]):
        x11_target_port (Union[Unset, int]):
    """

    account: Union[Unset, str] = UNSET
    account_gather_frequency: Union[Unset, str] = UNSET
    admin_comment: Union[Unset, str] = UNSET
    allocation_node_list: Union[Unset, str] = UNSET
    allocation_node_port: Union[Unset, int] = UNSET
    argv: Union[Unset, "V0040JobDescMsgArgv"] = UNSET
    array: Union[Unset, str] = UNSET
    batch_features: Union[Unset, str] = UNSET
    begin_time: Union[Unset, "V0040JobDescMsgBeginTime"] = UNSET
    flags: Union[Unset, list[V0040JobDescMsgFlagsItem]] = UNSET
    burst_buffer: Union[Unset, str] = UNSET
    clusters: Union[Unset, str] = UNSET
    cluster_constraint: Union[Unset, str] = UNSET
    comment: Union[Unset, str] = UNSET
    contiguous: Union[Unset, bool] = UNSET
    container: Union[Unset, str] = UNSET
    container_id: Union[Unset, str] = UNSET
    cores_per_socket: Union[Unset, int] = UNSET
    core_specification: Union[Unset, int] = UNSET
    thread_specification: Union[Unset, int] = UNSET
    cpu_binding: Union[Unset, str] = UNSET
    cpu_binding_flags: Union[Unset, list[V0040JobDescMsgCpuBindingFlagsItem]] = UNSET
    cpu_frequency: Union[Unset, str] = UNSET
    cpus_per_tres: Union[Unset, str] = UNSET
    crontab: Union[Unset, "V0040JobDescMsgCrontab"] = UNSET
    deadline: Union[Unset, int] = UNSET
    delay_boot: Union[Unset, int] = UNSET
    dependency: Union[Unset, str] = UNSET
    end_time: Union[Unset, int] = UNSET
    environment: Union[Unset, "V0040JobDescMsgEnvironment"] = UNSET
    rlimits: Union[Unset, "V0040JobDescMsgRlimits"] = UNSET
    excluded_nodes: Union[Unset, "V0040JobDescMsgExcludedNodes"] = UNSET
    extra: Union[Unset, str] = UNSET
    constraints: Union[Unset, str] = UNSET
    group_id: Union[Unset, str] = UNSET
    hetjob_group: Union[Unset, int] = UNSET
    immediate: Union[Unset, bool] = UNSET
    job_id: Union[Unset, int] = UNSET
    kill_on_node_fail: Union[Unset, bool] = UNSET
    licenses: Union[Unset, str] = UNSET
    mail_type: Union[Unset, list[V0040JobDescMsgMailTypeItem]] = UNSET
    mail_user: Union[Unset, str] = UNSET
    mcs_label: Union[Unset, str] = UNSET
    memory_binding: Union[Unset, str] = UNSET
    memory_binding_type: Union[Unset, list[V0040JobDescMsgMemoryBindingTypeItem]] = UNSET
    memory_per_tres: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    network: Union[Unset, str] = UNSET
    nice: Union[Unset, int] = UNSET
    tasks: Union[Unset, int] = UNSET
    open_mode: Union[Unset, list[V0040JobDescMsgOpenModeItem]] = UNSET
    reserve_ports: Union[Unset, int] = UNSET
    overcommit: Union[Unset, bool] = UNSET
    partition: Union[Unset, str] = UNSET
    distribution_plane_size: Union[Unset, int] = UNSET
    power_flags: Union[Unset, list[V0040JobDescMsgPowerFlagsItem]] = UNSET
    prefer: Union[Unset, str] = UNSET
    hold: Union[Unset, bool] = UNSET
    priority: Union[Unset, "V0040JobDescMsgPriority"] = UNSET
    profile: Union[Unset, list[V0040JobDescMsgProfileItem]] = UNSET
    qos: Union[Unset, str] = UNSET
    reboot: Union[Unset, bool] = UNSET
    required_nodes: Union[Unset, "V0040JobDescMsgRequiredNodes"] = UNSET
    requeue: Union[Unset, bool] = UNSET
    reservation: Union[Unset, str] = UNSET
    script: Union[Unset, str] = UNSET
    shared: Union[Unset, list[V0040JobDescMsgSharedItem]] = UNSET
    exclusive: Union[Unset, list[V0040JobDescMsgExclusiveItem]] = UNSET
    oversubscribe: Union[Unset, bool] = UNSET
    site_factor: Union[Unset, int] = UNSET
    spank_environment: Union[Unset, "V0040JobDescMsgSpankEnvironment"] = UNSET
    distribution: Union[Unset, str] = UNSET
    time_limit: Union[Unset, "V0040JobDescMsgTimeLimit"] = UNSET
    time_minimum: Union[Unset, "V0040JobDescMsgTimeMinimum"] = UNSET
    tres_bind: Union[Unset, str] = UNSET
    tres_freq: Union[Unset, str] = UNSET
    tres_per_job: Union[Unset, str] = UNSET
    tres_per_node: Union[Unset, str] = UNSET
    tres_per_socket: Union[Unset, str] = UNSET
    tres_per_task: Union[Unset, str] = UNSET
    user_id: Union[Unset, str] = UNSET
    wait_all_nodes: Union[Unset, bool] = UNSET
    kill_warning_flags: Union[Unset, list[V0040JobDescMsgKillWarningFlagsItem]] = UNSET
    kill_warning_signal: Union[Unset, str] = UNSET
    kill_warning_delay: Union[Unset, "V0040JobDescMsgKillWarningDelay"] = UNSET
    current_working_directory: Union[Unset, str] = UNSET
    cpus_per_task: Union[Unset, int] = UNSET
    minimum_cpus: Union[Unset, int] = UNSET
    maximum_cpus: Union[Unset, int] = UNSET
    nodes: Union[Unset, str] = UNSET
    minimum_nodes: Union[Unset, int] = UNSET
    maximum_nodes: Union[Unset, int] = UNSET
    minimum_boards_per_node: Union[Unset, int] = UNSET
    minimum_sockets_per_board: Union[Unset, int] = UNSET
    sockets_per_node: Union[Unset, int] = UNSET
    threads_per_core: Union[Unset, int] = UNSET
    tasks_per_node: Union[Unset, int] = UNSET
    tasks_per_socket: Union[Unset, int] = UNSET
    tasks_per_core: Union[Unset, int] = UNSET
    tasks_per_board: Union[Unset, int] = UNSET
    ntasks_per_tres: Union[Unset, int] = UNSET
    minimum_cpus_per_node: Union[Unset, int] = UNSET
    memory_per_cpu: Union[Unset, "V0040JobDescMsgMemoryPerCpu"] = UNSET
    memory_per_node: Union[Unset, "V0040JobDescMsgMemoryPerNode"] = UNSET
    temporary_disk_per_node: Union[Unset, int] = UNSET
    selinux_context: Union[Unset, str] = UNSET
    required_switches: Union[Unset, "V0040JobDescMsgRequiredSwitches"] = UNSET
    standard_error: Union[Unset, str] = UNSET
    standard_input: Union[Unset, str] = UNSET
    standard_output: Union[Unset, str] = UNSET
    wait_for_switch: Union[Unset, int] = UNSET
    wckey: Union[Unset, str] = UNSET
    x11: Union[Unset, list[V0040JobDescMsgX11Item]] = UNSET
    x11_magic_cookie: Union[Unset, str] = UNSET
    x11_target_host: Union[Unset, str] = UNSET
    x11_target_port: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        account = self.account

        account_gather_frequency = self.account_gather_frequency

        admin_comment = self.admin_comment

        allocation_node_list = self.allocation_node_list

        allocation_node_port = self.allocation_node_port

        argv: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.argv, Unset):
            argv = self.argv.to_dict()

        array = self.array

        batch_features = self.batch_features

        begin_time: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.begin_time, Unset):
            begin_time = self.begin_time.to_dict()

        flags: Union[Unset, list[str]] = UNSET
        if not isinstance(self.flags, Unset):
            flags = []
            for flags_item_data in self.flags:
                flags_item = flags_item_data.value
                flags.append(flags_item)

        burst_buffer = self.burst_buffer

        clusters = self.clusters

        cluster_constraint = self.cluster_constraint

        comment = self.comment

        contiguous = self.contiguous

        container = self.container

        container_id = self.container_id

        cores_per_socket = self.cores_per_socket

        core_specification = self.core_specification

        thread_specification = self.thread_specification

        cpu_binding = self.cpu_binding

        cpu_binding_flags: Union[Unset, list[str]] = UNSET
        if not isinstance(self.cpu_binding_flags, Unset):
            cpu_binding_flags = []
            for cpu_binding_flags_item_data in self.cpu_binding_flags:
                cpu_binding_flags_item = cpu_binding_flags_item_data.value
                cpu_binding_flags.append(cpu_binding_flags_item)

        cpu_frequency = self.cpu_frequency

        cpus_per_tres = self.cpus_per_tres

        crontab: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.crontab, Unset):
            crontab = self.crontab.to_dict()

        deadline = self.deadline

        delay_boot = self.delay_boot

        dependency = self.dependency

        end_time = self.end_time

        environment: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.environment, Unset):
            environment = self.environment.to_dict()

        rlimits: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.rlimits, Unset):
            rlimits = self.rlimits.to_dict()

        excluded_nodes: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.excluded_nodes, Unset):
            excluded_nodes = self.excluded_nodes.to_dict()

        extra = self.extra

        constraints = self.constraints

        group_id = self.group_id

        hetjob_group = self.hetjob_group

        immediate = self.immediate

        job_id = self.job_id

        kill_on_node_fail = self.kill_on_node_fail

        licenses = self.licenses

        mail_type: Union[Unset, list[str]] = UNSET
        if not isinstance(self.mail_type, Unset):
            mail_type = []
            for mail_type_item_data in self.mail_type:
                mail_type_item = mail_type_item_data.value
                mail_type.append(mail_type_item)

        mail_user = self.mail_user

        mcs_label = self.mcs_label

        memory_binding = self.memory_binding

        memory_binding_type: Union[Unset, list[str]] = UNSET
        if not isinstance(self.memory_binding_type, Unset):
            memory_binding_type = []
            for memory_binding_type_item_data in self.memory_binding_type:
                memory_binding_type_item = memory_binding_type_item_data.value
                memory_binding_type.append(memory_binding_type_item)

        memory_per_tres = self.memory_per_tres

        name = self.name

        network = self.network

        nice = self.nice

        tasks = self.tasks

        open_mode: Union[Unset, list[str]] = UNSET
        if not isinstance(self.open_mode, Unset):
            open_mode = []
            for open_mode_item_data in self.open_mode:
                open_mode_item = open_mode_item_data.value
                open_mode.append(open_mode_item)

        reserve_ports = self.reserve_ports

        overcommit = self.overcommit

        partition = self.partition

        distribution_plane_size = self.distribution_plane_size

        power_flags: Union[Unset, list[str]] = UNSET
        if not isinstance(self.power_flags, Unset):
            power_flags = []
            for power_flags_item_data in self.power_flags:
                power_flags_item = power_flags_item_data.value
                power_flags.append(power_flags_item)

        prefer = self.prefer

        hold = self.hold

        priority: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.priority, Unset):
            priority = self.priority.to_dict()

        profile: Union[Unset, list[str]] = UNSET
        if not isinstance(self.profile, Unset):
            profile = []
            for profile_item_data in self.profile:
                profile_item = profile_item_data.value
                profile.append(profile_item)

        qos = self.qos

        reboot = self.reboot

        required_nodes: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.required_nodes, Unset):
            required_nodes = self.required_nodes.to_dict()

        requeue = self.requeue

        reservation = self.reservation

        script = self.script

        shared: Union[Unset, list[str]] = UNSET
        if not isinstance(self.shared, Unset):
            shared = []
            for shared_item_data in self.shared:
                shared_item = shared_item_data.value
                shared.append(shared_item)

        exclusive: Union[Unset, list[str]] = UNSET
        if not isinstance(self.exclusive, Unset):
            exclusive = []
            for exclusive_item_data in self.exclusive:
                exclusive_item = exclusive_item_data.value
                exclusive.append(exclusive_item)

        oversubscribe = self.oversubscribe

        site_factor = self.site_factor

        spank_environment: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.spank_environment, Unset):
            spank_environment = self.spank_environment.to_dict()

        distribution = self.distribution

        time_limit: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.time_limit, Unset):
            time_limit = self.time_limit.to_dict()

        time_minimum: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.time_minimum, Unset):
            time_minimum = self.time_minimum.to_dict()

        tres_bind = self.tres_bind

        tres_freq = self.tres_freq

        tres_per_job = self.tres_per_job

        tres_per_node = self.tres_per_node

        tres_per_socket = self.tres_per_socket

        tres_per_task = self.tres_per_task

        user_id = self.user_id

        wait_all_nodes = self.wait_all_nodes

        kill_warning_flags: Union[Unset, list[str]] = UNSET
        if not isinstance(self.kill_warning_flags, Unset):
            kill_warning_flags = []
            for kill_warning_flags_item_data in self.kill_warning_flags:
                kill_warning_flags_item = kill_warning_flags_item_data.value
                kill_warning_flags.append(kill_warning_flags_item)

        kill_warning_signal = self.kill_warning_signal

        kill_warning_delay: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.kill_warning_delay, Unset):
            kill_warning_delay = self.kill_warning_delay.to_dict()

        current_working_directory = self.current_working_directory

        cpus_per_task = self.cpus_per_task

        minimum_cpus = self.minimum_cpus

        maximum_cpus = self.maximum_cpus

        nodes = self.nodes

        minimum_nodes = self.minimum_nodes

        maximum_nodes = self.maximum_nodes

        minimum_boards_per_node = self.minimum_boards_per_node

        minimum_sockets_per_board = self.minimum_sockets_per_board

        sockets_per_node = self.sockets_per_node

        threads_per_core = self.threads_per_core

        tasks_per_node = self.tasks_per_node

        tasks_per_socket = self.tasks_per_socket

        tasks_per_core = self.tasks_per_core

        tasks_per_board = self.tasks_per_board

        ntasks_per_tres = self.ntasks_per_tres

        minimum_cpus_per_node = self.minimum_cpus_per_node

        memory_per_cpu: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.memory_per_cpu, Unset):
            memory_per_cpu = self.memory_per_cpu.to_dict()

        memory_per_node: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.memory_per_node, Unset):
            memory_per_node = self.memory_per_node.to_dict()

        temporary_disk_per_node = self.temporary_disk_per_node

        selinux_context = self.selinux_context

        required_switches: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.required_switches, Unset):
            required_switches = self.required_switches.to_dict()

        standard_error = self.standard_error

        standard_input = self.standard_input

        standard_output = self.standard_output

        wait_for_switch = self.wait_for_switch

        wckey = self.wckey

        x11: Union[Unset, list[str]] = UNSET
        if not isinstance(self.x11, Unset):
            x11 = []
            for x11_item_data in self.x11:
                x11_item = x11_item_data.value
                x11.append(x11_item)

        x11_magic_cookie = self.x11_magic_cookie

        x11_target_host = self.x11_target_host

        x11_target_port = self.x11_target_port

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if account is not UNSET:
            field_dict["account"] = account
        if account_gather_frequency is not UNSET:
            field_dict["account_gather_frequency"] = account_gather_frequency
        if admin_comment is not UNSET:
            field_dict["admin_comment"] = admin_comment
        if allocation_node_list is not UNSET:
            field_dict["allocation_node_list"] = allocation_node_list
        if allocation_node_port is not UNSET:
            field_dict["allocation_node_port"] = allocation_node_port
        if argv is not UNSET:
            field_dict["argv"] = argv
        if array is not UNSET:
            field_dict["array"] = array
        if batch_features is not UNSET:
            field_dict["batch_features"] = batch_features
        if begin_time is not UNSET:
            field_dict["begin_time"] = begin_time
        if flags is not UNSET:
            field_dict["flags"] = flags
        if burst_buffer is not UNSET:
            field_dict["burst_buffer"] = burst_buffer
        if clusters is not UNSET:
            field_dict["clusters"] = clusters
        if cluster_constraint is not UNSET:
            field_dict["cluster_constraint"] = cluster_constraint
        if comment is not UNSET:
            field_dict["comment"] = comment
        if contiguous is not UNSET:
            field_dict["contiguous"] = contiguous
        if container is not UNSET:
            field_dict["container"] = container
        if container_id is not UNSET:
            field_dict["container_id"] = container_id
        if cores_per_socket is not UNSET:
            field_dict["cores_per_socket"] = cores_per_socket
        if core_specification is not UNSET:
            field_dict["core_specification"] = core_specification
        if thread_specification is not UNSET:
            field_dict["thread_specification"] = thread_specification
        if cpu_binding is not UNSET:
            field_dict["cpu_binding"] = cpu_binding
        if cpu_binding_flags is not UNSET:
            field_dict["cpu_binding_flags"] = cpu_binding_flags
        if cpu_frequency is not UNSET:
            field_dict["cpu_frequency"] = cpu_frequency
        if cpus_per_tres is not UNSET:
            field_dict["cpus_per_tres"] = cpus_per_tres
        if crontab is not UNSET:
            field_dict["crontab"] = crontab
        if deadline is not UNSET:
            field_dict["deadline"] = deadline
        if delay_boot is not UNSET:
            field_dict["delay_boot"] = delay_boot
        if dependency is not UNSET:
            field_dict["dependency"] = dependency
        if end_time is not UNSET:
            field_dict["end_time"] = end_time
        if environment is not UNSET:
            field_dict["environment"] = environment
        if rlimits is not UNSET:
            field_dict["rlimits"] = rlimits
        if excluded_nodes is not UNSET:
            field_dict["excluded_nodes"] = excluded_nodes
        if extra is not UNSET:
            field_dict["extra"] = extra
        if constraints is not UNSET:
            field_dict["constraints"] = constraints
        if group_id is not UNSET:
            field_dict["group_id"] = group_id
        if hetjob_group is not UNSET:
            field_dict["hetjob_group"] = hetjob_group
        if immediate is not UNSET:
            field_dict["immediate"] = immediate
        if job_id is not UNSET:
            field_dict["job_id"] = job_id
        if kill_on_node_fail is not UNSET:
            field_dict["kill_on_node_fail"] = kill_on_node_fail
        if licenses is not UNSET:
            field_dict["licenses"] = licenses
        if mail_type is not UNSET:
            field_dict["mail_type"] = mail_type
        if mail_user is not UNSET:
            field_dict["mail_user"] = mail_user
        if mcs_label is not UNSET:
            field_dict["mcs_label"] = mcs_label
        if memory_binding is not UNSET:
            field_dict["memory_binding"] = memory_binding
        if memory_binding_type is not UNSET:
            field_dict["memory_binding_type"] = memory_binding_type
        if memory_per_tres is not UNSET:
            field_dict["memory_per_tres"] = memory_per_tres
        if name is not UNSET:
            field_dict["name"] = name
        if network is not UNSET:
            field_dict["network"] = network
        if nice is not UNSET:
            field_dict["nice"] = nice
        if tasks is not UNSET:
            field_dict["tasks"] = tasks
        if open_mode is not UNSET:
            field_dict["open_mode"] = open_mode
        if reserve_ports is not UNSET:
            field_dict["reserve_ports"] = reserve_ports
        if overcommit is not UNSET:
            field_dict["overcommit"] = overcommit
        if partition is not UNSET:
            field_dict["partition"] = partition
        if distribution_plane_size is not UNSET:
            field_dict["distribution_plane_size"] = distribution_plane_size
        if power_flags is not UNSET:
            field_dict["power_flags"] = power_flags
        if prefer is not UNSET:
            field_dict["prefer"] = prefer
        if hold is not UNSET:
            field_dict["hold"] = hold
        if priority is not UNSET:
            field_dict["priority"] = priority
        if profile is not UNSET:
            field_dict["profile"] = profile
        if qos is not UNSET:
            field_dict["qos"] = qos
        if reboot is not UNSET:
            field_dict["reboot"] = reboot
        if required_nodes is not UNSET:
            field_dict["required_nodes"] = required_nodes
        if requeue is not UNSET:
            field_dict["requeue"] = requeue
        if reservation is not UNSET:
            field_dict["reservation"] = reservation
        if script is not UNSET:
            field_dict["script"] = script
        if shared is not UNSET:
            field_dict["shared"] = shared
        if exclusive is not UNSET:
            field_dict["exclusive"] = exclusive
        if oversubscribe is not UNSET:
            field_dict["oversubscribe"] = oversubscribe
        if site_factor is not UNSET:
            field_dict["site_factor"] = site_factor
        if spank_environment is not UNSET:
            field_dict["spank_environment"] = spank_environment
        if distribution is not UNSET:
            field_dict["distribution"] = distribution
        if time_limit is not UNSET:
            field_dict["time_limit"] = time_limit
        if time_minimum is not UNSET:
            field_dict["time_minimum"] = time_minimum
        if tres_bind is not UNSET:
            field_dict["tres_bind"] = tres_bind
        if tres_freq is not UNSET:
            field_dict["tres_freq"] = tres_freq
        if tres_per_job is not UNSET:
            field_dict["tres_per_job"] = tres_per_job
        if tres_per_node is not UNSET:
            field_dict["tres_per_node"] = tres_per_node
        if tres_per_socket is not UNSET:
            field_dict["tres_per_socket"] = tres_per_socket
        if tres_per_task is not UNSET:
            field_dict["tres_per_task"] = tres_per_task
        if user_id is not UNSET:
            field_dict["user_id"] = user_id
        if wait_all_nodes is not UNSET:
            field_dict["wait_all_nodes"] = wait_all_nodes
        if kill_warning_flags is not UNSET:
            field_dict["kill_warning_flags"] = kill_warning_flags
        if kill_warning_signal is not UNSET:
            field_dict["kill_warning_signal"] = kill_warning_signal
        if kill_warning_delay is not UNSET:
            field_dict["kill_warning_delay"] = kill_warning_delay
        if current_working_directory is not UNSET:
            field_dict["current_working_directory"] = current_working_directory
        if cpus_per_task is not UNSET:
            field_dict["cpus_per_task"] = cpus_per_task
        if minimum_cpus is not UNSET:
            field_dict["minimum_cpus"] = minimum_cpus
        if maximum_cpus is not UNSET:
            field_dict["maximum_cpus"] = maximum_cpus
        if nodes is not UNSET:
            field_dict["nodes"] = nodes
        if minimum_nodes is not UNSET:
            field_dict["minimum_nodes"] = minimum_nodes
        if maximum_nodes is not UNSET:
            field_dict["maximum_nodes"] = maximum_nodes
        if minimum_boards_per_node is not UNSET:
            field_dict["minimum_boards_per_node"] = minimum_boards_per_node
        if minimum_sockets_per_board is not UNSET:
            field_dict["minimum_sockets_per_board"] = minimum_sockets_per_board
        if sockets_per_node is not UNSET:
            field_dict["sockets_per_node"] = sockets_per_node
        if threads_per_core is not UNSET:
            field_dict["threads_per_core"] = threads_per_core
        if tasks_per_node is not UNSET:
            field_dict["tasks_per_node"] = tasks_per_node
        if tasks_per_socket is not UNSET:
            field_dict["tasks_per_socket"] = tasks_per_socket
        if tasks_per_core is not UNSET:
            field_dict["tasks_per_core"] = tasks_per_core
        if tasks_per_board is not UNSET:
            field_dict["tasks_per_board"] = tasks_per_board
        if ntasks_per_tres is not UNSET:
            field_dict["ntasks_per_tres"] = ntasks_per_tres
        if minimum_cpus_per_node is not UNSET:
            field_dict["minimum_cpus_per_node"] = minimum_cpus_per_node
        if memory_per_cpu is not UNSET:
            field_dict["memory_per_cpu"] = memory_per_cpu
        if memory_per_node is not UNSET:
            field_dict["memory_per_node"] = memory_per_node
        if temporary_disk_per_node is not UNSET:
            field_dict["temporary_disk_per_node"] = temporary_disk_per_node
        if selinux_context is not UNSET:
            field_dict["selinux_context"] = selinux_context
        if required_switches is not UNSET:
            field_dict["required_switches"] = required_switches
        if standard_error is not UNSET:
            field_dict["standard_error"] = standard_error
        if standard_input is not UNSET:
            field_dict["standard_input"] = standard_input
        if standard_output is not UNSET:
            field_dict["standard_output"] = standard_output
        if wait_for_switch is not UNSET:
            field_dict["wait_for_switch"] = wait_for_switch
        if wckey is not UNSET:
            field_dict["wckey"] = wckey
        if x11 is not UNSET:
            field_dict["x11"] = x11
        if x11_magic_cookie is not UNSET:
            field_dict["x11_magic_cookie"] = x11_magic_cookie
        if x11_target_host is not UNSET:
            field_dict["x11_target_host"] = x11_target_host
        if x11_target_port is not UNSET:
            field_dict["x11_target_port"] = x11_target_port

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0040_job_desc_msg_argv import V0040JobDescMsgArgv
        from ..models.v0040_job_desc_msg_begin_time import V0040JobDescMsgBeginTime
        from ..models.v0040_job_desc_msg_crontab import V0040JobDescMsgCrontab
        from ..models.v0040_job_desc_msg_environment import V0040JobDescMsgEnvironment
        from ..models.v0040_job_desc_msg_excluded_nodes import V0040JobDescMsgExcludedNodes
        from ..models.v0040_job_desc_msg_kill_warning_delay import V0040JobDescMsgKillWarningDelay
        from ..models.v0040_job_desc_msg_memory_per_cpu import V0040JobDescMsgMemoryPerCpu
        from ..models.v0040_job_desc_msg_memory_per_node import V0040JobDescMsgMemoryPerNode
        from ..models.v0040_job_desc_msg_priority import V0040JobDescMsgPriority
        from ..models.v0040_job_desc_msg_required_nodes import V0040JobDescMsgRequiredNodes
        from ..models.v0040_job_desc_msg_required_switches import V0040JobDescMsgRequiredSwitches
        from ..models.v0040_job_desc_msg_rlimits import V0040JobDescMsgRlimits
        from ..models.v0040_job_desc_msg_spank_environment import V0040JobDescMsgSpankEnvironment
        from ..models.v0040_job_desc_msg_time_limit import V0040JobDescMsgTimeLimit
        from ..models.v0040_job_desc_msg_time_minimum import V0040JobDescMsgTimeMinimum

        d = dict(src_dict)
        account = d.pop("account", UNSET)

        account_gather_frequency = d.pop("account_gather_frequency", UNSET)

        admin_comment = d.pop("admin_comment", UNSET)

        allocation_node_list = d.pop("allocation_node_list", UNSET)

        allocation_node_port = d.pop("allocation_node_port", UNSET)

        _argv = d.pop("argv", UNSET)
        argv: Union[Unset, V0040JobDescMsgArgv]
        if isinstance(_argv, Unset):
            argv = UNSET
        else:
            argv = V0040JobDescMsgArgv.from_dict(_argv)

        array = d.pop("array", UNSET)

        batch_features = d.pop("batch_features", UNSET)

        _begin_time = d.pop("begin_time", UNSET)
        begin_time: Union[Unset, V0040JobDescMsgBeginTime]
        if isinstance(_begin_time, Unset):
            begin_time = UNSET
        else:
            begin_time = V0040JobDescMsgBeginTime.from_dict(_begin_time)

        flags = []
        _flags = d.pop("flags", UNSET)
        for flags_item_data in _flags or []:
            flags_item = V0040JobDescMsgFlagsItem(flags_item_data)

            flags.append(flags_item)

        burst_buffer = d.pop("burst_buffer", UNSET)

        clusters = d.pop("clusters", UNSET)

        cluster_constraint = d.pop("cluster_constraint", UNSET)

        comment = d.pop("comment", UNSET)

        contiguous = d.pop("contiguous", UNSET)

        container = d.pop("container", UNSET)

        container_id = d.pop("container_id", UNSET)

        cores_per_socket = d.pop("cores_per_socket", UNSET)

        core_specification = d.pop("core_specification", UNSET)

        thread_specification = d.pop("thread_specification", UNSET)

        cpu_binding = d.pop("cpu_binding", UNSET)

        cpu_binding_flags = []
        _cpu_binding_flags = d.pop("cpu_binding_flags", UNSET)
        for cpu_binding_flags_item_data in _cpu_binding_flags or []:
            cpu_binding_flags_item = V0040JobDescMsgCpuBindingFlagsItem(cpu_binding_flags_item_data)

            cpu_binding_flags.append(cpu_binding_flags_item)

        cpu_frequency = d.pop("cpu_frequency", UNSET)

        cpus_per_tres = d.pop("cpus_per_tres", UNSET)

        _crontab = d.pop("crontab", UNSET)
        crontab: Union[Unset, V0040JobDescMsgCrontab]
        if isinstance(_crontab, Unset):
            crontab = UNSET
        else:
            crontab = V0040JobDescMsgCrontab.from_dict(_crontab)

        deadline = d.pop("deadline", UNSET)

        delay_boot = d.pop("delay_boot", UNSET)

        dependency = d.pop("dependency", UNSET)

        end_time = d.pop("end_time", UNSET)

        _environment = d.pop("environment", UNSET)
        environment: Union[Unset, V0040JobDescMsgEnvironment]
        if isinstance(_environment, Unset):
            environment = UNSET
        else:
            environment = V0040JobDescMsgEnvironment.from_dict(_environment)

        _rlimits = d.pop("rlimits", UNSET)
        rlimits: Union[Unset, V0040JobDescMsgRlimits]
        if isinstance(_rlimits, Unset):
            rlimits = UNSET
        else:
            rlimits = V0040JobDescMsgRlimits.from_dict(_rlimits)

        _excluded_nodes = d.pop("excluded_nodes", UNSET)
        excluded_nodes: Union[Unset, V0040JobDescMsgExcludedNodes]
        if isinstance(_excluded_nodes, Unset):
            excluded_nodes = UNSET
        else:
            excluded_nodes = V0040JobDescMsgExcludedNodes.from_dict(_excluded_nodes)

        extra = d.pop("extra", UNSET)

        constraints = d.pop("constraints", UNSET)

        group_id = d.pop("group_id", UNSET)

        hetjob_group = d.pop("hetjob_group", UNSET)

        immediate = d.pop("immediate", UNSET)

        job_id = d.pop("job_id", UNSET)

        kill_on_node_fail = d.pop("kill_on_node_fail", UNSET)

        licenses = d.pop("licenses", UNSET)

        mail_type = []
        _mail_type = d.pop("mail_type", UNSET)
        for mail_type_item_data in _mail_type or []:
            mail_type_item = V0040JobDescMsgMailTypeItem(mail_type_item_data)

            mail_type.append(mail_type_item)

        mail_user = d.pop("mail_user", UNSET)

        mcs_label = d.pop("mcs_label", UNSET)

        memory_binding = d.pop("memory_binding", UNSET)

        memory_binding_type = []
        _memory_binding_type = d.pop("memory_binding_type", UNSET)
        for memory_binding_type_item_data in _memory_binding_type or []:
            memory_binding_type_item = V0040JobDescMsgMemoryBindingTypeItem(memory_binding_type_item_data)

            memory_binding_type.append(memory_binding_type_item)

        memory_per_tres = d.pop("memory_per_tres", UNSET)

        name = d.pop("name", UNSET)

        network = d.pop("network", UNSET)

        nice = d.pop("nice", UNSET)

        tasks = d.pop("tasks", UNSET)

        open_mode = []
        _open_mode = d.pop("open_mode", UNSET)
        for open_mode_item_data in _open_mode or []:
            open_mode_item = V0040JobDescMsgOpenModeItem(open_mode_item_data)

            open_mode.append(open_mode_item)

        reserve_ports = d.pop("reserve_ports", UNSET)

        overcommit = d.pop("overcommit", UNSET)

        partition = d.pop("partition", UNSET)

        distribution_plane_size = d.pop("distribution_plane_size", UNSET)

        power_flags = []
        _power_flags = d.pop("power_flags", UNSET)
        for power_flags_item_data in _power_flags or []:
            power_flags_item = V0040JobDescMsgPowerFlagsItem(power_flags_item_data)

            power_flags.append(power_flags_item)

        prefer = d.pop("prefer", UNSET)

        hold = d.pop("hold", UNSET)

        _priority = d.pop("priority", UNSET)
        priority: Union[Unset, V0040JobDescMsgPriority]
        if isinstance(_priority, Unset):
            priority = UNSET
        else:
            priority = V0040JobDescMsgPriority.from_dict(_priority)

        profile = []
        _profile = d.pop("profile", UNSET)
        for profile_item_data in _profile or []:
            profile_item = V0040JobDescMsgProfileItem(profile_item_data)

            profile.append(profile_item)

        qos = d.pop("qos", UNSET)

        reboot = d.pop("reboot", UNSET)

        _required_nodes = d.pop("required_nodes", UNSET)
        required_nodes: Union[Unset, V0040JobDescMsgRequiredNodes]
        if isinstance(_required_nodes, Unset):
            required_nodes = UNSET
        else:
            required_nodes = V0040JobDescMsgRequiredNodes.from_dict(_required_nodes)

        requeue = d.pop("requeue", UNSET)

        reservation = d.pop("reservation", UNSET)

        script = d.pop("script", UNSET)

        shared = []
        _shared = d.pop("shared", UNSET)
        for shared_item_data in _shared or []:
            shared_item = V0040JobDescMsgSharedItem(shared_item_data)

            shared.append(shared_item)

        exclusive = []
        _exclusive = d.pop("exclusive", UNSET)
        for exclusive_item_data in _exclusive or []:
            exclusive_item = V0040JobDescMsgExclusiveItem(exclusive_item_data)

            exclusive.append(exclusive_item)

        oversubscribe = d.pop("oversubscribe", UNSET)

        site_factor = d.pop("site_factor", UNSET)

        _spank_environment = d.pop("spank_environment", UNSET)
        spank_environment: Union[Unset, V0040JobDescMsgSpankEnvironment]
        if isinstance(_spank_environment, Unset):
            spank_environment = UNSET
        else:
            spank_environment = V0040JobDescMsgSpankEnvironment.from_dict(_spank_environment)

        distribution = d.pop("distribution", UNSET)

        _time_limit = d.pop("time_limit", UNSET)
        time_limit: Union[Unset, V0040JobDescMsgTimeLimit]
        if isinstance(_time_limit, Unset):
            time_limit = UNSET
        else:
            time_limit = V0040JobDescMsgTimeLimit.from_dict(_time_limit)

        _time_minimum = d.pop("time_minimum", UNSET)
        time_minimum: Union[Unset, V0040JobDescMsgTimeMinimum]
        if isinstance(_time_minimum, Unset):
            time_minimum = UNSET
        else:
            time_minimum = V0040JobDescMsgTimeMinimum.from_dict(_time_minimum)

        tres_bind = d.pop("tres_bind", UNSET)

        tres_freq = d.pop("tres_freq", UNSET)

        tres_per_job = d.pop("tres_per_job", UNSET)

        tres_per_node = d.pop("tres_per_node", UNSET)

        tres_per_socket = d.pop("tres_per_socket", UNSET)

        tres_per_task = d.pop("tres_per_task", UNSET)

        user_id = d.pop("user_id", UNSET)

        wait_all_nodes = d.pop("wait_all_nodes", UNSET)

        kill_warning_flags = []
        _kill_warning_flags = d.pop("kill_warning_flags", UNSET)
        for kill_warning_flags_item_data in _kill_warning_flags or []:
            kill_warning_flags_item = V0040JobDescMsgKillWarningFlagsItem(kill_warning_flags_item_data)

            kill_warning_flags.append(kill_warning_flags_item)

        kill_warning_signal = d.pop("kill_warning_signal", UNSET)

        _kill_warning_delay = d.pop("kill_warning_delay", UNSET)
        kill_warning_delay: Union[Unset, V0040JobDescMsgKillWarningDelay]
        if isinstance(_kill_warning_delay, Unset):
            kill_warning_delay = UNSET
        else:
            kill_warning_delay = V0040JobDescMsgKillWarningDelay.from_dict(_kill_warning_delay)

        current_working_directory = d.pop("current_working_directory", UNSET)

        cpus_per_task = d.pop("cpus_per_task", UNSET)

        minimum_cpus = d.pop("minimum_cpus", UNSET)

        maximum_cpus = d.pop("maximum_cpus", UNSET)

        nodes = d.pop("nodes", UNSET)

        minimum_nodes = d.pop("minimum_nodes", UNSET)

        maximum_nodes = d.pop("maximum_nodes", UNSET)

        minimum_boards_per_node = d.pop("minimum_boards_per_node", UNSET)

        minimum_sockets_per_board = d.pop("minimum_sockets_per_board", UNSET)

        sockets_per_node = d.pop("sockets_per_node", UNSET)

        threads_per_core = d.pop("threads_per_core", UNSET)

        tasks_per_node = d.pop("tasks_per_node", UNSET)

        tasks_per_socket = d.pop("tasks_per_socket", UNSET)

        tasks_per_core = d.pop("tasks_per_core", UNSET)

        tasks_per_board = d.pop("tasks_per_board", UNSET)

        ntasks_per_tres = d.pop("ntasks_per_tres", UNSET)

        minimum_cpus_per_node = d.pop("minimum_cpus_per_node", UNSET)

        _memory_per_cpu = d.pop("memory_per_cpu", UNSET)
        memory_per_cpu: Union[Unset, V0040JobDescMsgMemoryPerCpu]
        if isinstance(_memory_per_cpu, Unset):
            memory_per_cpu = UNSET
        else:
            memory_per_cpu = V0040JobDescMsgMemoryPerCpu.from_dict(_memory_per_cpu)

        _memory_per_node = d.pop("memory_per_node", UNSET)
        memory_per_node: Union[Unset, V0040JobDescMsgMemoryPerNode]
        if isinstance(_memory_per_node, Unset):
            memory_per_node = UNSET
        else:
            memory_per_node = V0040JobDescMsgMemoryPerNode.from_dict(_memory_per_node)

        temporary_disk_per_node = d.pop("temporary_disk_per_node", UNSET)

        selinux_context = d.pop("selinux_context", UNSET)

        _required_switches = d.pop("required_switches", UNSET)
        required_switches: Union[Unset, V0040JobDescMsgRequiredSwitches]
        if isinstance(_required_switches, Unset):
            required_switches = UNSET
        else:
            required_switches = V0040JobDescMsgRequiredSwitches.from_dict(_required_switches)

        standard_error = d.pop("standard_error", UNSET)

        standard_input = d.pop("standard_input", UNSET)

        standard_output = d.pop("standard_output", UNSET)

        wait_for_switch = d.pop("wait_for_switch", UNSET)

        wckey = d.pop("wckey", UNSET)

        x11 = []
        _x11 = d.pop("x11", UNSET)
        for x11_item_data in _x11 or []:
            x11_item = V0040JobDescMsgX11Item(x11_item_data)

            x11.append(x11_item)

        x11_magic_cookie = d.pop("x11_magic_cookie", UNSET)

        x11_target_host = d.pop("x11_target_host", UNSET)

        x11_target_port = d.pop("x11_target_port", UNSET)

        v0040_job_desc_msg = cls(
            account=account,
            account_gather_frequency=account_gather_frequency,
            admin_comment=admin_comment,
            allocation_node_list=allocation_node_list,
            allocation_node_port=allocation_node_port,
            argv=argv,
            array=array,
            batch_features=batch_features,
            begin_time=begin_time,
            flags=flags,
            burst_buffer=burst_buffer,
            clusters=clusters,
            cluster_constraint=cluster_constraint,
            comment=comment,
            contiguous=contiguous,
            container=container,
            container_id=container_id,
            cores_per_socket=cores_per_socket,
            core_specification=core_specification,
            thread_specification=thread_specification,
            cpu_binding=cpu_binding,
            cpu_binding_flags=cpu_binding_flags,
            cpu_frequency=cpu_frequency,
            cpus_per_tres=cpus_per_tres,
            crontab=crontab,
            deadline=deadline,
            delay_boot=delay_boot,
            dependency=dependency,
            end_time=end_time,
            environment=environment,
            rlimits=rlimits,
            excluded_nodes=excluded_nodes,
            extra=extra,
            constraints=constraints,
            group_id=group_id,
            hetjob_group=hetjob_group,
            immediate=immediate,
            job_id=job_id,
            kill_on_node_fail=kill_on_node_fail,
            licenses=licenses,
            mail_type=mail_type,
            mail_user=mail_user,
            mcs_label=mcs_label,
            memory_binding=memory_binding,
            memory_binding_type=memory_binding_type,
            memory_per_tres=memory_per_tres,
            name=name,
            network=network,
            nice=nice,
            tasks=tasks,
            open_mode=open_mode,
            reserve_ports=reserve_ports,
            overcommit=overcommit,
            partition=partition,
            distribution_plane_size=distribution_plane_size,
            power_flags=power_flags,
            prefer=prefer,
            hold=hold,
            priority=priority,
            profile=profile,
            qos=qos,
            reboot=reboot,
            required_nodes=required_nodes,
            requeue=requeue,
            reservation=reservation,
            script=script,
            shared=shared,
            exclusive=exclusive,
            oversubscribe=oversubscribe,
            site_factor=site_factor,
            spank_environment=spank_environment,
            distribution=distribution,
            time_limit=time_limit,
            time_minimum=time_minimum,
            tres_bind=tres_bind,
            tres_freq=tres_freq,
            tres_per_job=tres_per_job,
            tres_per_node=tres_per_node,
            tres_per_socket=tres_per_socket,
            tres_per_task=tres_per_task,
            user_id=user_id,
            wait_all_nodes=wait_all_nodes,
            kill_warning_flags=kill_warning_flags,
            kill_warning_signal=kill_warning_signal,
            kill_warning_delay=kill_warning_delay,
            current_working_directory=current_working_directory,
            cpus_per_task=cpus_per_task,
            minimum_cpus=minimum_cpus,
            maximum_cpus=maximum_cpus,
            nodes=nodes,
            minimum_nodes=minimum_nodes,
            maximum_nodes=maximum_nodes,
            minimum_boards_per_node=minimum_boards_per_node,
            minimum_sockets_per_board=minimum_sockets_per_board,
            sockets_per_node=sockets_per_node,
            threads_per_core=threads_per_core,
            tasks_per_node=tasks_per_node,
            tasks_per_socket=tasks_per_socket,
            tasks_per_core=tasks_per_core,
            tasks_per_board=tasks_per_board,
            ntasks_per_tres=ntasks_per_tres,
            minimum_cpus_per_node=minimum_cpus_per_node,
            memory_per_cpu=memory_per_cpu,
            memory_per_node=memory_per_node,
            temporary_disk_per_node=temporary_disk_per_node,
            selinux_context=selinux_context,
            required_switches=required_switches,
            standard_error=standard_error,
            standard_input=standard_input,
            standard_output=standard_output,
            wait_for_switch=wait_for_switch,
            wckey=wckey,
            x11=x11,
            x11_magic_cookie=x11_magic_cookie,
            x11_target_host=x11_target_host,
            x11_target_port=x11_target_port,
        )

        v0040_job_desc_msg.additional_properties = d
        return v0040_job_desc_msg

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
