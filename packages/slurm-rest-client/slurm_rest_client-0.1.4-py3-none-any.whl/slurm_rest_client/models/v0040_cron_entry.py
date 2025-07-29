from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.v0040_cron_entry_flags_item import V0040CronEntryFlagsItem
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_cron_entry_line import V0040CronEntryLine


T = TypeVar("T", bound="V0040CronEntry")


@_attrs_define
class V0040CronEntry:
    """
    Attributes:
        flags (Union[Unset, list[V0040CronEntryFlagsItem]]):
        minute (Union[Unset, str]):
        hour (Union[Unset, str]):
        day_of_month (Union[Unset, str]):
        month (Union[Unset, str]):
        day_of_week (Union[Unset, str]):
        specification (Union[Unset, str]):
        command (Union[Unset, str]):
        line (Union[Unset, V0040CronEntryLine]):
    """

    flags: Union[Unset, list[V0040CronEntryFlagsItem]] = UNSET
    minute: Union[Unset, str] = UNSET
    hour: Union[Unset, str] = UNSET
    day_of_month: Union[Unset, str] = UNSET
    month: Union[Unset, str] = UNSET
    day_of_week: Union[Unset, str] = UNSET
    specification: Union[Unset, str] = UNSET
    command: Union[Unset, str] = UNSET
    line: Union[Unset, "V0040CronEntryLine"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        flags: Union[Unset, list[str]] = UNSET
        if not isinstance(self.flags, Unset):
            flags = []
            for flags_item_data in self.flags:
                flags_item = flags_item_data.value
                flags.append(flags_item)

        minute = self.minute

        hour = self.hour

        day_of_month = self.day_of_month

        month = self.month

        day_of_week = self.day_of_week

        specification = self.specification

        command = self.command

        line: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.line, Unset):
            line = self.line.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if flags is not UNSET:
            field_dict["flags"] = flags
        if minute is not UNSET:
            field_dict["minute"] = minute
        if hour is not UNSET:
            field_dict["hour"] = hour
        if day_of_month is not UNSET:
            field_dict["day_of_month"] = day_of_month
        if month is not UNSET:
            field_dict["month"] = month
        if day_of_week is not UNSET:
            field_dict["day_of_week"] = day_of_week
        if specification is not UNSET:
            field_dict["specification"] = specification
        if command is not UNSET:
            field_dict["command"] = command
        if line is not UNSET:
            field_dict["line"] = line

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0040_cron_entry_line import V0040CronEntryLine

        d = dict(src_dict)
        flags = []
        _flags = d.pop("flags", UNSET)
        for flags_item_data in _flags or []:
            flags_item = V0040CronEntryFlagsItem(flags_item_data)

            flags.append(flags_item)

        minute = d.pop("minute", UNSET)

        hour = d.pop("hour", UNSET)

        day_of_month = d.pop("day_of_month", UNSET)

        month = d.pop("month", UNSET)

        day_of_week = d.pop("day_of_week", UNSET)

        specification = d.pop("specification", UNSET)

        command = d.pop("command", UNSET)

        _line = d.pop("line", UNSET)
        line: Union[Unset, V0040CronEntryLine]
        if isinstance(_line, Unset):
            line = UNSET
        else:
            line = V0040CronEntryLine.from_dict(_line)

        v0040_cron_entry = cls(
            flags=flags,
            minute=minute,
            hour=hour,
            day_of_month=day_of_month,
            month=month,
            day_of_week=day_of_week,
            specification=specification,
            command=command,
            line=line,
        )

        v0040_cron_entry.additional_properties = d
        return v0040_cron_entry

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
