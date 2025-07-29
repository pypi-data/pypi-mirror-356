from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.v0040_job_info_exclusive_item import V0040JobInfoExclusiveItem
from ..models.v0040_job_info_flags_item import V0040JobInfoFlagsItem
from ..models.v0040_job_info_job_state_item import V0040JobInfoJobStateItem
from ..models.v0040_job_info_mail_type_item import V0040JobInfoMailTypeItem
from ..models.v0040_job_info_profile_item import V0040JobInfoProfileItem
from ..models.v0040_job_info_shared_item import V0040JobInfoSharedItem
from ..models.v0040_job_info_show_flags_item import V0040JobInfoShowFlagsItem
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_job_info_accrue_time import V0040JobInfoAccrueTime
    from ..models.v0040_job_info_array_job_id import V0040JobInfoArrayJobId
    from ..models.v0040_job_info_array_max_tasks import V0040JobInfoArrayMaxTasks
    from ..models.v0040_job_info_array_task_id import V0040JobInfoArrayTaskId
    from ..models.v0040_job_info_billable_tres import V0040JobInfoBillableTres
    from ..models.v0040_job_info_cores_per_socket import V0040JobInfoCoresPerSocket
    from ..models.v0040_job_info_cpu_frequency_governor import V0040JobInfoCpuFrequencyGovernor
    from ..models.v0040_job_info_cpu_frequency_maximum import V0040JobInfoCpuFrequencyMaximum
    from ..models.v0040_job_info_cpu_frequency_minimum import V0040JobInfoCpuFrequencyMinimum
    from ..models.v0040_job_info_cpus import V0040JobInfoCpus
    from ..models.v0040_job_info_cpus_per_task import V0040JobInfoCpusPerTask
    from ..models.v0040_job_info_deadline import V0040JobInfoDeadline
    from ..models.v0040_job_info_delay_boot import V0040JobInfoDelayBoot
    from ..models.v0040_job_info_derived_exit_code import V0040JobInfoDerivedExitCode
    from ..models.v0040_job_info_eligible_time import V0040JobInfoEligibleTime
    from ..models.v0040_job_info_end_time import V0040JobInfoEndTime
    from ..models.v0040_job_info_exit_code import V0040JobInfoExitCode
    from ..models.v0040_job_info_gres_detail import V0040JobInfoGresDetail
    from ..models.v0040_job_info_het_job_id import V0040JobInfoHetJobId
    from ..models.v0040_job_info_het_job_offset import V0040JobInfoHetJobOffset
    from ..models.v0040_job_info_job_resources import V0040JobInfoJobResources
    from ..models.v0040_job_info_job_size_str import V0040JobInfoJobSizeStr
    from ..models.v0040_job_info_last_sched_evaluation import V0040JobInfoLastSchedEvaluation
    from ..models.v0040_job_info_max_cpus import V0040JobInfoMaxCpus
    from ..models.v0040_job_info_max_nodes import V0040JobInfoMaxNodes
    from ..models.v0040_job_info_memory_per_cpu import V0040JobInfoMemoryPerCpu
    from ..models.v0040_job_info_memory_per_node import V0040JobInfoMemoryPerNode
    from ..models.v0040_job_info_minimum_cpus_per_node import V0040JobInfoMinimumCpusPerNode
    from ..models.v0040_job_info_minimum_tmp_disk_per_node import V0040JobInfoMinimumTmpDiskPerNode
    from ..models.v0040_job_info_node_count import V0040JobInfoNodeCount
    from ..models.v0040_job_info_power import V0040JobInfoPower
    from ..models.v0040_job_info_pre_sus_time import V0040JobInfoPreSusTime
    from ..models.v0040_job_info_preempt_time import V0040JobInfoPreemptTime
    from ..models.v0040_job_info_preemptable_time import V0040JobInfoPreemptableTime
    from ..models.v0040_job_info_priority import V0040JobInfoPriority
    from ..models.v0040_job_info_resize_time import V0040JobInfoResizeTime
    from ..models.v0040_job_info_sockets_per_node import V0040JobInfoSocketsPerNode
    from ..models.v0040_job_info_start_time import V0040JobInfoStartTime
    from ..models.v0040_job_info_submit_time import V0040JobInfoSubmitTime
    from ..models.v0040_job_info_suspend_time import V0040JobInfoSuspendTime
    from ..models.v0040_job_info_tasks import V0040JobInfoTasks
    from ..models.v0040_job_info_tasks_per_board import V0040JobInfoTasksPerBoard
    from ..models.v0040_job_info_tasks_per_core import V0040JobInfoTasksPerCore
    from ..models.v0040_job_info_tasks_per_node import V0040JobInfoTasksPerNode
    from ..models.v0040_job_info_tasks_per_socket import V0040JobInfoTasksPerSocket
    from ..models.v0040_job_info_tasks_per_tres import V0040JobInfoTasksPerTres
    from ..models.v0040_job_info_threads_per_core import V0040JobInfoThreadsPerCore
    from ..models.v0040_job_info_time_limit import V0040JobInfoTimeLimit
    from ..models.v0040_job_info_time_minimum import V0040JobInfoTimeMinimum


T = TypeVar("T", bound="V0040JobInfo")


