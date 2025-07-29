from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0040_assoc_rec_set_grpjobs import V0040AssocRecSetGrpjobs
    from ..models.v0040_assoc_rec_set_grpjobsaccrue import V0040AssocRecSetGrpjobsaccrue
    from ..models.v0040_assoc_rec_set_grpsubmitjobs import V0040AssocRecSetGrpsubmitjobs
    from ..models.v0040_assoc_rec_set_grptres import V0040AssocRecSetGrptres
    from ..models.v0040_assoc_rec_set_grptresmins import V0040AssocRecSetGrptresmins
    from ..models.v0040_assoc_rec_set_grptresrunmins import V0040AssocRecSetGrptresrunmins
    from ..models.v0040_assoc_rec_set_grpwall import V0040AssocRecSetGrpwall
    from ..models.v0040_assoc_rec_set_maxjobs import V0040AssocRecSetMaxjobs
    from ..models.v0040_assoc_rec_set_maxjobsaccrue import V0040AssocRecSetMaxjobsaccrue
    from ..models.v0040_assoc_rec_set_maxsubmitjobs import V0040AssocRecSetMaxsubmitjobs
    from ..models.v0040_assoc_rec_set_maxtresminsperjob import V0040AssocRecSetMaxtresminsperjob
    from ..models.v0040_assoc_rec_set_maxtresperjob import V0040AssocRecSetMaxtresperjob
    from ..models.v0040_assoc_rec_set_maxtrespernode import V0040AssocRecSetMaxtrespernode
    from ..models.v0040_assoc_rec_set_maxtresrunmins import V0040AssocRecSetMaxtresrunmins
    from ..models.v0040_assoc_rec_set_maxwalldurationperjob import V0040AssocRecSetMaxwalldurationperjob
    from ..models.v0040_assoc_rec_set_minpriothresh import V0040AssocRecSetMinpriothresh
    from ..models.v0040_assoc_rec_set_priority import V0040AssocRecSetPriority
    from ..models.v0040_assoc_rec_set_qoslevel import V0040AssocRecSetQoslevel


T = TypeVar("T", bound="V0040AssocRecSet")


