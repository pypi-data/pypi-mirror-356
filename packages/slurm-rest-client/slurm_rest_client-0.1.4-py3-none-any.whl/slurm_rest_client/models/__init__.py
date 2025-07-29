"""Contains all the data models used in inputs/outputs"""

from .slurm_v0040_delete_job_flags import SlurmV0040DeleteJobFlags
from .slurm_v0040_get_job_flags import SlurmV0040GetJobFlags
from .slurm_v0040_get_jobs_flags import SlurmV0040GetJobsFlags
from .slurm_v0040_get_node_flags import SlurmV0040GetNodeFlags
from .slurm_v0040_get_nodes_flags import SlurmV0040GetNodesFlags
from .slurmdb_v0040_delete_cluster_classification import SlurmdbV0040DeleteClusterClassification
from .slurmdb_v0040_delete_cluster_flags import SlurmdbV0040DeleteClusterFlags
from .slurmdb_v0040_get_cluster_classification import SlurmdbV0040GetClusterClassification
from .slurmdb_v0040_get_cluster_flags import SlurmdbV0040GetClusterFlags
from .slurmdb_v0040_get_clusters_classification import SlurmdbV0040GetClustersClassification
from .slurmdb_v0040_get_clusters_flags import SlurmdbV0040GetClustersFlags
from .slurmdb_v0040_get_qos_preempt_mode import SlurmdbV0040GetQosPreemptMode
from .slurmdb_v0040_get_users_admin_level import SlurmdbV0040GetUsersAdminLevel
from .v0040_account import V0040Account
from .v0040_account_flags_item import V0040AccountFlagsItem
from .v0040_account_short import V0040AccountShort
from .v0040_accounting import V0040Accounting
from .v0040_accounting_allocated import V0040AccountingAllocated
from .v0040_accounts_add_cond import V0040AccountsAddCond
from .v0040_acct_gather_energy import V0040AcctGatherEnergy
from .v0040_assoc import V0040Assoc
from .v0040_assoc_default import V0040AssocDefault
from .v0040_assoc_flags_item import V0040AssocFlagsItem
from .v0040_assoc_max import V0040AssocMax
from .v0040_assoc_max_jobs import V0040AssocMaxJobs
from .v0040_assoc_max_jobs_per import V0040AssocMaxJobsPer
from .v0040_assoc_max_per import V0040AssocMaxPer
from .v0040_assoc_max_per_account import V0040AssocMaxPerAccount
from .v0040_assoc_max_tres import V0040AssocMaxTres
from .v0040_assoc_max_tres_group import V0040AssocMaxTresGroup
from .v0040_assoc_max_tres_minutes import V0040AssocMaxTresMinutes
from .v0040_assoc_max_tres_minutes_per import V0040AssocMaxTresMinutesPer
from .v0040_assoc_max_tres_per import V0040AssocMaxTresPer
from .v0040_assoc_min import V0040AssocMin
from .v0040_assoc_rec_set import V0040AssocRecSet
from .v0040_assoc_shares_obj_wrap import V0040AssocSharesObjWrap
from .v0040_assoc_shares_obj_wrap_fairshare import V0040AssocSharesObjWrapFairshare
from .v0040_assoc_shares_obj_wrap_tres import V0040AssocSharesObjWrapTres
from .v0040_assoc_shares_obj_wrap_type_item import V0040AssocSharesObjWrapTypeItem
from .v0040_assoc_short import V0040AssocShort
from .v0040_bf_exit_fields import V0040BfExitFields
from .v0040_cluster_rec import V0040ClusterRec
from .v0040_cluster_rec_associations import V0040ClusterRecAssociations
from .v0040_cluster_rec_controller import V0040ClusterRecController
from .v0040_cluster_rec_flags_item import V0040ClusterRecFlagsItem
from .v0040_controller_ping import V0040ControllerPing
from .v0040_coord import V0040Coord
from .v0040_cron_entry import V0040CronEntry
from .v0040_cron_entry_flags_item import V0040CronEntryFlagsItem
from .v0040_cron_entry_line import V0040CronEntryLine
from .v0040_ext_sensors_data import V0040ExtSensorsData
from .v0040_instance import V0040Instance
from .v0040_instance_time import V0040InstanceTime
from .v0040_job import V0040Job
from .v0040_job_array import V0040JobArray
from .v0040_job_array_limits import V0040JobArrayLimits
from .v0040_job_array_limits_max import V0040JobArrayLimitsMax
from .v0040_job_array_limits_max_running import V0040JobArrayLimitsMaxRunning
from .v0040_job_array_response_msg_entry import V0040JobArrayResponseMsgEntry
from .v0040_job_comment import V0040JobComment
from .v0040_job_desc_msg import V0040JobDescMsg
from .v0040_job_desc_msg_cpu_binding_flags_item import V0040JobDescMsgCpuBindingFlagsItem
from .v0040_job_desc_msg_exclusive_item import V0040JobDescMsgExclusiveItem
from .v0040_job_desc_msg_flags_item import V0040JobDescMsgFlagsItem
from .v0040_job_desc_msg_kill_warning_flags_item import V0040JobDescMsgKillWarningFlagsItem
from .v0040_job_desc_msg_mail_type_item import V0040JobDescMsgMailTypeItem
from .v0040_job_desc_msg_memory_binding_type_item import V0040JobDescMsgMemoryBindingTypeItem
from .v0040_job_desc_msg_open_mode_item import V0040JobDescMsgOpenModeItem
from .v0040_job_desc_msg_power_flags_item import V0040JobDescMsgPowerFlagsItem
from .v0040_job_desc_msg_profile_item import V0040JobDescMsgProfileItem
from .v0040_job_desc_msg_rlimits import V0040JobDescMsgRlimits
from .v0040_job_desc_msg_shared_item import V0040JobDescMsgSharedItem
from .v0040_job_desc_msg_x11_item import V0040JobDescMsgX11Item
from .v0040_job_flags_item import V0040JobFlagsItem
from .v0040_job_het import V0040JobHet
from .v0040_job_info import V0040JobInfo
from .v0040_job_info_exclusive_item import V0040JobInfoExclusiveItem
from .v0040_job_info_flags_item import V0040JobInfoFlagsItem
from .v0040_job_info_job_state_item import V0040JobInfoJobStateItem
from .v0040_job_info_mail_type_item import V0040JobInfoMailTypeItem
from .v0040_job_info_power import V0040JobInfoPower
from .v0040_job_info_power_flags_item import V0040JobInfoPowerFlagsItem
from .v0040_job_info_profile_item import V0040JobInfoProfileItem
from .v0040_job_info_shared_item import V0040JobInfoSharedItem
from .v0040_job_info_show_flags_item import V0040JobInfoShowFlagsItem
from .v0040_job_mcs import V0040JobMcs
from .v0040_job_required import V0040JobRequired
from .v0040_job_res import V0040JobRes
from .v0040_job_reservation import V0040JobReservation
from .v0040_job_state import V0040JobState
from .v0040_job_state_current_item import V0040JobStateCurrentItem
from .v0040_job_state_resp_job import V0040JobStateRespJob
from .v0040_job_state_resp_job_state_item import V0040JobStateRespJobStateItem
from .v0040_job_submit_req import V0040JobSubmitReq
from .v0040_job_submit_response_msg import V0040JobSubmitResponseMsg
from .v0040_job_time import V0040JobTime
from .v0040_job_time_system import V0040JobTimeSystem
from .v0040_job_time_total import V0040JobTimeTotal
from .v0040_job_time_user import V0040JobTimeUser
from .v0040_job_tres import V0040JobTres
from .v0040_kill_jobs_msg import V0040KillJobsMsg
from .v0040_kill_jobs_msg_flags_item import V0040KillJobsMsgFlagsItem
from .v0040_kill_jobs_msg_job_state_item import V0040KillJobsMsgJobStateItem
from .v0040_kill_jobs_resp_job import V0040KillJobsRespJob
from .v0040_kill_jobs_resp_job_error import V0040KillJobsRespJobError
from .v0040_kill_jobs_resp_job_federation import V0040KillJobsRespJobFederation
from .v0040_license import V0040License
from .v0040_node import V0040Node
from .v0040_node_next_state_after_reboot_item import V0040NodeNextStateAfterRebootItem
from .v0040_node_state_item import V0040NodeStateItem
from .v0040_openapi_accounts_add_cond_resp import V0040OpenapiAccountsAddCondResp
from .v0040_openapi_accounts_add_cond_resp_str import V0040OpenapiAccountsAddCondRespStr
from .v0040_openapi_accounts_removed_resp import V0040OpenapiAccountsRemovedResp
from .v0040_openapi_accounts_resp import V0040OpenapiAccountsResp
from .v0040_openapi_assocs_removed_resp import V0040OpenapiAssocsRemovedResp
from .v0040_openapi_assocs_resp import V0040OpenapiAssocsResp
from .v0040_openapi_clusters_removed_resp import V0040OpenapiClustersRemovedResp
from .v0040_openapi_clusters_resp import V0040OpenapiClustersResp
from .v0040_openapi_diag_resp import V0040OpenapiDiagResp
from .v0040_openapi_error import V0040OpenapiError
from .v0040_openapi_instances_resp import V0040OpenapiInstancesResp
from .v0040_openapi_job_info_resp import V0040OpenapiJobInfoResp
from .v0040_openapi_job_post_response import V0040OpenapiJobPostResponse
from .v0040_openapi_job_state_resp import V0040OpenapiJobStateResp
from .v0040_openapi_job_submit_response import V0040OpenapiJobSubmitResponse
from .v0040_openapi_kill_jobs_resp import V0040OpenapiKillJobsResp
from .v0040_openapi_licenses_resp import V0040OpenapiLicensesResp
from .v0040_openapi_meta import V0040OpenapiMeta
from .v0040_openapi_meta_client import V0040OpenapiMetaClient
from .v0040_openapi_meta_plugin import V0040OpenapiMetaPlugin
from .v0040_openapi_meta_slurm import V0040OpenapiMetaSlurm
from .v0040_openapi_meta_slurm_version import V0040OpenapiMetaSlurmVersion
from .v0040_openapi_nodes_resp import V0040OpenapiNodesResp
from .v0040_openapi_partition_resp import V0040OpenapiPartitionResp
from .v0040_openapi_ping_array_resp import V0040OpenapiPingArrayResp
from .v0040_openapi_reservation_resp import V0040OpenapiReservationResp
from .v0040_openapi_resp import V0040OpenapiResp
from .v0040_openapi_shares_resp import V0040OpenapiSharesResp
from .v0040_openapi_slurmdbd_config_resp import V0040OpenapiSlurmdbdConfigResp
from .v0040_openapi_slurmdbd_jobs_resp import V0040OpenapiSlurmdbdJobsResp
from .v0040_openapi_slurmdbd_qos_removed_resp import V0040OpenapiSlurmdbdQosRemovedResp
from .v0040_openapi_slurmdbd_qos_resp import V0040OpenapiSlurmdbdQosResp
from .v0040_openapi_slurmdbd_stats_resp import V0040OpenapiSlurmdbdStatsResp
from .v0040_openapi_tres_resp import V0040OpenapiTresResp
from .v0040_openapi_users_add_cond_resp import V0040OpenapiUsersAddCondResp
from .v0040_openapi_users_add_cond_resp_str import V0040OpenapiUsersAddCondRespStr
from .v0040_openapi_users_resp import V0040OpenapiUsersResp
from .v0040_openapi_warning import V0040OpenapiWarning
from .v0040_openapi_wckey_removed_resp import V0040OpenapiWckeyRemovedResp
from .v0040_openapi_wckey_resp import V0040OpenapiWckeyResp
from .v0040_partition_info import V0040PartitionInfo
from .v0040_partition_info_accounts import V0040PartitionInfoAccounts
from .v0040_partition_info_cpus import V0040PartitionInfoCpus
from .v0040_partition_info_defaults import V0040PartitionInfoDefaults
from .v0040_partition_info_groups import V0040PartitionInfoGroups
from .v0040_partition_info_maximums import V0040PartitionInfoMaximums
from .v0040_partition_info_maximums_oversubscribe import V0040PartitionInfoMaximumsOversubscribe
from .v0040_partition_info_maximums_oversubscribe_flags_item import V0040PartitionInfoMaximumsOversubscribeFlagsItem
from .v0040_partition_info_minimums import V0040PartitionInfoMinimums
from .v0040_partition_info_nodes import V0040PartitionInfoNodes
from .v0040_partition_info_partition import V0040PartitionInfoPartition
from .v0040_partition_info_partition_state_item import V0040PartitionInfoPartitionStateItem
from .v0040_partition_info_priority import V0040PartitionInfoPriority
from .v0040_partition_info_qos import V0040PartitionInfoQos
from .v0040_partition_info_timeouts import V0040PartitionInfoTimeouts
from .v0040_partition_info_tres import V0040PartitionInfoTres
from .v0040_power_mgmt_data import V0040PowerMgmtData
from .v0040_process_exit_code_verbose import V0040ProcessExitCodeVerbose
from .v0040_process_exit_code_verbose_signal import V0040ProcessExitCodeVerboseSignal
from .v0040_process_exit_code_verbose_status_item import V0040ProcessExitCodeVerboseStatusItem
from .v0040_qos import V0040Qos
from .v0040_qos_flags_item import V0040QosFlagsItem
from .v0040_qos_limits import V0040QosLimits
from .v0040_qos_limits_max import V0040QosLimitsMax
from .v0040_qos_limits_max_accruing import V0040QosLimitsMaxAccruing
from .v0040_qos_limits_max_accruing_per import V0040QosLimitsMaxAccruingPer
from .v0040_qos_limits_max_active_jobs import V0040QosLimitsMaxActiveJobs
from .v0040_qos_limits_max_jobs import V0040QosLimitsMaxJobs
from .v0040_qos_limits_max_jobs_active_jobs import V0040QosLimitsMaxJobsActiveJobs
from .v0040_qos_limits_max_jobs_active_jobs_per import V0040QosLimitsMaxJobsActiveJobsPer
from .v0040_qos_limits_max_jobs_per import V0040QosLimitsMaxJobsPer
from .v0040_qos_limits_max_tres import V0040QosLimitsMaxTres
from .v0040_qos_limits_max_tres_minutes import V0040QosLimitsMaxTresMinutes
from .v0040_qos_limits_max_tres_minutes_per import V0040QosLimitsMaxTresMinutesPer
from .v0040_qos_limits_max_tres_per import V0040QosLimitsMaxTresPer
from .v0040_qos_limits_max_wall_clock import V0040QosLimitsMaxWallClock
from .v0040_qos_limits_max_wall_clock_per import V0040QosLimitsMaxWallClockPer
from .v0040_qos_limits_min import V0040QosLimitsMin
from .v0040_qos_limits_min_tres import V0040QosLimitsMinTres
from .v0040_qos_limits_min_tres_per import V0040QosLimitsMinTresPer
from .v0040_qos_preempt import V0040QosPreempt
from .v0040_qos_preempt_mode_item import V0040QosPreemptModeItem
from .v0040_reservation_core_spec import V0040ReservationCoreSpec
from .v0040_reservation_info import V0040ReservationInfo
from .v0040_reservation_info_flags_item import V0040ReservationInfoFlagsItem
from .v0040_reservation_info_purge_completed import V0040ReservationInfoPurgeCompleted
from .v0040_rollup_stats_item import V0040RollupStatsItem
from .v0040_rollup_stats_item_type import V0040RollupStatsItemType
from .v0040_schedule_exit_fields import V0040ScheduleExitFields
from .v0040_shares_float_128_tres import V0040SharesFloat128Tres
from .v0040_shares_resp_msg import V0040SharesRespMsg
from .v0040_shares_uint_64_tres import V0040SharesUint64Tres
from .v0040_stats_msg import V0040StatsMsg
from .v0040_stats_msg_rpcs_by_type_item import V0040StatsMsgRpcsByTypeItem
from .v0040_stats_msg_rpcs_by_user_item import V0040StatsMsgRpcsByUserItem
from .v0040_stats_rec import V0040StatsRec
from .v0040_stats_rpc import V0040StatsRpc
from .v0040_stats_rpc_time import V0040StatsRpcTime
from .v0040_stats_user import V0040StatsUser
from .v0040_stats_user_time import V0040StatsUserTime
from .v0040_step import V0040Step
from .v0040_step_cpu import V0040StepCPU
from .v0040_step_cpu_requested_frequency import V0040StepCPURequestedFrequency
from .v0040_step_nodes import V0040StepNodes
from .v0040_step_state_item import V0040StepStateItem
from .v0040_step_statistics import V0040StepStatistics
from .v0040_step_statistics_cpu import V0040StepStatisticsCPU
from .v0040_step_statistics_energy import V0040StepStatisticsEnergy
from .v0040_step_step import V0040StepStep
from .v0040_step_task import V0040StepTask
from .v0040_step_tasks import V0040StepTasks
from .v0040_step_time import V0040StepTime
from .v0040_step_time_system import V0040StepTimeSystem
from .v0040_step_time_total import V0040StepTimeTotal
from .v0040_step_time_user import V0040StepTimeUser
from .v0040_step_tres import V0040StepTres
from .v0040_step_tres_consumed import V0040StepTresConsumed
from .v0040_step_tres_requested import V0040StepTresRequested
from .v0040_tres import V0040Tres
from .v0040_update_node_msg import V0040UpdateNodeMsg
from .v0040_update_node_msg_state_item import V0040UpdateNodeMsgStateItem
from .v0040_user import V0040User
from .v0040_user_administrator_level_item import V0040UserAdministratorLevelItem
from .v0040_user_default import V0040UserDefault
from .v0040_user_flags_item import V0040UserFlagsItem
from .v0040_user_short import V0040UserShort
from .v0040_user_short_adminlevel_item import V0040UserShortAdminlevelItem
from .v0040_users_add_cond import V0040UsersAddCond
from .v0040_wckey import V0040Wckey
from .v0040_wckey_flags_item import V0040WckeyFlagsItem
from .v0040_wckey_tag_struct import V0040WckeyTagStruct
from .v0040_wckey_tag_struct_flags_item import V0040WckeyTagStructFlagsItem

