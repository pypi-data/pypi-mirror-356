from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_job_desc_msg_rlimits_as import V0040JobDescMsgRlimitsAs
    from ..models.v0040_job_desc_msg_rlimits_core import V0040JobDescMsgRlimitsCore
    from ..models.v0040_job_desc_msg_rlimits_cpu import V0040JobDescMsgRlimitsCpu
    from ..models.v0040_job_desc_msg_rlimits_data import V0040JobDescMsgRlimitsData
    from ..models.v0040_job_desc_msg_rlimits_fsize import V0040JobDescMsgRlimitsFsize
    from ..models.v0040_job_desc_msg_rlimits_memlock import V0040JobDescMsgRlimitsMemlock
    from ..models.v0040_job_desc_msg_rlimits_nofile import V0040JobDescMsgRlimitsNofile
    from ..models.v0040_job_desc_msg_rlimits_nproc import V0040JobDescMsgRlimitsNproc
    from ..models.v0040_job_desc_msg_rlimits_rss import V0040JobDescMsgRlimitsRss
    from ..models.v0040_job_desc_msg_rlimits_stack import V0040JobDescMsgRlimitsStack


T = TypeVar("T", bound="V0040JobDescMsgRlimits")


@_attrs_define
class V0040JobDescMsgRlimits:
    """
    Attributes:
        cpu (Union[Unset, V0040JobDescMsgRlimitsCpu]):
        fsize (Union[Unset, V0040JobDescMsgRlimitsFsize]):
        data (Union[Unset, V0040JobDescMsgRlimitsData]):
        stack (Union[Unset, V0040JobDescMsgRlimitsStack]):
        core (Union[Unset, V0040JobDescMsgRlimitsCore]):
        rss (Union[Unset, V0040JobDescMsgRlimitsRss]):
        nproc (Union[Unset, V0040JobDescMsgRlimitsNproc]):
        nofile (Union[Unset, V0040JobDescMsgRlimitsNofile]):
        memlock (Union[Unset, V0040JobDescMsgRlimitsMemlock]):
        as_ (Union[Unset, V0040JobDescMsgRlimitsAs]):
    """

    cpu: Union[Unset, "V0040JobDescMsgRlimitsCpu"] = UNSET
    fsize: Union[Unset, "V0040JobDescMsgRlimitsFsize"] = UNSET
    data: Union[Unset, "V0040JobDescMsgRlimitsData"] = UNSET
    stack: Union[Unset, "V0040JobDescMsgRlimitsStack"] = UNSET
    core: Union[Unset, "V0040JobDescMsgRlimitsCore"] = UNSET
    rss: Union[Unset, "V0040JobDescMsgRlimitsRss"] = UNSET
    nproc: Union[Unset, "V0040JobDescMsgRlimitsNproc"] = UNSET
    nofile: Union[Unset, "V0040JobDescMsgRlimitsNofile"] = UNSET
    memlock: Union[Unset, "V0040JobDescMsgRlimitsMemlock"] = UNSET
    as_: Union[Unset, "V0040JobDescMsgRlimitsAs"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cpu: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.cpu, Unset):
            cpu = self.cpu.to_dict()

        fsize: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.fsize, Unset):
            fsize = self.fsize.to_dict()

        data: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.data, Unset):
            data = self.data.to_dict()

        stack: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.stack, Unset):
            stack = self.stack.to_dict()

        core: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.core, Unset):
            core = self.core.to_dict()

        rss: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.rss, Unset):
            rss = self.rss.to_dict()

        nproc: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.nproc, Unset):
            nproc = self.nproc.to_dict()

        nofile: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.nofile, Unset):
            nofile = self.nofile.to_dict()

        memlock: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.memlock, Unset):
            memlock = self.memlock.to_dict()

        as_: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.as_, Unset):
            as_ = self.as_.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if cpu is not UNSET:
            field_dict["cpu"] = cpu
        if fsize is not UNSET:
            field_dict["fsize"] = fsize
        if data is not UNSET:
            field_dict["data"] = data
        if stack is not UNSET:
            field_dict["stack"] = stack
        if core is not UNSET:
            field_dict["core"] = core
        if rss is not UNSET:
            field_dict["rss"] = rss
        if nproc is not UNSET:
            field_dict["nproc"] = nproc
        if nofile is not UNSET:
            field_dict["nofile"] = nofile
        if memlock is not UNSET:
            field_dict["memlock"] = memlock
        if as_ is not UNSET:
            field_dict["as"] = as_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0040_job_desc_msg_rlimits_as import V0040JobDescMsgRlimitsAs
        from ..models.v0040_job_desc_msg_rlimits_core import V0040JobDescMsgRlimitsCore
        from ..models.v0040_job_desc_msg_rlimits_cpu import V0040JobDescMsgRlimitsCpu
        from ..models.v0040_job_desc_msg_rlimits_data import V0040JobDescMsgRlimitsData
        from ..models.v0040_job_desc_msg_rlimits_fsize import V0040JobDescMsgRlimitsFsize
        from ..models.v0040_job_desc_msg_rlimits_memlock import V0040JobDescMsgRlimitsMemlock
        from ..models.v0040_job_desc_msg_rlimits_nofile import V0040JobDescMsgRlimitsNofile
        from ..models.v0040_job_desc_msg_rlimits_nproc import V0040JobDescMsgRlimitsNproc
        from ..models.v0040_job_desc_msg_rlimits_rss import V0040JobDescMsgRlimitsRss
        from ..models.v0040_job_desc_msg_rlimits_stack import V0040JobDescMsgRlimitsStack

        d = dict(src_dict)
        _cpu = d.pop("cpu", UNSET)
        cpu: Union[Unset, V0040JobDescMsgRlimitsCpu]
        if isinstance(_cpu, Unset):
            cpu = UNSET
        else:
            cpu = V0040JobDescMsgRlimitsCpu.from_dict(_cpu)

        _fsize = d.pop("fsize", UNSET)
        fsize: Union[Unset, V0040JobDescMsgRlimitsFsize]
        if isinstance(_fsize, Unset):
            fsize = UNSET
        else:
            fsize = V0040JobDescMsgRlimitsFsize.from_dict(_fsize)

        _data = d.pop("data", UNSET)
        data: Union[Unset, V0040JobDescMsgRlimitsData]
        if isinstance(_data, Unset):
            data = UNSET
        else:
            data = V0040JobDescMsgRlimitsData.from_dict(_data)

        _stack = d.pop("stack", UNSET)
        stack: Union[Unset, V0040JobDescMsgRlimitsStack]
        if isinstance(_stack, Unset):
            stack = UNSET
        else:
            stack = V0040JobDescMsgRlimitsStack.from_dict(_stack)

        _core = d.pop("core", UNSET)
        core: Union[Unset, V0040JobDescMsgRlimitsCore]
        if isinstance(_core, Unset):
            core = UNSET
        else:
            core = V0040JobDescMsgRlimitsCore.from_dict(_core)

        _rss = d.pop("rss", UNSET)
        rss: Union[Unset, V0040JobDescMsgRlimitsRss]
        if isinstance(_rss, Unset):
            rss = UNSET
        else:
            rss = V0040JobDescMsgRlimitsRss.from_dict(_rss)

        _nproc = d.pop("nproc", UNSET)
        nproc: Union[Unset, V0040JobDescMsgRlimitsNproc]
        if isinstance(_nproc, Unset):
            nproc = UNSET
        else:
            nproc = V0040JobDescMsgRlimitsNproc.from_dict(_nproc)

        _nofile = d.pop("nofile", UNSET)
        nofile: Union[Unset, V0040JobDescMsgRlimitsNofile]
        if isinstance(_nofile, Unset):
            nofile = UNSET
        else:
            nofile = V0040JobDescMsgRlimitsNofile.from_dict(_nofile)

        _memlock = d.pop("memlock", UNSET)
        memlock: Union[Unset, V0040JobDescMsgRlimitsMemlock]
        if isinstance(_memlock, Unset):
            memlock = UNSET
        else:
            memlock = V0040JobDescMsgRlimitsMemlock.from_dict(_memlock)

        _as_ = d.pop("as", UNSET)
        as_: Union[Unset, V0040JobDescMsgRlimitsAs]
        if isinstance(_as_, Unset):
            as_ = UNSET
        else:
            as_ = V0040JobDescMsgRlimitsAs.from_dict(_as_)

        v0040_job_desc_msg_rlimits = cls(
            cpu=cpu,
            fsize=fsize,
            data=data,
            stack=stack,
            core=core,
            rss=rss,
            nproc=nproc,
            nofile=nofile,
            memlock=memlock,
            as_=as_,
        )

        v0040_job_desc_msg_rlimits.additional_properties = d
        return v0040_job_desc_msg_rlimits

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
