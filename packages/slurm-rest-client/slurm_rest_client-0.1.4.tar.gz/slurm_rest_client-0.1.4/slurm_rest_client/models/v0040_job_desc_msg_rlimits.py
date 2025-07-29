from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="V0040JobDescMsgRlimits")


@_attrs_define
class V0040JobDescMsgRlimits:
    """
    Attributes:
        cpu (Union[Unset, int]):
        fsize (Union[Unset, int]):
        data (Union[Unset, int]):
        stack (Union[Unset, int]):
        core (Union[Unset, int]):
        rss (Union[Unset, int]):
        nproc (Union[Unset, int]):
        nofile (Union[Unset, int]):
        memlock (Union[Unset, int]):
        as_ (Union[Unset, int]):
    """

    cpu: Union[Unset, int] = UNSET
    fsize: Union[Unset, int] = UNSET
    data: Union[Unset, int] = UNSET
    stack: Union[Unset, int] = UNSET
    core: Union[Unset, int] = UNSET
    rss: Union[Unset, int] = UNSET
    nproc: Union[Unset, int] = UNSET
    nofile: Union[Unset, int] = UNSET
    memlock: Union[Unset, int] = UNSET
    as_: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cpu = self.cpu

        fsize = self.fsize

        data = self.data

        stack = self.stack

        core = self.core

        rss = self.rss

        nproc = self.nproc

        nofile = self.nofile

        memlock = self.memlock

        as_ = self.as_

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
        d = dict(src_dict)
        cpu = d.pop("cpu", UNSET)

        fsize = d.pop("fsize", UNSET)

        data = d.pop("data", UNSET)

        stack = d.pop("stack", UNSET)

        core = d.pop("core", UNSET)

        rss = d.pop("rss", UNSET)

        nproc = d.pop("nproc", UNSET)

        nofile = d.pop("nofile", UNSET)

        memlock = d.pop("memlock", UNSET)

        as_ = d.pop("as", UNSET)

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
