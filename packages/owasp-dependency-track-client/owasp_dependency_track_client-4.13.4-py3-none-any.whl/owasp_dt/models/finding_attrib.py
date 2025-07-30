from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.finding_attrib_analyzer_identity import FindingAttribAnalyzerIdentity
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.component import Component
    from ..models.vulnerability import Vulnerability


T = TypeVar("T", bound="FindingAttrib")


@_attrs_define
class FindingAttrib:
    """
    Attributes:
        attributed_on (int): UNIX epoch timestamp in milliseconds
        component (Component):
        vulnerability (Vulnerability):
        uuid (UUID):
        analyzer_identity (Union[Unset, FindingAttribAnalyzerIdentity]):
        alternate_identifier (Union[Unset, str]):
        reference_url (Union[Unset, str]):
    """

    attributed_on: int
    component: "Component"
    vulnerability: "Vulnerability"
    uuid: UUID
    analyzer_identity: Union[Unset, FindingAttribAnalyzerIdentity] = UNSET
    alternate_identifier: Union[Unset, str] = UNSET
    reference_url: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        attributed_on = self.attributed_on

        component = self.component.to_dict()

        vulnerability = self.vulnerability.to_dict()

        uuid = str(self.uuid)

        analyzer_identity: Union[Unset, str] = UNSET
        if not isinstance(self.analyzer_identity, Unset):
            analyzer_identity = self.analyzer_identity.value

        alternate_identifier = self.alternate_identifier

        reference_url = self.reference_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "attributedOn": attributed_on,
                "component": component,
                "vulnerability": vulnerability,
                "uuid": uuid,
            }
        )
        if analyzer_identity is not UNSET:
            field_dict["analyzerIdentity"] = analyzer_identity
        if alternate_identifier is not UNSET:
            field_dict["alternateIdentifier"] = alternate_identifier
        if reference_url is not UNSET:
            field_dict["referenceUrl"] = reference_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.component import Component
        from ..models.vulnerability import Vulnerability

        d = dict(src_dict)
        attributed_on = d.pop("attributedOn")

        component = Component.from_dict(d.pop("component"))

        vulnerability = Vulnerability.from_dict(d.pop("vulnerability"))

        uuid = UUID(d.pop("uuid"))

        _analyzer_identity = d.pop("analyzerIdentity", UNSET)
        analyzer_identity: Union[Unset, FindingAttribAnalyzerIdentity]
        if isinstance(_analyzer_identity, Unset):
            analyzer_identity = UNSET
        else:
            analyzer_identity = FindingAttribAnalyzerIdentity(_analyzer_identity)

        alternate_identifier = d.pop("alternateIdentifier", UNSET)

        reference_url = d.pop("referenceUrl", UNSET)

        finding_attrib = cls(
            attributed_on=attributed_on,
            component=component,
            vulnerability=vulnerability,
            uuid=uuid,
            analyzer_identity=analyzer_identity,
            alternate_identifier=alternate_identifier,
            reference_url=reference_url,
        )

        finding_attrib.additional_properties = d
        return finding_attrib

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