__all__ = (
    "SlurmdbV0040DeleteClusterClassification",
    "SlurmdbV0040DeleteClusterFlags",
    "SlurmdbV0040GetClusterClassification",
    "SlurmdbV0040GetClusterFlags",
    "SlurmdbV0040GetClustersClassification",
    "SlurmdbV0040GetClustersFlags",
    "SlurmdbV0040GetQosPreemptMode",
    "SlurmdbV0040GetUsersAdminLevel",
    "SlurmV0040DeleteJobFlags",
    "SlurmV0040GetJobFlags",
    "SlurmV0040GetJobsFlags",
    "SlurmV0040GetNodeFlags",
    "SlurmV0040GetNodesFlags",
    "V0040Account",
    "V0040AccountFlagsItem",
    "V0040Accounting",
    "V0040AccountingAllocated",
    "V0040AccountsAddCond",
    "V0040AccountShort",
    "V0040AcctGatherEnergy",
    "V0040Assoc",
    "V0040AssocDefault",
    "V0040AssocFlagsItem",
    "V0040AssocMax",
    "V0040AssocMaxJobs",
    "V0040AssocMaxJobsPer",
    "V0040AssocMaxPer",
    "V0040AssocMaxPerAccount",
    "V0040AssocMaxTres",
    "V0040AssocMaxTresGroup",
    "V0040AssocMaxTresMinutes",
    "V0040AssocMaxTresMinutesPer",
    "V0040AssocMaxTresPer",
    "V0040AssocMin",
    "V0040AssocRecSet",
    "V0040AssocSharesObjWrap",
    "V0040AssocSharesObjWrapFairshare",
    "V0040AssocSharesObjWrapTres",
    "V0040AssocSharesObjWrapTypeItem",
    "V0040AssocShort",
    "V0040BfExitFields",
    "V0040ClusterRec",
    "V0040ClusterRecAssociations",
    "V0040ClusterRecController",
    "V0040ClusterRecFlagsItem",
    "V0040ControllerPing",
    "V0040Coord",
    "V0040CronEntry",
    "V0040CronEntryFlagsItem",
    "V0040CronEntryLine",
    "V0040ExtSensorsData",
    "V0040Instance",
    "V0040InstanceTime",
    "V0040Job",
    "V0040JobArray",
    "V0040JobArrayLimits",
    "V0040JobArrayLimitsMax",
    "V0040JobArrayLimitsMaxRunning",
    "V0040JobArrayResponseMsgEntry",
    "V0040JobComment",
    "V0040JobDescMsg",
    "V0040JobDescMsgCpuBindingFlagsItem",
    "V0040JobDescMsgExclusiveItem",
    "V0040JobDescMsgFlagsItem",
    "V0040JobDescMsgKillWarningFlagsItem",
    "V0040JobDescMsgMailTypeItem",
    "V0040JobDescMsgMemoryBindingTypeItem",
    "V0040JobDescMsgOpenModeItem",
    "V0040JobDescMsgPowerFlagsItem",
    "V0040JobDescMsgProfileItem",
    "V0040JobDescMsgRlimits",
    "V0040JobDescMsgSharedItem",
    "V0040JobDescMsgX11Item",
    "V0040JobFlagsItem",
    "V0040JobHet",
    "V0040JobInfo",
    "V0040JobInfoExclusiveItem",
    "V0040JobInfoFlagsItem",
    "V0040JobInfoJobStateItem",
    "V0040JobInfoMailTypeItem",
    "V0040JobInfoPower",
    "V0040JobInfoPowerFlagsItem",
    "V0040JobInfoProfileItem",
    "V0040JobInfoSharedItem",
    "V0040JobInfoShowFlagsItem",
    "V0040JobMcs",
    "V0040JobRequired",
    "V0040JobRes",
    "V0040JobReservation",
    "V0040JobState",
    "V0040JobStateCurrentItem",
    "V0040JobStateRespJob",
    "V0040JobStateRespJobStateItem",
    "V0040JobSubmitReq",
    "V0040JobSubmitResponseMsg",
    "V0040JobTime",
    "V0040JobTimeSystem",
    "V0040JobTimeTotal",
    "V0040JobTimeUser",
    "V0040JobTres",
    "V0040KillJobsMsg",
    "V0040KillJobsMsgFlagsItem",
    "V0040KillJobsMsgJobStateItem",
    "V0040KillJobsRespJob",
    "V0040KillJobsRespJobError",
    "V0040KillJobsRespJobFederation",
    "V0040License",
    "V0040Node",
    "V0040NodeNextStateAfterRebootItem",
    "V0040NodeStateItem",
    "V0040OpenapiAccountsAddCondResp",
    "V0040OpenapiAccountsAddCondRespStr",
    "V0040OpenapiAccountsRemovedResp",
    "V0040OpenapiAccountsResp",
    "V0040OpenapiAssocsRemovedResp",
    "V0040OpenapiAssocsResp",
    "V0040OpenapiClustersRemovedResp",
    "V0040OpenapiClustersResp",
    "V0040OpenapiDiagResp",
    "V0040OpenapiError",
    "V0040OpenapiInstancesResp",
    "V0040OpenapiJobInfoResp",
    "V0040OpenapiJobPostResponse",
    "V0040OpenapiJobStateResp",
    "V0040OpenapiJobSubmitResponse",
    "V0040OpenapiKillJobsResp",
    "V0040OpenapiLicensesResp",
    "V0040OpenapiMeta",
    "V0040OpenapiMetaClient",
    "V0040OpenapiMetaPlugin",
    "V0040OpenapiMetaSlurm",
    "V0040OpenapiMetaSlurmVersion",
    "V0040OpenapiNodesResp",
    "V0040OpenapiPartitionResp",
    "V0040OpenapiPingArrayResp",
    "V0040OpenapiReservationResp",
    "V0040OpenapiResp",
    "V0040OpenapiSharesResp",
    "V0040OpenapiSlurmdbdConfigResp",
    "V0040OpenapiSlurmdbdJobsResp",
    "V0040OpenapiSlurmdbdQosRemovedResp",
    "V0040OpenapiSlurmdbdQosResp",
    "V0040OpenapiSlurmdbdStatsResp",
    "V0040OpenapiTresResp",
    "V0040OpenapiUsersAddCondResp",
    "V0040OpenapiUsersAddCondRespStr",
    "V0040OpenapiUsersResp",
    "V0040OpenapiWarning",
    "V0040OpenapiWckeyRemovedResp",
    "V0040OpenapiWckeyResp",
    "V0040PartitionInfo",
    "V0040PartitionInfoAccounts",
    "V0040PartitionInfoCpus",
    "V0040PartitionInfoDefaults",
    "V0040PartitionInfoGroups",
    "V0040PartitionInfoMaximums",
    "V0040PartitionInfoMaximumsOversubscribe",
    "V0040PartitionInfoMaximumsOversubscribeFlagsItem",
    "V0040PartitionInfoMinimums",
    "V0040PartitionInfoNodes",
    "V0040PartitionInfoPartition",
    "V0040PartitionInfoPartitionStateItem",
    "V0040PartitionInfoPriority",
    "V0040PartitionInfoQos",
    "V0040PartitionInfoTimeouts",
    "V0040PartitionInfoTres",
    "V0040PowerMgmtData",
    "V0040ProcessExitCodeVerbose",
    "V0040ProcessExitCodeVerboseSignal",
    "V0040ProcessExitCodeVerboseStatusItem",
    "V0040Qos",
    "V0040QosFlagsItem",
    "V0040QosLimits",
    "V0040QosLimitsMax",
    "V0040QosLimitsMaxAccruing",
    "V0040QosLimitsMaxAccruingPer",
    "V0040QosLimitsMaxActiveJobs",
    "V0040QosLimitsMaxJobs",
    "V0040QosLimitsMaxJobsActiveJobs",
    "V0040QosLimitsMaxJobsActiveJobsPer",
    "V0040QosLimitsMaxJobsPer",
    "V0040QosLimitsMaxTres",
    "V0040QosLimitsMaxTresMinutes",
    "V0040QosLimitsMaxTresMinutesPer",
    "V0040QosLimitsMaxTresPer",
    "V0040QosLimitsMaxWallClock",
    "V0040QosLimitsMaxWallClockPer",
    "V0040QosLimitsMin",
    "V0040QosLimitsMinTres",
    "V0040QosLimitsMinTresPer",
    "V0040QosPreempt",
    "V0040QosPreemptModeItem",
    "V0040ReservationCoreSpec",
    "V0040ReservationInfo",
    "V0040ReservationInfoFlagsItem",
    "V0040ReservationInfoPurgeCompleted",
    "V0040RollupStatsItem",
    "V0040RollupStatsItemType",
    "V0040ScheduleExitFields",
    "V0040SharesFloat128Tres",
    "V0040SharesRespMsg",
    "V0040SharesUint64Tres",
    "V0040StatsMsg",
    "V0040StatsMsgRpcsByTypeItem",
    "V0040StatsMsgRpcsByUserItem",
    "V0040StatsRec",
    "V0040StatsRpc",
    "V0040StatsRpcTime",
    "V0040StatsUser",
    "V0040StatsUserTime",
    "V0040Step",
    "V0040StepCPU",
    "V0040StepCPURequestedFrequency",
    "V0040StepNodes",
    "V0040StepStateItem",
    "V0040StepStatistics",
    "V0040StepStatisticsCPU",
    "V0040StepStatisticsEnergy",
    "V0040StepStep",
    "V0040StepTask",
    "V0040StepTasks",
    "V0040StepTime",
    "V0040StepTimeSystem",
    "V0040StepTimeTotal",
    "V0040StepTimeUser",
    "V0040StepTres",
    "V0040StepTresConsumed",
    "V0040StepTresRequested",
    "V0040Tres",
    "V0040UpdateNodeMsg",
    "V0040UpdateNodeMsgStateItem",
    "V0040User",
    "V0040UserAdministratorLevelItem",
    "V0040UserDefault",
    "V0040UserFlagsItem",
    "V0040UsersAddCond",
    "V0040UserShort",
    "V0040UserShortAdminlevelItem",
    "V0040Wckey",
    "V0040WckeyFlagsItem",
    "V0040WckeyTagStruct",
    "V0040WckeyTagStructFlagsItem",
)
