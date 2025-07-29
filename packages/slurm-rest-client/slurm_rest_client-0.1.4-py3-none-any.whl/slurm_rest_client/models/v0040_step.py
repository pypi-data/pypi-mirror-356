from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.v0040_step_state_item import V0040StepStateItem
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_process_exit_code_verbose import V0040ProcessExitCodeVerbose
    from ..models.v0040_step_cpu import V0040StepCPU
    from ..models.v0040_step_nodes import V0040StepNodes
    from ..models.v0040_step_statistics import V0040StepStatistics
    from ..models.v0040_step_step import V0040StepStep
    from ..models.v0040_step_task import V0040StepTask
    from ..models.v0040_step_tasks import V0040StepTasks
    from ..models.v0040_step_time import V0040StepTime
    from ..models.v0040_step_tres import V0040StepTres


T = TypeVar("T", bound="V0040Step")


@_attrs_define
class V0040Step:
    """
    Attributes:
        time (Union[Unset, V0040StepTime]):
        exit_code (Union[Unset, V0040ProcessExitCodeVerbose]):
        nodes (Union[Unset, V0040StepNodes]):
        tasks (Union[Unset, V0040StepTasks]):
        pid (Union[Unset, str]):
        cpu (Union[Unset, V0040StepCPU]):
        kill_request_user (Union[Unset, str]):
        state (Union[Unset, list[V0040StepStateItem]]):
        statistics (Union[Unset, V0040StepStatistics]):
        step (Union[Unset, V0040StepStep]):
        task (Union[Unset, V0040StepTask]):
        tres (Union[Unset, V0040StepTres]):
    """

    time: Union[Unset, "V0040StepTime"] = UNSET
    exit_code: Union[Unset, "V0040ProcessExitCodeVerbose"] = UNSET
    nodes: Union[Unset, "V0040StepNodes"] = UNSET
    tasks: Union[Unset, "V0040StepTasks"] = UNSET
    pid: Union[Unset, str] = UNSET
    cpu: Union[Unset, "V0040StepCPU"] = UNSET
    kill_request_user: Union[Unset, str] = UNSET
    state: Union[Unset, list[V0040StepStateItem]] = UNSET
    statistics: Union[Unset, "V0040StepStatistics"] = UNSET
    step: Union[Unset, "V0040StepStep"] = UNSET
    task: Union[Unset, "V0040StepTask"] = UNSET
    tres: Union[Unset, "V0040StepTres"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        time: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.time, Unset):
            time = self.time.to_dict()

        exit_code: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.exit_code, Unset):
            exit_code = self.exit_code.to_dict()

        nodes: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.nodes, Unset):
            nodes = self.nodes.to_dict()

        tasks: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.tasks, Unset):
            tasks = self.tasks.to_dict()

        pid = self.pid

        cpu: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.cpu, Unset):
            cpu = self.cpu.to_dict()

        kill_request_user = self.kill_request_user

        state: Union[Unset, list[str]] = UNSET
        if not isinstance(self.state, Unset):
            state = []
            for state_item_data in self.state:
                state_item = state_item_data.value
                state.append(state_item)

        statistics: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.statistics, Unset):
            statistics = self.statistics.to_dict()

        step: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.step, Unset):
            step = self.step.to_dict()

        task: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.task, Unset):
            task = self.task.to_dict()

        tres: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.tres, Unset):
            tres = self.tres.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if time is not UNSET:
            field_dict["time"] = time
        if exit_code is not UNSET:
            field_dict["exit_code"] = exit_code
        if nodes is not UNSET:
            field_dict["nodes"] = nodes
        if tasks is not UNSET:
            field_dict["tasks"] = tasks
        if pid is not UNSET:
            field_dict["pid"] = pid
        if cpu is not UNSET:
            field_dict["CPU"] = cpu
        if kill_request_user is not UNSET:
            field_dict["kill_request_user"] = kill_request_user
        if state is not UNSET:
            field_dict["state"] = state
        if statistics is not UNSET:
            field_dict["statistics"] = statistics
        if step is not UNSET:
            field_dict["step"] = step
        if task is not UNSET:
            field_dict["task"] = task
        if tres is not UNSET:
            field_dict["tres"] = tres

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0040_process_exit_code_verbose import V0040ProcessExitCodeVerbose
        from ..models.v0040_step_cpu import V0040StepCPU
        from ..models.v0040_step_nodes import V0040StepNodes
        from ..models.v0040_step_statistics import V0040StepStatistics
        from ..models.v0040_step_step import V0040StepStep
        from ..models.v0040_step_task import V0040StepTask
        from ..models.v0040_step_tasks import V0040StepTasks
        from ..models.v0040_step_time import V0040StepTime
        from ..models.v0040_step_tres import V0040StepTres

        d = dict(src_dict)
        _time = d.pop("time", UNSET)
        time: Union[Unset, V0040StepTime]
        if isinstance(_time, Unset):
            time = UNSET
        else:
            time = V0040StepTime.from_dict(_time)

        _exit_code = d.pop("exit_code", UNSET)
        exit_code: Union[Unset, V0040ProcessExitCodeVerbose]
        if isinstance(_exit_code, Unset):
            exit_code = UNSET
        else:
            exit_code = V0040ProcessExitCodeVerbose.from_dict(_exit_code)

        _nodes = d.pop("nodes", UNSET)
        nodes: Union[Unset, V0040StepNodes]
        if isinstance(_nodes, Unset):
            nodes = UNSET
        else:
            nodes = V0040StepNodes.from_dict(_nodes)

        _tasks = d.pop("tasks", UNSET)
        tasks: Union[Unset, V0040StepTasks]
        if isinstance(_tasks, Unset):
            tasks = UNSET
        else:
            tasks = V0040StepTasks.from_dict(_tasks)

        pid = d.pop("pid", UNSET)

        _cpu = d.pop("CPU", UNSET)
        cpu: Union[Unset, V0040StepCPU]
        if isinstance(_cpu, Unset):
            cpu = UNSET
        else:
            cpu = V0040StepCPU.from_dict(_cpu)

        kill_request_user = d.pop("kill_request_user", UNSET)

        state = []
        _state = d.pop("state", UNSET)
        for state_item_data in _state or []:
            state_item = V0040StepStateItem(state_item_data)

            state.append(state_item)

        _statistics = d.pop("statistics", UNSET)
        statistics: Union[Unset, V0040StepStatistics]
        if isinstance(_statistics, Unset):
            statistics = UNSET
        else:
            statistics = V0040StepStatistics.from_dict(_statistics)

        _step = d.pop("step", UNSET)
        step: Union[Unset, V0040StepStep]
        if isinstance(_step, Unset):
            step = UNSET
        else:
            step = V0040StepStep.from_dict(_step)

        _task = d.pop("task", UNSET)
        task: Union[Unset, V0040StepTask]
        if isinstance(_task, Unset):
            task = UNSET
        else:
            task = V0040StepTask.from_dict(_task)

        _tres = d.pop("tres", UNSET)
        tres: Union[Unset, V0040StepTres]
        if isinstance(_tres, Unset):
            tres = UNSET
        else:
            tres = V0040StepTres.from_dict(_tres)

        v0040_step = cls(
            time=time,
            exit_code=exit_code,
            nodes=nodes,
            tasks=tasks,
            pid=pid,
            cpu=cpu,
            kill_request_user=kill_request_user,
            state=state,
            statistics=statistics,
            step=step,
            task=task,
            tres=tres,
        )

        v0040_step.additional_properties = d
        return v0040_step

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
