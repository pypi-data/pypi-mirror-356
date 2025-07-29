from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_step_time_end import V0040StepTimeEnd
    from ..models.v0040_step_time_start import V0040StepTimeStart
    from ..models.v0040_step_time_system import V0040StepTimeSystem
    from ..models.v0040_step_time_total import V0040StepTimeTotal
    from ..models.v0040_step_time_user import V0040StepTimeUser


T = TypeVar("T", bound="V0040StepTime")


@_attrs_define
class V0040StepTime:
    """
    Attributes:
        elapsed (Union[Unset, int]):
        end (Union[Unset, V0040StepTimeEnd]):
        start (Union[Unset, V0040StepTimeStart]):
        suspended (Union[Unset, int]):
        system (Union[Unset, V0040StepTimeSystem]):
        total (Union[Unset, V0040StepTimeTotal]):
        user (Union[Unset, V0040StepTimeUser]):
    """

    elapsed: Union[Unset, int] = UNSET
    end: Union[Unset, "V0040StepTimeEnd"] = UNSET
    start: Union[Unset, "V0040StepTimeStart"] = UNSET
    suspended: Union[Unset, int] = UNSET
    system: Union[Unset, "V0040StepTimeSystem"] = UNSET
    total: Union[Unset, "V0040StepTimeTotal"] = UNSET
    user: Union[Unset, "V0040StepTimeUser"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        elapsed = self.elapsed

        end: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.end, Unset):
            end = self.end.to_dict()

        start: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.start, Unset):
            start = self.start.to_dict()

        suspended = self.suspended

        system: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.system, Unset):
            system = self.system.to_dict()

        total: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.total, Unset):
            total = self.total.to_dict()

        user: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.user, Unset):
            user = self.user.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if elapsed is not UNSET:
            field_dict["elapsed"] = elapsed
        if end is not UNSET:
            field_dict["end"] = end
        if start is not UNSET:
            field_dict["start"] = start
        if suspended is not UNSET:
            field_dict["suspended"] = suspended
        if system is not UNSET:
            field_dict["system"] = system
        if total is not UNSET:
            field_dict["total"] = total
        if user is not UNSET:
            field_dict["user"] = user

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0040_step_time_end import V0040StepTimeEnd
        from ..models.v0040_step_time_start import V0040StepTimeStart
        from ..models.v0040_step_time_system import V0040StepTimeSystem
        from ..models.v0040_step_time_total import V0040StepTimeTotal
        from ..models.v0040_step_time_user import V0040StepTimeUser

        d = dict(src_dict)
        elapsed = d.pop("elapsed", UNSET)

        _end = d.pop("end", UNSET)
        end: Union[Unset, V0040StepTimeEnd]
        if isinstance(_end, Unset):
            end = UNSET
        else:
            end = V0040StepTimeEnd.from_dict(_end)

        _start = d.pop("start", UNSET)
        start: Union[Unset, V0040StepTimeStart]
        if isinstance(_start, Unset):
            start = UNSET
        else:
            start = V0040StepTimeStart.from_dict(_start)

        suspended = d.pop("suspended", UNSET)

        _system = d.pop("system", UNSET)
        system: Union[Unset, V0040StepTimeSystem]
        if isinstance(_system, Unset):
            system = UNSET
        else:
            system = V0040StepTimeSystem.from_dict(_system)

        _total = d.pop("total", UNSET)
        total: Union[Unset, V0040StepTimeTotal]
        if isinstance(_total, Unset):
            total = UNSET
        else:
            total = V0040StepTimeTotal.from_dict(_total)

        _user = d.pop("user", UNSET)
        user: Union[Unset, V0040StepTimeUser]
        if isinstance(_user, Unset):
            user = UNSET
        else:
            user = V0040StepTimeUser.from_dict(_user)

        v0040_step_time = cls(
            elapsed=elapsed,
            end=end,
            start=start,
            suspended=suspended,
            system=system,
            total=total,
            user=user,
        )

        v0040_step_time.additional_properties = d
        return v0040_step_time

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
