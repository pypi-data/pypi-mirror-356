from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.v0040_job_flags_item import V0040JobFlagsItem
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_assoc_short import V0040AssocShort
    from ..models.v0040_job_array import V0040JobArray
    from ..models.v0040_job_comment import V0040JobComment
    from ..models.v0040_job_het import V0040JobHet
    from ..models.v0040_job_mcs import V0040JobMcs
    from ..models.v0040_job_required import V0040JobRequired
    from ..models.v0040_job_reservation import V0040JobReservation
    from ..models.v0040_job_state import V0040JobState
    from ..models.v0040_job_time import V0040JobTime
    from ..models.v0040_job_tres import V0040JobTres
    from ..models.v0040_process_exit_code_verbose import V0040ProcessExitCodeVerbose
    from ..models.v0040_step import V0040Step
    from ..models.v0040_wckey_tag_struct import V0040WckeyTagStruct


T = TypeVar("T", bound="V0040Job")


@_attrs_define
class V0040Job:
    """
    Attributes:
        account (Union[Unset, str]):
        comment (Union[Unset, V0040JobComment]):
        allocation_nodes (Union[Unset, int]):
        array (Union[Unset, V0040JobArray]):
        association (Union[Unset, V0040AssocShort]):
        block (Union[Unset, str]):
        cluster (Union[Unset, str]):
        constraints (Union[Unset, str]):
        container (Union[Unset, str]):
        derived_exit_code (Union[Unset, V0040ProcessExitCodeVerbose]):
        time (Union[Unset, V0040JobTime]):
        exit_code (Union[Unset, V0040ProcessExitCodeVerbose]):
        extra (Union[Unset, str]):
        failed_node (Union[Unset, str]):
        flags (Union[Unset, list[V0040JobFlagsItem]]):
        group (Union[Unset, str]):
        het (Union[Unset, V0040JobHet]):
        job_id (Union[Unset, int]):
        name (Union[Unset, str]):
        licenses (Union[Unset, str]):
        mcs (Union[Unset, V0040JobMcs]):
        nodes (Union[Unset, str]):
        partition (Union[Unset, str]):
        hold (Union[Unset, bool]): Job held
        priority (Union[Unset, int]):
        qos (Union[Unset, str]):
        required (Union[Unset, V0040JobRequired]):
        kill_request_user (Union[Unset, str]):
        reservation (Union[Unset, V0040JobReservation]):
        script (Union[Unset, str]):
        state (Union[Unset, V0040JobState]):
        steps (Union[Unset, list['V0040Step']]):
        submit_line (Union[Unset, str]):
        tres (Union[Unset, V0040JobTres]):
        used_gres (Union[Unset, str]):
        user (Union[Unset, str]):
        wckey (Union[Unset, V0040WckeyTagStruct]):
        working_directory (Union[Unset, str]):
    """

    account: Union[Unset, str] = UNSET
    comment: Union[Unset, "V0040JobComment"] = UNSET
    allocation_nodes: Union[Unset, int] = UNSET
    array: Union[Unset, "V0040JobArray"] = UNSET
    association: Union[Unset, "V0040AssocShort"] = UNSET
    block: Union[Unset, str] = UNSET
    cluster: Union[Unset, str] = UNSET
    constraints: Union[Unset, str] = UNSET
    container: Union[Unset, str] = UNSET
    derived_exit_code: Union[Unset, "V0040ProcessExitCodeVerbose"] = UNSET
    time: Union[Unset, "V0040JobTime"] = UNSET
    exit_code: Union[Unset, "V0040ProcessExitCodeVerbose"] = UNSET
    extra: Union[Unset, str] = UNSET
    failed_node: Union[Unset, str] = UNSET
    flags: Union[Unset, list[V0040JobFlagsItem]] = UNSET
    group: Union[Unset, str] = UNSET
    het: Union[Unset, "V0040JobHet"] = UNSET
    job_id: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    licenses: Union[Unset, str] = UNSET
    mcs: Union[Unset, "V0040JobMcs"] = UNSET
    nodes: Union[Unset, str] = UNSET
    partition: Union[Unset, str] = UNSET
    hold: Union[Unset, bool] = UNSET
    priority: Union[Unset, int] = UNSET
    qos: Union[Unset, str] = UNSET
    required: Union[Unset, "V0040JobRequired"] = UNSET
    kill_request_user: Union[Unset, str] = UNSET
    reservation: Union[Unset, "V0040JobReservation"] = UNSET
    script: Union[Unset, str] = UNSET
    state: Union[Unset, "V0040JobState"] = UNSET
    steps: Union[Unset, list["V0040Step"]] = UNSET
    submit_line: Union[Unset, str] = UNSET
    tres: Union[Unset, "V0040JobTres"] = UNSET
    used_gres: Union[Unset, str] = UNSET
    user: Union[Unset, str] = UNSET
    wckey: Union[Unset, "V0040WckeyTagStruct"] = UNSET
    working_directory: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        account = self.account

        comment: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.comment, Unset):
            comment = self.comment.to_dict()

        allocation_nodes = self.allocation_nodes

        array: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.array, Unset):
            array = self.array.to_dict()

        association: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.association, Unset):
            association = self.association.to_dict()

        block = self.block

        cluster = self.cluster

        constraints = self.constraints

        container = self.container

        derived_exit_code: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.derived_exit_code, Unset):
            derived_exit_code = self.derived_exit_code.to_dict()

        time: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.time, Unset):
            time = self.time.to_dict()

        exit_code: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.exit_code, Unset):
            exit_code = self.exit_code.to_dict()

        extra = self.extra

        failed_node = self.failed_node

        flags: Union[Unset, list[str]] = UNSET
        if not isinstance(self.flags, Unset):
            flags = []
            for flags_item_data in self.flags:
                flags_item = flags_item_data.value
                flags.append(flags_item)

        group = self.group

        het: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.het, Unset):
            het = self.het.to_dict()

        job_id = self.job_id

        name = self.name

        licenses = self.licenses

        mcs: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.mcs, Unset):
            mcs = self.mcs.to_dict()

        nodes = self.nodes

        partition = self.partition

        hold = self.hold

        priority = self.priority

        qos = self.qos

        required: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.required, Unset):
            required = self.required.to_dict()

        kill_request_user = self.kill_request_user

        reservation: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.reservation, Unset):
            reservation = self.reservation.to_dict()

        script = self.script

        state: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.state, Unset):
            state = self.state.to_dict()

        steps: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.steps, Unset):
            steps = []
            for componentsschemasv0_0_40_step_list_item_data in self.steps:
                componentsschemasv0_0_40_step_list_item = componentsschemasv0_0_40_step_list_item_data.to_dict()
                steps.append(componentsschemasv0_0_40_step_list_item)

        submit_line = self.submit_line

        tres: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.tres, Unset):
            tres = self.tres.to_dict()

        used_gres = self.used_gres

        user = self.user

        wckey: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.wckey, Unset):
            wckey = self.wckey.to_dict()

        working_directory = self.working_directory

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if account is not UNSET:
            field_dict["account"] = account
        if comment is not UNSET:
            field_dict["comment"] = comment
        if allocation_nodes is not UNSET:
            field_dict["allocation_nodes"] = allocation_nodes
        if array is not UNSET:
            field_dict["array"] = array
        if association is not UNSET:
            field_dict["association"] = association
        if block is not UNSET:
            field_dict["block"] = block
        if cluster is not UNSET:
            field_dict["cluster"] = cluster
        if constraints is not UNSET:
            field_dict["constraints"] = constraints
        if container is not UNSET:
            field_dict["container"] = container
        if derived_exit_code is not UNSET:
            field_dict["derived_exit_code"] = derived_exit_code
        if time is not UNSET:
            field_dict["time"] = time
        if exit_code is not UNSET:
            field_dict["exit_code"] = exit_code
        if extra is not UNSET:
            field_dict["extra"] = extra
        if failed_node is not UNSET:
            field_dict["failed_node"] = failed_node
        if flags is not UNSET:
            field_dict["flags"] = flags
        if group is not UNSET:
            field_dict["group"] = group
        if het is not UNSET:
            field_dict["het"] = het
        if job_id is not UNSET:
            field_dict["job_id"] = job_id
        if name is not UNSET:
            field_dict["name"] = name
        if licenses is not UNSET:
            field_dict["licenses"] = licenses
        if mcs is not UNSET:
            field_dict["mcs"] = mcs
        if nodes is not UNSET:
            field_dict["nodes"] = nodes
        if partition is not UNSET:
            field_dict["partition"] = partition
        if hold is not UNSET:
            field_dict["hold"] = hold
        if priority is not UNSET:
            field_dict["priority"] = priority
        if qos is not UNSET:
            field_dict["qos"] = qos
        if required is not UNSET:
            field_dict["required"] = required
        if kill_request_user is not UNSET:
            field_dict["kill_request_user"] = kill_request_user
        if reservation is not UNSET:
            field_dict["reservation"] = reservation
        if script is not UNSET:
            field_dict["script"] = script
        if state is not UNSET:
            field_dict["state"] = state
        if steps is not UNSET:
            field_dict["steps"] = steps
        if submit_line is not UNSET:
            field_dict["submit_line"] = submit_line
        if tres is not UNSET:
            field_dict["tres"] = tres
        if used_gres is not UNSET:
            field_dict["used_gres"] = used_gres
        if user is not UNSET:
            field_dict["user"] = user
        if wckey is not UNSET:
            field_dict["wckey"] = wckey
        if working_directory is not UNSET:
            field_dict["working_directory"] = working_directory

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0040_assoc_short import V0040AssocShort
        from ..models.v0040_job_array import V0040JobArray
        from ..models.v0040_job_comment import V0040JobComment
        from ..models.v0040_job_het import V0040JobHet
        from ..models.v0040_job_mcs import V0040JobMcs
        from ..models.v0040_job_required import V0040JobRequired
        from ..models.v0040_job_reservation import V0040JobReservation
        from ..models.v0040_job_state import V0040JobState
        from ..models.v0040_job_time import V0040JobTime
        from ..models.v0040_job_tres import V0040JobTres
        from ..models.v0040_process_exit_code_verbose import V0040ProcessExitCodeVerbose
        from ..models.v0040_step import V0040Step
        from ..models.v0040_wckey_tag_struct import V0040WckeyTagStruct

        d = dict(src_dict)
        account = d.pop("account", UNSET)

        _comment = d.pop("comment", UNSET)
        comment: Union[Unset, V0040JobComment]
        if isinstance(_comment, Unset):
            comment = UNSET
        else:
            comment = V0040JobComment.from_dict(_comment)

        allocation_nodes = d.pop("allocation_nodes", UNSET)

        _array = d.pop("array", UNSET)
        array: Union[Unset, V0040JobArray]
        if isinstance(_array, Unset):
            array = UNSET
        else:
            array = V0040JobArray.from_dict(_array)

        _association = d.pop("association", UNSET)
        association: Union[Unset, V0040AssocShort]
        if isinstance(_association, Unset):
            association = UNSET
        else:
            association = V0040AssocShort.from_dict(_association)

        block = d.pop("block", UNSET)

        cluster = d.pop("cluster", UNSET)

        constraints = d.pop("constraints", UNSET)

        container = d.pop("container", UNSET)

        _derived_exit_code = d.pop("derived_exit_code", UNSET)
        derived_exit_code: Union[Unset, V0040ProcessExitCodeVerbose]
        if isinstance(_derived_exit_code, Unset):
            derived_exit_code = UNSET
        else:
            derived_exit_code = V0040ProcessExitCodeVerbose.from_dict(_derived_exit_code)

        _time = d.pop("time", UNSET)
        time: Union[Unset, V0040JobTime]
        if isinstance(_time, Unset):
            time = UNSET
        else:
            time = V0040JobTime.from_dict(_time)

        _exit_code = d.pop("exit_code", UNSET)
        exit_code: Union[Unset, V0040ProcessExitCodeVerbose]
        if isinstance(_exit_code, Unset):
            exit_code = UNSET
        else:
            exit_code = V0040ProcessExitCodeVerbose.from_dict(_exit_code)

        extra = d.pop("extra", UNSET)

        failed_node = d.pop("failed_node", UNSET)

        flags = []
        _flags = d.pop("flags", UNSET)
        for flags_item_data in _flags or []:
            flags_item = V0040JobFlagsItem(flags_item_data)

            flags.append(flags_item)

        group = d.pop("group", UNSET)

        _het = d.pop("het", UNSET)
        het: Union[Unset, V0040JobHet]
        if isinstance(_het, Unset):
            het = UNSET
        else:
            het = V0040JobHet.from_dict(_het)

        job_id = d.pop("job_id", UNSET)

        name = d.pop("name", UNSET)

        licenses = d.pop("licenses", UNSET)

        _mcs = d.pop("mcs", UNSET)
        mcs: Union[Unset, V0040JobMcs]
        if isinstance(_mcs, Unset):
            mcs = UNSET
        else:
            mcs = V0040JobMcs.from_dict(_mcs)

        nodes = d.pop("nodes", UNSET)

        partition = d.pop("partition", UNSET)

        hold = d.pop("hold", UNSET)

        priority = d.pop("priority", UNSET)

        qos = d.pop("qos", UNSET)

        _required = d.pop("required", UNSET)
        required: Union[Unset, V0040JobRequired]
        if isinstance(_required, Unset):
            required = UNSET
        else:
            required = V0040JobRequired.from_dict(_required)

        kill_request_user = d.pop("kill_request_user", UNSET)

        _reservation = d.pop("reservation", UNSET)
        reservation: Union[Unset, V0040JobReservation]
        if isinstance(_reservation, Unset):
            reservation = UNSET
        else:
            reservation = V0040JobReservation.from_dict(_reservation)

        script = d.pop("script", UNSET)

        _state = d.pop("state", UNSET)
        state: Union[Unset, V0040JobState]
        if isinstance(_state, Unset):
            state = UNSET
        else:
            state = V0040JobState.from_dict(_state)

        steps = []
        _steps = d.pop("steps", UNSET)
        for componentsschemasv0_0_40_step_list_item_data in _steps or []:
            componentsschemasv0_0_40_step_list_item = V0040Step.from_dict(componentsschemasv0_0_40_step_list_item_data)

            steps.append(componentsschemasv0_0_40_step_list_item)

        submit_line = d.pop("submit_line", UNSET)

        _tres = d.pop("tres", UNSET)
        tres: Union[Unset, V0040JobTres]
        if isinstance(_tres, Unset):
            tres = UNSET
        else:
            tres = V0040JobTres.from_dict(_tres)

        used_gres = d.pop("used_gres", UNSET)

        user = d.pop("user", UNSET)

        _wckey = d.pop("wckey", UNSET)
        wckey: Union[Unset, V0040WckeyTagStruct]
        if isinstance(_wckey, Unset):
            wckey = UNSET
        else:
            wckey = V0040WckeyTagStruct.from_dict(_wckey)

        working_directory = d.pop("working_directory", UNSET)

        v0040_job = cls(
            account=account,
            comment=comment,
            allocation_nodes=allocation_nodes,
            array=array,
            association=association,
            block=block,
            cluster=cluster,
            constraints=constraints,
            container=container,
            derived_exit_code=derived_exit_code,
            time=time,
            exit_code=exit_code,
            extra=extra,
            failed_node=failed_node,
            flags=flags,
            group=group,
            het=het,
            job_id=job_id,
            name=name,
            licenses=licenses,
            mcs=mcs,
            nodes=nodes,
            partition=partition,
            hold=hold,
            priority=priority,
            qos=qos,
            required=required,
            kill_request_user=kill_request_user,
            reservation=reservation,
            script=script,
            state=state,
            steps=steps,
            submit_line=submit_line,
            tres=tres,
            used_gres=used_gres,
            user=user,
            wckey=wckey,
            working_directory=working_directory,
        )

        v0040_job.additional_properties = d
        return v0040_job

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