@_attrs_define
class V0040JobInfo:
    """
    Attributes:
        account (Union[Unset, str]):
        accrue_time (Union[Unset, V0040JobInfoAccrueTime]):
        admin_comment (Union[Unset, str]):
        allocating_node (Union[Unset, str]):
        array_job_id (Union[Unset, V0040JobInfoArrayJobId]):
        array_task_id (Union[Unset, V0040JobInfoArrayTaskId]):
        array_max_tasks (Union[Unset, V0040JobInfoArrayMaxTasks]):
        array_task_string (Union[Unset, str]):
        association_id (Union[Unset, int]):
        batch_features (Union[Unset, str]):
        batch_flag (Union[Unset, bool]):
        batch_host (Union[Unset, str]):
        flags (Union[Unset, list[V0040JobInfoFlagsItem]]):
        burst_buffer (Union[Unset, str]):
        burst_buffer_state (Union[Unset, str]):
        cluster (Union[Unset, str]):
        cluster_features (Union[Unset, str]):
        command (Union[Unset, str]):
        comment (Union[Unset, str]):
        container (Union[Unset, str]):
        container_id (Union[Unset, str]):
        contiguous (Union[Unset, bool]):
        core_spec (Union[Unset, int]):
        thread_spec (Union[Unset, int]):
        cores_per_socket (Union[Unset, V0040JobInfoCoresPerSocket]):
        billable_tres (Union[Unset, V0040JobInfoBillableTres]):
        cpus_per_task (Union[Unset, V0040JobInfoCpusPerTask]):
        cpu_frequency_minimum (Union[Unset, V0040JobInfoCpuFrequencyMinimum]):
        cpu_frequency_maximum (Union[Unset, V0040JobInfoCpuFrequencyMaximum]):
        cpu_frequency_governor (Union[Unset, V0040JobInfoCpuFrequencyGovernor]):
        cpus_per_tres (Union[Unset, str]):
        cron (Union[Unset, str]):
        deadline (Union[Unset, V0040JobInfoDeadline]):
        delay_boot (Union[Unset, V0040JobInfoDelayBoot]):
        dependency (Union[Unset, str]):
        derived_exit_code (Union[Unset, V0040JobInfoDerivedExitCode]):
        eligible_time (Union[Unset, V0040JobInfoEligibleTime]):
        end_time (Union[Unset, V0040JobInfoEndTime]):
        excluded_nodes (Union[Unset, str]):
        exit_code (Union[Unset, V0040JobInfoExitCode]):
        extra (Union[Unset, str]):
        failed_node (Union[Unset, str]):
        features (Union[Unset, str]):
        federation_origin (Union[Unset, str]):
        federation_siblings_active (Union[Unset, str]):
        federation_siblings_viable (Union[Unset, str]):
        gres_detail (Union[Unset, V0040JobInfoGresDetail]):
        group_id (Union[Unset, int]):
        group_name (Union[Unset, str]):
        het_job_id (Union[Unset, V0040JobInfoHetJobId]):
        het_job_id_set (Union[Unset, str]):
        het_job_offset (Union[Unset, V0040JobInfoHetJobOffset]):
        job_id (Union[Unset, int]):
        job_resources (Union[Unset, V0040JobInfoJobResources]):
        job_size_str (Union[Unset, V0040JobInfoJobSizeStr]):
        job_state (Union[Unset, list[V0040JobInfoJobStateItem]]):
        last_sched_evaluation (Union[Unset, V0040JobInfoLastSchedEvaluation]):
        licenses (Union[Unset, str]):
        mail_type (Union[Unset, list[V0040JobInfoMailTypeItem]]):
        mail_user (Union[Unset, str]):
        max_cpus (Union[Unset, V0040JobInfoMaxCpus]):
        max_nodes (Union[Unset, V0040JobInfoMaxNodes]):
        mcs_label (Union[Unset, str]):
        memory_per_tres (Union[Unset, str]):
        name (Union[Unset, str]):
        network (Union[Unset, str]):
        nodes (Union[Unset, str]):
        nice (Union[Unset, int]):
        tasks_per_core (Union[Unset, V0040JobInfoTasksPerCore]):
        tasks_per_tres (Union[Unset, V0040JobInfoTasksPerTres]):
        tasks_per_node (Union[Unset, V0040JobInfoTasksPerNode]):
        tasks_per_socket (Union[Unset, V0040JobInfoTasksPerSocket]):
        tasks_per_board (Union[Unset, V0040JobInfoTasksPerBoard]):
        cpus (Union[Unset, V0040JobInfoCpus]):
        node_count (Union[Unset, V0040JobInfoNodeCount]):
        tasks (Union[Unset, V0040JobInfoTasks]):
        partition (Union[Unset, str]):
        prefer (Union[Unset, str]):
        memory_per_cpu (Union[Unset, V0040JobInfoMemoryPerCpu]):
        memory_per_node (Union[Unset, V0040JobInfoMemoryPerNode]):
        minimum_cpus_per_node (Union[Unset, V0040JobInfoMinimumCpusPerNode]):
        minimum_tmp_disk_per_node (Union[Unset, V0040JobInfoMinimumTmpDiskPerNode]):
        power (Union[Unset, V0040JobInfoPower]):
        preempt_time (Union[Unset, V0040JobInfoPreemptTime]):
        preemptable_time (Union[Unset, V0040JobInfoPreemptableTime]):
        pre_sus_time (Union[Unset, V0040JobInfoPreSusTime]):
        hold (Union[Unset, bool]): Job held
        priority (Union[Unset, V0040JobInfoPriority]):
        profile (Union[Unset, list[V0040JobInfoProfileItem]]):
        qos (Union[Unset, str]):
        reboot (Union[Unset, bool]):
        required_nodes (Union[Unset, str]):
        minimum_switches (Union[Unset, int]):
        requeue (Union[Unset, bool]):
        resize_time (Union[Unset, V0040JobInfoResizeTime]):
        restart_cnt (Union[Unset, int]):
        resv_name (Union[Unset, str]):
        scheduled_nodes (Union[Unset, str]):
        selinux_context (Union[Unset, str]):
        shared (Union[Unset, list[V0040JobInfoSharedItem]]):
        exclusive (Union[Unset, list[V0040JobInfoExclusiveItem]]):
        oversubscribe (Union[Unset, bool]):
        show_flags (Union[Unset, list[V0040JobInfoShowFlagsItem]]):
        sockets_per_board (Union[Unset, int]):
        sockets_per_node (Union[Unset, V0040JobInfoSocketsPerNode]):
        start_time (Union[Unset, V0040JobInfoStartTime]):
        state_description (Union[Unset, str]):
        state_reason (Union[Unset, str]):
        standard_error (Union[Unset, str]):
        standard_input (Union[Unset, str]):
        standard_output (Union[Unset, str]):
        submit_time (Union[Unset, V0040JobInfoSubmitTime]):
        suspend_time (Union[Unset, V0040JobInfoSuspendTime]):
        system_comment (Union[Unset, str]):
        time_limit (Union[Unset, V0040JobInfoTimeLimit]):
        time_minimum (Union[Unset, V0040JobInfoTimeMinimum]):
        threads_per_core (Union[Unset, V0040JobInfoThreadsPerCore]):
        tres_bind (Union[Unset, str]):
        tres_freq (Union[Unset, str]):
        tres_per_job (Union[Unset, str]):
        tres_per_node (Union[Unset, str]):
        tres_per_socket (Union[Unset, str]):
        tres_per_task (Union[Unset, str]):
        tres_req_str (Union[Unset, str]):
        tres_alloc_str (Union[Unset, str]):
        user_id (Union[Unset, int]):
        user_name (Union[Unset, str]):
        maximum_switch_wait_time (Union[Unset, int]):
        wckey (Union[Unset, str]):
        current_working_directory (Union[Unset, str]):
    """

    account: Union[Unset, str] = UNSET
    accrue_time: Union[Unset, "V0040JobInfoAccrueTime"] = UNSET
    admin_comment: Union[Unset, str] = UNSET
    allocating_node: Union[Unset, str] = UNSET
    array_job_id: Union[Unset, "V0040JobInfoArrayJobId"] = UNSET
    array_task_id: Union[Unset, "V0040JobInfoArrayTaskId"] = UNSET
    array_max_tasks: Union[Unset, "V0040JobInfoArrayMaxTasks"] = UNSET
    array_task_string: Union[Unset, str] = UNSET
    association_id: Union[Unset, int] = UNSET
    batch_features: Union[Unset, str] = UNSET
    batch_flag: Union[Unset, bool] = UNSET
    batch_host: Union[Unset, str] = UNSET
    flags: Union[Unset, list[V0040JobInfoFlagsItem]] = UNSET
    burst_buffer: Union[Unset, str] = UNSET
    burst_buffer_state: Union[Unset, str] = UNSET
    cluster: Union[Unset, str] = UNSET
    cluster_features: Union[Unset, str] = UNSET
    command: Union[Unset, str] = UNSET
    comment: Union[Unset, str] = UNSET
    container: Union[Unset, str] = UNSET
    container_id: Union[Unset, str] = UNSET
    contiguous: Union[Unset, bool] = UNSET
    core_spec: Union[Unset, int] = UNSET
    thread_spec: Union[Unset, int] = UNSET
    cores_per_socket: Union[Unset, "V0040JobInfoCoresPerSocket"] = UNSET
    billable_tres: Union[Unset, "V0040JobInfoBillableTres"] = UNSET
    cpus_per_task: Union[Unset, "V0040JobInfoCpusPerTask"] = UNSET
    cpu_frequency_minimum: Union[Unset, "V0040JobInfoCpuFrequencyMinimum"] = UNSET
    cpu_frequency_maximum: Union[Unset, "V0040JobInfoCpuFrequencyMaximum"] = UNSET
    cpu_frequency_governor: Union[Unset, "V0040JobInfoCpuFrequencyGovernor"] = UNSET
    cpus_per_tres: Union[Unset, str] = UNSET
    cron: Union[Unset, str] = UNSET
    deadline: Union[Unset, "V0040JobInfoDeadline"] = UNSET
    delay_boot: Union[Unset, "V0040JobInfoDelayBoot"] = UNSET
    dependency: Union[Unset, str] = UNSET
    derived_exit_code: Union[Unset, "V0040JobInfoDerivedExitCode"] = UNSET
    eligible_time: Union[Unset, "V0040JobInfoEligibleTime"] = UNSET
    end_time: Union[Unset, "V0040JobInfoEndTime"] = UNSET
    excluded_nodes: Union[Unset, str] = UNSET
    exit_code: Union[Unset, "V0040JobInfoExitCode"] = UNSET
    extra: Union[Unset, str] = UNSET
    failed_node: Union[Unset, str] = UNSET
    features: Union[Unset, str] = UNSET
    federation_origin: Union[Unset, str] = UNSET
    federation_siblings_active: Union[Unset, str] = UNSET
    federation_siblings_viable: Union[Unset, str] = UNSET
    gres_detail: Union[Unset, "V0040JobInfoGresDetail"] = UNSET
    group_id: Union[Unset, int] = UNSET
    group_name: Union[Unset, str] = UNSET
    het_job_id: Union[Unset, "V0040JobInfoHetJobId"] = UNSET
    het_job_id_set: Union[Unset, str] = UNSET
    het_job_offset: Union[Unset, "V0040JobInfoHetJobOffset"] = UNSET
    job_id: Union[Unset, int] = UNSET
    job_resources: Union[Unset, "V0040JobInfoJobResources"] = UNSET
    job_size_str: Union[Unset, "V0040JobInfoJobSizeStr"] = UNSET
    job_state: Union[Unset, list[V0040JobInfoJobStateItem]] = UNSET
    last_sched_evaluation: Union[Unset, "V0040JobInfoLastSchedEvaluation"] = UNSET
    licenses: Union[Unset, str] = UNSET
    mail_type: Union[Unset, list[V0040JobInfoMailTypeItem]] = UNSET
    mail_user: Union[Unset, str] = UNSET
    max_cpus: Union[Unset, "V0040JobInfoMaxCpus"] = UNSET
    max_nodes: Union[Unset, "V0040JobInfoMaxNodes"] = UNSET
    mcs_label: Union[Unset, str] = UNSET
    memory_per_tres: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    network: Union[Unset, str] = UNSET
    nodes: Union[Unset, str] = UNSET
    nice: Union[Unset, int] = UNSET
    tasks_per_core: Union[Unset, "V0040JobInfoTasksPerCore"] = UNSET
    tasks_per_tres: Union[Unset, "V0040JobInfoTasksPerTres"] = UNSET
    tasks_per_node: Union[Unset, "V0040JobInfoTasksPerNode"] = UNSET
    tasks_per_socket: Union[Unset, "V0040JobInfoTasksPerSocket"] = UNSET
    tasks_per_board: Union[Unset, "V0040JobInfoTasksPerBoard"] = UNSET
    cpus: Union[Unset, "V0040JobInfoCpus"] = UNSET
    node_count: Union[Unset, "V0040JobInfoNodeCount"] = UNSET
    tasks: Union[Unset, "V0040JobInfoTasks"] = UNSET
    partition: Union[Unset, str] = UNSET
    prefer: Union[Unset, str] = UNSET
    memory_per_cpu: Union[Unset, "V0040JobInfoMemoryPerCpu"] = UNSET
    memory_per_node: Union[Unset, "V0040JobInfoMemoryPerNode"] = UNSET
    minimum_cpus_per_node: Union[Unset, "V0040JobInfoMinimumCpusPerNode"] = UNSET
    minimum_tmp_disk_per_node: Union[Unset, "V0040JobInfoMinimumTmpDiskPerNode"] = UNSET
    power: Union[Unset, "V0040JobInfoPower"] = UNSET
    preempt_time: Union[Unset, "V0040JobInfoPreemptTime"] = UNSET
    preemptable_time: Union[Unset, "V0040JobInfoPreemptableTime"] = UNSET
    pre_sus_time: Union[Unset, "V0040JobInfoPreSusTime"] = UNSET
    hold: Union[Unset, bool] = UNSET
    priority: Union[Unset, "V0040JobInfoPriority"] = UNSET
    profile: Union[Unset, list[V0040JobInfoProfileItem]] = UNSET
    qos: Union[Unset, str] = UNSET
    reboot: Union[Unset, bool] = UNSET
    required_nodes: Union[Unset, str] = UNSET
    minimum_switches: Union[Unset, int] = UNSET
    requeue: Union[Unset, bool] = UNSET
    resize_time: Union[Unset, "V0040JobInfoResizeTime"] = UNSET
    restart_cnt: Union[Unset, int] = UNSET
    resv_name: Union[Unset, str] = UNSET
    scheduled_nodes: Union[Unset, str] = UNSET
    selinux_context: Union[Unset, str] = UNSET
    shared: Union[Unset, list[V0040JobInfoSharedItem]] = UNSET
    exclusive: Union[Unset, list[V0040JobInfoExclusiveItem]] = UNSET
    oversubscribe: Union[Unset, bool] = UNSET
    show_flags: Union[Unset, list[V0040JobInfoShowFlagsItem]] = UNSET
    sockets_per_board: Union[Unset, int] = UNSET
    sockets_per_node: Union[Unset, "V0040JobInfoSocketsPerNode"] = UNSET
    start_time: Union[Unset, "V0040JobInfoStartTime"] = UNSET
    state_description: Union[Unset, str] = UNSET
    state_reason: Union[Unset, str] = UNSET
    standard_error: Union[Unset, str] = UNSET
    standard_input: Union[Unset, str] = UNSET
    standard_output: Union[Unset, str] = UNSET
    submit_time: Union[Unset, "V0040JobInfoSubmitTime"] = UNSET
    suspend_time: Union[Unset, "V0040JobInfoSuspendTime"] = UNSET
    system_comment: Union[Unset, str] = UNSET
    time_limit: Union[Unset, "V0040JobInfoTimeLimit"] = UNSET
    time_minimum: Union[Unset, "V0040JobInfoTimeMinimum"] = UNSET
    threads_per_core: Union[Unset, "V0040JobInfoThreadsPerCore"] = UNSET
    tres_bind: Union[Unset, str] = UNSET
    tres_freq: Union[Unset, str] = UNSET
    tres_per_job: Union[Unset, str] = UNSET
    tres_per_node: Union[Unset, str] = UNSET
    tres_per_socket: Union[Unset, str] = UNSET
    tres_per_task: Union[Unset, str] = UNSET
    tres_req_str: Union[Unset, str] = UNSET
    tres_alloc_str: Union[Unset, str] = UNSET
    user_id: Union[Unset, int] = UNSET
    user_name: Union[Unset, str] = UNSET
    maximum_switch_wait_time: Union[Unset, int] = UNSET
    wckey: Union[Unset, str] = UNSET
    current_working_directory: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        account = self.account

        accrue_time: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.accrue_time, Unset):
            accrue_time = self.accrue_time.to_dict()

        admin_comment = self.admin_comment

        allocating_node = self.allocating_node

        array_job_id: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.array_job_id, Unset):
            array_job_id = self.array_job_id.to_dict()

        array_task_id: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.array_task_id, Unset):
            array_task_id = self.array_task_id.to_dict()

        array_max_tasks: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.array_max_tasks, Unset):
            array_max_tasks = self.array_max_tasks.to_dict()

        array_task_string = self.array_task_string

        association_id = self.association_id

        batch_features = self.batch_features

        batch_flag = self.batch_flag

        batch_host = self.batch_host

        flags: Union[Unset, list[str]] = UNSET
        if not isinstance(self.flags, Unset):
            flags = []
            for flags_item_data in self.flags:
                flags_item = flags_item_data.value
                flags.append(flags_item)

        burst_buffer = self.burst_buffer

        burst_buffer_state = self.burst_buffer_state

        cluster = self.cluster

        cluster_features = self.cluster_features

        command = self.command

        comment = self.comment

        container = self.container

        container_id = self.container_id

        contiguous = self.contiguous

        core_spec = self.core_spec

        thread_spec = self.thread_spec

        cores_per_socket: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.cores_per_socket, Unset):
            cores_per_socket = self.cores_per_socket.to_dict()

        billable_tres: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.billable_tres, Unset):
            billable_tres = self.billable_tres.to_dict()

        cpus_per_task: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.cpus_per_task, Unset):
            cpus_per_task = self.cpus_per_task.to_dict()

        cpu_frequency_minimum: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.cpu_frequency_minimum, Unset):
            cpu_frequency_minimum = self.cpu_frequency_minimum.to_dict()

        cpu_frequency_maximum: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.cpu_frequency_maximum, Unset):
            cpu_frequency_maximum = self.cpu_frequency_maximum.to_dict()

        cpu_frequency_governor: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.cpu_frequency_governor, Unset):
            cpu_frequency_governor = self.cpu_frequency_governor.to_dict()

        cpus_per_tres = self.cpus_per_tres

        cron = self.cron

        deadline: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.deadline, Unset):
            deadline = self.deadline.to_dict()

        delay_boot: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.delay_boot, Unset):
            delay_boot = self.delay_boot.to_dict()

        dependency = self.dependency

        derived_exit_code: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.derived_exit_code, Unset):
            derived_exit_code = self.derived_exit_code.to_dict()

        eligible_time: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.eligible_time, Unset):
            eligible_time = self.eligible_time.to_dict()

        end_time: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.end_time, Unset):
            end_time = self.end_time.to_dict()

        excluded_nodes = self.excluded_nodes

        exit_code: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.exit_code, Unset):
            exit_code = self.exit_code.to_dict()

        extra = self.extra

        failed_node = self.failed_node

        features = self.features

        federation_origin = self.federation_origin

        federation_siblings_active = self.federation_siblings_active

        federation_siblings_viable = self.federation_siblings_viable

        gres_detail: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.gres_detail, Unset):
            gres_detail = self.gres_detail.to_dict()

        group_id = self.group_id

        group_name = self.group_name

        het_job_id: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.het_job_id, Unset):
            het_job_id = self.het_job_id.to_dict()

        het_job_id_set = self.het_job_id_set

        het_job_offset: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.het_job_offset, Unset):
            het_job_offset = self.het_job_offset.to_dict()

        job_id = self.job_id

        job_resources: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.job_resources, Unset):
            job_resources = self.job_resources.to_dict()

        job_size_str: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.job_size_str, Unset):
            job_size_str = self.job_size_str.to_dict()

        job_state: Union[Unset, list[str]] = UNSET
        if not isinstance(self.job_state, Unset):
            job_state = []
            for job_state_item_data in self.job_state:
                job_state_item = job_state_item_data.value
                job_state.append(job_state_item)

        last_sched_evaluation: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.last_sched_evaluation, Unset):
            last_sched_evaluation = self.last_sched_evaluation.to_dict()

        licenses = self.licenses

        mail_type: Union[Unset, list[str]] = UNSET
        if not isinstance(self.mail_type, Unset):
            mail_type = []
            for mail_type_item_data in self.mail_type:
                mail_type_item = mail_type_item_data.value
                mail_type.append(mail_type_item)

        mail_user = self.mail_user

        max_cpus: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.max_cpus, Unset):
            max_cpus = self.max_cpus.to_dict()

        max_nodes: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.max_nodes, Unset):
            max_nodes = self.max_nodes.to_dict()

        mcs_label = self.mcs_label

        memory_per_tres = self.memory_per_tres

        name = self.name

        network = self.network

        nodes = self.nodes

        nice = self.nice

        tasks_per_core: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.tasks_per_core, Unset):
            tasks_per_core = self.tasks_per_core.to_dict()

        tasks_per_tres: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.tasks_per_tres, Unset):
            tasks_per_tres = self.tasks_per_tres.to_dict()

        tasks_per_node: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.tasks_per_node, Unset):
            tasks_per_node = self.tasks_per_node.to_dict()

        tasks_per_socket: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.tasks_per_socket, Unset):
            tasks_per_socket = self.tasks_per_socket.to_dict()

        tasks_per_board: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.tasks_per_board, Unset):
            tasks_per_board = self.tasks_per_board.to_dict()

        cpus: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.cpus, Unset):
            cpus = self.cpus.to_dict()

        node_count: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.node_count, Unset):
            node_count = self.node_count.to_dict()

        tasks: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.tasks, Unset):
            tasks = self.tasks.to_dict()

        partition = self.partition

        prefer = self.prefer

        memory_per_cpu: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.memory_per_cpu, Unset):
            memory_per_cpu = self.memory_per_cpu.to_dict()

        memory_per_node: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.memory_per_node, Unset):
            memory_per_node = self.memory_per_node.to_dict()

        minimum_cpus_per_node: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.minimum_cpus_per_node, Unset):
            minimum_cpus_per_node = self.minimum_cpus_per_node.to_dict()

        minimum_tmp_disk_per_node: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.minimum_tmp_disk_per_node, Unset):
            minimum_tmp_disk_per_node = self.minimum_tmp_disk_per_node.to_dict()

        power: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.power, Unset):
            power = self.power.to_dict()

        preempt_time: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.preempt_time, Unset):
            preempt_time = self.preempt_time.to_dict()

        preemptable_time: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.preemptable_time, Unset):
            preemptable_time = self.preemptable_time.to_dict()

        pre_sus_time: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.pre_sus_time, Unset):
            pre_sus_time = self.pre_sus_time.to_dict()

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

        required_nodes = self.required_nodes

        minimum_switches = self.minimum_switches

        requeue = self.requeue

        resize_time: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.resize_time, Unset):
            resize_time = self.resize_time.to_dict()

        restart_cnt = self.restart_cnt

        resv_name = self.resv_name

        scheduled_nodes = self.scheduled_nodes

        selinux_context = self.selinux_context

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

        show_flags: Union[Unset, list[str]] = UNSET
        if not isinstance(self.show_flags, Unset):
            show_flags = []
            for show_flags_item_data in self.show_flags:
                show_flags_item = show_flags_item_data.value
                show_flags.append(show_flags_item)

        sockets_per_board = self.sockets_per_board

        sockets_per_node: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.sockets_per_node, Unset):
            sockets_per_node = self.sockets_per_node.to_dict()

        start_time: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.start_time, Unset):
            start_time = self.start_time.to_dict()

        state_description = self.state_description

        state_reason = self.state_reason

        standard_error = self.standard_error

        standard_input = self.standard_input

        standard_output = self.standard_output

        submit_time: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.submit_time, Unset):
            submit_time = self.submit_time.to_dict()

        suspend_time: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.suspend_time, Unset):
            suspend_time = self.suspend_time.to_dict()

        system_comment = self.system_comment

        time_limit: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.time_limit, Unset):
            time_limit = self.time_limit.to_dict()

        time_minimum: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.time_minimum, Unset):
            time_minimum = self.time_minimum.to_dict()

        threads_per_core: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.threads_per_core, Unset):
            threads_per_core = self.threads_per_core.to_dict()

        tres_bind = self.tres_bind

        tres_freq = self.tres_freq

        tres_per_job = self.tres_per_job

        tres_per_node = self.tres_per_node

        tres_per_socket = self.tres_per_socket

        tres_per_task = self.tres_per_task

        tres_req_str = self.tres_req_str

        tres_alloc_str = self.tres_alloc_str

        user_id = self.user_id

        user_name = self.user_name

        maximum_switch_wait_time = self.maximum_switch_wait_time

        wckey = self.wckey

        current_working_directory = self.current_working_directory

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if account is not UNSET:
            field_dict["account"] = account
        if accrue_time is not UNSET:
            field_dict["accrue_time"] = accrue_time
        if admin_comment is not UNSET:
            field_dict["admin_comment"] = admin_comment
        if allocating_node is not UNSET:
            field_dict["allocating_node"] = allocating_node
        if array_job_id is not UNSET:
            field_dict["array_job_id"] = array_job_id
        if array_task_id is not UNSET:
            field_dict["array_task_id"] = array_task_id
        if array_max_tasks is not UNSET:
            field_dict["array_max_tasks"] = array_max_tasks
        if array_task_string is not UNSET:
            field_dict["array_task_string"] = array_task_string
        if association_id is not UNSET:
            field_dict["association_id"] = association_id
        if batch_features is not UNSET:
            field_dict["batch_features"] = batch_features
        if batch_flag is not UNSET:
            field_dict["batch_flag"] = batch_flag
        if batch_host is not UNSET:
            field_dict["batch_host"] = batch_host
        if flags is not UNSET:
            field_dict["flags"] = flags
        if burst_buffer is not UNSET:
            field_dict["burst_buffer"] = burst_buffer
        if burst_buffer_state is not UNSET:
            field_dict["burst_buffer_state"] = burst_buffer_state
        if cluster is not UNSET:
            field_dict["cluster"] = cluster
        if cluster_features is not UNSET:
            field_dict["cluster_features"] = cluster_features
        if command is not UNSET:
            field_dict["command"] = command
        if comment is not UNSET:
            field_dict["comment"] = comment
        if container is not UNSET:
            field_dict["container"] = container
        if container_id is not UNSET:
            field_dict["container_id"] = container_id
        if contiguous is not UNSET:
            field_dict["contiguous"] = contiguous
        if core_spec is not UNSET:
            field_dict["core_spec"] = core_spec
        if thread_spec is not UNSET:
            field_dict["thread_spec"] = thread_spec
        if cores_per_socket is not UNSET:
            field_dict["cores_per_socket"] = cores_per_socket
        if billable_tres is not UNSET:
            field_dict["billable_tres"] = billable_tres
        if cpus_per_task is not UNSET:
            field_dict["cpus_per_task"] = cpus_per_task
        if cpu_frequency_minimum is not UNSET:
            field_dict["cpu_frequency_minimum"] = cpu_frequency_minimum
        if cpu_frequency_maximum is not UNSET:
            field_dict["cpu_frequency_maximum"] = cpu_frequency_maximum
        if cpu_frequency_governor is not UNSET:
            field_dict["cpu_frequency_governor"] = cpu_frequency_governor
        if cpus_per_tres is not UNSET:
            field_dict["cpus_per_tres"] = cpus_per_tres
        if cron is not UNSET:
            field_dict["cron"] = cron
        if deadline is not UNSET:
            field_dict["deadline"] = deadline
        if delay_boot is not UNSET:
            field_dict["delay_boot"] = delay_boot
        if dependency is not UNSET:
            field_dict["dependency"] = dependency
        if derived_exit_code is not UNSET:
            field_dict["derived_exit_code"] = derived_exit_code
        if eligible_time is not UNSET:
            field_dict["eligible_time"] = eligible_time
        if end_time is not UNSET:
            field_dict["end_time"] = end_time
        if excluded_nodes is not UNSET:
            field_dict["excluded_nodes"] = excluded_nodes
        if exit_code is not UNSET:
            field_dict["exit_code"] = exit_code
        if extra is not UNSET:
            field_dict["extra"] = extra
        if failed_node is not UNSET:
            field_dict["failed_node"] = failed_node
        if features is not UNSET:
            field_dict["features"] = features
        if federation_origin is not UNSET:
            field_dict["federation_origin"] = federation_origin
        if federation_siblings_active is not UNSET:
            field_dict["federation_siblings_active"] = federation_siblings_active
        if federation_siblings_viable is not UNSET:
            field_dict["federation_siblings_viable"] = federation_siblings_viable
        if gres_detail is not UNSET:
            field_dict["gres_detail"] = gres_detail
        if group_id is not UNSET:
            field_dict["group_id"] = group_id
        if group_name is not UNSET:
            field_dict["group_name"] = group_name
        if het_job_id is not UNSET:
            field_dict["het_job_id"] = het_job_id
        if het_job_id_set is not UNSET:
            field_dict["het_job_id_set"] = het_job_id_set
        if het_job_offset is not UNSET:
            field_dict["het_job_offset"] = het_job_offset
        if job_id is not UNSET:
            field_dict["job_id"] = job_id
        if job_resources is not UNSET:
            field_dict["job_resources"] = job_resources
        if job_size_str is not UNSET:
            field_dict["job_size_str"] = job_size_str
        if job_state is not UNSET:
            field_dict["job_state"] = job_state
        if last_sched_evaluation is not UNSET:
            field_dict["last_sched_evaluation"] = last_sched_evaluation
        if licenses is not UNSET:
            field_dict["licenses"] = licenses
        if mail_type is not UNSET:
            field_dict["mail_type"] = mail_type
        if mail_user is not UNSET:
            field_dict["mail_user"] = mail_user
        if max_cpus is not UNSET:
            field_dict["max_cpus"] = max_cpus
        if max_nodes is not UNSET:
            field_dict["max_nodes"] = max_nodes
        if mcs_label is not UNSET:
            field_dict["mcs_label"] = mcs_label
        if memory_per_tres is not UNSET:
            field_dict["memory_per_tres"] = memory_per_tres
        if name is not UNSET:
            field_dict["name"] = name
        if network is not UNSET:
            field_dict["network"] = network
        if nodes is not UNSET:
            field_dict["nodes"] = nodes
        if nice is not UNSET:
            field_dict["nice"] = nice
        if tasks_per_core is not UNSET:
            field_dict["tasks_per_core"] = tasks_per_core
        if tasks_per_tres is not UNSET:
            field_dict["tasks_per_tres"] = tasks_per_tres
        if tasks_per_node is not UNSET:
            field_dict["tasks_per_node"] = tasks_per_node
        if tasks_per_socket is not UNSET:
            field_dict["tasks_per_socket"] = tasks_per_socket
        if tasks_per_board is not UNSET:
            field_dict["tasks_per_board"] = tasks_per_board
        if cpus is not UNSET:
            field_dict["cpus"] = cpus
        if node_count is not UNSET:
            field_dict["node_count"] = node_count
        if tasks is not UNSET:
            field_dict["tasks"] = tasks
        if partition is not UNSET:
            field_dict["partition"] = partition
        if prefer is not UNSET:
            field_dict["prefer"] = prefer
        if memory_per_cpu is not UNSET:
            field_dict["memory_per_cpu"] = memory_per_cpu
        if memory_per_node is not UNSET:
            field_dict["memory_per_node"] = memory_per_node
        if minimum_cpus_per_node is not UNSET:
            field_dict["minimum_cpus_per_node"] = minimum_cpus_per_node
        if minimum_tmp_disk_per_node is not UNSET:
            field_dict["minimum_tmp_disk_per_node"] = minimum_tmp_disk_per_node
        if power is not UNSET:
            field_dict["power"] = power
        if preempt_time is not UNSET:
            field_dict["preempt_time"] = preempt_time
        if preemptable_time is not UNSET:
            field_dict["preemptable_time"] = preemptable_time
        if pre_sus_time is not UNSET:
            field_dict["pre_sus_time"] = pre_sus_time
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
        if minimum_switches is not UNSET:
            field_dict["minimum_switches"] = minimum_switches
        if requeue is not UNSET:
            field_dict["requeue"] = requeue
        if resize_time is not UNSET:
            field_dict["resize_time"] = resize_time
        if restart_cnt is not UNSET:
            field_dict["restart_cnt"] = restart_cnt
        if resv_name is not UNSET:
            field_dict["resv_name"] = resv_name
        if scheduled_nodes is not UNSET:
            field_dict["scheduled_nodes"] = scheduled_nodes
        if selinux_context is not UNSET:
            field_dict["selinux_context"] = selinux_context
        if shared is not UNSET:
            field_dict["shared"] = shared
        if exclusive is not UNSET:
            field_dict["exclusive"] = exclusive
        if oversubscribe is not UNSET:
            field_dict["oversubscribe"] = oversubscribe
        if show_flags is not UNSET:
            field_dict["show_flags"] = show_flags
        if sockets_per_board is not UNSET:
            field_dict["sockets_per_board"] = sockets_per_board
        if sockets_per_node is not UNSET:
            field_dict["sockets_per_node"] = sockets_per_node
        if start_time is not UNSET:
            field_dict["start_time"] = start_time
        if state_description is not UNSET:
            field_dict["state_description"] = state_description
        if state_reason is not UNSET:
            field_dict["state_reason"] = state_reason
        if standard_error is not UNSET:
            field_dict["standard_error"] = standard_error
        if standard_input is not UNSET:
            field_dict["standard_input"] = standard_input
        if standard_output is not UNSET:
            field_dict["standard_output"] = standard_output
        if submit_time is not UNSET:
            field_dict["submit_time"] = submit_time
        if suspend_time is not UNSET:
            field_dict["suspend_time"] = suspend_time
        if system_comment is not UNSET:
            field_dict["system_comment"] = system_comment
        if time_limit is not UNSET:
            field_dict["time_limit"] = time_limit
        if time_minimum is not UNSET:
            field_dict["time_minimum"] = time_minimum
        if threads_per_core is not UNSET:
            field_dict["threads_per_core"] = threads_per_core
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
        if tres_req_str is not UNSET:
            field_dict["tres_req_str"] = tres_req_str
        if tres_alloc_str is not UNSET:
            field_dict["tres_alloc_str"] = tres_alloc_str
        if user_id is not UNSET:
            field_dict["user_id"] = user_id
        if user_name is not UNSET:
            field_dict["user_name"] = user_name
        if maximum_switch_wait_time is not UNSET:
            field_dict["maximum_switch_wait_time"] = maximum_switch_wait_time
        if wckey is not UNSET:
            field_dict["wckey"] = wckey
        if current_working_directory is not UNSET:
            field_dict["current_working_directory"] = current_working_directory

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0040_job_info_accrue_time import V0040JobInfoAccrueTime
        from ..models.v0040_job_info_array_job_id import V0040JobInfoArrayJobId
        from ..models.v0040_job_info_array_max_tasks import V0040JobInfoArrayMaxTasks
        from ..models.v0040_job_info_array_task_id import V0040JobInfoArrayTaskId
        from ..models.v0040_job_info_billable_tres import V0040JobInfoBillableTres
        from ..models.v0040_job_info_cores_per_socket import V0040JobInfoCoresPerSocket
        from ..models.v0040_job_info_cpu_frequency_governor import V0040JobInfoCpuFrequencyGovernor
        from ..models.v0040_job_info_cpu_frequency_maximum import V0040JobInfoCpuFrequencyMaximum
        from ..models.v0040_job_info_cpu_frequency_minimum import V0040JobInfoCpuFrequencyMinimum
        from ..models.v0040_job_info_cpus import V0040JobInfoCpus
        from ..models.v0040_job_info_cpus_per_task import V0040JobInfoCpusPerTask
        from ..models.v0040_job_info_deadline import V0040JobInfoDeadline
        from ..models.v0040_job_info_delay_boot import V0040JobInfoDelayBoot
        from ..models.v0040_job_info_derived_exit_code import V0040JobInfoDerivedExitCode
        from ..models.v0040_job_info_eligible_time import V0040JobInfoEligibleTime
        from ..models.v0040_job_info_end_time import V0040JobInfoEndTime
        from ..models.v0040_job_info_exit_code import V0040JobInfoExitCode
        from ..models.v0040_job_info_gres_detail import V0040JobInfoGresDetail
        from ..models.v0040_job_info_het_job_id import V0040JobInfoHetJobId
        from ..models.v0040_job_info_het_job_offset import V0040JobInfoHetJobOffset
        from ..models.v0040_job_info_job_resources import V0040JobInfoJobResources
        from ..models.v0040_job_info_job_size_str import V0040JobInfoJobSizeStr
        from ..models.v0040_job_info_last_sched_evaluation import V0040JobInfoLastSchedEvaluation
        from ..models.v0040_job_info_max_cpus import V0040JobInfoMaxCpus
        from ..models.v0040_job_info_max_nodes import V0040JobInfoMaxNodes
        from ..models.v0040_job_info_memory_per_cpu import V0040JobInfoMemoryPerCpu
        from ..models.v0040_job_info_memory_per_node import V0040JobInfoMemoryPerNode
        from ..models.v0040_job_info_minimum_cpus_per_node import V0040JobInfoMinimumCpusPerNode
        from ..models.v0040_job_info_minimum_tmp_disk_per_node import V0040JobInfoMinimumTmpDiskPerNode
        from ..models.v0040_job_info_node_count import V0040JobInfoNodeCount
        from ..models.v0040_job_info_power import V0040JobInfoPower
        from ..models.v0040_job_info_pre_sus_time import V0040JobInfoPreSusTime
        from ..models.v0040_job_info_preempt_time import V0040JobInfoPreemptTime
        from ..models.v0040_job_info_preemptable_time import V0040JobInfoPreemptableTime
        from ..models.v0040_job_info_priority import V0040JobInfoPriority
        from ..models.v0040_job_info_resize_time import V0040JobInfoResizeTime
        from ..models.v0040_job_info_sockets_per_node import V0040JobInfoSocketsPerNode
        from ..models.v0040_job_info_start_time import V0040JobInfoStartTime
        from ..models.v0040_job_info_submit_time import V0040JobInfoSubmitTime
        from ..models.v0040_job_info_suspend_time import V0040JobInfoSuspendTime
        from ..models.v0040_job_info_tasks import V0040JobInfoTasks
        from ..models.v0040_job_info_tasks_per_board import V0040JobInfoTasksPerBoard
        from ..models.v0040_job_info_tasks_per_core import V0040JobInfoTasksPerCore
        from ..models.v0040_job_info_tasks_per_node import V0040JobInfoTasksPerNode
        from ..models.v0040_job_info_tasks_per_socket import V0040JobInfoTasksPerSocket
        from ..models.v0040_job_info_tasks_per_tres import V0040JobInfoTasksPerTres
        from ..models.v0040_job_info_threads_per_core import V0040JobInfoThreadsPerCore
        from ..models.v0040_job_info_time_limit import V0040JobInfoTimeLimit
        from ..models.v0040_job_info_time_minimum import V0040JobInfoTimeMinimum

        d = dict(src_dict)
        account = d.pop("account", UNSET)

        _accrue_time = d.pop("accrue_time", UNSET)
        accrue_time: Union[Unset, V0040JobInfoAccrueTime]
        if isinstance(_accrue_time, Unset):
            accrue_time = UNSET
        else:
            accrue_time = V0040JobInfoAccrueTime.from_dict(_accrue_time)

        admin_comment = d.pop("admin_comment", UNSET)

        allocating_node = d.pop("allocating_node", UNSET)

        _array_job_id = d.pop("array_job_id", UNSET)
        array_job_id: Union[Unset, V0040JobInfoArrayJobId]
        if isinstance(_array_job_id, Unset):
            array_job_id = UNSET
        else:
            array_job_id = V0040JobInfoArrayJobId.from_dict(_array_job_id)

        _array_task_id = d.pop("array_task_id", UNSET)
        array_task_id: Union[Unset, V0040JobInfoArrayTaskId]
        if isinstance(_array_task_id, Unset):
            array_task_id = UNSET
        else:
            array_task_id = V0040JobInfoArrayTaskId.from_dict(_array_task_id)

        _array_max_tasks = d.pop("array_max_tasks", UNSET)
        array_max_tasks: Union[Unset, V0040JobInfoArrayMaxTasks]
        if isinstance(_array_max_tasks, Unset):
            array_max_tasks = UNSET
        else:
            array_max_tasks = V0040JobInfoArrayMaxTasks.from_dict(_array_max_tasks)

        array_task_string = d.pop("array_task_string", UNSET)

        association_id = d.pop("association_id", UNSET)

        batch_features = d.pop("batch_features", UNSET)

        batch_flag = d.pop("batch_flag", UNSET)

        batch_host = d.pop("batch_host", UNSET)

        flags = []
        _flags = d.pop("flags", UNSET)
        for flags_item_data in _flags or []:
            flags_item = V0040JobInfoFlagsItem(flags_item_data)

            flags.append(flags_item)

        burst_buffer = d.pop("burst_buffer", UNSET)

        burst_buffer_state = d.pop("burst_buffer_state", UNSET)

        cluster = d.pop("cluster", UNSET)

        cluster_features = d.pop("cluster_features", UNSET)

        command = d.pop("command", UNSET)

        comment = d.pop("comment", UNSET)

        container = d.pop("container", UNSET)

        container_id = d.pop("container_id", UNSET)

        contiguous = d.pop("contiguous", UNSET)

        core_spec = d.pop("core_spec", UNSET)

        thread_spec = d.pop("thread_spec", UNSET)

        _cores_per_socket = d.pop("cores_per_socket", UNSET)
        cores_per_socket: Union[Unset, V0040JobInfoCoresPerSocket]
        if isinstance(_cores_per_socket, Unset):
            cores_per_socket = UNSET
        else:
            cores_per_socket = V0040JobInfoCoresPerSocket.from_dict(_cores_per_socket)

        _billable_tres = d.pop("billable_tres", UNSET)
        billable_tres: Union[Unset, V0040JobInfoBillableTres]
        if isinstance(_billable_tres, Unset):
            billable_tres = UNSET
        else:
            billable_tres = V0040JobInfoBillableTres.from_dict(_billable_tres)

        _cpus_per_task = d.pop("cpus_per_task", UNSET)
        cpus_per_task: Union[Unset, V0040JobInfoCpusPerTask]
        if isinstance(_cpus_per_task, Unset):
            cpus_per_task = UNSET
        else:
            cpus_per_task = V0040JobInfoCpusPerTask.from_dict(_cpus_per_task)

        _cpu_frequency_minimum = d.pop("cpu_frequency_minimum", UNSET)
        cpu_frequency_minimum: Union[Unset, V0040JobInfoCpuFrequencyMinimum]
        if isinstance(_cpu_frequency_minimum, Unset):
            cpu_frequency_minimum = UNSET
        else:
            cpu_frequency_minimum = V0040JobInfoCpuFrequencyMinimum.from_dict(_cpu_frequency_minimum)

        _cpu_frequency_maximum = d.pop("cpu_frequency_maximum", UNSET)
        cpu_frequency_maximum: Union[Unset, V0040JobInfoCpuFrequencyMaximum]
        if isinstance(_cpu_frequency_maximum, Unset):
            cpu_frequency_maximum = UNSET
        else:
            cpu_frequency_maximum = V0040JobInfoCpuFrequencyMaximum.from_dict(_cpu_frequency_maximum)

        _cpu_frequency_governor = d.pop("cpu_frequency_governor", UNSET)
        cpu_frequency_governor: Union[Unset, V0040JobInfoCpuFrequencyGovernor]
        if isinstance(_cpu_frequency_governor, Unset):
            cpu_frequency_governor = UNSET
        else:
            cpu_frequency_governor = V0040JobInfoCpuFrequencyGovernor.from_dict(_cpu_frequency_governor)

        cpus_per_tres = d.pop("cpus_per_tres", UNSET)

        cron = d.pop("cron", UNSET)

        _deadline = d.pop("deadline", UNSET)
        deadline: Union[Unset, V0040JobInfoDeadline]
        if isinstance(_deadline, Unset):
            deadline = UNSET
        else:
            deadline = V0040JobInfoDeadline.from_dict(_deadline)

        _delay_boot = d.pop("delay_boot", UNSET)
        delay_boot: Union[Unset, V0040JobInfoDelayBoot]
        if isinstance(_delay_boot, Unset):
            delay_boot = UNSET
        else:
            delay_boot = V0040JobInfoDelayBoot.from_dict(_delay_boot)

        dependency = d.pop("dependency", UNSET)

        _derived_exit_code = d.pop("derived_exit_code", UNSET)
        derived_exit_code: Union[Unset, V0040JobInfoDerivedExitCode]
        if isinstance(_derived_exit_code, Unset):
            derived_exit_code = UNSET
        else:
            derived_exit_code = V0040JobInfoDerivedExitCode.from_dict(_derived_exit_code)

        _eligible_time = d.pop("eligible_time", UNSET)
        eligible_time: Union[Unset, V0040JobInfoEligibleTime]
        if isinstance(_eligible_time, Unset):
            eligible_time = UNSET
        else:
            eligible_time = V0040JobInfoEligibleTime.from_dict(_eligible_time)

        _end_time = d.pop("end_time", UNSET)
        end_time: Union[Unset, V0040JobInfoEndTime]
        if isinstance(_end_time, Unset):
            end_time = UNSET
        else:
            end_time = V0040JobInfoEndTime.from_dict(_end_time)

        excluded_nodes = d.pop("excluded_nodes", UNSET)

        _exit_code = d.pop("exit_code", UNSET)
        exit_code: Union[Unset, V0040JobInfoExitCode]
        if isinstance(_exit_code, Unset):
            exit_code = UNSET
        else:
            exit_code = V0040JobInfoExitCode.from_dict(_exit_code)

        extra = d.pop("extra", UNSET)

        failed_node = d.pop("failed_node", UNSET)

        features = d.pop("features", UNSET)

        federation_origin = d.pop("federation_origin", UNSET)

        federation_siblings_active = d.pop("federation_siblings_active", UNSET)

        federation_siblings_viable = d.pop("federation_siblings_viable", UNSET)

        _gres_detail = d.pop("gres_detail", UNSET)
        gres_detail: Union[Unset, V0040JobInfoGresDetail]
        if isinstance(_gres_detail, Unset):
            gres_detail = UNSET
        else:
            gres_detail = V0040JobInfoGresDetail.from_dict(_gres_detail)

        group_id = d.pop("group_id", UNSET)

        group_name = d.pop("group_name", UNSET)

        _het_job_id = d.pop("het_job_id", UNSET)
        het_job_id: Union[Unset, V0040JobInfoHetJobId]
        if isinstance(_het_job_id, Unset):
            het_job_id = UNSET
        else:
            het_job_id = V0040JobInfoHetJobId.from_dict(_het_job_id)

        het_job_id_set = d.pop("het_job_id_set", UNSET)

        _het_job_offset = d.pop("het_job_offset", UNSET)
        het_job_offset: Union[Unset, V0040JobInfoHetJobOffset]
        if isinstance(_het_job_offset, Unset):
            het_job_offset = UNSET
        else:
            het_job_offset = V0040JobInfoHetJobOffset.from_dict(_het_job_offset)

        job_id = d.pop("job_id", UNSET)

        _job_resources = d.pop("job_resources", UNSET)
        job_resources: Union[Unset, V0040JobInfoJobResources]
        if isinstance(_job_resources, Unset):
            job_resources = UNSET
        else:
            job_resources = V0040JobInfoJobResources.from_dict(_job_resources)

        _job_size_str = d.pop("job_size_str", UNSET)
        job_size_str: Union[Unset, V0040JobInfoJobSizeStr]
        if isinstance(_job_size_str, Unset):
            job_size_str = UNSET
        else:
            job_size_str = V0040JobInfoJobSizeStr.from_dict(_job_size_str)

        job_state = []
        _job_state = d.pop("job_state", UNSET)
        for job_state_item_data in _job_state or []:
            job_state_item = V0040JobInfoJobStateItem(job_state_item_data)

            job_state.append(job_state_item)

        _last_sched_evaluation = d.pop("last_sched_evaluation", UNSET)
        last_sched_evaluation: Union[Unset, V0040JobInfoLastSchedEvaluation]
        if isinstance(_last_sched_evaluation, Unset):
            last_sched_evaluation = UNSET
        else:
            last_sched_evaluation = V0040JobInfoLastSchedEvaluation.from_dict(_last_sched_evaluation)

        licenses = d.pop("licenses", UNSET)

        mail_type = []
        _mail_type = d.pop("mail_type", UNSET)
        for mail_type_item_data in _mail_type or []:
            mail_type_item = V0040JobInfoMailTypeItem(mail_type_item_data)

            mail_type.append(mail_type_item)

        mail_user = d.pop("mail_user", UNSET)

        _max_cpus = d.pop("max_cpus", UNSET)
        max_cpus: Union[Unset, V0040JobInfoMaxCpus]
        if isinstance(_max_cpus, Unset):
            max_cpus = UNSET
        else:
            max_cpus = V0040JobInfoMaxCpus.from_dict(_max_cpus)

        _max_nodes = d.pop("max_nodes", UNSET)
        max_nodes: Union[Unset, V0040JobInfoMaxNodes]
        if isinstance(_max_nodes, Unset):
            max_nodes = UNSET
        else:
            max_nodes = V0040JobInfoMaxNodes.from_dict(_max_nodes)

        mcs_label = d.pop("mcs_label", UNSET)

        memory_per_tres = d.pop("memory_per_tres", UNSET)

        name = d.pop("name", UNSET)

        network = d.pop("network", UNSET)

        nodes = d.pop("nodes", UNSET)

        nice = d.pop("nice", UNSET)

        _tasks_per_core = d.pop("tasks_per_core", UNSET)
        tasks_per_core: Union[Unset, V0040JobInfoTasksPerCore]
        if isinstance(_tasks_per_core, Unset):
            tasks_per_core = UNSET
        else:
            tasks_per_core = V0040JobInfoTasksPerCore.from_dict(_tasks_per_core)

        _tasks_per_tres = d.pop("tasks_per_tres", UNSET)
        tasks_per_tres: Union[Unset, V0040JobInfoTasksPerTres]
        if isinstance(_tasks_per_tres, Unset):
            tasks_per_tres = UNSET
        else:
            tasks_per_tres = V0040JobInfoTasksPerTres.from_dict(_tasks_per_tres)

        _tasks_per_node = d.pop("tasks_per_node", UNSET)
        tasks_per_node: Union[Unset, V0040JobInfoTasksPerNode]
        if isinstance(_tasks_per_node, Unset):
            tasks_per_node = UNSET
        else:
            tasks_per_node = V0040JobInfoTasksPerNode.from_dict(_tasks_per_node)

        _tasks_per_socket = d.pop("tasks_per_socket", UNSET)
        tasks_per_socket: Union[Unset, V0040JobInfoTasksPerSocket]
        if isinstance(_tasks_per_socket, Unset):
            tasks_per_socket = UNSET
        else:
            tasks_per_socket = V0040JobInfoTasksPerSocket.from_dict(_tasks_per_socket)

        _tasks_per_board = d.pop("tasks_per_board", UNSET)
        tasks_per_board: Union[Unset, V0040JobInfoTasksPerBoard]
        if isinstance(_tasks_per_board, Unset):
            tasks_per_board = UNSET
        else:
            tasks_per_board = V0040JobInfoTasksPerBoard.from_dict(_tasks_per_board)

        _cpus = d.pop("cpus", UNSET)
        cpus: Union[Unset, V0040JobInfoCpus]
        if isinstance(_cpus, Unset):
            cpus = UNSET
        else:
            cpus = V0040JobInfoCpus.from_dict(_cpus)

        _node_count = d.pop("node_count", UNSET)
        node_count: Union[Unset, V0040JobInfoNodeCount]
        if isinstance(_node_count, Unset):
            node_count = UNSET
        else:
            node_count = V0040JobInfoNodeCount.from_dict(_node_count)

        _tasks = d.pop("tasks", UNSET)
        tasks: Union[Unset, V0040JobInfoTasks]
        if isinstance(_tasks, Unset):
            tasks = UNSET
        else:
            tasks = V0040JobInfoTasks.from_dict(_tasks)

        partition = d.pop("partition", UNSET)

        prefer = d.pop("prefer", UNSET)

        _memory_per_cpu = d.pop("memory_per_cpu", UNSET)
        memory_per_cpu: Union[Unset, V0040JobInfoMemoryPerCpu]
        if isinstance(_memory_per_cpu, Unset):
            memory_per_cpu = UNSET
        else:
            memory_per_cpu = V0040JobInfoMemoryPerCpu.from_dict(_memory_per_cpu)

        _memory_per_node = d.pop("memory_per_node", UNSET)
        memory_per_node: Union[Unset, V0040JobInfoMemoryPerNode]
        if isinstance(_memory_per_node, Unset):
            memory_per_node = UNSET
        else:
            memory_per_node = V0040JobInfoMemoryPerNode.from_dict(_memory_per_node)

        _minimum_cpus_per_node = d.pop("minimum_cpus_per_node", UNSET)
        minimum_cpus_per_node: Union[Unset, V0040JobInfoMinimumCpusPerNode]
        if isinstance(_minimum_cpus_per_node, Unset):
            minimum_cpus_per_node = UNSET
        else:
            minimum_cpus_per_node = V0040JobInfoMinimumCpusPerNode.from_dict(_minimum_cpus_per_node)

        _minimum_tmp_disk_per_node = d.pop("minimum_tmp_disk_per_node", UNSET)
        minimum_tmp_disk_per_node: Union[Unset, V0040JobInfoMinimumTmpDiskPerNode]
        if isinstance(_minimum_tmp_disk_per_node, Unset):
            minimum_tmp_disk_per_node = UNSET
        else:
            minimum_tmp_disk_per_node = V0040JobInfoMinimumTmpDiskPerNode.from_dict(_minimum_tmp_disk_per_node)

        _power = d.pop("power", UNSET)
        power: Union[Unset, V0040JobInfoPower]
        if isinstance(_power, Unset):
            power = UNSET
        else:
            power = V0040JobInfoPower.from_dict(_power)

        _preempt_time = d.pop("preempt_time", UNSET)
        preempt_time: Union[Unset, V0040JobInfoPreemptTime]
        if isinstance(_preempt_time, Unset):
            preempt_time = UNSET
        else:
            preempt_time = V0040JobInfoPreemptTime.from_dict(_preempt_time)

        _preemptable_time = d.pop("preemptable_time", UNSET)
        preemptable_time: Union[Unset, V0040JobInfoPreemptableTime]
        if isinstance(_preemptable_time, Unset):
            preemptable_time = UNSET
        else:
            preemptable_time = V0040JobInfoPreemptableTime.from_dict(_preemptable_time)

        _pre_sus_time = d.pop("pre_sus_time", UNSET)
        pre_sus_time: Union[Unset, V0040JobInfoPreSusTime]
        if isinstance(_pre_sus_time, Unset):
            pre_sus_time = UNSET
        else:
            pre_sus_time = V0040JobInfoPreSusTime.from_dict(_pre_sus_time)

        hold = d.pop("hold", UNSET)

        _priority = d.pop("priority", UNSET)
        priority: Union[Unset, V0040JobInfoPriority]
        if isinstance(_priority, Unset):
            priority = UNSET
        else:
            priority = V0040JobInfoPriority.from_dict(_priority)

        profile = []
        _profile = d.pop("profile", UNSET)
        for profile_item_data in _profile or []:
            profile_item = V0040JobInfoProfileItem(profile_item_data)

            profile.append(profile_item)

        qos = d.pop("qos", UNSET)

        reboot = d.pop("reboot", UNSET)

        required_nodes = d.pop("required_nodes", UNSET)

        minimum_switches = d.pop("minimum_switches", UNSET)

        requeue = d.pop("requeue", UNSET)

        _resize_time = d.pop("resize_time", UNSET)
        resize_time: Union[Unset, V0040JobInfoResizeTime]
        if isinstance(_resize_time, Unset):
            resize_time = UNSET
        else:
            resize_time = V0040JobInfoResizeTime.from_dict(_resize_time)

        restart_cnt = d.pop("restart_cnt", UNSET)

        resv_name = d.pop("resv_name", UNSET)

        scheduled_nodes = d.pop("scheduled_nodes", UNSET)

        selinux_context = d.pop("selinux_context", UNSET)

        shared = []
        _shared = d.pop("shared", UNSET)
        for shared_item_data in _shared or []:
            shared_item = V0040JobInfoSharedItem(shared_item_data)

            shared.append(shared_item)

        exclusive = []
        _exclusive = d.pop("exclusive", UNSET)
        for exclusive_item_data in _exclusive or []:
            exclusive_item = V0040JobInfoExclusiveItem(exclusive_item_data)

            exclusive.append(exclusive_item)

        oversubscribe = d.pop("oversubscribe", UNSET)

        show_flags = []
        _show_flags = d.pop("show_flags", UNSET)
        for show_flags_item_data in _show_flags or []:
            show_flags_item = V0040JobInfoShowFlagsItem(show_flags_item_data)

            show_flags.append(show_flags_item)

        sockets_per_board = d.pop("sockets_per_board", UNSET)

        _sockets_per_node = d.pop("sockets_per_node", UNSET)
        sockets_per_node: Union[Unset, V0040JobInfoSocketsPerNode]
        if isinstance(_sockets_per_node, Unset):
            sockets_per_node = UNSET
        else:
            sockets_per_node = V0040JobInfoSocketsPerNode.from_dict(_sockets_per_node)

        _start_time = d.pop("start_time", UNSET)
        start_time: Union[Unset, V0040JobInfoStartTime]
        if isinstance(_start_time, Unset):
            start_time = UNSET
        else:
            start_time = V0040JobInfoStartTime.from_dict(_start_time)

        state_description = d.pop("state_description", UNSET)

        state_reason = d.pop("state_reason", UNSET)

        standard_error = d.pop("standard_error", UNSET)

        standard_input = d.pop("standard_input", UNSET)

        standard_output = d.pop("standard_output", UNSET)

        _submit_time = d.pop("submit_time", UNSET)
        submit_time: Union[Unset, V0040JobInfoSubmitTime]
        if isinstance(_submit_time, Unset):
            submit_time = UNSET
        else:
            submit_time = V0040JobInfoSubmitTime.from_dict(_submit_time)

        _suspend_time = d.pop("suspend_time", UNSET)
        suspend_time: Union[Unset, V0040JobInfoSuspendTime]
        if isinstance(_suspend_time, Unset):
            suspend_time = UNSET
        else:
            suspend_time = V0040JobInfoSuspendTime.from_dict(_suspend_time)

        system_comment = d.pop("system_comment", UNSET)

        _time_limit = d.pop("time_limit", UNSET)
        time_limit: Union[Unset, V0040JobInfoTimeLimit]
        if isinstance(_time_limit, Unset):
            time_limit = UNSET
        else:
            time_limit = V0040JobInfoTimeLimit.from_dict(_time_limit)

        _time_minimum = d.pop("time_minimum", UNSET)
        time_minimum: Union[Unset, V0040JobInfoTimeMinimum]
        if isinstance(_time_minimum, Unset):
            time_minimum = UNSET
        else:
            time_minimum = V0040JobInfoTimeMinimum.from_dict(_time_minimum)

        _threads_per_core = d.pop("threads_per_core", UNSET)
        threads_per_core: Union[Unset, V0040JobInfoThreadsPerCore]
        if isinstance(_threads_per_core, Unset):
            threads_per_core = UNSET
        else:
            threads_per_core = V0040JobInfoThreadsPerCore.from_dict(_threads_per_core)

        tres_bind = d.pop("tres_bind", UNSET)

        tres_freq = d.pop("tres_freq", UNSET)

        tres_per_job = d.pop("tres_per_job", UNSET)

        tres_per_node = d.pop("tres_per_node", UNSET)

        tres_per_socket = d.pop("tres_per_socket", UNSET)

        tres_per_task = d.pop("tres_per_task", UNSET)

        tres_req_str = d.pop("tres_req_str", UNSET)

        tres_alloc_str = d.pop("tres_alloc_str", UNSET)

        user_id = d.pop("user_id", UNSET)

        user_name = d.pop("user_name", UNSET)

        maximum_switch_wait_time = d.pop("maximum_switch_wait_time", UNSET)

        wckey = d.pop("wckey", UNSET)

        current_working_directory = d.pop("current_working_directory", UNSET)

        v0040_job_info = cls(
            account=account,
            accrue_time=accrue_time,
            admin_comment=admin_comment,
            allocating_node=allocating_node,
            array_job_id=array_job_id,
            array_task_id=array_task_id,
            array_max_tasks=array_max_tasks,
            array_task_string=array_task_string,
            association_id=association_id,
            batch_features=batch_features,
            batch_flag=batch_flag,
            batch_host=batch_host,
            flags=flags,
            burst_buffer=burst_buffer,
            burst_buffer_state=burst_buffer_state,
            cluster=cluster,
            cluster_features=cluster_features,
            command=command,
            comment=comment,
            container=container,
            container_id=container_id,
            contiguous=contiguous,
            core_spec=core_spec,
            thread_spec=thread_spec,
            cores_per_socket=cores_per_socket,
            billable_tres=billable_tres,
            cpus_per_task=cpus_per_task,
            cpu_frequency_minimum=cpu_frequency_minimum,
            cpu_frequency_maximum=cpu_frequency_maximum,
            cpu_frequency_governor=cpu_frequency_governor,
            cpus_per_tres=cpus_per_tres,
            cron=cron,
            deadline=deadline,
            delay_boot=delay_boot,
            dependency=dependency,
            derived_exit_code=derived_exit_code,
            eligible_time=eligible_time,
            end_time=end_time,
            excluded_nodes=excluded_nodes,
            exit_code=exit_code,
            extra=extra,
            failed_node=failed_node,
            features=features,
            federation_origin=federation_origin,
            federation_siblings_active=federation_siblings_active,
            federation_siblings_viable=federation_siblings_viable,
            gres_detail=gres_detail,
            group_id=group_id,
            group_name=group_name,
            het_job_id=het_job_id,
            het_job_id_set=het_job_id_set,
            het_job_offset=het_job_offset,
            job_id=job_id,
            job_resources=job_resources,
            job_size_str=job_size_str,
            job_state=job_state,
            last_sched_evaluation=last_sched_evaluation,
            licenses=licenses,
            mail_type=mail_type,
            mail_user=mail_user,
            max_cpus=max_cpus,
            max_nodes=max_nodes,
            mcs_label=mcs_label,
            memory_per_tres=memory_per_tres,
            name=name,
            network=network,
            nodes=nodes,
            nice=nice,
            tasks_per_core=tasks_per_core,
            tasks_per_tres=tasks_per_tres,
            tasks_per_node=tasks_per_node,
            tasks_per_socket=tasks_per_socket,
            tasks_per_board=tasks_per_board,
            cpus=cpus,
            node_count=node_count,
            tasks=tasks,
            partition=partition,
            prefer=prefer,
            memory_per_cpu=memory_per_cpu,
            memory_per_node=memory_per_node,
            minimum_cpus_per_node=minimum_cpus_per_node,
            minimum_tmp_disk_per_node=minimum_tmp_disk_per_node,
            power=power,
            preempt_time=preempt_time,
            preemptable_time=preemptable_time,
            pre_sus_time=pre_sus_time,
            hold=hold,
            priority=priority,
            profile=profile,
            qos=qos,
            reboot=reboot,
            required_nodes=required_nodes,
            minimum_switches=minimum_switches,
            requeue=requeue,
            resize_time=resize_time,
            restart_cnt=restart_cnt,
            resv_name=resv_name,
            scheduled_nodes=scheduled_nodes,
            selinux_context=selinux_context,
            shared=shared,
            exclusive=exclusive,
            oversubscribe=oversubscribe,
            show_flags=show_flags,
            sockets_per_board=sockets_per_board,
            sockets_per_node=sockets_per_node,
            start_time=start_time,
            state_description=state_description,
            state_reason=state_reason,
            standard_error=standard_error,
            standard_input=standard_input,
            standard_output=standard_output,
            submit_time=submit_time,
            suspend_time=suspend_time,
            system_comment=system_comment,
            time_limit=time_limit,
            time_minimum=time_minimum,
            threads_per_core=threads_per_core,
            tres_bind=tres_bind,
            tres_freq=tres_freq,
            tres_per_job=tres_per_job,
            tres_per_node=tres_per_node,
            tres_per_socket=tres_per_socket,
            tres_per_task=tres_per_task,
            tres_req_str=tres_req_str,
            tres_alloc_str=tres_alloc_str,
            user_id=user_id,
            user_name=user_name,
            maximum_switch_wait_time=maximum_switch_wait_time,
            wckey=wckey,
            current_working_directory=current_working_directory,
        )

        v0040_job_info.additional_properties = d
        return v0040_job_info

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