@_attrs_define
class V0040AssocRecSet:
    """
    Attributes:
        comment (Union[Unset, str]): Comment for the association
        defaultqos (Union[Unset, str]): Which QOS id is this association default
        grpjobs (Union[Unset, V0040AssocRecSetGrpjobs]):
        grpjobsaccrue (Union[Unset, V0040AssocRecSetGrpjobsaccrue]):
        grpsubmitjobs (Union[Unset, V0040AssocRecSetGrpsubmitjobs]):
        grptres (Union[Unset, V0040AssocRecSetGrptres]):
        grptresmins (Union[Unset, V0040AssocRecSetGrptresmins]):
        grptresrunmins (Union[Unset, V0040AssocRecSetGrptresrunmins]):
        grpwall (Union[Unset, V0040AssocRecSetGrpwall]):
        maxjobs (Union[Unset, V0040AssocRecSetMaxjobs]):
        maxjobsaccrue (Union[Unset, V0040AssocRecSetMaxjobsaccrue]):
        maxsubmitjobs (Union[Unset, V0040AssocRecSetMaxsubmitjobs]):
        maxtresminsperjob (Union[Unset, V0040AssocRecSetMaxtresminsperjob]):
        maxtresrunmins (Union[Unset, V0040AssocRecSetMaxtresrunmins]):
        maxtresperjob (Union[Unset, V0040AssocRecSetMaxtresperjob]):
        maxtrespernode (Union[Unset, V0040AssocRecSetMaxtrespernode]):
        maxwalldurationperjob (Union[Unset, V0040AssocRecSetMaxwalldurationperjob]):
        minpriothresh (Union[Unset, V0040AssocRecSetMinpriothresh]):
        parent (Union[Unset, str]): Name of parent account
        priority (Union[Unset, V0040AssocRecSetPriority]):
        qoslevel (Union[Unset, V0040AssocRecSetQoslevel]):
        fairshare (Union[Unset, int]): Number of shares allocated to this association
    """

    comment: Union[Unset, str] = UNSET
    defaultqos: Union[Unset, str] = UNSET
    grpjobs: Union[Unset, "V0040AssocRecSetGrpjobs"] = UNSET
    grpjobsaccrue: Union[Unset, "V0040AssocRecSetGrpjobsaccrue"] = UNSET
    grpsubmitjobs: Union[Unset, "V0040AssocRecSetGrpsubmitjobs"] = UNSET
    grptres: Union[Unset, "V0040AssocRecSetGrptres"] = UNSET
    grptresmins: Union[Unset, "V0040AssocRecSetGrptresmins"] = UNSET
    grptresrunmins: Union[Unset, "V0040AssocRecSetGrptresrunmins"] = UNSET
    grpwall: Union[Unset, "V0040AssocRecSetGrpwall"] = UNSET
    maxjobs: Union[Unset, "V0040AssocRecSetMaxjobs"] = UNSET
    maxjobsaccrue: Union[Unset, "V0040AssocRecSetMaxjobsaccrue"] = UNSET
    maxsubmitjobs: Union[Unset, "V0040AssocRecSetMaxsubmitjobs"] = UNSET
    maxtresminsperjob: Union[Unset, "V0040AssocRecSetMaxtresminsperjob"] = UNSET
    maxtresrunmins: Union[Unset, "V0040AssocRecSetMaxtresrunmins"] = UNSET
    maxtresperjob: Union[Unset, "V0040AssocRecSetMaxtresperjob"] = UNSET
    maxtrespernode: Union[Unset, "V0040AssocRecSetMaxtrespernode"] = UNSET
    maxwalldurationperjob: Union[Unset, "V0040AssocRecSetMaxwalldurationperjob"] = UNSET
    minpriothresh: Union[Unset, "V0040AssocRecSetMinpriothresh"] = UNSET
    parent: Union[Unset, str] = UNSET
    priority: Union[Unset, "V0040AssocRecSetPriority"] = UNSET
    qoslevel: Union[Unset, "V0040AssocRecSetQoslevel"] = UNSET
    fairshare: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        comment = self.comment

        defaultqos = self.defaultqos

        grpjobs: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.grpjobs, Unset):
            grpjobs = self.grpjobs.to_dict()

        grpjobsaccrue: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.grpjobsaccrue, Unset):
            grpjobsaccrue = self.grpjobsaccrue.to_dict()

        grpsubmitjobs: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.grpsubmitjobs, Unset):
            grpsubmitjobs = self.grpsubmitjobs.to_dict()

        grptres: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.grptres, Unset):
            grptres = self.grptres.to_dict()

        grptresmins: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.grptresmins, Unset):
            grptresmins = self.grptresmins.to_dict()

        grptresrunmins: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.grptresrunmins, Unset):
            grptresrunmins = self.grptresrunmins.to_dict()

        grpwall: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.grpwall, Unset):
            grpwall = self.grpwall.to_dict()

        maxjobs: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.maxjobs, Unset):
            maxjobs = self.maxjobs.to_dict()

        maxjobsaccrue: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.maxjobsaccrue, Unset):
            maxjobsaccrue = self.maxjobsaccrue.to_dict()

        maxsubmitjobs: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.maxsubmitjobs, Unset):
            maxsubmitjobs = self.maxsubmitjobs.to_dict()

        maxtresminsperjob: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.maxtresminsperjob, Unset):
            maxtresminsperjob = self.maxtresminsperjob.to_dict()

        maxtresrunmins: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.maxtresrunmins, Unset):
            maxtresrunmins = self.maxtresrunmins.to_dict()

        maxtresperjob: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.maxtresperjob, Unset):
            maxtresperjob = self.maxtresperjob.to_dict()

        maxtrespernode: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.maxtrespernode, Unset):
            maxtrespernode = self.maxtrespernode.to_dict()

        maxwalldurationperjob: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.maxwalldurationperjob, Unset):
            maxwalldurationperjob = self.maxwalldurationperjob.to_dict()

        minpriothresh: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.minpriothresh, Unset):
            minpriothresh = self.minpriothresh.to_dict()

        parent = self.parent

        priority: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.priority, Unset):
            priority = self.priority.to_dict()

        qoslevel: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.qoslevel, Unset):
            qoslevel = self.qoslevel.to_dict()

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
        from ..models.v0040_assoc_rec_set_grpjobs import V0040AssocRecSetGrpjobs
        from ..models.v0040_assoc_rec_set_grpjobsaccrue import V0040AssocRecSetGrpjobsaccrue
        from ..models.v0040_assoc_rec_set_grpsubmitjobs import V0040AssocRecSetGrpsubmitjobs
        from ..models.v0040_assoc_rec_set_grptres import V0040AssocRecSetGrptres
        from ..models.v0040_assoc_rec_set_grptresmins import V0040AssocRecSetGrptresmins
        from ..models.v0040_assoc_rec_set_grptresrunmins import V0040AssocRecSetGrptresrunmins
        from ..models.v0040_assoc_rec_set_grpwall import V0040AssocRecSetGrpwall
        from ..models.v0040_assoc_rec_set_maxjobs import V0040AssocRecSetMaxjobs
        from ..models.v0040_assoc_rec_set_maxjobsaccrue import V0040AssocRecSetMaxjobsaccrue
        from ..models.v0040_assoc_rec_set_maxsubmitjobs import V0040AssocRecSetMaxsubmitjobs
        from ..models.v0040_assoc_rec_set_maxtresminsperjob import V0040AssocRecSetMaxtresminsperjob
        from ..models.v0040_assoc_rec_set_maxtresperjob import V0040AssocRecSetMaxtresperjob
        from ..models.v0040_assoc_rec_set_maxtrespernode import V0040AssocRecSetMaxtrespernode
        from ..models.v0040_assoc_rec_set_maxtresrunmins import V0040AssocRecSetMaxtresrunmins
        from ..models.v0040_assoc_rec_set_maxwalldurationperjob import V0040AssocRecSetMaxwalldurationperjob
        from ..models.v0040_assoc_rec_set_minpriothresh import V0040AssocRecSetMinpriothresh
        from ..models.v0040_assoc_rec_set_priority import V0040AssocRecSetPriority
        from ..models.v0040_assoc_rec_set_qoslevel import V0040AssocRecSetQoslevel

        d = dict(src_dict)
        comment = d.pop("comment", UNSET)

        defaultqos = d.pop("defaultqos", UNSET)

        _grpjobs = d.pop("grpjobs", UNSET)
        grpjobs: Union[Unset, V0040AssocRecSetGrpjobs]
        if isinstance(_grpjobs, Unset):
            grpjobs = UNSET
        else:
            grpjobs = V0040AssocRecSetGrpjobs.from_dict(_grpjobs)

        _grpjobsaccrue = d.pop("grpjobsaccrue", UNSET)
        grpjobsaccrue: Union[Unset, V0040AssocRecSetGrpjobsaccrue]
        if isinstance(_grpjobsaccrue, Unset):
            grpjobsaccrue = UNSET
        else:
            grpjobsaccrue = V0040AssocRecSetGrpjobsaccrue.from_dict(_grpjobsaccrue)

        _grpsubmitjobs = d.pop("grpsubmitjobs", UNSET)
        grpsubmitjobs: Union[Unset, V0040AssocRecSetGrpsubmitjobs]
        if isinstance(_grpsubmitjobs, Unset):
            grpsubmitjobs = UNSET
        else:
            grpsubmitjobs = V0040AssocRecSetGrpsubmitjobs.from_dict(_grpsubmitjobs)

        _grptres = d.pop("grptres", UNSET)
        grptres: Union[Unset, V0040AssocRecSetGrptres]
        if isinstance(_grptres, Unset):
            grptres = UNSET
        else:
            grptres = V0040AssocRecSetGrptres.from_dict(_grptres)

        _grptresmins = d.pop("grptresmins", UNSET)
        grptresmins: Union[Unset, V0040AssocRecSetGrptresmins]
        if isinstance(_grptresmins, Unset):
            grptresmins = UNSET
        else:
            grptresmins = V0040AssocRecSetGrptresmins.from_dict(_grptresmins)

        _grptresrunmins = d.pop("grptresrunmins", UNSET)
        grptresrunmins: Union[Unset, V0040AssocRecSetGrptresrunmins]
        if isinstance(_grptresrunmins, Unset):
            grptresrunmins = UNSET
        else:
            grptresrunmins = V0040AssocRecSetGrptresrunmins.from_dict(_grptresrunmins)

        _grpwall = d.pop("grpwall", UNSET)
        grpwall: Union[Unset, V0040AssocRecSetGrpwall]
        if isinstance(_grpwall, Unset):
            grpwall = UNSET
        else:
            grpwall = V0040AssocRecSetGrpwall.from_dict(_grpwall)

        _maxjobs = d.pop("maxjobs", UNSET)
        maxjobs: Union[Unset, V0040AssocRecSetMaxjobs]
        if isinstance(_maxjobs, Unset):
            maxjobs = UNSET
        else:
            maxjobs = V0040AssocRecSetMaxjobs.from_dict(_maxjobs)

        _maxjobsaccrue = d.pop("maxjobsaccrue", UNSET)
        maxjobsaccrue: Union[Unset, V0040AssocRecSetMaxjobsaccrue]
        if isinstance(_maxjobsaccrue, Unset):
            maxjobsaccrue = UNSET
        else:
            maxjobsaccrue = V0040AssocRecSetMaxjobsaccrue.from_dict(_maxjobsaccrue)

        _maxsubmitjobs = d.pop("maxsubmitjobs", UNSET)
        maxsubmitjobs: Union[Unset, V0040AssocRecSetMaxsubmitjobs]
        if isinstance(_maxsubmitjobs, Unset):
            maxsubmitjobs = UNSET
        else:
            maxsubmitjobs = V0040AssocRecSetMaxsubmitjobs.from_dict(_maxsubmitjobs)

        _maxtresminsperjob = d.pop("maxtresminsperjob", UNSET)
        maxtresminsperjob: Union[Unset, V0040AssocRecSetMaxtresminsperjob]
        if isinstance(_maxtresminsperjob, Unset):
            maxtresminsperjob = UNSET
        else:
            maxtresminsperjob = V0040AssocRecSetMaxtresminsperjob.from_dict(_maxtresminsperjob)

        _maxtresrunmins = d.pop("maxtresrunmins", UNSET)
        maxtresrunmins: Union[Unset, V0040AssocRecSetMaxtresrunmins]
        if isinstance(_maxtresrunmins, Unset):
            maxtresrunmins = UNSET
        else:
            maxtresrunmins = V0040AssocRecSetMaxtresrunmins.from_dict(_maxtresrunmins)

        _maxtresperjob = d.pop("maxtresperjob", UNSET)
        maxtresperjob: Union[Unset, V0040AssocRecSetMaxtresperjob]
        if isinstance(_maxtresperjob, Unset):
            maxtresperjob = UNSET
        else:
            maxtresperjob = V0040AssocRecSetMaxtresperjob.from_dict(_maxtresperjob)

        _maxtrespernode = d.pop("maxtrespernode", UNSET)
        maxtrespernode: Union[Unset, V0040AssocRecSetMaxtrespernode]
        if isinstance(_maxtrespernode, Unset):
            maxtrespernode = UNSET
        else:
            maxtrespernode = V0040AssocRecSetMaxtrespernode.from_dict(_maxtrespernode)

        _maxwalldurationperjob = d.pop("maxwalldurationperjob", UNSET)
        maxwalldurationperjob: Union[Unset, V0040AssocRecSetMaxwalldurationperjob]
        if isinstance(_maxwalldurationperjob, Unset):
            maxwalldurationperjob = UNSET
        else:
            maxwalldurationperjob = V0040AssocRecSetMaxwalldurationperjob.from_dict(_maxwalldurationperjob)

        _minpriothresh = d.pop("minpriothresh", UNSET)
        minpriothresh: Union[Unset, V0040AssocRecSetMinpriothresh]
        if isinstance(_minpriothresh, Unset):
            minpriothresh = UNSET
        else:
            minpriothresh = V0040AssocRecSetMinpriothresh.from_dict(_minpriothresh)

        parent = d.pop("parent", UNSET)

        _priority = d.pop("priority", UNSET)
        priority: Union[Unset, V0040AssocRecSetPriority]
        if isinstance(_priority, Unset):
            priority = UNSET
        else:
            priority = V0040AssocRecSetPriority.from_dict(_priority)

        _qoslevel = d.pop("qoslevel", UNSET)
        qoslevel: Union[Unset, V0040AssocRecSetQoslevel]
        if isinstance(_qoslevel, Unset):
            qoslevel = UNSET
        else:
            qoslevel = V0040AssocRecSetQoslevel.from_dict(_qoslevel)

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
