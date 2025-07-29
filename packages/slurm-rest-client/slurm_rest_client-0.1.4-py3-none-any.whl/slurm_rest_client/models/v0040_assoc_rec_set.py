from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_tres import V0040Tres


T = TypeVar("T", bound="V0040AssocRecSet")


@_attrs_define
class V0040AssocRecSet:
    """
    Attributes:
        comment (Union[Unset, str]): Comment for the association
        defaultqos (Union[Unset, str]): Which QOS id is this association default
        grpjobs (Union[Unset, int]):
        grpjobsaccrue (Union[Unset, int]):
        grpsubmitjobs (Union[Unset, int]):
        grptres (Union[Unset, list['V0040Tres']]):
        grptresmins (Union[Unset, list['V0040Tres']]):
        grptresrunmins (Union[Unset, list['V0040Tres']]):
        grpwall (Union[Unset, int]):
        maxjobs (Union[Unset, int]):
        maxjobsaccrue (Union[Unset, int]):
        maxsubmitjobs (Union[Unset, int]):
        maxtresminsperjob (Union[Unset, list['V0040Tres']]):
        maxtresrunmins (Union[Unset, list['V0040Tres']]):
        maxtresperjob (Union[Unset, list['V0040Tres']]):
        maxtrespernode (Union[Unset, list['V0040Tres']]):
        maxwalldurationperjob (Union[Unset, int]):
        minpriothresh (Union[Unset, int]):
        parent (Union[Unset, str]): Name of parent account
        priority (Union[Unset, int]):
        qoslevel (Union[Unset, list[str]]): List of QOS names
        fairshare (Union[Unset, int]): Number of shares allocated to this association
    """

    comment: Union[Unset, str] = UNSET
    defaultqos: Union[Unset, str] = UNSET
    grpjobs: Union[Unset, int] = UNSET
    grpjobsaccrue: Union[Unset, int] = UNSET
    grpsubmitjobs: Union[Unset, int] = UNSET
    grptres: Union[Unset, list["V0040Tres"]] = UNSET
    grptresmins: Union[Unset, list["V0040Tres"]] = UNSET
    grptresrunmins: Union[Unset, list["V0040Tres"]] = UNSET
    grpwall: Union[Unset, int] = UNSET
    maxjobs: Union[Unset, int] = UNSET
    maxjobsaccrue: Union[Unset, int] = UNSET
    maxsubmitjobs: Union[Unset, int] = UNSET
    maxtresminsperjob: Union[Unset, list["V0040Tres"]] = UNSET
    maxtresrunmins: Union[Unset, list["V0040Tres"]] = UNSET
    maxtresperjob: Union[Unset, list["V0040Tres"]] = UNSET
    maxtrespernode: Union[Unset, list["V0040Tres"]] = UNSET
    maxwalldurationperjob: Union[Unset, int] = UNSET
    minpriothresh: Union[Unset, int] = UNSET
    parent: Union[Unset, str] = UNSET
    priority: Union[Unset, int] = UNSET
    qoslevel: Union[Unset, list[str]] = UNSET
    fairshare: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        comment = self.comment

        defaultqos = self.defaultqos

        grpjobs = self.grpjobs

        grpjobsaccrue = self.grpjobsaccrue

        grpsubmitjobs = self.grpsubmitjobs

        grptres: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.grptres, Unset):
            grptres = []
            for componentsschemasv0_0_40_tres_list_item_data in self.grptres:
                componentsschemasv0_0_40_tres_list_item = componentsschemasv0_0_40_tres_list_item_data.to_dict()
                grptres.append(componentsschemasv0_0_40_tres_list_item)

        grptresmins: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.grptresmins, Unset):
            grptresmins = []
            for componentsschemasv0_0_40_tres_list_item_data in self.grptresmins:
                componentsschemasv0_0_40_tres_list_item = componentsschemasv0_0_40_tres_list_item_data.to_dict()
                grptresmins.append(componentsschemasv0_0_40_tres_list_item)

        grptresrunmins: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.grptresrunmins, Unset):
            grptresrunmins = []
            for componentsschemasv0_0_40_tres_list_item_data in self.grptresrunmins:
                componentsschemasv0_0_40_tres_list_item = componentsschemasv0_0_40_tres_list_item_data.to_dict()
                grptresrunmins.append(componentsschemasv0_0_40_tres_list_item)

        grpwall = self.grpwall

        maxjobs = self.maxjobs

        maxjobsaccrue = self.maxjobsaccrue

        maxsubmitjobs = self.maxsubmitjobs

        maxtresminsperjob: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.maxtresminsperjob, Unset):
            maxtresminsperjob = []
            for componentsschemasv0_0_40_tres_list_item_data in self.maxtresminsperjob:
                componentsschemasv0_0_40_tres_list_item = componentsschemasv0_0_40_tres_list_item_data.to_dict()
                maxtresminsperjob.append(componentsschemasv0_0_40_tres_list_item)

        maxtresrunmins: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.maxtresrunmins, Unset):
            maxtresrunmins = []
            for componentsschemasv0_0_40_tres_list_item_data in self.maxtresrunmins:
                componentsschemasv0_0_40_tres_list_item = componentsschemasv0_0_40_tres_list_item_data.to_dict()
                maxtresrunmins.append(componentsschemasv0_0_40_tres_list_item)

        maxtresperjob: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.maxtresperjob, Unset):
            maxtresperjob = []
            for componentsschemasv0_0_40_tres_list_item_data in self.maxtresperjob:
                componentsschemasv0_0_40_tres_list_item = componentsschemasv0_0_40_tres_list_item_data.to_dict()
                maxtresperjob.append(componentsschemasv0_0_40_tres_list_item)

        maxtrespernode: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.maxtrespernode, Unset):
            maxtrespernode = []
            for componentsschemasv0_0_40_tres_list_item_data in self.maxtrespernode:
                componentsschemasv0_0_40_tres_list_item = componentsschemasv0_0_40_tres_list_item_data.to_dict()
                maxtrespernode.append(componentsschemasv0_0_40_tres_list_item)

        maxwalldurationperjob = self.maxwalldurationperjob

        minpriothresh = self.minpriothresh

        parent = self.parent

        priority = self.priority

        qoslevel: Union[Unset, list[str]] = UNSET
        if not isinstance(self.qoslevel, Unset):
            qoslevel = self.qoslevel

        fairshare = self.fairshare

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if comment is not UNSET:
            field_dict["comment"] = comment
        if defaultqos is not UNSET:
            field_dict["defaultqos"] = defaultqos
        if grpjobs is not UNSET:
            field_dict["grpjobs"] = grpjobs
        if grpjobsaccrue is not UNSET:
            field_dict["grpjobsaccrue"] = grpjobsaccrue
        if grpsubmitjobs is not UNSET:
            field_dict["grpsubmitjobs"] = grpsubmitjobs
        if grptres is not UNSET:
            field_dict["grptres"] = grptres
        if grptresmins is not UNSET:
            field_dict["grptresmins"] = grptresmins
        if grptresrunmins is not UNSET:
            field_dict["grptresrunmins"] = grptresrunmins
        if grpwall is not UNSET:
            field_dict["grpwall"] = grpwall
        if maxjobs is not UNSET:
            field_dict["maxjobs"] = maxjobs
        if maxjobsaccrue is not UNSET:
            field_dict["maxjobsaccrue"] = maxjobsaccrue
        if maxsubmitjobs is not UNSET:
            field_dict["maxsubmitjobs"] = maxsubmitjobs
        if maxtresminsperjob is not UNSET:
            field_dict["maxtresminsperjob"] = maxtresminsperjob
        if maxtresrunmins is not UNSET:
            field_dict["maxtresrunmins"] = maxtresrunmins
        if maxtresperjob is not UNSET:
            field_dict["maxtresperjob"] = maxtresperjob
        if maxtrespernode is not UNSET:
            field_dict["maxtrespernode"] = maxtrespernode
        if maxwalldurationperjob is not UNSET:
            field_dict["maxwalldurationperjob"] = maxwalldurationperjob
        if minpriothresh is not UNSET:
            field_dict["minpriothresh"] = minpriothresh
        if parent is not UNSET:
            field_dict["parent"] = parent
        if priority is not UNSET:
            field_dict["priority"] = priority
        if qoslevel is not UNSET:
            field_dict["qoslevel"] = qoslevel
        if fairshare is not UNSET:
            field_dict["fairshare"] = fairshare

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0040_tres import V0040Tres

        d = dict(src_dict)
        comment = d.pop("comment", UNSET)

        defaultqos = d.pop("defaultqos", UNSET)

        grpjobs = d.pop("grpjobs", UNSET)

        grpjobsaccrue = d.pop("grpjobsaccrue", UNSET)

        grpsubmitjobs = d.pop("grpsubmitjobs", UNSET)

        grptres = []
        _grptres = d.pop("grptres", UNSET)
        for componentsschemasv0_0_40_tres_list_item_data in _grptres or []:
            componentsschemasv0_0_40_tres_list_item = V0040Tres.from_dict(componentsschemasv0_0_40_tres_list_item_data)

            grptres.append(componentsschemasv0_0_40_tres_list_item)

        grptresmins = []
        _grptresmins = d.pop("grptresmins", UNSET)
        for componentsschemasv0_0_40_tres_list_item_data in _grptresmins or []:
            componentsschemasv0_0_40_tres_list_item = V0040Tres.from_dict(componentsschemasv0_0_40_tres_list_item_data)

            grptresmins.append(componentsschemasv0_0_40_tres_list_item)

        grptresrunmins = []
        _grptresrunmins = d.pop("grptresrunmins", UNSET)
        for componentsschemasv0_0_40_tres_list_item_data in _grptresrunmins or []:
            componentsschemasv0_0_40_tres_list_item = V0040Tres.from_dict(componentsschemasv0_0_40_tres_list_item_data)

            grptresrunmins.append(componentsschemasv0_0_40_tres_list_item)

        grpwall = d.pop("grpwall", UNSET)

        maxjobs = d.pop("maxjobs", UNSET)

        maxjobsaccrue = d.pop("maxjobsaccrue", UNSET)

        maxsubmitjobs = d.pop("maxsubmitjobs", UNSET)

        maxtresminsperjob = []
        _maxtresminsperjob = d.pop("maxtresminsperjob", UNSET)
        for componentsschemasv0_0_40_tres_list_item_data in _maxtresminsperjob or []:
            componentsschemasv0_0_40_tres_list_item = V0040Tres.from_dict(componentsschemasv0_0_40_tres_list_item_data)

            maxtresminsperjob.append(componentsschemasv0_0_40_tres_list_item)

        maxtresrunmins = []
        _maxtresrunmins = d.pop("maxtresrunmins", UNSET)
        for componentsschemasv0_0_40_tres_list_item_data in _maxtresrunmins or []:
            componentsschemasv0_0_40_tres_list_item = V0040Tres.from_dict(componentsschemasv0_0_40_tres_list_item_data)

            maxtresrunmins.append(componentsschemasv0_0_40_tres_list_item)

        maxtresperjob = []
        _maxtresperjob = d.pop("maxtresperjob", UNSET)
        for componentsschemasv0_0_40_tres_list_item_data in _maxtresperjob or []:
            componentsschemasv0_0_40_tres_list_item = V0040Tres.from_dict(componentsschemasv0_0_40_tres_list_item_data)

            maxtresperjob.append(componentsschemasv0_0_40_tres_list_item)

        maxtrespernode = []
        _maxtrespernode = d.pop("maxtrespernode", UNSET)
        for componentsschemasv0_0_40_tres_list_item_data in _maxtrespernode or []:
            componentsschemasv0_0_40_tres_list_item = V0040Tres.from_dict(componentsschemasv0_0_40_tres_list_item_data)

            maxtrespernode.append(componentsschemasv0_0_40_tres_list_item)

        maxwalldurationperjob = d.pop("maxwalldurationperjob", UNSET)

        minpriothresh = d.pop("minpriothresh", UNSET)

        parent = d.pop("parent", UNSET)

        priority = d.pop("priority", UNSET)

        qoslevel = cast(list[str], d.pop("qoslevel", UNSET))

        fairshare = d.pop("fairshare", UNSET)

        v0040_assoc_rec_set = cls(
            comment=comment,
            defaultqos=defaultqos,
            grpjobs=grpjobs,
            grpjobsaccrue=grpjobsaccrue,
            grpsubmitjobs=grpsubmitjobs,
            grptres=grptres,
            grptresmins=grptresmins,
            grptresrunmins=grptresrunmins,
            grpwall=grpwall,
            maxjobs=maxjobs,
            maxjobsaccrue=maxjobsaccrue,
            maxsubmitjobs=maxsubmitjobs,
            maxtresminsperjob=maxtresminsperjob,
            maxtresrunmins=maxtresrunmins,
            maxtresperjob=maxtresperjob,
            maxtrespernode=maxtrespernode,
            maxwalldurationperjob=maxwalldurationperjob,
            minpriothresh=minpriothresh,
            parent=parent,
            priority=priority,
            qoslevel=qoslevel,
            fairshare=fairshare,
        )

        v0040_assoc_rec_set.additional_properties = d
        return v0040_assoc_rec_set

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
